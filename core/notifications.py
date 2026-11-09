"""Emails sent by the site. Failures are logged, never shown to visitors."""
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from .models import SiteSettings

log = logging.getLogger(__name__)


def _teacher_address():
    return settings.TEACHER_EMAIL or SiteSettings.load().contact_email


def _send(subject, template, context, to):
    if not to:
        log.warning("No recipient for email %r; set TEACHER_EMAIL", subject)
        return False
    body = render_to_string(template, {**context, "site_url": settings.SITE_URL})
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to])
        return True
    except Exception:  # noqa: BLE001 - email must never break a form submission
        log.exception("Could not send email %r to %s", subject, to)
        return False


def notify_trial_request(trial):
    return _send(
        f"New trial request: {trial.name}",
        "emails/trial_request.txt",
        {"trial": trial, "link": settings.SITE_URL + reverse("dashboard:bookings")},
        _teacher_address(),
    )


def notify_new_question(question):
    return _send(
        "New student question",
        "emails/new_question.txt",
        {"question": question, "link": settings.SITE_URL + reverse("dashboard:answer", args=[question.pk])},
        _teacher_address(),
    )


def notify_answer_published(question):
    if not question.student or not question.student.email:
        return False
    return _send(
        "Rahaf answered your question",
        "emails/answer_published.txt",
        {"question": question, "link": settings.SITE_URL + reverse("portal:home") + "#questions"},
        question.student.email,
    )
