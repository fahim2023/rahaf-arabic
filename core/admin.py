from django.contrib import admin

from .models import FAQ, Course, NewsletterSubscriber, Resource, SiteSettings, Testimonial


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Contact", {"fields": ["whatsapp_number", "contact_email", "instagram_url", "youtube_url", "facebook_url"]}),
        ("Numbers shown on the site", {"fields": ["years_teaching", "students_taught", "reply_hours",
                                                  "trial_minutes", "kids_ages"]}),
        ("Photo & video", {"fields": ["teacher_photo", "intro_video_url"]}),
        ("About me (English)", {"fields": ["story_en", "story2_en", "qualifications_en"]}),
        ("About me (Arabic)", {"fields": ["story_ar", "story2_ar", "qualifications_ar"]}),
    ]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["name_en", "name_ar", "price", "order", "active"]
    list_editable = ["order", "active"]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["name", "country_en", "course_en", "order", "active"]
    list_editable = ["order", "active"]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question_en", "order"]
    list_editable = ["order"]


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ["title_en", "category", "file_format", "file", "order", "active"]
    list_editable = ["order", "active"]
    list_filter = ["category"]


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "language", "created_at"]
    search_fields = ["email"]
