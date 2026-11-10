# Rahaf Malasy · Arabic lessons

A bilingual (English / العربية) website for Rahaf Malasy, a private Arabic teacher who teaches online from Syria. It includes a student portal, a public Q&A that she answers, and a dashboard designed for her phone.

Built with Django 5.2, PostgreSQL and plain CSS. There is no front-end framework. The pages work without JavaScript, and a small script adds the extras.

## What's in it

| Area | URL | Who uses it |
|---|---|---|
| Homepage: hero, about, courses, how it works, testimonials, Q&A, FAQ, booking form | `/en/`, `/ar/` | Everyone |
| Free resources with category filter and newsletter sign-up | `/en/resources/` | Everyone |
| Student Q&A with search, topic filter and "Ask a question" | `/en/qa/` | Everyone (asking needs a login) |
| Trial booking form and thank-you page | `/en/book/` | Everyone |
| Privacy policy (UK/EU template, both languages) | `/en/privacy/` | Everyone |
| Log in, email login link, password reset, sign-up with invite code | `/en/accounts/…` | Students & parents |
| Student portal: next lesson in the student's own time zone, plan, homework, files, questions | `/en/portal/` | Students |
| Teaching dashboard: answer questions, trial requests, students, invite codes, lessons, homework, files | `/en/dashboard/` | Rahaf (staff only) |
| Django admin: courses, FAQs, resources, testimonials, site settings | `/admin/` | Rahaf / you |

Every public page and the student portal work in Arabic with a right-to-left layout. The dashboard is English only.

### How things flow

1. A visitor fills in the **booking form**. The request is saved, Rahaf gets an email, and it appears under **Dashboard → Bookings**.
2. After the trial, Rahaf creates an **invite code** under **Dashboard → Students** and sends the sign-up link. A code can only be used once.
3. The student **signs up** as an adult learner or as a parent for a child. Their portal shows the lessons, plan, homework and files Rahaf adds from the student's dashboard page.
4. Students **ask questions** from the portal or the Q&A page. Rahaf gets an email and answers from her phone. When she publishes, the student gets an email, and the answer appears on the public Q&A page without the student's name, unless she unticks "public".

## Run it locally

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                     # DEBUG=True, SQLite by default
python manage.py migrate
python manage.py seed_content                            # courses, FAQs, resources, sample Q&A
python manage.py createsuperuser                         # this is Rahaf's login (staff)
python manage.py runserver
```

Open http://localhost:8000. Emails print in the terminal while `EMAIL_BACKEND` is left at its default.

To use PostgreSQL locally, set `DATABASE_URL=postgres://user:pass@localhost:5432/rahaf` in `.env`.

Run the tests:

```bash
python manage.py test core
```

## Deploy

### Render (free tier, easiest)
1. Push this repo to GitHub.
2. On Render, go to **New → Blueprint** and pick the repo. `render.yaml` creates the Postgres database and the web service.
3. Fill in the environment variables it asks for: `TEACHER_EMAIL`, `SITE_URL` (for example `https://rahaf-arabic.onrender.com`), the email settings, and `CLOUDINARY_URL`.
4. Open the Render **Shell** and run `python manage.py createsuperuser` to create Rahaf's account.

### Heroku
`Procfile` and `.python-version` are included. Add the Heroku Postgres add-on and set the same config vars. Migrations and `seed_content` run on release.

### Production settings to check
- `DEBUG=False`, a long random `SECRET_KEY`, and `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS` set to your domain.
- **Email:** with Gmail, use an [app password](https://support.google.com/accounts/answer/185833). Any SMTP provider works, such as Brevo or Mailgun.
- **Uploads:** Render and Heroku wipe their disks on every deploy, so lesson files, resource PDFs and the teacher photo need `CLOUDINARY_URL` set. Without it, uploads disappear.

## Search engines and link previews

Every page has a title, a description and link-preview tags (Open Graph and Twitter), plus `hreflang` links that join each English page to its Arabic version. Titles and descriptions are in `core/seo.py`, with the Arabic in `locale/translate_ar.py`. The homepage also carries structured data (`core/jsonld.py`) describing Rahaf and her courses. Log-in, portal, dashboard, thank-you and search-result pages are marked `noindex`.

1. **Set `SITE_URL` to the real domain**, e.g. `https://www.example.com` with no trailing slash. Canonical links, preview images, `robots.txt` and the sitemap are all built from it. If it's left as `localhost`, Google sees the wrong addresses.
2. **Submit the sitemap in [Google Search Console](https://search.google.com/search-console).** Add the domain as a property, verify it, then go to *Sitemaps* and enter `sitemap.xml`. You can check both files at `/robots.txt` and `/sitemap.xml`.
3. **Check the link previews.** Paste a page link into a WhatsApp chat (to yourself) or into the [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/). English links show `static/img/og-image.png`, Arabic links `og-image-ar.png`. WhatsApp and Facebook cache previews, so after changing an image use the debugger's *Scrape Again* button.

## Before launch: things Rahaf needs to fill in

Most of these are in **/admin → Site settings**:

- [ ] WhatsApp number (digits only, with country code). WhatsApp buttons appear once it's set.
- [ ] Contact email, social links, years teaching, students taught, reply time
- [ ] Teacher photo (4:5 portrait) and intro video link (YouTube *embed* URL)
- [ ] "About me" story and qualifications, in English and Arabic (they start as [bracket] prompts)
- [ ] Course prices (**Courses**). Prices stay hidden until added.
- [ ] FAQ answers for **payment** and **cancellation** (they start as [bracket] prompts)
- [ ] Upload the six **resource** PDFs. Until then they show "Coming soon".
- [ ] Add **testimonials** from real students. The section stays hidden until at least one is added.
- [ ] Fill in the brackets in `templates/core/privacy.html`, remove the yellow template box, and get the policy checked before launch.
- [ ] Have Rahaf read the Arabic text (her surname is spelled ملسي) (`locale/translate_ar.py` and the course/FAQ content in admin).

## Editing translations

Interface text lives in templates inside `{% trans %}` tags. Arabic versions are in `locale/translate_ar.py`. After changing text:

```bash
python manage.py makemessages -l ar --ignore=dashboard/* --ignore=templates/dashboard/* --ignore=templates/emails/*
python locale/translate_ar.py      # fills known strings, lists any missing ones
python manage.py compilemessages   # needs gettext (apt install gettext / brew install gettext)
```

Content that Rahaf edits herself (courses, FAQs, resources, testimonials, the About text) has separate English and Arabic fields in the admin. If an Arabic field is left empty, the Arabic site falls back to the English text.

## Project layout

```
config/       settings, URLs (with /en/ and /ar/ prefixes)
core/         homepage, resources, privacy, site settings, emails, seed command, tests
accounts/     email login, magic links, invite-code sign-up, student profiles
bookings/     trial requests
qa/           student questions and Rahaf's answers
portal/       lessons, learning plan, homework, shared files
dashboard/    Rahaf's phone-friendly dashboard
templates/    all HTML
static/       site.css, site.js, favicon
locale/       Arabic translations
```

Design: the "Arabic Tutor Website" design canvas (star-and-ر logo, sand/teal/gold palette, Plus Jakarta Sans, IBM Plex Sans Arabic and Amiri).
