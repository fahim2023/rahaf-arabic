from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from qa.forms import AskForm

from .models import Homework, SharedFile


@login_required
def home(request):
    user = request.user
    if user.is_staff and not hasattr(user, "profile"):
        return redirect("dashboard:questions")
    now = timezone.now()
    upcoming = user.lessons.filter(starts_at__gte=now - timedelta(hours=1))
    steps = list(user.plan_steps.all())
    done_steps = sum(1 for s in steps if s.done)
    homework = list(user.homework.all())
    return render(request, "portal/home.html", {
        "profile": getattr(user, "profile", None),
        "next_lesson": upcoming.first(),
        "later_lessons": upcoming[1:4],
        "lesson_count": user.lessons.filter(starts_at__lt=now).count(),
        "steps": steps,
        "plan_pct": round(100 * done_steps / len(steps)) if steps else 0,
        "homework": homework,
        "hw_done": sum(1 for h in homework if h.done),
        "files": user.files.all()[:8],
        "my_questions": user.questions.all()[:10],
        "ask_form": AskForm(),
    })


@login_required
@require_POST
def toggle_homework(request, pk):
    hw = get_object_or_404(Homework, pk=pk, student=request.user)
    hw.done = not hw.done
    hw.save(update_fields=["done"])
    return redirect(reverse("portal:home") + "#homework")


@login_required
def download(request, pk):
    item = get_object_or_404(SharedFile, pk=pk)
    if item.student_id != request.user.id and not request.user.is_staff:
        raise Http404
    try:
        return FileResponse(item.file.open("rb"), as_attachment=True, filename=item.file.name.rsplit("/", 1)[-1])
    except FileNotFoundError:
        raise Http404
    except NotImplementedError:  # remote storage (Cloudinary)
        return redirect(item.file.url)
