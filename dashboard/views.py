"""Rahaf's phone-friendly dashboard. Staff accounts only."""
from functools import wraps

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone, translation
from django.views.decorators.http import require_POST

from accounts.models import InviteCode
from bookings.models import TrialRequest
from core.notifications import notify_answer_published
from portal.models import Homework, Lesson, PlanStep, SharedFile
from qa.forms import AnswerForm
from qa.models import Question

from .forms import (HomeworkForm, InviteForm, LessonForm, PlanStepForm, ProfileForm, SharedFileForm,
                    TrialStatusForm)

User = get_user_model()


def teacher_required(view):
    @wraps(view)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect("portal:home")
        translation.activate("en")  # the dashboard is English-only
        return view(request, *args, **kwargs)
    return wrapper


def _counts():
    today = timezone.localdate()
    return {
        "new_count": Question.objects.exclude(status=Question.STATUS_ANSWERED).count(),
        "answered_count": Question.objects.filter(status=Question.STATUS_ANSWERED).count(),
        "lessons_today": Lesson.objects.filter(starts_at__date=today).count(),
        "new_bookings": TrialRequest.objects.filter(status="new").count(),
    }


@teacher_required
def questions(request):
    tab = "answered" if request.GET.get("tab") == "answered" else "new"
    qs = Question.objects.select_related("student", "student__profile")
    if tab == "new":
        qs = qs.exclude(status=Question.STATUS_ANSWERED).order_by("-created_at")
    else:
        qs = qs.filter(status=Question.STATUS_ANSWERED).order_by("-answered_at")
    return render(request, "dashboard/questions.html", {
        "tab": tab, "list": qs[:50], "nav": "questions", **_counts(),
        "greeting_hour": timezone.localtime().hour,
    })


@teacher_required
def answer(request, pk):
    question = get_object_or_404(Question, pk=pk)
    was_answered = question.status == Question.STATUS_ANSWERED
    form = AnswerForm(request.POST or None, instance=question)
    if request.method == "POST" and form.is_valid():
        question = form.save(commit=False)
        if "publish" in request.POST:
            if not question.answer.strip():
                form.add_error("answer", "Write an answer before publishing.")
                return render(request, "dashboard/answer.html", {"q": question, "form": form, "nav": "questions"})
            question.publish_answer(question.answer)
            if not was_answered:
                notify_answer_published(question)
            messages.success(request, "Answer published to the Q&A page" if question.is_public
                             else "Answer sent to the student")
        else:
            if question.status != Question.STATUS_ANSWERED:
                question.status = Question.STATUS_DRAFT
            question.save()
            messages.success(request, "Draft saved")
        return redirect("dashboard:questions")
    return render(request, "dashboard/answer.html", {"q": question, "form": form, "nav": "questions"})


@teacher_required
@require_POST
def delete_question(request, pk):
    get_object_or_404(Question, pk=pk).delete()
    messages.success(request, "Question deleted")
    return redirect("dashboard:questions")


@teacher_required
def bookings(request):
    show = request.GET.get("show", "open")
    qs = TrialRequest.objects.all()
    if show == "open":
        qs = qs.exclude(status__in=["enrolled", "closed"])
    return render(request, "dashboard/bookings.html", {
        "list": qs[:100], "show": show, "nav": "bookings", "statuses": TrialRequest.STATUSES, **_counts(),
    })


@teacher_required
@require_POST
def update_booking(request, pk):
    trial = get_object_or_404(TrialRequest, pk=pk)
    form = TrialStatusForm(request.POST, instance=trial)
    if form.is_valid():
        form.save()
        messages.success(request, f"Updated {trial.name}")
    return redirect(reverse("dashboard:bookings") + f"#trial-{trial.pk}")


@teacher_required
def students(request):
    people = (
        User.objects.filter(profile__isnull=False)
        .select_related("profile")
        .annotate(open_questions=Count("questions", filter=~Q(questions__status=Question.STATUS_ANSWERED)))
        .order_by("first_name", "email")
    )
    invite_form = InviteForm(request.POST or None)
    if request.method == "POST" and invite_form.is_valid():
        invite = invite_form.save()
        messages.success(request, f"New invite code: {invite.code}")
        return redirect("dashboard:students")
    return render(request, "dashboard/students.html", {
        "people": people, "nav": "students", "invite_form": invite_form,
        "invites": InviteCode.objects.filter(used_by__isnull=True)[:20], **_counts(),
    })


FORMS = {
    "lesson": (LessonForm, "lessons"),
    "homework": (HomeworkForm, "homework"),
    "file": (SharedFileForm, "files"),
    "step": (PlanStepForm, "plan"),
}


@teacher_required
def student_detail(request, pk):
    student = get_object_or_404(User.objects.select_related("profile"), pk=pk, profile__isnull=False)
    kind = request.POST.get("kind") if request.method == "POST" else None
    forms = {k: cls(prefix=k) for k, (cls, _a) in FORMS.items()}
    profile_form = ProfileForm(instance=student.profile, prefix="profile")
    if kind in FORMS:
        cls, anchor = FORMS[kind]
        form = cls(request.POST, request.FILES, prefix=kind)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.student = student
            if kind == "step":
                obj.order = student.plan_steps.count()
            obj.save()
            messages.success(request, "Saved")
            return redirect(reverse("dashboard:student", args=[pk]) + f"#{anchor}")
        forms[kind] = form
    elif kind == "profile":
        profile_form = ProfileForm(request.POST, instance=student.profile, prefix="profile")
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Saved")
            return redirect("dashboard:student", pk=pk)
    return render(request, "dashboard/student.html", {
        "student": student, "profile": student.profile, "forms": forms, "profile_form": profile_form,
        "lessons": student.lessons.order_by("-starts_at")[:12],
        "steps": student.plan_steps.all(), "homework": student.homework.all(),
        "files": student.files.all(), "nav": "students",
    })


MODELS = {"lesson": Lesson, "homework": Homework, "file": SharedFile, "step": PlanStep}


@teacher_required
@require_POST
def student_item(request, pk, kind, item_pk):
    """Delete an item, or for plan steps cycle done/current."""
    model = MODELS.get(kind)
    if not model:
        return redirect("dashboard:student", pk=pk)
    item = get_object_or_404(model, pk=item_pk, student_id=pk)
    action = request.POST.get("action", "delete")
    if kind == "step" and action == "done":
        item.done, item.current = not item.done, False
        item.save()
    elif kind == "step" and action == "current":
        PlanStep.objects.filter(student_id=pk).update(current=False)
        item.current, item.done = True, False
        item.save()
    elif action == "delete":
        if kind == "file":
            item.file.delete(save=False)
        item.delete()
    return redirect(reverse("dashboard:student", args=[pk]) + f"#{FORMS[kind][1]}")


@teacher_required
@require_POST
def delete_invite(request, pk):
    get_object_or_404(InviteCode, pk=pk, used_by__isnull=True).delete()
    return redirect("dashboard:students")

