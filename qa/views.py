from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from core.notifications import notify_new_question

from .forms import AskForm
from .models import Question


def public_questions():
    return Question.objects.filter(status=Question.STATUS_ANSWERED, is_public=True).order_by("-answered_at")


def question_list(request):
    qs = public_questions()
    query = request.GET.get("q", "").strip()
    topic = request.GET.get("topic", "")
    if query:
        qs = qs.filter(
            Q(question__icontains=query) | Q(answer__icontains=query)
            | Q(question_ar__icontains=query) | Q(answer_ar__icontains=query)
        )
    if topic in dict(Question.TOPICS):
        qs = qs.filter(topic=topic)
    page = Paginator(qs, 10).get_page(request.GET.get("page"))
    return render(request, "qa/list.html", {
        "page": page, "query": query, "topic": topic, "topics": Question.TOPICS,
        "form": AskForm() if request.user.is_authenticated else None,
    })


def _profile_label(user):
    profile = getattr(user, "profile", None)
    if profile and profile.is_child:
        return "parent"
    return ""


@login_required
@require_POST
def ask(request):
    form = AskForm(request.POST)
    next_url = request.POST.get("next", "")
    if form.is_valid():
        question = form.save(commit=False)
        question.student = request.user
        question.asker_label = _profile_label(request.user)
        question.save()
        notify_new_question(question)
        messages.success(request, _("Thanks! Your question has gone to Rahaf."))
    else:
        messages.error(request, _("Please write your question before sending."))
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("portal:home")
