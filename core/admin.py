from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html

from .admin_utils import yes_no
from .models import FAQ, Course, NewsletterSubscriber, Resource, SiteSettings, Testimonial

BILINGUAL = "Fill in English first. Arabic is optional — if it's empty, the Arabic page shows the English text."


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Contact", {"fields": ["whatsapp_number", "contact_email"]}),
        ("Social links", {"fields": ["instagram_url", "youtube_url", "facebook_url"], "classes": ["collapse"]}),
        ("Numbers shown on the site", {"fields": [("years_teaching", "students_taught"),
                                                  ("reply_hours", "trial_minutes"), "kids_ages"]}),
        ("Photo & video", {"fields": ["teacher_photo", "photo_preview", "intro_video_url"]}),
        ("About me", {"fields": [("story_en", "story_ar"), ("story2_en", "story2_ar"),
                                 ("qualifications_en", "qualifications_ar")], "description": BILINGUAL}),
    ]
    readonly_fields = ["photo_preview"]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # There's only ever one row, so skip the list and open it directly.
        obj = SiteSettings.load()
        return redirect(reverse("admin:core_sitesettings_change", args=[obj.pk]))

    @admin.display(description="Current photo")
    def photo_preview(self, obj):
        if obj and obj.teacher_photo:
            return format_html('<img src="{}" class="rm-thumb" alt="">', obj.teacher_photo.url)
        return "No photo yet"


class OrderedAdmin(admin.ModelAdmin):
    """Shared settings for content shown in a set order on the site."""
    list_per_page = 50
    save_on_top = False


@admin.register(Course)
class CourseAdmin(OrderedAdmin):
    list_display = ["name_en", "name_ar", "level_label_en", "price", "order", "active"]
    list_editable = ["order", "active"]
    list_filter = ["active", "highlighted"]
    search_fields = ["name_en", "name_ar"]
    fieldsets = [
        ("Course", {"fields": [("name_en", "name_ar"), ("level_label_en", "level_label_ar"),
                               ("description_en", "description_ar"), ("duration_en", "duration_ar"),
                               ("price", "price_ar")], "description": BILINGUAL}),
        ("Display", {"fields": [("order", "active", "highlighted")]}),
    ]


@admin.register(Testimonial)
class TestimonialAdmin(OrderedAdmin):
    list_display = ["name", "short_quote", "country_en", "course_en", "order", "active"]
    list_editable = ["order", "active"]
    list_filter = ["active", "is_parent"]
    search_fields = ["name", "quote_en", "quote_ar"]
    fieldsets = [
        ("Review", {"fields": ["name", ("quote_en", "quote_ar"), ("country_en", "country_ar"),
                               ("course_en", "course_ar"), "is_parent"], "description": BILINGUAL}),
        ("Display", {"fields": [("order", "active")]}),
    ]

    @admin.display(description="Quote")
    def short_quote(self, obj):
        return (obj.quote_en[:70] + "…") if len(obj.quote_en) > 70 else obj.quote_en


@admin.register(FAQ)
class FAQAdmin(OrderedAdmin):
    list_display = ["question_en", "has_arabic", "order"]
    list_editable = ["order"]
    search_fields = ["question_en", "question_ar", "answer_en"]
    fieldsets = [
        (None, {"fields": [("question_en", "question_ar"), ("answer_en", "answer_ar"), "order"],
                "description": BILINGUAL}),
    ]

    @admin.display(description="Arabic")
    def has_arabic(self, obj):
        return yes_no(bool(obj.question_ar and obj.answer_ar), "Translated", "English only")


@admin.register(Resource)
class ResourceAdmin(OrderedAdmin):
    list_display = ["title_en", "category", "file_format", "has_file", "order", "active"]
    list_editable = ["order", "active"]
    list_filter = ["category", "active"]
    search_fields = ["title_en", "title_ar"]
    fieldsets = [
        ("Resource", {"fields": ["category", ("title_en", "title_ar"), ("description_en", "description_ar"),
                                 "glyph"], "description": BILINGUAL}),
        ("File", {"fields": ["file", ("file_format", "size_note_en", "size_note_ar")]}),
        ("Display", {"fields": [("order", "active")]}),
    ]

    @admin.display(description="File")
    def has_file(self, obj):
        return yes_no(bool(obj.file), "Uploaded", "Missing")


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "language", "created_at"]
    list_filter = ["language"]
    search_fields = ["email"]
    date_hierarchy = "created_at"
    actions = ["export_emails"]

    @admin.action(description="Show selected emails (to copy into an email)")
    def export_emails(self, request, queryset):
        emails = ", ".join(queryset.values_list("email", flat=True))
        self.message_user(request, emails or "No emails selected.")
