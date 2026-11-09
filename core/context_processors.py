from django.urls import translate_url
from django.utils.translation import get_language

from .models import SiteSettings


def site(request):
    lang = (get_language() or "en")[:2]
    path = request.get_full_path()
    return {
        "site": SiteSettings.load(),
        "is_rtl": lang == "ar",
        "lang": lang,
        "url_en": translate_url(path, "en"),
        "url_ar": translate_url(path, "ar"),
    }
