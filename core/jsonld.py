"""Structured data (JSON-LD) that helps Google understand the homepage."""
import json

from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe

ORG_NAME = "Rahaf Malasy · Arabic lessons"

# Stop text like "</script>" inside a course description from ending the tag
# early. These are standard JSON escapes, so the output is still valid JSON.
_ESCAPES = {ord("<"): "\\u003C", ord(">"): "\\u003E", ord("&"): "\\u0026"}


def home_jsonld_data(site, courses):
    home_url = settings.SITE_URL + reverse("core:home")
    provider = {"@type": "EducationalOrganization", "name": ORG_NAME, "url": home_url}
    org = {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "name": ORG_NAME,
        "url": home_url,
        "logo": settings.SITE_URL + static("img/apple-touch-icon.png"),
        "image": settings.SITE_URL + static("img/og-image.png"),
        "areaServed": "Worldwide",
        "founder": {
            "@type": "Person",
            "name": "Rahaf Malasy",
            "alternateName": "رهف ملسي",
            "jobTitle": "Arabic teacher",
            "knowsLanguage": ["ar", "en"],
        },
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Arabic courses",
            "itemListElement": [
                {
                    "@type": "Course",
                    "name": course.tr("name"),
                    "description": course.tr("description"),
                    "provider": provider,
                    "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Online"},
                }
                for course in courses
            ],
        },
    }
    if site is not None:
        if site.contact_email:
            org["email"] = site.contact_email
        same_as = [u for u in (site.instagram_url, site.youtube_url, site.facebook_url) if u]
        if same_as:
            org["sameAs"] = same_as
    return org


def home_jsonld_script(site, courses):
    data = json.dumps(home_jsonld_data(site, courses), ensure_ascii=False, indent=1).translate(_ESCAPES)
    return mark_safe(f'<script type="application/ld+json">{data}</script>')
