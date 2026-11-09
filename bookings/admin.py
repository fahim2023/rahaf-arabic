from django.contrib import admin

from .models import TrialRequest


@admin.register(TrialRequest)
class TrialRequestAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "level", "status", "language", "created_at"]
    list_filter = ["status", "level", "language"]
    search_fields = ["name", "email", "message"]
