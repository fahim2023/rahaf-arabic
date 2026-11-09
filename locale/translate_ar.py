"""Fill the Arabic .po file from the table below, then compile it.

After adding new {% trans %} strings to templates:
    python manage.py makemessages -l ar --ignore=dashboard/* --ignore=templates/dashboard/* --ignore=templates/emails/*
    python locale/translate_ar.py      # fills what it knows, lists what's missing
    python manage.py compilemessages

Ask a native speaker (Rahaf!) to read through the Arabic before launch.
"""
from pathlib import Path

import polib

AR = {
    # Forms & accounts
    "Email": "البريد الإلكتروني",
    "Password": "كلمة المرور",
    "Your password": "كلمة المرور",
    "Keep me logged in": "تذكّرني",
    "That email and password don't match. Please try again.": "البريد الإلكتروني وكلمة المرور غير متطابقين. حاول مرة أخرى.",
    "This account is inactive.": "هذا الحساب غير مفعّل.",
    "Your name": "الاسم",
    "Full name": "الاسم الكامل",
    "Child's first name": "الاسم الأول للطفل",
    "First name only": "الاسم الأول فقط",
    "Age range": "الفئة العمرية",
    "At least 8 characters": "٨ أحرف على الأقل",
    "Invite code": "رمز الدعوة",
    "I agree to the privacy policy.": "أوافق على سياسة الخصوصية.",
    "Send me the free monthly worksheet (optional).": "أرسلوا لي ورقة العمل الشهرية المجانية (اختياري).",
    "There's already an account with this email. Try logging in.": "يوجد حساب بهذا البريد الإلكتروني. جرّب تسجيل الدخول.",
    "That invite code isn't valid or has already been used.": "رمز الدعوة غير صالح أو استُخدم من قبل.",
    "Please add your child's first name.": "يرجى إضافة الاسم الأول للطفل.",
    "Please choose an age range.": "يرجى اختيار الفئة العمرية.",
    "Myself": "أنا",
    "My child": "طفلي",
    "Welcome! Your account is ready.": "أهلاً بك! حسابك جاهز.",
    "Your login link": "رابط تسجيل الدخول",
    "If that email has an account, a login link is on its way. It works for 20 minutes.":
        "إن كان لهذا البريد حساب، فرابط الدخول في طريقه إليك. يعمل الرابط لمدة ٢٠ دقيقة.",
    "That login link has expired or was already used. Please request a new one.":
        "انتهت صلاحية رابط الدخول أو استُخدم من قبل. اطلب رابطًا جديدًا.",
    "Level / course": "المستوى / الدورة",
    "Preferred times": "الأوقات المفضّلة",
    "Message": "رسالتك",
    "e.g. Sarah": "مثلًا: سارة",
    "e.g. Weekday evenings, UK time": "مثلًا: مساء أيام الأسبوع، بتوقيت بريطانيا",
    "Why do you want to learn Arabic? Any experience so far?": "لماذا تريد تعلّم العربية؟ هل لديك أي خبرة سابقة؟",
    "Complete beginner": "مبتدئ تمامًا",
    "Beginner": "مبتدئ",
    "Intermediate": "متوسط",
    "Advanced": "متقدم",
    "Quranic Arabic": "العربية القرآنية",
    "Kids' Classes": "دروس الأطفال",
    "English": "الإنجليزية",
    "Arabic": "العربية",
    "Email address": "البريد الإلكتروني",
    "You're subscribed. The next worksheet will land in your inbox.": "تم الاشتراك. ستصلك ورقة العمل القادمة على بريدك.",
    "Please enter a valid email address.": "يرجى إدخال بريد إلكتروني صحيح.",
    "Writing": "الكتابة",
    "Listening": "الاستماع",
    "Speaking": "المحادثة",
    "Reading": "القراءة",
    "Vocabulary": "المفردات",
    "Your question": "سؤالك",
    "Any details (optional)": "تفاصيل إضافية (اختياري)",
    "Topic": "الموضوع",
    "e.g. How do I say “the bill, please” in Levantine?": "مثلًا: كيف أقول «الحساب لو سمحت» بالشامية؟",
    "Dialects": "اللهجات",
    "Grammar": "القواعد",
    "Quranic": "القرآنية",
    "Kids": "الأطفال",
    "Other": "أخرى",
    "Thanks! Your question has gone to Rahaf.": "شكرًا! وصل سؤالك إلى رهف.",
    "Please write your question before sending.": "يرجى كتابة سؤالك قبل الإرسال.",

    # Login / signup / reset
    "Rahaf Malasy": "رهف ملاسي",
    "Log in": "تسجيل الدخول",
    "Your lessons, homework and answers to your questions are waiting for you.": "دروسك وواجباتك وإجابات أسئلتك بانتظارك.",
    "For students and parents with an account.": "للطلاب والأهل الذين لديهم حساب.",
    "Forgot password?": "نسيت كلمة المرور؟",
    "Show": "إظهار",
    "Hide": "إخفاء",
    "or": "أو",
    "Email me a login link": "أرسل لي رابط دخول بالبريد",
    "Send link": "أرسل الرابط",
    "New here?": "جديد هنا؟",
    "Accounts are for current students.": "الحسابات مخصّصة للطلاب الحاليين.",
    "Create your account": "أنشئ حسابك",
    "after your trial, or": "بعد الدرس التجريبي، أو",
    "book a free trial": "احجز درسًا تجريبيًا مجانيًا",
    "first.": "أولًا.",
    "Reset your password": "إعادة تعيين كلمة المرور",
    "It happens to everyone. We'll get you back in.": "يحدث هذا للجميع. سنساعدك على الدخول من جديد.",
    "Enter your email and we'll send you a link to choose a new password.": "أدخل بريدك الإلكتروني وسنرسل لك رابطًا لاختيار كلمة مرور جديدة.",
    "Send reset link": "أرسل رابط إعادة التعيين",
    "Back to log in": "العودة إلى تسجيل الدخول",
    "Password changed": "تم تغيير كلمة المرور",
    "You can now log in with your new password.": "يمكنك الآن تسجيل الدخول بكلمة المرور الجديدة.",
    "Choose a new password": "اختر كلمة مرور جديدة",
    "Save password": "احفظ كلمة المرور",
    "Link expired": "انتهت صلاحية الرابط",
    "This reset link has expired or was already used.": "انتهت صلاحية هذا الرابط أو استُخدم من قبل.",
    "Request a new link": "اطلب رابطًا جديدًا",
    "Check your email": "تفقّد بريدك الإلكتروني",
    "If that email has an account, a reset link is on its way. Check your spam folder too.":
        "إن كان لهذا البريد حساب، فرابط إعادة التعيين في طريقه إليك. تفقّد مجلد الرسائل غير المرغوب فيها أيضًا.",
    "See your upcoming lessons": "شاهد دروسك القادمة",
    "Download notes and homework": "حمّل الملاحظات والواجبات",
    "Ask questions between lessons": "اطرح أسئلتك بين الدروس",
    "Already have one?": "لديك حساب؟",
    "Who is learning?": "من سيتعلّم؟",
    "Adult learner": "متعلّم بالغ",
    "I'm the parent or guardian": "أنا وليّ الأمر",
    "Your name (parent)": "اسمك (وليّ الأمر)",
    "Use 8 or more characters.": "استخدم ٨ أحرف أو أكثر.",
    "(from Rahaf after your trial)": "(من رهف بعد الدرس التجريبي)",
    "I agree to the": "أوافق على",
    "privacy policy": "سياسة الخصوصية",
    "Create account": "إنشاء الحساب",
    "No invite code yet?": "ليس لديك رمز دعوة بعد؟",
    "Book a free trial": "احجز درسًا تجريبيًا",

    # Base / booking
    "Learn Arabic with Rahaf": "تعلّم العربية مع رهف",
    "Patient, personal one-to-one Arabic lessons online with Rahaf Malasy, a native Syrian teacher. Modern Standard, Levantine and Quranic Arabic for adults and children.":
        "دروس عربية فردية أونلاين بصبر واهتمام مع رهف ملاسي، معلّمة سورية. الفصحى واللهجة الشامية والعربية القرآنية للكبار والأطفال.",
    "Skip to content": "تخطَّ إلى المحتوى",
    "I'll only use your details to arrange lessons.": "سأستخدم بياناتك فقط لترتيب الدروس.",
    "See the privacy policy.": "اطّلع على سياسة الخصوصية.",
    "Request my free trial": "أرسل طلب الدرس التجريبي",
    "Book your free trial lesson": "احجز درسك التجريبي المجاني",
    "Please check the highlighted fields.": "يرجى مراجعة الحقول المحدّدة.",
    "Trial request received": "وصل طلب الدرس التجريبي",
    "Thanks! Your trial request is in": "شكرًا! وصلني طلبك للدرس التجريبي",
    "I'll reply within %(h)s hours to find a time that suits you. Keep an eye on your inbox, and check your spam folder just in case.":
        "سأردّ خلال %(h)s ساعة لنجد وقتًا يناسبك. تابع بريدك الوارد، وتفقّد مجلد الرسائل غير المرغوب فيها احتياطًا.",
    "I'll email you": "سأراسلك بالبريد",
    "with a few times in your time zone.": "مع بعض المواعيد بحسب توقيتك.",
    "You pick a time": "تختار موعدًا",
    "and get a Zoom or Google Meet link.": "ويصلك رابط Zoom أو Google Meet.",
    "We meet": "نلتقي",
    "for a relaxed %(m)s-minute chat about your goals.": "في دردشة مريحة مدتها %(m)s دقيقة عن أهدافك.",
    "Rather chat on WhatsApp?": "تفضّل واتساب؟",
    "Get a head start: free resources": "ابدأ مبكرًا: مصادر مجانية",

    # Homepage
    "Learn Arabic with Rahaf · Online Arabic lessons": "تعلّم العربية مع رهف · دروس عربية أونلاين",
    "Online 1-to-1 lessons · Modern Standard, Levantine & Quranic Arabic": "دروس فردية أونلاين · الفصحى، اللهجة الشامية، والعربية القرآنية",
    "Learn Arabic with Rahaf: patient, personal online lessons": "تعلّم العربية مع رهف: دروس شخصية بصبر واهتمام",
    "Live one-to-one lessons for adults and children, built around your goals and your pace. From your first letter to confident conversation.":
        "دروس فردية مباشرة عبر الإنترنت للكبار والأطفال، بخطة تناسب أهدافك ووتيرتك. من أول حرف حتى المحادثة بثقة.",
    "Book a Free Trial Lesson": "احجز درسًا تجريبيًا مجانيًا",
    "WhatsApp Me": "راسلني على واتساب",
    "%(n)s years teaching": "سنوات التدريس: %(n)s",
    "Native Syrian speaker": "متحدثة أصلية من سوريا",
    "Adults & children": "للكبار والأطفال",
    "Teacher photo coming soon": "صورة المعلّمة قريبًا",
    "Rahaf Malasy, Arabic teacher": "رهف ملاسي، معلّمة لغة عربية",
    "Teacher photo": "صورة المعلّمة",
    "Meet Rahaf": "تعرّف على رهف",
    "Meet Rahaf · intro video coming soon": "تعرّف على رهف · فيديو تعريفي قريبًا",
    "years teaching": "سنوات تدريس",
    "students taught": "طالب وطالبة",
    "1-to-1": "فردي",
    "live lessons": "دروس مباشرة",
    "Hello, I'm Rahaf": "أهلاً، أنا رهف",
    "Qualifications": "المؤهلات",
    "Patient pace": "صبر ووتيرة مريحة",
    "No rushing. Mistakes are part of learning.": "لا استعجال، فالأخطاء جزء من التعلّم.",
    "Speak from day one": "محادثة من اليوم الأول",
    "Real phrases in your very first lesson.": "عبارات حقيقية من درسك الأول.",
    "Your goals": "أهدافك أولًا",
    "Every plan is built around why you're learning.": "كل خطة مبنية على سبب تعلّمك.",
    "Courses for every learner": "دروس لكل متعلّم",
    "Not sure where you fit? Book a free trial and we'll find your level together.": "لست متأكدًا من مستواك؟ احجز درسًا تجريبيًا مجانيًا وسنحدّده معًا.",
    "Book": "احجز",
    "Something else in mind?": "لديك هدف آخر؟",
    "Arabic for travel, work, or speaking with family? Tell me your goal and I'll shape lessons around it.":
        "العربية للسفر أو العمل أو للتواصل مع العائلة؟ أخبرني بهدفك وسأصمّم الدروس حوله.",
    "Ask me on WhatsApp": "اسألني على واتساب",
    "Tell me your goal": "أخبرني بهدفك",
    "How it works": "كيف تبدأ",
    "Pick a time that suits you. We'll chat about your level and what you want to achieve.": "اختر وقتًا يناسبك، وسنتحدث عن مستواك وما تريد تحقيقه.",
    "Get a personalised plan": "احصل على خطة شخصية",
    "I'll put together a lesson plan for your goal, whether that's travel, faith, family or work.":
        "أعدّ لك خطة دروس تناسب هدفك، سواء كان السفر أو الدين أو العائلة أو العمل.",
    "Learn on Zoom or Google Meet": "تعلّم عبر Zoom أو Google Meet",
    "Live lessons from anywhere, with notes and practice in your student portal after every class.":
        "دروس مباشرة من أي مكان، مع ملاحظات وتمارين تجدها في بوابة الطالب بعد كل درس.",
    "What students say": "آراء الطلاب",
    ", parent": "، وليّ أمر",
    "Student Q&A": "أسئلة الطلاب",
    "Real questions from my students, answered. Browse, search, or ask your own.": "أسئلة حقيقية من طلابي مع إجاباتها. تصفّح، أو ابحث، أو اطرح سؤالك.",
    "Search questions": "ابحث في الأسئلة",
    "Search questions, e.g. letters": "ابحث في الأسئلة، مثلًا: الحروف",
    "Search": "بحث",
    "Ask a Question": "اطرح سؤالًا",
    "Asking questions is for enrolled students. Log in and your question goes straight to Rahaf.":
        "طرح الأسئلة متاح للطلاب المسجّلين. سجّل الدخول وسيصل سؤالك مباشرة إلى رهف.",
    "Become a student": "انضم كطالب",
    "No questions yet. Students can log in and ask the first one.": "لا توجد أسئلة بعد. يمكن للطلاب تسجيل الدخول وطرح أول سؤال.",
    "See all questions": "كل الأسئلة",
    "Frequently asked questions": "الأسئلة الشائعة",
    "Tell me a little about yourself and when you're free. I reply within %(h)s hours to arrange a time in your time zone.":
        "أخبرني قليلًا عن نفسك وعن أوقات فراغك. أردّ خلال %(h)s ساعة لنحدّد موعدًا حسب توقيتك.",
    "Prefer to chat?": "تفضّل المحادثة؟",
    "Message me on WhatsApp": "راسلني على واتساب",
    "Or email": "أو عبر البريد الإلكتروني:",
    "Privacy policy": "سياسة الخصوصية",

    # Resources
    "Free Arabic resources": "مصادر عربية مجانية",
    "Worksheets, charts and phrase lists I use with my own students. Download, print and practise at your own pace.":
        "أوراق عمل وجداول وقوائم عبارات أستخدمها مع طلابي. حمّلها واطبعها وتدرّب على راحتك.",
    "Filter resources": "تصفية المصادر",
    "All": "الكل",
    "Alphabet": "الحروف",
    "Levantine": "الشامية",
    "MSA": "الفصحى",
    "Download": "تحميل",
    "Coming soon": "قريبًا",
    "No resources in this category yet.": "لا توجد مصادر في هذا القسم بعد.",
    "For my students": "لطلابي",
    "Full lesson notes, audio and homework": "ملاحظات الدروس كاملة مع التسجيلات والواجبات",
    "Students get every worksheet, listening exercise and lesson note in their own portal.":
        "يحصل الطلاب على كل أوراق العمل وتمارين الاستماع وملاحظات الدروس في بوابتهم الخاصة.",
    "A new worksheet every month": "ورقة عمل جديدة كل شهر",
    "One free resource and one useful phrase, straight to your inbox. No spam.": "مصدر مجاني وعبارة مفيدة تصلك على بريدك. بلا رسائل مزعجة.",
    "Subscribe": "اشترك",
    "By subscribing you agree to the": "باشتراكك فإنك توافق على",
    "Unsubscribe any time.": "يمكنك إلغاء الاشتراك في أي وقت.",

    # Header / footer
    "Rahaf Malasy · Online Arabic lessons": "رهف ملاسي · دروس عربية أونلاين",
    "Language": "اللغة",
    "Main": "القائمة الرئيسية",
    "Arabic Teacher": "معلّمة لغة عربية",
    "Menu": "القائمة",
    "About": "نبذة عني",
    "Courses": "الدروس",
    "Resources": "المصادر",
    "FAQ": "الأسئلة الشائعة",
    "Dashboard": "لوحة التحكم",
    "My portal": "بوابتي",

    # Q&A
    "Asked by a parent": "سؤال من أحد الأهل",
    "Asked by a beginner student": "سؤال من طالب مبتدئ",
    "Asked by an intermediate student": "سؤال من طالب متوسط",
    "Asked by an advanced student": "سؤال من طالب متقدم",
    "Asked by a student": "سؤال من طالب",
    "Rahaf answered": "إجابة رهف",
    "Topics": "المواضيع",
    "No questions match that yet. Students can log in and ask it.": "لا توجد أسئلة مطابقة بعد. يمكن للطلاب تسجيل الدخول وطرحها.",
    "Pages": "الصفحات",
    "Newer": "الأحدث",
    "Older": "الأقدم",

    # Portal
    "My learning": "تعلّمي",
    "Student portal": "بوابة الطالب",
    "Log out": "تسجيل الخروج",
    "Portal": "البوابة",
    "Overview": "نظرة عامة",
    "My lessons": "دروسي",
    "Homework": "الواجبات",
    "Files": "الملفات",
    "My questions": "أسئلتي",
    "Welcome back, %(name)s": "أهلاً بعودتك يا %(name)s",
    "Next lesson": "الدرس القادم",
    "Your time": "بتوقيتك",
    "%(m)s min": "%(m)s دقيقة",
    "Topic:": "الموضوع:",
    "Join lesson": "انضم إلى الدرس",
    "Reschedule": "تغيير الموعد",
    "No lesson booked yet": "لا يوجد درس محجوز بعد",
    "Rahaf will add your next lesson here once it's arranged.": "ستضيف رهف درسك القادم هنا عند تحديد موعده.",
    "Your plan": "خطتك",
    "%(p)s%% complete": "مكتملة بنسبة %(p)s%%",
    "Plan progress": "التقدّم في الخطة",
    ", done": "، مكتمل",
    "Now": "الآن",
    "Your personalised plan will appear here after your first lessons.": "ستظهر خطتك الشخصية هنا بعد دروسك الأولى.",
    "%(d)s of %(t)s done": "أُنجز %(d)s من %(t)s",
    "Mark as not done": "تحديد كغير منجز",
    "Mark as done": "تحديد كمنجز",
    "Due": "التسليم",
    "No homework right now. Enjoy the break!": "لا واجبات الآن. استمتع بالاستراحة!",
    "Shared with you": "ملفات مشتركة معك",
    "Lesson notes and audio from Rahaf will appear here.": "ستظهر هنا ملاحظات الدروس والتسجيلات من رهف.",
    "Ask Rahaf a question": "اسأل رهف",
    "Answers may be shared on the public Q&A without your name.": "قد تُنشر الإجابات في صفحة الأسئلة العامة دون ذكر اسمك.",
    "Send question": "أرسل السؤال",
    "Answered": "تمت الإجابة",
    "Waiting": "بانتظار الإجابة",
}

PLURALS = {
    "%(n)s lesson so far": ["عدد الدروس حتى الآن: %(n)s"] * 6,
}


def main():
    path = Path(__file__).parent / "ar" / "LC_MESSAGES" / "django.po"
    po = polib.pofile(str(path))
    po.metadata["Language"] = "ar"
    po.metadata["Content-Type"] = "text/plain; charset=UTF-8"
    missing = []
    for entry in po:
        if entry.msgid_plural:
            forms = PLURALS.get(entry.msgid)
            if forms:
                entry.msgstr_plural = {i: f for i, f in enumerate(forms)}
            else:
                missing.append(entry.msgid)
        elif entry.msgid in AR:
            entry.msgstr = AR[entry.msgid]
        else:
            missing.append(entry.msgid)
        if "fuzzy" in entry.flags:
            entry.flags.remove("fuzzy")
    po.save()
    print(f"Translated {len(po) - len(missing)} of {len(po)} strings.")
    for m in missing:
        print("  missing:", m)


if __name__ == "__main__":
    main()
