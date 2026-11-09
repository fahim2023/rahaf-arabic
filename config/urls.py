from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("qa/", include("qa.urls")),
    path("book/", include("bookings.urls")),
    path("portal/", include("portal.urls")),
    path("dashboard/", include("dashboard.urls")),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
