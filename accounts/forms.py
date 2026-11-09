from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from .models import InviteCode, StudentProfile

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "you@example.com", "autofocus": True}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": _("Your password")}),
    )
    remember = forms.BooleanField(label=_("Keep me logged in"), required=False, initial=True)

    error_messages = {
        "invalid_login": _("That email and password don't match. Please try again."),
        "inactive": _("This account is inactive."),
    }


class SignupForm(forms.Form):
    learner = forms.ChoiceField(choices=StudentProfile.LEARNER_CHOICES, initial=StudentProfile.LEARNER_SELF,
                                widget=forms.RadioSelect)
    name = forms.CharField(label=_("Your name"), max_length=100,
                           widget=forms.TextInput(attrs={"autocomplete": "name", "placeholder": _("Full name")}))
    email = forms.EmailField(label=_("Email"),
                             widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "you@example.com"}))
    child_first_name = forms.CharField(label=_("Child's first name"), max_length=40, required=False,
                                       widget=forms.TextInput(attrs={"placeholder": _("First name only")}))
    child_age_range = forms.ChoiceField(label=_("Age range"), choices=[("", "—")] + StudentProfile.AGE_RANGES,
                                        required=False)
    password = forms.CharField(label=_("Password"), strip=False,
                               widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                                                 "placeholder": _("At least 8 characters")}))
    invite_code = forms.CharField(label=_("Invite code"), max_length=20,
                                  widget=forms.TextInput(attrs={"placeholder": "ARB-1234", "autocapitalize": "characters"}))
    privacy = forms.BooleanField(label=_("I agree to the privacy policy."))
    newsletter = forms.BooleanField(label=_("Send me the free monthly worksheet (optional)."), required=False)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("There's already an account with this email. Try logging in."))
        return email

    def clean_invite_code(self):
        code = self.cleaned_data["invite_code"].strip().upper()
        invite = InviteCode.objects.filter(code=code, used_by__isnull=True).first()
        if invite is None:
            raise forms.ValidationError(_("That invite code isn't valid or has already been used."))
        self.invite = invite
        return code

    def clean(self):
        data = super().clean()
        if data.get("learner") == StudentProfile.LEARNER_CHILD:
            if not data.get("child_first_name"):
                self.add_error("child_first_name", _("Please add your child's first name."))
            if not data.get("child_age_range"):
                self.add_error("child_age_range", _("Please choose an age range."))
        password = data.get("password")
        if password:
            temp_user = User(email=data.get("email", ""), first_name=data.get("name", ""))
            try:
                password_validation.validate_password(password, temp_user)
            except forms.ValidationError as exc:
                self.add_error("password", exc)
        return data


class EmailLinkForm(forms.Form):
    email = forms.EmailField(label=_("Email"),
                             widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "you@example.com"}))
