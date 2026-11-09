from django.contrib import admin, messages
from django.utils.html import format_html

from core.admin_utils import status_badge

from .models import TrialRequest


@admin.register(TrialRequest)
class TrialRequestAdmin(admin.ModelAdmin):
    list_display = ["name", "email_link", "level", "status_label", "preferred_times", "language", "created_at"]
    list_display_links = ["name"]
    list_filter = ["status", "level", "language"]
    search_fields = ["name", "email", "message", "notes"]
    date_hierarchy = "created_at"
    list_per_page = 30
    readonly_fields = ["created_at", "language"]
    actions = ["mark_contacted", "mark_booked", "mark_enrolled", "mark_closed"]
    fieldsets = [
        ("Who", {"fields": ["name", "email", "language", "created_at"]}),
        ("What they asked for", {"fields": ["level", "preferred_times", "message"]}),
        ("Follow-up", {"fields": ["status", "notes"]}),
    ]

    @admin.display(description="Email", ordering="email")
    def email_link(self, obj):
        return format_html('<a href="mailto:{0}">{0}</a>', obj.email)

    @admin.display(description="Status", ordering="status")
    def status_label(self, obj):
        return status_badge(obj)

    def _set(self, request, queryset, status):
        n = queryset.update(status=status)
        label = dict(TrialRequest.STATUSES)[status]
        self.message_user(request, f"{n} request(s) marked “{label}”.", messages.SUCCESS)

    @admin.action(description="Mark as contacted")
    def mark_contacted(self, request, queryset):
        self._set(request, queryset, "contacted")

    @admin.action(description="Mark as trial booked")
    def mark_booked(self, request, queryset):
        self._set(request, queryset, "booked")

    @admin.action(description="Mark as became a student")
    def mark_enrolled(self, request, queryset):
        self._set(request, queryset, "enrolled")

    @admin.action(description="Mark as closed")
    def mark_closed(self, request, queryset):
        self._set(request, queryset, "closed")
