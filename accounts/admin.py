from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html

from core.admin_utils import badge
from portal.models import Homework, Lesson, PlanStep, SharedFile

from .models import InviteCode, StudentProfile

User = get_user_model()

# Rahaf doesn't use permission groups; hiding them keeps the menu short.
admin.site.unregister(Group)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["student", "user", "learner", "course_label", "newsletter"]
    list_filter = ["learner", "newsletter"]
    search_fields = ["user__email", "user__first_name", "user__last_name", "child_first_name"]
    autocomplete_fields = ["user"]

    @admin.display(description="Learner", ordering="user__first_name")
    def student(self, obj):
        return obj.learner_name


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "note", "state", "used_by", "created_at"]
    search_fields = ["code", "note", "used_by__email"]
    readonly_fields = ["used_by", "used_at", "created_at"]
    fields = ["code", "note", "used_by", "used_at", "created_at"]

    @admin.display(description="Status")
    def state(self, obj):
        return badge("Used", "muted") if obj.is_used else badge("Available", "ok")


# ---- Students: everything about one student on a single page ----

class ProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    extra = 0
    fields = [("learner", "child_first_name", "child_age_range"), "course_label",
              ("newsletter", "preferred_language")]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ["starts_at", "duration_minutes", "topic", "meeting_url"]
    classes = ["collapse"]


class PlanStepInline(admin.TabularInline):
    model = PlanStep
    extra = 0
    fields = ["order", "title", "current", "done"]
    classes = ["collapse"]


class HomeworkInline(admin.TabularInline):
    model = Homework
    extra = 0
    fields = ["title", "kind", "due_date", "done"]
    classes = ["collapse"]


class SharedFileInline(admin.TabularInline):
    model = SharedFile
    extra = 0
    fields = ["title", "file"]
    classes = ["collapse"]


admin.site.unregister(User)


@admin.register(User)
class StudentUserAdmin(UserAdmin):
    list_display = ["display_name", "email", "role", "course", "date_joined", "last_login"]
    list_display_links = ["display_name", "email"]
    list_filter = ["is_staff", "is_active", "profile__learner"]
    search_fields = ["email", "first_name", "last_name", "profile__child_first_name"]
    ordering = ["-date_joined"]
    list_per_page = 30
    readonly_fields = ["last_login", "date_joined", "dashboard_link"]
    fieldsets = [
        ("Details", {"fields": ["first_name", "last_name", "email", "username", "dashboard_link"]}),
        ("Account", {"fields": ["is_active", "password", ("last_login", "date_joined")]}),
        ("Admin access", {
            "fields": ["is_staff", "is_superuser"],
            "classes": ["collapse"],
            "description": "Only tick these for people who should be able to manage the site.",
        }),
    ]
    add_fieldsets = [
        (None, {"classes": ["wide"], "fields": ["username", "email", "first_name", "usable_password",
                                                "password1", "password2"]}),
    ]

    def get_inlines(self, request, obj):
        if obj is None or obj.is_staff:
            return []
        return [ProfileInline, LessonInline, PlanStepInline, HomeworkInline, SharedFileInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("profile")

    @admin.display(description="Name", ordering="first_name")
    def display_name(self, obj):
        return obj.get_full_name() or obj.username

    @admin.display(description="Role", ordering="is_staff")
    def role(self, obj):
        if obj.is_staff:
            return badge("Teacher / admin", "info")
        if not obj.is_active:
            return badge("Inactive", "muted")
        return badge("Student", "ok")

    @admin.display(description="Course")
    def course(self, obj):
        profile = getattr(obj, "profile", None)
        return (profile.course_label if profile else "") or "—"

    @admin.display(description="Teaching dashboard")
    def dashboard_link(self, obj):
        if not obj.pk or obj.is_staff:
            return "—"
        return format_html('<a href="{}">Open student in the Teaching dashboard →</a>',
                           reverse("dashboard:student", args=[obj.pk]))
