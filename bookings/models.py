from django.db import models
from django.utils.translation import gettext_lazy as _


class TrialRequest(models.Model):
    LEVELS = [
        ("complete_beginner", _("Complete beginner")),
        ("beginner", _("Beginner")),
        ("intermediate", _("Intermediate")),
        ("advanced", _("Advanced")),
        ("quranic", _("Quranic Arabic")),
        ("kids", _("Kids' Classes")),
    ]
    STATUSES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("booked", "Trial booked"),
        ("enrolled", "Became a student"),
        ("closed", "Closed"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    level = models.CharField(max_length=20, choices=LEVELS, default="complete_beginner")
    preferred_times = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    language = models.CharField(max_length=5, default="en", help_text="Language of the page they booked from")
    status = models.CharField(max_length=12, choices=STATUSES, default="new")
    notes = models.TextField(blank=True, help_text="Private notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"
