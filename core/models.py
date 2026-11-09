from django.db import models
from django.utils.translation import get_language


class Translated(models.Model):
    """Mixin for content edited in the admin in both English and Arabic.

    Fields come in pairs: ``title_en`` / ``title_ar``. ``obj.tr("title")``
    returns the Arabic version on Arabic pages (falling back to English if
    Rahaf hasn't filled it in yet).
    """

    class Meta:
        abstract = True

    def tr(self, field):
        lang = (get_language() or "en")[:2]
        if lang == "ar":
            value = getattr(self, f"{field}_ar", "")
            if value:
                return value
        return getattr(self, f"{field}_en", "")


class SiteSettings(Translated):
    """One row of editable details used across the site."""

    whatsapp_number = models.CharField(
        max_length=20, blank=True,
        help_text="International format, digits only, e.g. 963912345678",
    )
    contact_email = models.EmailField(blank=True)
    years_teaching = models.PositiveIntegerField(default=5)
    students_taught = models.PositiveIntegerField(default=100)
    reply_hours = models.PositiveIntegerField(default=24, help_text="Shown as 'I reply within X hours'")
    trial_minutes = models.PositiveIntegerField(default=30)
    kids_ages = models.CharField(max_length=20, default="5–12")

    teacher_photo = models.ImageField(upload_to="site/", blank=True)
    intro_video_url = models.URLField(blank=True, help_text="YouTube embed link, e.g. https://www.youtube.com/embed/VIDEO_ID")

    story_en = models.TextField(blank=True)
    story_ar = models.TextField(blank=True)
    story2_en = models.TextField(blank=True)
    story2_ar = models.TextField(blank=True)
    qualifications_en = models.TextField(blank=True, help_text="One per line")
    qualifications_ar = models.TextField(blank=True, help_text="One per line")

    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def whatsapp_link(self):
        if self.whatsapp_number:
            return f"https://wa.me/{self.whatsapp_number}"
        return ""

    def qualification_list(self):
        return [line.strip() for line in self.tr("qualifications").splitlines() if line.strip()]


class Course(Translated):
    level_label_en = models.CharField(max_length=40, help_text="Small tag, e.g. 'Level 1'")
    level_label_ar = models.CharField(max_length=40, blank=True)
    name_en = models.CharField(max_length=80)
    name_ar = models.CharField(max_length=80, blank=True)
    description_en = models.TextField()
    description_ar = models.TextField(blank=True)
    duration_en = models.CharField(max_length=40, default="60 min · 1-to-1")
    duration_ar = models.CharField(max_length=40, blank=True)
    price = models.CharField(max_length=40, blank=True, help_text="e.g. £20 / lesson. Leave blank to hide.")
    price_ar = models.CharField(max_length=40, blank=True)
    highlighted = models.BooleanField(default=False, help_text="Show as the dark teal card")
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name_en

    def price_display(self):
        lang = (get_language() or "en")[:2]
        return (self.price_ar if lang == "ar" and self.price_ar else self.price)


class Testimonial(Translated):
    quote_en = models.TextField()
    quote_ar = models.TextField(blank=True)
    name = models.CharField(max_length=60)
    country_en = models.CharField(max_length=60, blank=True)
    country_ar = models.CharField(max_length=60, blank=True)
    course_en = models.CharField(max_length=60, blank=True)
    course_ar = models.CharField(max_length=60, blank=True)
    is_parent = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.name}: {self.quote_en[:40]}"


class FAQ(Translated):
    question_en = models.CharField(max_length=200)
    question_ar = models.CharField(max_length=200, blank=True)
    answer_en = models.TextField()
    answer_ar = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question_en


class Resource(Translated):
    CATEGORIES = [
        ("alphabet", "Alphabet"),
        ("levantine", "Levantine"),
        ("msa", "MSA"),
        ("quranic", "Quranic"),
        ("kids", "Kids"),
    ]
    category = models.CharField(max_length=20, choices=CATEGORIES)
    title_en = models.CharField(max_length=120)
    title_ar = models.CharField(max_length=120, blank=True)
    description_en = models.TextField()
    description_ar = models.TextField(blank=True)
    glyph = models.CharField(max_length=30, help_text="Arabic text shown on the card, e.g. أ ب ت ث")
    file_format = models.CharField(max_length=20, default="PDF")
    size_note_en = models.CharField(max_length=40, blank=True, help_text="e.g. 2 pages")
    size_note_ar = models.CharField(max_length=40, blank=True)
    file = models.FileField(upload_to="resources/", blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title_en


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    language = models.CharField(max_length=5, default="en")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
