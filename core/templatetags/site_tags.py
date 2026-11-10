from django import template
from django.utils.translation import get_language

register = template.Library()

ARABIC_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


@register.filter
def t(obj, field):
    """{{ course|t:"name" }} → name_ar on Arabic pages, name_en otherwise."""
    return obj.tr(field)


@register.filter
def num(value):
    """Show digits as Arabic-Indic numerals on Arabic pages."""
    text = str(value)
    if (get_language() or "en")[:2] == "ar":
        return text.translate(ARABIC_DIGITS)
    return text


@register.inclusion_tag("partials/logo_mark.html")
def logo_mark(size=44, inverse=False):
    return {"size": size, "inverse": inverse, "glyph_size": round(size * 0.55)}


@register.inclusion_tag("partials/icon.html")
def icon(name, size=20, stroke=2):
    return {"name": name, "size": size, "stroke": stroke}


@register.simple_tag(takes_context=True)
def home_jsonld(context):
    """schema.org data for the homepage (EducationalOrganization + courses)."""
    from core.jsonld import home_jsonld_script
    return home_jsonld_script(context.get("site"), context.get("courses") or [])
