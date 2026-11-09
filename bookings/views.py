from django.shortcuts import redirect, render
from django.utils.translation import get_language
from django.views.decorators.http import require_http_methods

from core.notifications import notify_trial_request

from .forms import TrialRequestForm


@require_http_methods(["GET", "POST"])
def book_trial(request):
    initial = {}
    if request.GET.get("level"):
        initial["level"] = request.GET["level"]
    form = TrialRequestForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        trial = form.save(commit=False)
        trial.language = (get_language() or "en")[:2]
        trial.save()
        notify_trial_request(trial)
        return redirect("bookings:thanks")
    return render(request, "bookings/book.html", {"form": form})


def thanks(request):
    return render(request, "bookings/thanks.html")
