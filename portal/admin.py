from django.contrib import admin, messages
from django.utils import timezone

from core.admin_utils import badge, yes_no

from .models import Homework, Lesson, PlanStep, SharedFile


def student_name(obj):
    return obj.student.get_full_name() or obj.student.email


class UpcomingFilter(admin.SimpleListFilter):
    title = "when"
    parameter_name = "when"

    def lookups(self, request, model_admin):
        return [("upcoming", "Upcoming"), ("today", "Today"), ("past", "Past")]

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == "upcoming":
            return queryset.filter(starts_at__gte=now)
        if self.value() == "today":
            return queryset.filter(starts_at__date=timezone.localdate())
        if self.value() == "past":
            return queryset.filter(starts_at__lt=now)
        return queryset


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["starts_at", "student_col", "duration_minutes", "topic", "when_label"]
    list_display_links = ["starts_at"]
    list_filter = [UpcomingFilter]
    search_fields = ["topic", "student__email", "student__first_name", "student__last_name"]
    date_hierarchy = "starts_at"
    autocomplete_fields = ["student"]
    fields = ["student", "starts_at", "duration_minutes", "topic", "meeting_url"]

    @admin.display(description="Student", ordering="student__first_name")
    def student_col(self, obj):
        return student_name(obj)

    @admin.display(description="")
    def when_label(self, obj):
        return badge("Upcoming", "info") if obj.is_upcoming else badge("Done", "muted")


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ["title", "student_col", "kind", "due_date", "done_label"]
    list_filter = ["done", "kind"]
    search_fields = ["title", "student__email", "student__first_name"]
    autocomplete_fields = ["student"]
    actions = ["mark_done", "mark_not_done"]

    @admin.display(description="Student", ordering="student__first_name")
    def student_col(self, obj):
        return student_name(obj)

    @admin.display(description="Done", ordering="done")
    def done_label(self, obj):
        return yes_no(obj.done, "Done", "To do")

    @admin.action(description="Mark as done")
    def mark_done(self, request, queryset):
        self.message_user(request, f"{queryset.update(done=True)} item(s) marked done.", messages.SUCCESS)

    @admin.action(description="Mark as not done")
    def mark_not_done(self, request, queryset):
        self.message_user(request, f"{queryset.update(done=False)} item(s) marked to do.", messages.SUCCESS)


@admin.register(PlanStep)
class PlanStepAdmin(admin.ModelAdmin):
    list_display = ["title", "student_col", "order", "done", "current"]
    list_editable = ["order", "done", "current"]
    list_filter = ["done", "current"]
    search_fields = ["title", "student__email", "student__first_name"]
    autocomplete_fields = ["student"]

    @admin.display(description="Student", ordering="student__first_name")
    def student_col(self, obj):
        return student_name(obj)


@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    list_display = ["title", "student_col", "extension", "created_at"]
    search_fields = ["title", "student__email", "student__first_name"]
    autocomplete_fields = ["student"]
    date_hierarchy = "created_at"

    @admin.display(description="Student", ordering="student__first_name")
    def student_col(self, obj):
        return student_name(obj)
