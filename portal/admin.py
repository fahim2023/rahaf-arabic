from django.contrib import admin

from .models import Homework, Lesson, PlanStep, SharedFile


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["student", "starts_at", "duration_minutes", "topic"]
    list_filter = ["starts_at"]


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ["title", "student", "kind", "due_date", "done"]


@admin.register(PlanStep)
class PlanStepAdmin(admin.ModelAdmin):
    list_display = ["title", "student", "order", "done", "current"]


@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    list_display = ["title", "student", "created_at"]
