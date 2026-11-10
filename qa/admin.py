from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html

from core.admin_utils import status_badge, yes_no

from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "asked_by", "topic", "status_label", "public_label", "created_at"]
    list_display_links = ["question"]
    list_filter = ["status", "topic", "is_public"]
    search_fields = ["question", "detail", "answer", "student__email", "student__first_name"]
    date_hierarchy = "created_at"
    list_per_page = 30
    autocomplete_fields = ["student"]
    readonly_fields = ["created_at", "answered_at", "dashboard_link"]
    actions = ["make_public", "make_private"]
    fieldsets = [
        ("The question", {"fields": ["question", "detail", "topic", "student", "asker_label", "created_at"]}),
        ("Your answer", {
            "fields": ["status", "answer", "is_public", "answered_at", "dashboard_link"],
            "description": "Tip: answering from the Teaching dashboard also emails the student for you.",
        }),
        ("Arabic version (optional)", {
            "fields": [("question_ar", "answer_ar")],
            "classes": ["collapse"],
            "description": "Shown on the Arabic Q&A page. Leave blank to show the English text.",
        }),
    ]

    @admin.display(description="Asked by", ordering="student__first_name")
    def asked_by(self, obj):
        if obj.student:
            return obj.student.get_full_name() or obj.student.email
        return obj.asker_label or "—"

    @admin.display(description="Status", ordering="status")
    def status_label(self, obj):
        return status_badge(obj)

    @admin.display(description="On Q&A page", ordering="is_public")
    def public_label(self, obj):
        return yes_no(obj.is_public, "Public", "Private")

    @admin.display(description="Teaching dashboard")
    def dashboard_link(self, obj):
        if not obj.pk:
            return "—"
        return format_html('<a href="{}">Answer in the Teaching dashboard →</a>', reverse("dashboard:answer", args=[obj.pk]))

    @admin.action(description="Show on the public Q&A page")
    def make_public(self, request, queryset):
        n = queryset.update(is_public=True)
        self.message_user(request, f"{n} question(s) are now public.", messages.SUCCESS)

    @admin.action(description="Hide from the public Q&A page")
    def make_private(self, request, queryset):
        n = queryset.update(is_public=False)
        self.message_user(request, f"{n} question(s) are now private.", messages.SUCCESS)
