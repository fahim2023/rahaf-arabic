from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from bookings.forms import TrialRequestForm
from qa.views import public_questions

from .forms import NewsletterForm
from .models import FAQ, Course, NewsletterSubscriber, Resource, Testimonial


def home(request):
    return render(request, "core/home.html", {
        "courses": Course.objects.filter(active=True),
        "testimonials": Testimonial.objects.filter(active=True)[:3],
        "faqs": FAQ.objects.all(),
        "questions": public_questions()[:4],
        "booking_form": TrialRequestForm(),
    })


def resources(request):
    category = request.GET.get("cat", "")
    items = Resource.objects.filter(active=True)
    if category in dict(Resource.CATEGORIES):
        items = items.filter(category=category)
    else:
        category = ""
    return render(request, "core/resources.html", {
        "items": items,
        "category": category,
        "categories": Resource.CATEGORIES,
        "newsletter_form": NewsletterForm(),
    })


def privacy(request):
    return render(request, "core/privacy.html")


@require_POST
def subscribe(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        NewsletterSubscriber.objects.get_or_create(
            email=form.cleaned_data["email"].lower(),
            defaults={"language": (get_language() or "en")[:2]},
        )
        messages.success(request, _("You're subscribed. The next worksheet will land in your inbox."))
    else:
        messages.error(request, _("Please enter a valid email address."))
    return redirect("core:resources")


ROBOTS_DISALLOW = ["/admin/", "/en/dashboard/", "/ar/dashboard/", "/en/portal/", "/ar/portal/"]


def robots_txt(request):
    from django.conf import settings
    from django.http import HttpResponse

    lines = ["User-agent: *", "Allow: /"]
    lines += [f"Disallow: {path}" for path in ROBOTS_DISALLOW]
    lines += ["", f"Sitemap: {settings.SITE_URL}/sitemap.xml", ""]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")
