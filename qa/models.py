from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    TOPICS = [
        ("dialects", _("Dialects")),
        ("reading", _("Reading")),
        ("writing", _("Writing")),
        ("grammar", _("Grammar")),
        ("vocabulary", _("Vocabulary")),
        ("speaking", _("Speaking")),
        ("quranic", _("Quranic")),
        ("kids", _("Kids")),
        ("other", _("Other")),
    ]
    STATUS_NEW = "new"
    STATUS_DRAFT = "draft"
    STATUS_ANSWERED = "answered"
    STATUSES = [(STATUS_NEW, "New"), (STATUS_DRAFT, "Draft answer"), (STATUS_ANSWERED, "Answered")]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="questions"
    )
    question = models.CharField(max_length=300)
    detail = models.TextField(blank=True)
    topic = models.CharField(max_length=20, choices=TOPICS, default="other")
    asker_label = models.CharField(
        max_length=60, blank=True,
        help_text="Shown publicly instead of a name, e.g. 'beginner' → 'Asked by a beginner student'",
    )
    status = models.CharField(max_length=10, choices=STATUSES, default=STATUS_NEW)
    answer = models.TextField(blank=True)
    is_public = models.BooleanField(default=True, help_text="Show on the public Q&A page (without the student's name)")
    # Optional Arabic versions for the Arabic Q&A page
    question_ar = models.CharField(max_length=300, blank=True)
    answer_ar = models.TextField(blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    answered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.question

    def publish_answer(self, text):
        self.answer = text
        self.status = self.STATUS_ANSWERED
        if not self.answered_at:
            self.answered_at = timezone.now()
        self.save()

    def _ar(self):
        return (get_language() or "en")[:2] == "ar"

    @property
    def display_question(self):
        return self.question_ar if self._ar() and self.question_ar else self.question

    @property
    def display_answer(self):
        return self.answer_ar if self._ar() and self.answer_ar else self.answer
