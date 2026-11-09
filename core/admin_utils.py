"""Small helpers shared by the admin classes."""
from django.utils.html import format_html

# status value → badge colour (classes defined in static/css/admin.css)
TONES = {
    "new": "warn", "draft": "info", "answered": "ok",
    "contacted": "info", "booked": "info", "enrolled": "ok", "closed": "muted",
}


def badge(text, tone="muted"):
    return format_html('<span class="rm-badge rm-badge-{}">{}</span>', tone, text)


def status_badge(obj, field="status"):
    value = getattr(obj, field)
    return badge(getattr(obj, f"get_{field}_display")(), TONES.get(value, "muted"))


def yes_no(value, yes="Yes", no="No"):
    return badge(yes, "ok") if value else badge(no, "muted")
