from django.contrib import admin

from .models import InviteCode, StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "learner", "child_first_name", "course_label", "newsletter"]
    search_fields = ["user__email", "user__first_name", "child_first_name"]


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "note", "used_by", "created_at", "used_at"]
    readonly_fields = ["used_by", "used_at"]
