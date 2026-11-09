from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from .forms import EmailLinkForm, LoginForm, SignupForm
from .models import StudentProfile

User = get_user_model()
LINK_SALT = "accounts.login-link"
LINK_MAX_AGE = 60 * 20  # 20 minutes


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        if not form.cleaned_data.get("remember"):
            self.request.session.set_expiry(0)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["link_form"] = EmailLinkForm()
        return ctx


@login_required
def after_login(request):
    if request.user.is_staff:
        return redirect("dashboard:questions")
    return redirect("portal:home")


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect("accounts:after_login")
    form = SignupForm(request.POST or None, initial={"invite_code": request.GET.get("code", "")})
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        with transaction.atomic():
            first, _sep, last = data["name"].strip().partition(" ")
            user = User.objects.create_user(
                username=data["email"], email=data["email"], password=data["password"],
                first_name=first[:150], last_name=last[:150],
            )
            StudentProfile.objects.create(
                user=user,
                learner=data["learner"],
                child_first_name=data.get("child_first_name", "") if data["learner"] == "child" else "",
                child_age_range=data.get("child_age_range", "") if data["learner"] == "child" else "",
                newsletter=data.get("newsletter", False),
                privacy_accepted_at=timezone.now(),
                preferred_language=(get_language() or "en")[:2],
            )
            invite = form.invite
            invite.used_by = user
            invite.used_at = timezone.now()
            invite.save()
        login(request, user, backend="accounts.backends.EmailBackend")
        messages.success(request, _("Welcome! Your account is ready."))
        return redirect("portal:home")
    is_child = (form.data.get("learner") if form.is_bound else form.initial.get("learner")) == "child"
    return render(request, "accounts/signup.html", {"form": form, "is_child": is_child})


@require_http_methods(["POST"])
def email_login_link(request):
    """Send a one-time login link. Always shows the same message, so it
    can't be used to find out who has an account."""
    form = EmailLinkForm(request.POST)
    if form.is_valid():
        user = User.objects.filter(email__iexact=form.cleaned_data["email"], is_active=True).first()
        if user:
            token = signing.dumps({"u": user.pk, "l": str(user.last_login)}, salt=LINK_SALT)
            link = settings.SITE_URL + reverse("accounts:link_login", args=[token])
            body = render_to_string("emails/login_link.txt", {"user": user, "link": link})
            send_mail(_("Your login link"), body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
    messages.info(request, _("If that email has an account, a login link is on its way. It works for 20 minutes."))
    return redirect("accounts:login")


def link_login(request, token):
    try:
        data = signing.loads(token, salt=LINK_SALT, max_age=LINK_MAX_AGE)
        user = User.objects.get(pk=data["u"], is_active=True)
        if str(user.last_login) != data["l"]:  # link already used
            raise signing.BadSignature
    except (signing.BadSignature, User.DoesNotExist, KeyError):
        messages.error(request, _("That login link has expired or was already used. Please request a new one."))
        return redirect("accounts:login")
    login(request, user, backend="accounts.backends.EmailBackend")
    return redirect("accounts:after_login")


class PasswordResetView(auth_views.PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "emails/password_reset.txt"
    subject_template_name = "emails/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")
