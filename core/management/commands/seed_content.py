"""Load the starting content from the design: courses, FAQs, resources and
sample Q&A, in English and Arabic. Safe to run more than once: it only
adds things that aren't there yet.

    python manage.py seed_content
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import FAQ, Course, Resource, SiteSettings
from qa.models import Question

COURSES = [
    dict(level_label_en="Level 1", level_label_ar="المستوى ١", name_en="Beginner", name_ar="مبتدئ",
         description_en="The alphabet, sounds, reading and writing, plus everyday phrases from lesson one.",
         description_ar="الحروف والأصوات والقراءة والكتابة، مع عبارات يومية من الدرس الأول.",
         duration_en="60 min · 1-to-1", duration_ar="٦٠ دقيقة · درس فردي"),
    dict(level_label_en="Level 2", level_label_ar="المستوى ٢", name_en="Intermediate", name_ar="متوسط",
         description_en="Grow your vocabulary and grammar, and hold real conversations about daily life.",
         description_ar="بناء المفردات والقواعد، ومحادثات حقيقية حول مواضيع الحياة اليومية.",
         duration_en="60 min · 1-to-1", duration_ar="٦٠ دقيقة · درس فردي"),
    dict(level_label_en="Level 3", level_label_ar="المستوى ٣", name_en="Advanced", name_ar="متقدم",
         description_en="Fluency, authentic texts, writing practice and deeper discussion on topics you choose.",
         description_ar="طلاقة في الحديث، ونصوص أصيلة، وتدريب على الكتابة، ونقاشات أعمق في مواضيع تختارها.",
         duration_en="60 min · 1-to-1", duration_ar="٦٠ دقيقة · درس فردي"),
    dict(level_label_en="Faith & reading", level_label_ar="للقراءة والتدبّر", name_en="Quranic Arabic",
         name_ar="العربية القرآنية", highlighted=True,
         description_en="Read the Quran correctly, learn the basics of tajweed, and understand its vocabulary and structure.",
         description_ar="قراءة صحيحة للقرآن، وأساسيات التجويد، وفهم مفرداته وتراكيبه.",
         duration_en="60 min · 1-to-1", duration_ar="٦٠ دقيقة · درس فردي"),
    dict(level_label_en="Ages 5–12", level_label_ar="الأعمار ٥–١٢", name_en="Kids' Classes", name_ar="دروس الأطفال",
         description_en="Short, playful lessons with games, stories and songs. Parents get simple activities to practise at home.",
         description_ar="دروس قصيرة ومرحة بالألعاب والقصص والأناشيد، مع أنشطة بسيطة للأهل للتدرّب في البيت.",
         duration_en="30–45 min · 1-to-1", duration_ar="٣٠–٤٥ دقيقة · درس فردي"),
]

FAQS = [
    ("What about time zones?", "ماذا عن فرق التوقيت؟",
     "Lessons are booked in your local time. Syria is on UTC+3 all year, and I teach students in the UK, Europe "
     "and North America, so evenings and weekends are usually available.",
     "تُحجز الدروس حسب توقيتك المحلي. توقيت سوريا هو UTC+3 طوال العام، وأدرّس طلابًا في بريطانيا وأوروبا "
     "وأمريكا الشمالية، لذلك تتوفر عادةً أوقات مسائية وفي عطلة نهاية الأسبوع."),
    ("How do I pay?", "كيف أدفع؟",
     "[How payment works: e.g. pay per lesson or in packages, and by which method. Payment details are sent after "
     "your free trial.]",
     "[طريقة الدفع: مثلًا الدفع لكل درس أو باقات، وعبر أي وسيلة. تُرسل تفاصيل الدفع بعد الدرس التجريبي.]"),
    ("Which platform do we use?", "ما المنصة التي نستخدمها؟",
     "Zoom or Google Meet, whichever you prefer. You get the link before each lesson. All you need is a laptop, "
     "tablet or phone with a stable connection.",
     "Zoom أو Google Meet، حسب ما تفضّل. يصلك الرابط قبل كل درس، وكل ما تحتاجه حاسوب أو جهاز لوحي أو هاتف "
     "واتصال جيد بالإنترنت."),
    ("Do I need to buy books or materials?", "هل أحتاج إلى شراء كتب أو مواد؟",
     "No. I provide everything: PDF worksheets, slides and audio, shared in your student portal after each lesson "
     "so you can review at your own pace.",
     "لا. أوفّر لك كل شيء: أوراق عمل PDF وشرائح وتسجيلات صوتية، تجدها في بوابة الطالب بعد كل درس لتراجعها على راحتك."),
    ("What if I need to cancel or reschedule?", "ماذا لو احتجت إلى إلغاء درس أو تغيير موعده؟",
     "[Cancellation policy: e.g. free rescheduling with 24 hours' notice.]",
     "[سياسة الإلغاء: مثلًا تغيير الموعد مجانًا قبل ٢٤ ساعة.]"),
]

RESOURCES = [
    dict(category="alphabet", glyph="أ ب ت ث", file_format="PDF", title_en="The Arabic alphabet chart",
         title_ar="جدول الحروف العربية",
         description_en="All 28 letters in their isolated, initial, middle and final forms, with sounds and example words.",
         description_ar="الحروف الثمانية والعشرون بأشكالها المنفصلة وفي أول الكلمة ووسطها وآخرها، مع أصواتها وأمثلة.",
         size_note_en="2 pages", size_note_ar="صفحتان"),
    dict(category="alphabet", glyph="ا د ذ ر ز و", file_format="PDF", title_en="Letter-joining practice sheets",
         title_ar="أوراق تدريب على وصل الحروف",
         description_en="Trace and copy the six letters that never connect forward, then practise joining full words.",
         description_ar="تتبّع وانسخ الحروف الستة التي لا تتصل بما بعدها، ثم تدرّب على وصل كلمات كاملة.",
         size_note_en="6 pages", size_note_ar="٦ صفحات"),
    dict(category="levantine", glyph="كيفك؟", file_format="PDF + MP3", title_en="50 everyday Levantine phrases",
         title_ar="٥٠ عبارة شامية يومية",
         description_en="Greetings, café, shopping and getting around, with transliteration and audio by Rahaf.",
         description_ar="التحية والمقهى والتسوّق والتنقّل، مع الكتابة بالحروف اللاتينية وتسجيل صوتي بصوت رهف.",
         size_note_en="4 pages · audio", size_note_ar="٤ صفحات · صوت"),
    dict(category="msa", glyph="١ ٢ ٣", file_format="PDF", title_en="Numbers 1–100", title_ar="الأرقام من ١ إلى ١٠٠",
         description_en="Arabic-Indic and Western digits side by side, with how to say each number in Modern Standard Arabic.",
         description_ar="الأرقام العربية والغربية جنبًا إلى جنب، مع نطق كل رقم بالفصحى.",
         size_note_en="3 pages", size_note_ar="٣ صفحات"),
    dict(category="quranic", glyph="بسم الله", file_format="PDF", title_en="Key words in the short surahs",
         title_ar="كلمات أساسية في قصار السور",
         description_en="The most frequent words in Juz’ ‘Amma, grouped by root, to help you understand what you recite.",
         description_ar="أكثر الكلمات تكرارًا في جزء عمّ، مجمّعة حسب الجذر، لتفهم ما تقرأ.",
         size_note_en="5 pages", size_note_ar="٥ صفحات"),
    dict(category="kids", glyph="ب بطة", file_format="PDF", title_en="Alphabet colouring pages",
         title_ar="صفحات تلوين الحروف",
         description_en="One page per letter with a simple picture to colour. Great alongside kids’ lessons.",
         description_ar="صفحة لكل حرف مع رسمة بسيطة للتلوين. مناسبة مع دروس الأطفال.",
         size_note_en="28 pages", size_note_ar="٢٨ صفحة"),
]

QUESTIONS = [
    dict(topic="dialects", asker_label="beginner",
         question="What is the difference between Modern Standard Arabic and Levantine?",
         question_ar="ما الفرق بين العربية الفصحى واللهجة الشامية؟",
         answer="Modern Standard Arabic (fusha) is used in books, news and formal speech across the Arab world. "
                "Levantine is the everyday spoken Arabic of Syria, Lebanon, Jordan and Palestine. If you mainly want "
                "to chat with people, start with Levantine; for reading and the Quran, start with MSA. Many students "
                "learn both.",
         answer_ar="الفصحى هي لغة الكتب والأخبار والخطاب الرسمي في العالم العربي كله، أما الشامية فهي العربية المحكية "
                   "يوميًا في سوريا ولبنان والأردن وفلسطين. إن كان هدفك الحديث مع الناس فابدأ بالشامية، وإن كان "
                   "القراءة أو القرآن فابدأ بالفصحى. كثير من الطلاب يتعلّمون الاثنتين."),
    dict(topic="reading", asker_label="beginner",
         question="How long will it take me to read Arabic script?",
         question_ar="كم من الوقت أحتاج لأقرأ الحروف العربية؟",
         answer="With regular lessons, most beginners read simple words within a few weeks. There are 28 letters, and "
                "most change shape depending on where they sit in a word, so we practise them step by step.",
         answer_ar="مع دروس منتظمة، يقرأ معظم المبتدئين كلمات بسيطة خلال أسابيع قليلة. في العربية ٢٨ حرفًا، ويتغيّر "
                   "شكل معظمها حسب موقعه في الكلمة، لذلك نتدرّب عليها خطوة بخطوة."),
    dict(topic="writing", asker_label="intermediate",
         question="Why do some letters connect and others don’t?",
         question_ar="لماذا تتصل بعض الحروف ولا يتصل بعضها الآخر؟",
         answer="Six letters (ا د ذ ر ز و) never join to the letter after them. Every other letter connects on both "
                "sides. Once you know those six, handwriting gets much easier.",
         answer_ar="ستة حروف لا تتصل بما بعدها أبدًا: ا د ذ ر ز و. وكل الحروف الأخرى تتصل من الجهتين. حين تحفظ هذه "
                   "الستة تصبح الكتابة أسهل بكثير."),
    dict(topic="kids", asker_label="parent",
         question="Can my child learn if we don’t speak Arabic at home?",
         question_ar="هل يمكن لطفلي أن يتعلّم مع أننا لا نتحدث العربية في البيت؟",
         answer="Yes. Kids’ lessons use games, songs and stories, and I send short activities you can do together, "
                "even if you are learning too.",
         answer_ar="نعم. دروس الأطفال تعتمد على الألعاب والأناشيد والقصص، وأرسل أنشطة قصيرة يمكنكم القيام بها معًا، "
                   "حتى لو كنتم تتعلّمون أيضًا."),
]

SETTINGS_PLACEHOLDERS = dict(
    story_en="[Her story in her own words: where she grew up in Syria, how she started teaching, and why she loves "
             "helping people discover Arabic. Two or three warm, personal sentences.]",
    story_ar="[قصتها بكلماتها: أين نشأت في سوريا، وكيف بدأت التدريس، ولماذا تحب مساعدة الناس على اكتشاف العربية.]",
    story2_en="[A second short paragraph on the kind of students she teaches and what they go on to do: travel, "
              "faith, family, work or study.]",
    story2_ar="[فقرة قصيرة ثانية عن الطلاب الذين تدرّسهم وما يحققونه: السفر، أو الدين، أو العائلة، أو العمل، أو الدراسة.]",
    qualifications_en="[Degree, e.g. BA in Arabic Language & Literature, University of ...]\n"
                      "[Teaching certificate or ijazah, if any]\n"
                      "[X] years teaching Arabic to non-native speakers",
    qualifications_ar="[الشهادة الجامعية، مثلًا: إجازة في اللغة العربية وآدابها، جامعة ...]\n"
                      "[شهادة تدريس أو إجازة، إن وُجدت]\n"
                      "[X] سنوات في تعليم العربية لغير الناطقين بها",
)


class Command(BaseCommand):
    help = "Load starting courses, FAQs, resources and sample Q&A from the design"

    def handle(self, *args, **options):
        site = SiteSettings.load()
        changed = False
        for field, value in SETTINGS_PLACEHOLDERS.items():
            if not getattr(site, field):
                setattr(site, field, value)
                changed = True
        if changed:
            site.save()

        added = 0
        for i, data in enumerate(COURSES):
            _, created = Course.objects.get_or_create(name_en=data["name_en"], defaults={**data, "order": i})
            added += created
        for i, (q_en, q_ar, a_en, a_ar) in enumerate(FAQS):
            _, created = FAQ.objects.get_or_create(
                question_en=q_en, defaults=dict(question_ar=q_ar, answer_en=a_en, answer_ar=a_ar, order=i))
            added += created
        for i, data in enumerate(RESOURCES):
            _, created = Resource.objects.get_or_create(title_en=data["title_en"], defaults={**data, "order": i})
            added += created
        for i, data in enumerate(QUESTIONS):
            _, created = Question.objects.get_or_create(
                question=data["question"],
                defaults={**data, "status": Question.STATUS_ANSWERED, "is_public": True,
                          "answered_at": timezone.now() - timedelta(days=i)})
            added += created
        self.stdout.write(self.style.SUCCESS(f"Done. Added {added} items."))
