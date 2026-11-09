import os
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


class Lesson(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lessons")
    starts_at = models.DateTimeField(help_text="In UK time (Europe/London). Students see it in their own time zone.")
    duration_minutes = models.PositiveIntegerField(default=60)
    topic = models.CharField(max_length=120, blank=True)
    meeting_url = models.URLField(blank=True, help_text="Zoom or Google Meet link")

    class Meta:
        ordering = ["starts_at"]

    def __str__(self):
        return f"{self.student} · {self.starts_at:%d %b %H:%M}"

    @property
    def is_upcoming(self):
        return self.starts_at >= timezone.now() - timedelta(minutes=self.duration_minutes)


class PlanStep(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="plan_steps")
    title = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)
    done = models.BooleanField(default=False)
    current = models.BooleanField(default=False, help_text="The topic you're working on now")

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Homework(models.Model):
    KINDS = [
        ("writing", _("Writing")),
        ("listening", _("Listening")),
        ("speaking", _("Speaking")),
        ("reading", _("Reading")),
        ("vocabulary", _("Vocabulary")),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="homework")
    title = models.CharField(max_length=200)
    kind = models.CharField(max_length=20, choices=KINDS, default="writing")
    due_date = models.DateField(null=True, blank=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["done", "due_date", "id"]
        verbose_name_plural = "homework"

    def __str__(self):
        return self.title


class SharedFile(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    title = models.CharField(max_length=150)
    file = models.FileField(upload_to="students/%Y/%m/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def extension(self):
        ext = os.path.splitext(self.file.name)[1].lstrip(".").upper()
        return ext[:4] or "FILE"
