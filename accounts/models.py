import secrets

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


def make_invite_code():
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "ARB-" + "".join(secrets.choice(alphabet) for _ in range(5))


class StudentProfile(models.Model):
    LEARNER_SELF = "self"
    LEARNER_CHILD = "child"
    LEARNER_CHOICES = [(LEARNER_SELF, _("Myself")), (LEARNER_CHILD, _("My child"))]
    AGE_RANGES = [("5-7", "5–7"), ("8-10", "8–10"), ("11-13", "11–13"), ("14-17", "14–17")]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    learner = models.CharField(max_length=10, choices=LEARNER_CHOICES, default=LEARNER_SELF)
    child_first_name = models.CharField(max_length=40, blank=True)
    child_age_range = models.CharField(max_length=10, choices=AGE_RANGES, blank=True)
    course_label = models.CharField(
        max_length=80, blank=True,
        help_text="Shown in the portal, e.g. 'Beginner · Levantine Arabic'",
    )
    newsletter = models.BooleanField(default=False)
    privacy_accepted_at = models.DateTimeField(null=True, blank=True)
    preferred_language = models.CharField(max_length=5, default="en")

    def __str__(self):
        return f"Profile of {self.user.get_full_name() or self.user.email}"

    @property
    def is_child(self):
        return self.learner == self.LEARNER_CHILD

    @property
    def learner_name(self):
        if self.is_child and self.child_first_name:
            return self.child_first_name
        return self.user.first_name or self.user.email.split("@")[0]


class InviteCode(models.Model):
    code = models.CharField(max_length=20, unique=True, default=make_invite_code)
    note = models.CharField(max_length=120, blank=True, help_text="Who you gave it to, e.g. 'Sarah, trial 10 Nov'")
    created_at = models.DateTimeField(auto_now_add=True)
    used_by = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="invite_code"
    )
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.code

    @property
    def is_used(self):
        return self.used_by_id is not None
