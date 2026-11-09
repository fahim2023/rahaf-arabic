from django import forms
from django.utils.translation import gettext_lazy as _

from .models import TrialRequest


class TrialRequestForm(forms.ModelForm):
    # Honeypot: real people leave this empty, bots fill it in
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}))

    class Meta:
        model = TrialRequest
        fields = ["name", "email", "level", "preferred_times", "message"]
        labels = {
            "name": _("Your name"),
            "email": _("Email"),
            "level": _("Level / course"),
            "preferred_times": _("Preferred times"),
            "message": _("Message"),
        }
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name", "placeholder": _("e.g. Sarah")}),
            "email": forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "you@example.com"}),
            "preferred_times": forms.TextInput(attrs={"placeholder": _("e.g. Weekday evenings, UK time")}),
            "message": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": _("Why do you want to learn Arabic? Any experience so far?"),
            }),
        }

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam")
        return ""
