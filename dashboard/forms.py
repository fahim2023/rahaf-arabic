from django import forms

from accounts.models import InviteCode, StudentProfile
from bookings.models import TrialRequest
from portal.models import Homework, Lesson, PlanStep, SharedFile


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["starts_at", "duration_minutes", "topic", "meeting_url"]
        labels = {"starts_at": "Date & time (UK time)", "duration_minutes": "Minutes", "meeting_url": "Zoom / Meet link"}
        widgets = {"starts_at": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M")}


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ["title", "kind", "due_date"]
        labels = {"title": "Task", "kind": "Type", "due_date": "Due"}
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}


class SharedFileForm(forms.ModelForm):
    class Meta:
        model = SharedFile
        fields = ["title", "file"]


class PlanStepForm(forms.ModelForm):
    class Meta:
        model = PlanStep
        fields = ["title"]
        labels = {"title": "New plan topic"}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ["course_label"]
        labels = {"course_label": "Course shown to student"}
        widgets = {"course_label": forms.TextInput(attrs={"placeholder": "e.g. Beginner · Levantine Arabic"})}


class InviteForm(forms.ModelForm):
    class Meta:
        model = InviteCode
        fields = ["note"]
        labels = {"note": "Who is it for?"}
        widgets = {"note": forms.TextInput(attrs={"placeholder": "e.g. Sarah, trial on 10 Nov"})}


class TrialStatusForm(forms.ModelForm):
    class Meta:
        model = TrialRequest
        fields = ["status", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 2, "placeholder": "Private notes"})}
