from django.contrib import admin

from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "student", "topic", "status", "is_public", "created_at"]
    list_filter = ["status", "topic", "is_public"]
    search_fields = ["question", "answer"]
