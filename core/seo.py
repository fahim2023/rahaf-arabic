"""Search-engine titles, descriptions and link-preview details.

Each public page is keyed by its URL name. Pages that aren't listed
(log in, portal…) fall back to the homepage text; they're kept out of
search results by ``robots`` below anyway.

Keep descriptions under about 155 characters so Google shows them whole.
"""
from django.conf import settings
from django.templatetags.static import static
from django.urls import translate_url
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

PAGES = {
    "core:home": {
        "title": _("Online Arabic lessons with a native Syrian teacher · Rahaf Malasy"),
        "description": _("Online Arabic lessons with Rahaf, a native Syrian teacher. Modern Standard, "
                         "Levantine and Quranic Arabic for adults and kids. Book a free trial."),
    },
    "core:resources": {
        "title": _("Free Arabic worksheets and resources · Rahaf Malasy"),
        "description": _("Free Arabic worksheets from a native Syrian teacher: the alphabet, "
                         "Levantine phrases, Modern Standard and Quranic Arabic, and sheets for kids."),
    },
    "qa:list": {
        "title": _("Arabic questions answered · Student Q&A · Rahaf Malasy"),
        "description": _("Arabic learners' questions answered by Rahaf, a native Syrian teacher: "
                         "grammar, Levantine dialect, Modern Standard and Quranic Arabic."),
    },
    "bookings:book": {
        "title": _("Book a free online Arabic trial lesson · Rahaf Malasy"),
        "description": _("Book a free online Arabic trial lesson with Rahaf, a native Syrian teacher. "
                         "Modern Standard, Levantine or Quranic Arabic, for adults and kids."),
    },
    "core:privacy": {
        "title": _("Privacy policy · Rahaf Malasy"),
        "description": _("How Rahaf Malasy's online Arabic lessons site collects, uses and protects "
                         "your personal details, and how to have them changed or deleted."),
    },
}
DEFAULT_PAGE = "core:home"

SITE_NAME = _("Rahaf Malasy · Arabic lessons")
IMAGE_ALT = _("Learn Arabic with Rahaf: patient, personal online lessons")

INDEX = "index, follow"
NOINDEX = "noindex, follow"
PRIVATE_APPS = ("accounts:", "portal:", "dashboard:")
LOCALES = {"en": "en_GB", "ar": "ar_SY"}


def absolute(path):
    """Full URL on the real domain (settings.SITE_URL), never the request host."""
    return settings.SITE_URL + path


def robots_for(request, view_name):
    if view_name.startswith("dashboard:"):
        return "noindex, nofollow"
    if view_name.startswith(PRIVATE_APPS) or view_name == "bookings:thanks":
        return NOINDEX
    if view_name == "qa:list" and request.GET.get("q"):
        return NOINDEX
    return INDEX


def build_meta(request):
    match = getattr(request, "resolver_match", None)
    view_name = match.view_name if match else ""
    page = PAGES.get(view_name, PAGES[DEFAULT_PAGE])
    lang = (get_language() or "en")[:2]
    other = "en" if lang == "ar" else "ar"
    path = request.path  # no query string
    return {
        "title": page["title"],
        "description": page["description"],
        "robots": robots_for(request, view_name),
        "canonical": absolute(path),
        "url_en": absolute(translate_url(path, "en")),
        "url_ar": absolute(translate_url(path, "ar")),
        "image": absolute(static("img/og-image-ar.png" if lang == "ar" else "img/og-image.png")),
        "image_alt": IMAGE_ALT,
        "site_name": SITE_NAME,
        "locale": LOCALES[lang],
        "locale_alternate": LOCALES[other],
    }
