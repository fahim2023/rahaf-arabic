from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

# Public pages only; the portal, dashboard and log-in pages stay out.
PRIORITIES = {
    "core:home": 1.0,
    "qa:list": 0.8,
    "core:resources": 0.7,
    "bookings:book": 0.4,
    "core:privacy": 0.4,
}


class PageSitemap(Sitemap):
    i18n = True          # one entry per language: /en/… and /ar/…
    alternates = True    # each entry lists its other-language version
    changefreq = "weekly"

    def items(self):
        return list(PRIORITIES)

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return PRIORITIES[item]

    # Use the real domain from SITE_URL rather than whatever host the request came in on.
    def get_protocol(self, protocol=None):
        return urlsplit(settings.SITE_URL).scheme or "https"

    def get_domain(self, site=None):
        return urlsplit(settings.SITE_URL).netloc
