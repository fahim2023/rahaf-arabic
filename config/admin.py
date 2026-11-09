"""Rahaf's admin site: same colours as the public site, plain-English
section names, and a home page that shows what needs attention."""
from django.contrib import admin
from django.utils import timezone

# Order of the sections on the admin home page and in the sidebar
APP_ORDER = ["qa", "bookings", "portal", "accounts", "core", "auth"]


class RahafAdminSite(admin.AdminSite):
    site_header = "Rahaf Malasy"
    site_title = "Rahaf Malasy · Admin"
    index_title = "Welcome back"
    enable_nav_sidebar = True

    def get_app_list(self, request, app_label=None):
        apps = super().get_app_list(request, app_label)
        rank = {label: i for i, label in enumerate(APP_ORDER)}
        apps.sort(key=lambda a: rank.get(a["app_label"], len(rank)))
        return apps

    def index(self, request, extra_context=None):
        from bookings.models import TrialRequest
        from portal.models import Homework, Lesson
        from qa.models import Question

        now = timezone.now()
        today = timezone.localdate()
        extra_context = {
            "stats": {
                "questions": Question.objects.exclude(status=Question.STATUS_ANSWERED).count(),
                "bookings": TrialRequest.objects.filter(status="new").count(),
                "lessons_today": Lesson.objects.filter(starts_at__date=today).count(),
                "homework": Homework.objects.filter(done=False).count(),
            },
            "upcoming_lessons": Lesson.objects.filter(starts_at__gte=now)
            .select_related("student")[:5],
            **(extra_context or {}),
        }
        return super().index(request, extra_context)
