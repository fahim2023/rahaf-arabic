from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Question


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question", "detail", "topic"]
        labels = {"question": _("Your question"), "detail": _("Any details (optional)"), "topic": _("Topic")}
        widgets = {
            "question": forms.TextInput(attrs={"placeholder": _("e.g. How do I say “the bill, please” in Levantine?")}),
            "detail": forms.Textarea(attrs={"rows": 3}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["answer", "topic", "asker_label", "is_public", "question_ar", "answer_ar"]
        labels = {
            "answer": "Your answer",
            "asker_label": "Public label",
            "is_public": "Show on the public Q&A page (without the student's name)",
            "question_ar": "Question in Arabic (optional, for the Arabic site)",
            "answer_ar": "Answer in Arabic (optional)",
        }
        help_texts = {"asker_label": "e.g. beginner, intermediate, parent"}
        widgets = {
            "answer": forms.Textarea(attrs={
                "rows": 7,
                "placeholder": "Write a clear, friendly answer. It will appear on the public Q&A page.",
            }),
            "answer_ar": forms.Textarea(attrs={"rows": 4, "dir": "rtl", "lang": "ar"}),
            "question_ar": forms.TextInput(attrs={"dir": "rtl", "lang": "ar"}),
        }
