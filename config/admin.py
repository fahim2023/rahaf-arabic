"""Rahaf's admin ("Settings"): editing the website itself. Day-to-day teaching
(questions, bookings, students) lives in the Teaching dashboard at /dashboard/."""
from django.contrib import admin

# Order of the sections on the admin home page and in the sidebar
APP_ORDER = ["core", "qa", "bookings", "portal", "accounts", "auth"]


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
