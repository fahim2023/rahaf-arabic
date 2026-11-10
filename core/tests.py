from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone, translation

from accounts.models import InviteCode, StudentProfile
from bookings.models import TrialRequest
from portal.models import Homework, Lesson, SharedFile
from qa.models import Question

User = get_user_model()

TEST_SETTINGS = dict(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    TEACHER_EMAIL="rahaf@example.com",
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    },
    SECURE_SSL_REDIRECT=False,
)


def url(name, lang="en", *args):
    with translation.override(lang):
        return reverse(name, args=args)


def make_student(email="sam@example.com"):
    user = User.objects.create_user(username=email, email=email, password="a-good-pass-123", first_name="Sam")
    StudentProfile.objects.create(user=user)
    return user


@override_settings(**TEST_SETTINGS)
class PublicPagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_content", verbosity=0)

    def test_pages_render_in_both_languages(self):
        for lang in ("en", "ar"):
            for name in ("core:home", "core:resources", "core:privacy", "qa:list", "bookings:book",
                         "bookings:thanks", "accounts:login", "accounts:signup"):
                with self.subTest(lang=lang, page=name):
                    self.assertEqual(self.client.get(url(name, lang)).status_code, 200)

    def test_arabic_page_is_rtl_and_translated(self):
        html = self.client.get(url("core:home", "ar")).content.decode()
        self.assertIn('dir="rtl"', html)
        self.assertIn("تعلّم العربية مع رهف", html)
        self.assertIn("العربية القرآنية", html)  # course name from the database

    def test_root_redirects_to_a_language(self):
        self.assertEqual(self.client.get("/").status_code, 302)

    def test_qa_search(self):
        r = self.client.get(url("qa:list"), {"q": "letters"})
        self.assertContains(r, "Why do some letters connect")
        self.assertNotContains(r, "Can my child learn")

    def test_unanswered_and_private_questions_are_hidden(self):
        Question.objects.create(question="Secret unanswered question")
        Question.objects.create(question="Private answered", answer="x", status="answered", is_public=False)
        r = self.client.get(url("qa:list"))
        self.assertNotContains(r, "Secret unanswered")
        self.assertNotContains(r, "Private answered")

    def test_newsletter_subscribe(self):
        self.client.post(url("core:subscribe"), {"email": "a@b.com"})
        self.client.post(url("core:subscribe"), {"email": "A@b.com"})
        from core.models import NewsletterSubscriber
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)


@override_settings(**TEST_SETTINGS)
class BookingTests(TestCase):
    def test_trial_request_saves_and_emails_rahaf(self):
        r = self.client.post(url("bookings:book", "ar"), {
            "name": "Lena", "email": "lena@example.com", "level": "beginner",
            "preferred_times": "Evenings", "message": "Hello", "website": "",
        })
        self.assertRedirects(r, url("bookings:thanks", "ar"))
        trial = TrialRequest.objects.get()
        self.assertEqual(trial.language, "ar")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["rahaf@example.com"])
        self.assertIn("Lena", mail.outbox[0].body)

    def test_honeypot_blocks_bots(self):
        self.client.post(url("bookings:book"), {
            "name": "Bot", "email": "bot@example.com", "level": "beginner", "website": "http://spam",
        })
        self.assertEqual(TrialRequest.objects.count(), 0)

    def test_invalid_form_shows_errors(self):
        r = self.client.post(url("bookings:book"), {"name": "", "email": "nope", "level": "beginner"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Please check the highlighted fields")


@override_settings(**TEST_SETTINGS)
class AccountTests(TestCase):
    def signup_data(self, **extra):
        data = {"learner": "self", "name": "Sara Ali", "email": "sara@example.com", "password": "olive-tree-2026",
                "invite_code": InviteCode.objects.create().code, "privacy": "on"}
        data.update(extra)
        return data

    def test_signup_with_invite_code(self):
        data = self.signup_data()
        r = self.client.post(url("accounts:signup"), data)
        self.assertRedirects(r, url("portal:home"))
        user = User.objects.get(email="sara@example.com")
        self.assertEqual(user.first_name, "Sara")
        self.assertTrue(InviteCode.objects.get(code=data["invite_code"]).is_used)

    def test_invite_code_can_only_be_used_once(self):
        data = self.signup_data()
        self.client.post(url("accounts:signup"), data)
        self.client.logout()
        r = self.client.post(url("accounts:signup"), {**data, "email": "other@example.com"})
        self.assertContains(r, "invite code isn")
        self.assertEqual(User.objects.count(), 1)

    def test_signup_requires_valid_code(self):
        r = self.client.post(url("accounts:signup"), self.signup_data(invite_code="ARB-NOPE1"))
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.exists())

    def test_child_signup_needs_child_details(self):
        r = self.client.post(url("accounts:signup"), self.signup_data(learner="child"))
        self.assertContains(r, "child&#x27;s first name")
        self.client.post(url("accounts:signup"), self.signup_data(learner="child", child_first_name="Yusuf",
                                                                  child_age_range="8-10"))
        self.assertEqual(StudentProfile.objects.get().child_first_name, "Yusuf")

    def test_login_with_email_any_case(self):
        make_student()
        r = self.client.post(url("accounts:login"), {"username": "SAM@example.com", "password": "a-good-pass-123"})
        self.assertRedirects(r, url("accounts:after_login"), fetch_redirect_response=False)

    def test_staff_go_to_dashboard_after_login(self):
        User.objects.create_user(username="rahaf", email="r@example.com", password="x-pass-123456", is_staff=True)
        self.client.login(username="r@example.com", password="x-pass-123456")
        self.assertRedirects(self.client.get(url("accounts:after_login")), url("dashboard:questions"))

    def test_email_login_link_works_once(self):
        make_student()
        self.client.post(url("accounts:email_login_link"), {"email": "sam@example.com"})
        self.assertEqual(len(mail.outbox), 1)
        link = [line for line in mail.outbox[0].body.splitlines() if "/login-link/" in line][0].strip()
        path = link.replace("http://localhost:8000", "")
        self.assertRedirects(self.client.get(path), url("accounts:after_login"), fetch_redirect_response=False)
        self.client.logout()
        r = self.client.get(path)
        self.assertRedirects(r, url("accounts:login"))

    def test_login_link_does_not_reveal_unknown_emails(self):
        r = self.client.post(url("accounts:email_login_link"), {"email": "nobody@example.com"}, follow=True)
        self.assertContains(r, "If that email has an account")
        self.assertEqual(len(mail.outbox), 0)


@override_settings(**TEST_SETTINGS)
class PortalTests(TestCase):
    def setUp(self):
        self.student = make_student()
        self.client.login(username="sam@example.com", password="a-good-pass-123")

    def test_portal_requires_login(self):
        self.client.logout()
        self.assertEqual(self.client.get(url("portal:home")).status_code, 302)

    def test_portal_shows_next_lesson_and_homework(self):
        Lesson.objects.create(student=self.student, starts_at=timezone.now() + timedelta(days=1), topic="Café words")
        Homework.objects.create(student=self.student, title="Write ten words")
        r = self.client.get(url("portal:home", "ar"))
        self.assertContains(r, "Café words")
        self.assertContains(r, "Write ten words")

    def test_toggle_own_homework_only(self):
        mine = Homework.objects.create(student=self.student, title="Mine")
        other = Homework.objects.create(student=make_student("x@example.com"), title="Theirs")
        self.client.post(url("portal:toggle_homework", "en", mine.pk))
        mine.refresh_from_db()
        self.assertTrue(mine.done)
        self.assertEqual(self.client.post(url("portal:toggle_homework", "en", other.pk)).status_code, 404)

    def test_files_are_private(self):
        from django.core.files.base import ContentFile
        other = make_student("x@example.com")
        f = SharedFile(student=other, title="Notes")
        f.file.save("notes.pdf", ContentFile(b"%PDF"), save=True)
        self.assertEqual(self.client.get(url("portal:download", "en", f.pk)).status_code, 404)
        self.client.login(username="x@example.com", password="a-good-pass-123")
        self.assertEqual(self.client.get(url("portal:download", "en", f.pk)).status_code, 200)

    def test_ask_question_emails_rahaf(self):
        r = self.client.post(url("qa:ask"), {"question": "How do I say thanks?", "topic": "other",
                                             "next": url("portal:home")})
        self.assertRedirects(r, url("portal:home"))
        self.assertEqual(Question.objects.get().student, self.student)
        self.assertEqual(len(mail.outbox), 1)

    def test_ask_ignores_external_next(self):
        r = self.client.post(url("qa:ask"), {"question": "Q?", "topic": "other", "next": "https://evil.example"})
        self.assertRedirects(r, url("portal:home"))

    def test_students_cannot_open_dashboard(self):
        self.assertRedirects(self.client.get(url("dashboard:questions")), url("portal:home"))


@override_settings(**TEST_SETTINGS)
class DashboardTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="rahaf", email="r@example.com", password="x-pass-123456",
                                                is_staff=True, first_name="Rahaf")
        self.client.login(username="r@example.com", password="x-pass-123456")
        self.student = make_student()
        self.q = Question.objects.create(student=self.student, question="Is ة pronounced?")

    def test_dashboard_lists_new_questions(self):
        self.assertContains(self.client.get(url("dashboard:questions")), "Is ة pronounced?")

    def test_dashboard_is_english_even_from_arabic_url(self):
        html = self.client.get(url("dashboard:questions", "ar")).content.decode()
        self.assertIn('dir="ltr"', html)

    def test_publish_answer_emails_student_once(self):
        data = {"answer": "Usually silent.", "topic": "reading", "asker_label": "beginner", "is_public": "on",
                "publish": "1"}
        self.client.post(url("dashboard:answer", "en", self.q.pk), data)
        self.q.refresh_from_db()
        self.assertEqual(self.q.status, "answered")
        self.assertEqual(mail.outbox[-1].to, ["sam@example.com"])
        sent = len(mail.outbox)
        self.client.post(url("dashboard:answer", "en", self.q.pk), {**data, "answer": "Edited."})
        self.assertEqual(len(mail.outbox), sent)  # editing doesn't re-email
        self.assertContains(self.client.get(url("qa:list")), "Edited.")

    def test_save_draft(self):
        self.client.post(url("dashboard:answer", "en", self.q.pk), {"answer": "Draft", "topic": "other", "save": "1"})
        self.q.refresh_from_db()
        self.assertEqual(self.q.status, "draft")

    def test_cannot_publish_empty_answer(self):
        r = self.client.post(url("dashboard:answer", "en", self.q.pk), {"answer": "", "topic": "other",
                                                                       "publish": "1"})
        self.assertContains(r, "Write an answer before publishing")

    def test_create_invite_and_add_lesson(self):
        self.client.post(url("dashboard:students"), {"note": "Lena"})
        self.assertTrue(InviteCode.objects.filter(note="Lena").exists())
        self.client.post(url("dashboard:student", "en", self.student.pk), {
            "kind": "lesson", "lesson-starts_at": "2030-01-05T18:00", "lesson-duration_minutes": "60",
            "lesson-topic": "Numbers", "lesson-meeting_url": "",
        })
        self.assertEqual(self.student.lessons.get().topic, "Numbers")

    def test_update_booking_status(self):
        t = TrialRequest.objects.create(name="Lena", email="l@example.com", level="beginner")
        self.client.post(url("dashboard:update_booking", "en", t.pk), {"status": "booked", "notes": "Fri 6pm"})
        t.refresh_from_db()
        self.assertEqual(t.status, "booked")


@override_settings(**TEST_SETTINGS, SITE_URL="https://rahaf.example")
class SeoTests(TestCase):
    PUBLIC = ("core:home", "core:resources", "qa:list", "bookings:book", "core:privacy")

    @classmethod
    def setUpTestData(cls):
        call_command("seed_content", verbosity=0)

    def head(self, path, **params):
        html = self.client.get(path, params).content.decode()
        return html[: html.index("</head>")]

    def robots(self, head):
        import re
        return re.search(r'<meta name="robots" content="([^"]+)"', head).group(1)

    def test_public_pages_have_full_meta_in_both_languages(self):
        for lang in ("en", "ar"):
            for name in self.PUBLIC:
                with self.subTest(lang=lang, page=name):
                    path = url(name, lang)
                    head = self.head(path)
                    self.assertIn('<meta name="description" content="', head)
                    self.assertIn(f'<link rel="canonical" href="https://rahaf.example{path}">', head)
                    for hreflang in ("en", "ar", "x-default"):
                        self.assertIn(f'hreflang="{hreflang}" href="https://rahaf.example/', head)
                    self.assertIn('property="og:title"', head)
                    self.assertIn('property="og:image" content="https://rahaf.example/static/img/og-image', head)
                    self.assertIn('<meta name="twitter:card" content="summary_large_image">', head)
                    self.assertEqual(self.robots(head), "index, follow")

    def test_canonical_drops_query_string(self):
        head = self.head(url("core:resources"), cat="kids")
        self.assertIn('<link rel="canonical" href="https://rahaf.example/en/resources/">', head)

    def test_arabic_pages_use_arabic_title_and_image(self):
        for name in self.PUBLIC:
            with self.subTest(page=name):
                head = self.head(url(name, "ar"))
                title = head[head.index("<title>") + 7: head.index("</title>")]
                self.assertRegex(title, "[؀-ۿ]")
                self.assertIn("og-image-ar.png", head)
                self.assertIn('content="ar_SY"', head)

    def test_private_pages_are_noindex(self):
        student = make_student()
        self.assertEqual(self.robots(self.head(url("accounts:login"))), "noindex, follow")
        self.assertEqual(self.robots(self.head(url("bookings:thanks"))), "noindex, follow")
        self.assertEqual(self.robots(self.head(url("qa:list"), q="letters")), "noindex, follow")
        self.client.force_login(student)
        self.assertEqual(self.robots(self.head(url("portal:home"))), "noindex, follow")

    def test_dashboard_is_noindex_nofollow(self):
        teacher = User.objects.create_user("t@example.com", "t@example.com", "a-good-pass-123", is_staff=True)
        self.client.force_login(teacher)
        self.assertEqual(self.robots(self.head(url("dashboard:questions"))), "noindex, nofollow")

    def test_homepage_json_ld_is_valid(self):
        import json
        import re
        for lang in ("en", "ar"):
            html = self.client.get(url("core:home", lang)).content.decode()
            raw = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1)
            data = json.loads(raw)
            self.assertEqual(data["@type"], "EducationalOrganization")
            self.assertEqual(data["founder"]["name"], "Rahaf Malasy")
            courses = data["hasOfferCatalog"]["itemListElement"]
            self.assertTrue(courses)
            self.assertEqual(courses[0]["hasCourseInstance"]["courseMode"], "Online")
        self.assertNotIn("application/ld+json", self.client.get(url("qa:list")).content.decode())

    def test_robots_txt(self):
        r = self.client.get("/robots.txt")
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertIn("Disallow: /admin/", body)
        self.assertIn("Disallow: /ar/portal/", body)
        self.assertIn("Sitemap: https://rahaf.example/sitemap.xml", body)

    def test_sitemap(self):
        r = self.client.get("/sitemap.xml")
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        for path in ("/en/", "/ar/", "/en/qa/", "/ar/resources/", "/en/book/", "/ar/privacy/"):
            self.assertIn(f"<loc>https://rahaf.example{path}</loc>", body)
        self.assertIn('hreflang="ar"', body)
        self.assertNotIn("portal", body)
        self.assertNotIn("dashboard", body)
