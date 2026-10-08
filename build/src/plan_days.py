# -*- coding: utf-8 -*-
"""Day-by-day plan (Day 1 = Wed 7 Oct 2026 ... Day 45 = Fri 20 Nov 2026)."""
from datetime import date, timedelta

START = date(2026, 10, 7)
WD = ['จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 'ศุกร์', 'เสาร์', 'อาทิตย์']
TH_MONTH = {10: 'ต.ค.', 11: 'พ.ย.'}

FILES = {
    'book': 'All that IELTS คู่มือเตรียมสอบ IELTS ใหม่ล่าสุด (1).pdf',
    'aelt': 'Aelt Writing 0421.pdf',
    'image': 'Image (1).pdf',
    'guide': 'Opinion_Essay_Guide.docx',
    'improved': 'Improved_Opinion_Essays.docx',
}
SRC_NAME = {
    'book': 'All that IELTS',
    'aelt': 'Aelt Writing 0421.pdf',
    'image': 'Image (1).pdf',
    'guide': 'Opinion_Essay_Guide.docx',
    'improved': 'Improved_Opinion_Essays.docx',
    'app': 'ในแอปนี้',
}


def pdf_page(p):
    """Printed book page -> PDF page index (scan has duplicated pp. 66-67 and 180-181)."""
    return p + 2 if p <= 67 else (p + 4 if p <= 181 else p + 6)


def B(a, b=None, what=''):
    b = b or a
    return {'src': 'book', 'pages': f'{a}' + (f'–{b}' if b != a else ''), 'pdf': pdf_page(a),
            'pdfEnd': pdf_page(b), 'what': what}


def S(src, what, pages='', pdf=None):
    return {'src': src, 'pages': pages, 'pdf': pdf, 'pdfEnd': pdf, 'what': what}


def APP(what, link=''):
    return {'src': 'app', 'pages': '', 'pdf': None, 'what': what, 'link': link}


# Weekday default blocks: Vocabulary 15 -> Reading 40 -> Writing/Grammar 30 -> Error notebook 5
WEEKDAY = [('vocab', 15), ('reading', 40), ('writing', 30), ('errors', 5)]
INTEGRATION = [('vocab', 10), ('reading', 30), ('writing', 40), ('errors', 10)]
SATURDAY = [('test', 120), ('vocab', 15), ('review', 15)]
SUNDAY = [('essay', 60), ('weekly', 20), ('vocabreview', 15)]
MOCK = [('test', 120), ('essay', 60), ('review', 20), ('vocab', 15)]

PHASES = [
    {'id': 'P1', 'name': 'Diagnostic', 'th': 'วัดระดับ + ปูพื้น Grammar', 'days': (1, 6), 'range': '7–12 ต.ค.',
     'goal': 'ทดสอบ Reading + Writing เพื่อหาจุดอ่อน ทบทวน Grammar ที่จำเป็น และเริ่มศัพท์ Academic'},
    {'id': 'P2', 'name': 'Reading Foundation', 'th': 'พื้นฐานการอ่าน', 'days': (7, 13), 'range': '13–19 ต.ค.',
     'goal': 'Main idea, Topic, Supporting details, Reference, Context clues'},
    {'id': 'P3', 'name': 'Reading Strategy', 'th': 'กลยุทธ์การอ่าน', 'days': (14, 20), 'range': '20–26 ต.ค.',
     'goal': 'Skimming, Scanning, Inference, Vocabulary in context, Academic passages'},
    {'id': 'P4', 'name': 'Writing Foundation', 'th': 'พื้นฐานการเขียน', 'days': (21, 27), 'range': '27 ต.ค.–2 พ.ย.',
     'goal': 'Sentence → Topic sentence → Supporting ideas → Conclusion'},
    {'id': 'P5', 'name': 'Academic Writing', 'th': 'เขียนเชิงวิชาการ', 'days': (28, 34), 'range': '3–9 พ.ย.',
     'goal': 'Opinion writing, coherence/cohesion, connectors, grammar correction'},
    {'id': 'P6', 'name': 'Integration', 'th': 'รวมทักษะ + จับเวลา', 'days': (35, 40), 'range': '10–15 พ.ย.',
     'goal': 'Reading จับเวลา + Writing จับเวลา'},
    {'id': 'P7', 'name': 'Mock Exam', 'th': 'สอบจำลองเต็มชุด', 'days': (41, 43), 'range': '16–18 พ.ย.',
     'goal': 'จำลองสอบเต็มชุด 3 ชั่วโมง (Reading 120 + Writing 60) 3 ครั้ง'},
    {'id': 'P8', 'name': 'Error Review', 'th': 'ปิดจุดอ่อน', 'days': (44, 44), 'range': '19 พ.ย.',
     'goal': 'ทบทวนเฉพาะข้อผิดพลาด + Vocabulary'},
    {'id': 'P9', 'name': 'Light Review', 'th': 'ทบทวนเบา ๆ แล้วพัก', 'days': (45, 45), 'range': '20 พ.ย.',
     'goal': 'ไม่ทำข้อสอบหนัก ทบทวน template + คำศัพท์ แล้วพัก'},
]


def phase_of(d):
    for p in PHASES:
        if p['days'][0] <= d <= p['days'][1]:
            return p['id']


# ---------------------------------------------------------------------------
# Writing tasks. kind: diag-paragraph | analysis | sentences | paragraph | intro | body | parts | essay | summary | rewrite
# topic: essay-bank id (R1..R16, RX) or docx model id (GE1..GE5, IE1..IE5, IMG) for comparison.
# ---------------------------------------------------------------------------
D = {}

D[1] = dict(
    title='เปิดตัว + วัดระดับเบื้องต้น', focusR='รู้จักข้อสอบ + Diagnostic', focusW='Grammar diagnostic + ย่อหน้าแรก',
    goal='รู้จักรูปแบบข้อสอบ KKU-AELT และวัดพื้นฐาน Reading / Grammar / Writing ก่อนเริ่มแผน 45 วัน',
    read=[APP('คู่มือในแอป → แท็บ “ข้อมูลข้อสอบ” และ “กลยุทธ์ Reading” (10 นาทีก่อนเริ่ม)', 'guide'),
          S('aelt', 'หัวข้อ Writing 15 ข้อ (เลข 1–16 ไม่มีข้อ 12; หลายข้อระบุว่าเป็นข้อสอบจริงปี 2020–2021) + Tips “Writing ชอบออกแนวการศึกษา ตาม TREND”', 'หน้า 1–3', 1),
          S('guide', 'ส่วนที่ 1: โครงสร้าง Opinion Essay 4 ย่อหน้า + เทคนิคสำคัญ (อ่านให้จบ)'),
          B(21, 25, 'Writing Task 2 คืออะไร + ชนิดของ Essay (KKU-AELT ใช้แบบแสดงความเห็น Agree/Disagree)'),
          B(206, 210, 'ภาพรวมรูปแบบคำถาม Reading + Tips ของ John (อ่านเร็ว ๆ ไม่ต้องจำ)')],
    reading=dict(lesson='L_FORMAT', passages=['W01']),
    grammar='G01',
    task=dict(kind='paragraph', topic='GE1', minutes=20, words='120–150',
              prompt='Some people believe that technology has made our lives more stressful. Do you agree or disagree?',
              steps=['อ่านโจทย์ 1 นาที ขีดเส้นใต้คำสำคัญ (technology / more stressful)',
                     'เลือกจุดยืนเดียว (Agree หรือ Disagree) แล้วจดเหตุผล 2 ข้อ (2 นาที)',
                     'เขียน 1 ย่อหน้า 120–150 คำ: ประโยคจุดยืน → เหตุผล 1 + ตัวอย่าง → เหตุผล 2 → ประโยคปิด',
                     'ห้ามเปิดตัวอย่างก่อนเขียนเสร็จ — นี่คืองานตั้งต้น (baseline) ไว้เทียบในวันที่ 45'],
              compare='เทียบกับ Essay 1 “Technology and Stress” ใน Opinion_Essay_Guide.docx'),
    error='จดคะแนน Diagnostic: Reading W01 __/10, Grammar G01 __/15, ย่อหน้า __ คำ และจุดอ่อน 3 อันดับแรก',
)
D[2] = dict(
    title='Previewing & Predicting + โครงประโยค', focusR='Previewing & predicting', focusW='Fragment / Run-on + วิเคราะห์ตัวอย่าง essay',
    goal='อ่านแบบ “ดูภาพรวมก่อน” และเขียนประโยคให้ครบโครงสร้าง ไม่มี fragment / run-on',
    read=[B(25, 35, 'เกณฑ์ให้คะแนน 4 ด้าน + “50 วลีใช้บ่อยใน Writing” (หน้า 32–33) + ไวยากรณ์ 5 ข้อที่ห้ามผิด (หน้า 33–35)'),
          S('image', 'ตัวอย่าง essay “Big salary is much more important than job satisfaction” (291 คำ) — อ่านแล้ววิเคราะห์โครงสร้าง', 'หน้า 1', 1),
          S('improved', 'Essay 1 (Big salary): เทียบ “พี่เขียนเอง” กับฉบับปรับปรุง + “จุดที่ปรับปรุง” 6 ข้อ')],
    reading=dict(lesson='L_PREVIEW', passages=['W02']),
    grammar='G02',
    task=dict(kind='analysis', topic='IMG', minutes=15, words='3 ประโยค',
              prompt='วิเคราะห์ essay ตัวอย่าง “Big salary…” แล้วเขียน thesis statement ของตัวเองให้โจทย์จริง 3 ข้อ',
              steps=['ในตัวอย่าง (Image (1).pdf) หา: ประโยค paraphrase โจทย์ / thesis / topic sentence ย่อหน้า 2 และ 3 / ตัวอย่างที่ใช้ / คำเชื่อม / ประโยคสรุป',
                     'สังเกตจุดที่ควรแก้ในตัวอย่าง เช่น “twentieth first century” → “twenty-first century”, “get inspire” → “get inspired”',
                     'เขียน thesis statement (1 ประโยค/ข้อ) แสดงจุดยืนชัดเจนสำหรับ: R1 Students will learn a foreign language easily if it is integrated with another subject. / R4 Students perform better in school when they are rewarded rather than punished. / R5 Online courses are preferable to face-to-face courses.'],
              compare='ดูตัวอย่าง thesis ในคลัง Essay (R1, R4, R5) หลังเขียนเสร็จ'),
    error='จดประโยค fragment หรือ run-on ที่ตัวเองเคยเขียน 2 ประโยค พร้อมฉบับแก้',
)
D[3] = dict(
    title='Scanning + Tense/SVA + Paraphrase โจทย์', focusR='Scanning (ตัวเลข ชื่อ วันที่)', focusW='Tense & Subject–verb agreement + paraphrase',
    goal='หาข้อมูลเฉพาะได้เร็วด้วย scanning และ paraphrase โจทย์ได้ 3 วิธี',
    read=[B(35, 40, 'Band score 5–8 + ตัวอย่างย่อหน้าแต่ละระดับ — ดูว่า 6 กับ 7 ต่างกันตรงไหน'),
          S('guide', 'ส่วนที่ 2: คำศัพท์สำคัญ 50 คำสำหรับ Opinion Essay (อ่านผ่าน ทำเครื่องหมายคำที่ยังไม่รู้)')],
    reading=dict(lesson='L_SCAN', passages=['W03']),
    grammar='G03',
    task=dict(kind='sentences', topic=None, minutes=15, words='5 ประโยค',
              prompt='Paraphrase ประโยคแรกของบทนำสำหรับโจทย์จริง 5 ข้อ (ห้ามลอกคำในโจทย์ทั้งประโยค)',
              steps=['R2 Students value grades over learning.',
                     'R6 Some people think that they can learn better by themselves than with a teacher.',
                     'R11 Education is the single most important factor in the development of a country.',
                     'R13 National university entrance examination should be abolished.',
                     'R14 Learning from experience is better than learning from a book.',
                     'ใช้อย่างน้อย 2 วิธีต่อประโยค: (1) synonym  (2) เปลี่ยน word form  (3) เปลี่ยนโครงสร้าง เช่น active → passive / It is often argued that …'],
              compare='ดูตัวอย่าง paraphrase ในคลัง Essay ของแต่ละหัวข้อ'),
    error='จดคำถาม scanning ที่พลาด (อ่านตัวเลข/ชื่อผิด) และสาเหตุ',
)
D[4] = dict(
    title='Reading Test 1 — Diagnostic เต็มรูปแบบ', focusR='Full test 6 passages / 69 ข้อ / 120 นาที', focusW='—',
    goal='ทำข้อสอบเต็มชุดครั้งแรกเพื่อหาจุดอ่อนรายทักษะ (ไม่ต้องกังวลคะแนน)',
    read=[APP('ก่อนสอบ: อ่าน “กลยุทธ์ทำข้อสอบ 120 นาที” ในคู่มือ (5 นาที)', 'guide'),
          APP('หลังสอบ: อ่านคำอธิบายเฉลยทุกข้อที่ผิด แล้วดูกราฟแยกทักษะในหน้า “สถิติ”', 'stats')],
    test='T1',
    error='ทักษะที่ผิดมากที่สุด 2 อันดับ (ดูจากผลแยกทักษะ) และ passage ที่ใช้เวลามากเกินไป',
)
D[5] = dict(
    title='Writing Diagnostic 60 นาที + ทบทวนสัปดาห์', focusR='ทบทวนข้อผิดสัปดาห์ 1', focusW='Essay เต็ม: ข้อสอบจริง R3',
    goal='เขียน essay เต็มครั้งแรกภายใต้เวลาจริง แล้วตรวจด้วย checklist',
    read=[B(68, 70, 'Final Check 10 ข้อ + ตัวอย่างการตรวจงานระดับ 5.5 (อ่านหลังเขียนเสร็จ)'),
          B(380, 383, 'ภาคผนวก I: Checklist 3 นาทีสุดท้าย พร้อมตัวอย่างข้อผิด 10 แบบ')],
    essay=dict(topic='R3', minutes=60),
    review=dict(days=[1, 2, 3, 4]),
    error='จาก checklist: ข้อผิดที่เจอบ่อยที่สุดใน essay นี้ 3 อย่าง',
)
D[6] = dict(
    title='วิเคราะห์ผล Diagnostic + Articles/Prepositions', focusR='วิเคราะห์ข้อผิด + Mixed practice', focusW='Articles, countable nouns, prepositions',
    goal='เปลี่ยนผล Diagnostic เป็นแผนแก้จุดอ่อน และแก้ article/preposition ที่ผิดบ่อย',
    read=[B(380, 383, 'ภาคผนวก I: ทบทวนข้อ 3 (Article) และข้อ 5 (Preposition)'),
          S('improved', '“สรุปหลักการปรับปรุงสำคัญ (เพื่อให้ได้ 80+)” 6 ข้อ')],
    reading=dict(lesson='L_ERRORS', passages=['W04']),
    grammar='G04',
    task=dict(kind='rewrite', topic='R3', minutes=20, words='50–60 คำ + 5 ประโยค',
              prompt='เขียนบทนำของ essay วันที่ 5 ใหม่ และแก้ประโยคที่ผิดอย่างน้อย 5 ประโยค',
              steps=['เปิด essay วันที่ 5 (Writing Studio) อ่านทั้งเรื่องอีกครั้ง',
                     'เขียนบทนำใหม่ 50–60 คำ: paraphrase โจทย์ + thesis ที่แสดงจุดยืนชัดเจน (strongly agree / disagree)',
                     'เลือก 5 ประโยคที่ผิด (article, preposition, tense, SVA) แล้วเขียนฉบับแก้'],
              compare='เทียบบทนำกับ model ของ R3 ในคลัง Essay'),
    error='ตั้งเป้า 3 ข้อ: (1) ทักษะ Reading ที่อ่อนที่สุด (2) Grammar ที่ผิดบ่อย (3) คะแนน Reading ที่อยากได้ใน Mock',
)
D[7] = dict(
    title='Topic vs Main idea + Relative clauses', focusR='Topic vs Main idea', focusW='Relative clauses + topic sentences',
    goal='แยก “เรื่องอะไร” (topic) กับ “ผู้เขียนพูดอะไรเกี่ยวกับเรื่องนั้น” (main idea) ได้ทุกย่อหน้า',
    read=[B(222, 223, 'เคล็ดลับข้อสอบ Heading = หา main idea ของย่อหน้า (ประเด็นหลักมักอยู่หลัง however)'),
          B(84, 86, 'Relative pronoun 1–2 และ where (ใช้รวม 2–3 ประโยคเป็นประโยคเดียว)')],
    reading=dict(lesson='L_TOPIC_MAIN', passages=['W05']),
    grammar='G05',
    task=dict(kind='sentences', topic='GE2', minutes=15, words='2 topic sentences + 3 ประโยค',
              prompt='University education should be free for all students. Do you agree or disagree?',
              steps=['เลือกจุดยืน แล้วเขียน topic sentence สำหรับเหตุผล 1 และเหตุผล 2 (คนละมุม เช่น ความเท่าเทียม / เศรษฐกิจของประเทศ)',
                     'รวมประโยคต่อไปนี้ด้วย relative clause: (1) Students come from low-income families. They often cannot afford tuition. (2) Germany offers tuition-free education. It ranks highly in innovation. (3) Graduates have large loans. They delay buying homes.'],
              compare='เทียบกับ Essay 2 “Free University Education” ใน Opinion_Essay_Guide.docx (ดู topic sentence ของ Body 1–2)'),
    error='จด 1 ย่อหน้าที่ตอบ main idea ผิด: ทำไมตัวเลือกที่เลือก “แคบไป/กว้างไป”',
)
D[8] = dict(
    title='Implied main idea & Best title + Passive voice', focusR='Implied main idea + best title', focusW='Passive voice + ย่อหน้าแรก',
    goal='หา main idea ที่ไม่ได้เขียนตรง ๆ และเลือกชื่อเรื่องที่ครอบคลุมพอดี',
    read=[B(223, 226, 'แบบฝึก Heading “Onyx” Q1–4 (ทำจริง 8 นาที) + เฉลยหน้า 225–226'),
          B(90, 92, 'แบบฝึกเขียนประโยค 10 ข้อ (ทำข้อ 3 = passive) + ประโยคคำตอบตัวอย่าง')],
    reading=dict(lesson='L_IMPLIED', passages=['W06'], bookTask='All that IELTS หน้า 223–226: Heading “Onyx” Q1–4'),
    grammar='G06',
    task=dict(kind='paragraph', topic='GE3', minutes=20, words='120–150',
              prompt='Working from home is more productive than working in an office. Do you agree or disagree?',
              steps=['เลือกจุดยืน เขียน 1 ย่อหน้า: topic sentence → อธิบาย → ตัวอย่าง → ประโยคเชื่อมกลับ',
                     'ใช้ passive voice อย่างน้อย 2 ครั้ง (เช่น employees are expected to…, productivity is affected by…)'],
              compare='เทียบกับ Essay 3 “Working from Home (Disagree)” Body 1 ใน Opinion_Essay_Guide.docx'),
    error='จดชื่อเรื่อง (title) ที่เลือกผิดและเหตุผลว่าทำไมตัวเลือกนั้นแคบ/กว้างเกินไป',
)
D[9] = dict(
    title='Supporting details + Connectors', focusR='Major vs minor details + signal words', focusW='Connectors & punctuation',
    goal='แยกรายละเอียดหลัก/รอง และใช้คำเชื่อมถูกตำแหน่งพร้อมเครื่องหมายวรรคตอน',
    read=[B(226, 230, 'Matching A/B: “Orinoco River”, “Louis Pasteur” (ทำจริง) + เฉลยหน้า 229–230'),
          B(26, 30, 'การเชื่อมระหว่าง/ภายในย่อหน้า + ตาราง Transitional words ที่ใช้บ่อย (เลือกจำ 2 คำต่อหน้าที่)')],
    reading=dict(lesson='L_DETAILS', passages=['W07'], bookTask='All that IELTS หน้า 226–230: Matching A (Q11–12) และ B (Q13–15)'),
    grammar='G07',
    task=dict(kind='paragraph', topic='GE5', minutes=20, words='130–150',
              prompt='Children should be taught financial literacy in school. Do you agree or disagree?',
              steps=['เขียน 1 ย่อหน้าเหตุผลข้อที่ 1 ให้มี: First and foremost, … For instance, … Therefore, …',
                     'ตรวจ: หลัง However / Therefore / For instance ต้องมี comma; but / so เชื่อม 2 ประโยคด้วย comma หน้า but/so'],
              compare='เทียบกับ Essay 5 “Financial Literacy in Schools” ใน Opinion_Essay_Guide.docx'),
    error='จดคำเชื่อมที่ใช้ผิดหน้าที่ (เช่น ใช้ however แทน but) พร้อมประโยคแก้',
)
D[10] = dict(
    title='Reference words + Pronoun agreement', focusR='Reference (it, they, this, which, the former…)', focusW='Pronoun reference & agreement',
    goal='ตามคำอ้างอิงกลับไปหาคำนามที่ถูกต้อง และเขียนสรรพนามให้ชัดเจน',
    read=[B(34, 34, 'ไวยากรณ์ห้ามผิดข้อ v: ใช้สรรพนามผิด (the individual → their)'),
          B(67, 68, 'เครื่องหมายวรรคตอน: full stop, comma, semicolon, apostrophe')],
    reading=dict(lesson='L_REFERENCE', passages=['W08']),
    grammar='G08',
    task=dict(kind='paragraph', topic='GE4', minutes=20, words='130–150',
              prompt='Governments should ban private cars in city centres. Do you agree or disagree?',
              steps=['เขียน 1 ย่อหน้า ใช้ “this/these + คำนาม” อย่างน้อย 3 ครั้ง (this policy, these emissions, such measures)',
                     'ขีดเส้นใต้สรรพนามทุกตัวแล้วถามว่า “หมายถึงอะไร” ถ้าตอบไม่ได้ทันที ให้เปลี่ยนเป็นคำนาม'],
              compare='เทียบกับ Essay 4 “Banning Private Cars” ใน Opinion_Essay_Guide.docx'),
    error='จดคำถาม reference ที่ผิด: คำอ้างอิง → สิ่งที่เลือก → คำตอบจริง',
)
D[11] = dict(
    title='Reading Test 2', focusR='Full test 6 passages / 69 ข้อ / 120 นาที', focusW='—',
    goal='ทำข้อสอบเต็มชุดครั้งที่ 2 ใช้ทักษะ main idea / details / reference ที่ฝึกมา',
    read=[APP('ก่อนสอบ: ทบทวน “แผนเวลา 120 นาที” ในคู่มือ', 'guide'),
          APP('หลังสอบ: เทียบกราฟทักษะกับ Test 1 ในหน้า “สถิติ”', 'stats')],
    test='T2',
    error='เปรียบเทียบกับ Test 1: ทักษะไหนดีขึ้น / แย่ลง',
)
D[12] = dict(
    title='Writing 60 นาที (ข้อสอบจริง R2) + ทบทวนสัปดาห์', focusR='ทบทวนข้อผิดสัปดาห์ 2', focusW='Essay เต็ม: R2',
    goal='เขียน essay เต็มเวลา 60 นาที โดยใช้โครง 4 ย่อหน้าและ checklist',
    read=[S('guide', 'ทวน “เทคนิคสำคัญที่ต้องจำ” (ส่วนที่ 1) ก่อนเขียน 3 นาที'),
          B(380, 383, 'ภาคผนวก I: Checklist ตรวจงาน (หลังเขียน)')],
    essay=dict(topic='R2', minutes=60),
    review=dict(days=[6, 7, 8, 9, 10, 11]),
    error='ข้อผิดใน essay ที่ซ้ำกับวันที่ 5 (ถ้ามี) และวิธีป้องกัน',
)
D[13] = dict(
    title='Context clues + Word forms', focusR='Context clues (definition, synonym, antonym, example)', focusW='Word forms',
    goal='เดาความหมายศัพท์จากบริบทโดยไม่ต้องแปลทุกคำ และเลือก word form ถูกชนิด',
    read=[B(210, 215, 'TFNG: “ความหมายต้องตรงกัน 100%” + ทักษะ 16 ข้อ (ฝึกจับ paraphrase/synonym)'),
          B(32, 33, '50 วลีใช้บ่อยใน Writing (achieve, allocate, contribute to, cope with …)')],
    reading=dict(lesson='L_CONTEXT', passages=['W09']),
    grammar='G09',
    task=dict(kind='paragraph', topic='IE2', minutes=20, words='130–150',
              prompt='Social skills are more important than academic skills. Do you agree or disagree?',
              steps=['เขียน 1 ย่อหน้าเหตุผลหลัก (เลือกจุดยืนเอง)',
                     'ใช้ word form อย่างน้อย 4 คู่: success/succeed/successful, importance/important, analysis/analytical, competence/competent'],
              compare='เทียบกับ Essay 2 (Social vs Academic skills) ใน Improved_Opinion_Essays.docx — ดูทั้งต้นฉบับและฉบับปรับปรุง'),
    error='จดศัพท์ที่เดาจากบริบทผิด + clue ที่มองข้ามไป',
)
D[14] = dict(
    title='Skimming & Paragraph function + Comparison', focusR='Skimming + หน้าที่ของย่อหน้า', focusW='Comparison + Introduction',
    goal='จับโครงเรื่องบทความยาวใน 2–3 นาที และรู้ว่าย่อหน้าแต่ละย่อหน้า “ทำหน้าที่อะไร”',
    read=[B(217, 220, 'แบบฝึก TFNG: “Mars – the Red Planet”, “Taste” (skim หาตำแหน่งก่อนตอบ) + เฉลย'),
          B(65, 66, 'E. การเปรียบเทียบ (while, but, however, more than, in contrast)'),
          S('improved', 'Essay 3 (Friends) และ Essay 4 (Telling the truth): อ่านเฉพาะบทนำฉบับปรับปรุง + บทวิเคราะห์ต้นฉบับ Essay 4 ข้อ 1')],
    reading=dict(lesson='L_SKIM', passages=['W10'], bookTask='All that IELTS หน้า 217–220: TFNG ชุด 1–2'),
    grammar='G10',
    task=dict(kind='intro', topic='IE3', minutes=20, words='50–60 คำ × 2',
              prompt='เขียนบทนำ 2 เรื่อง: (1) “Friends make you happier than family.” (2) “Always telling the truth is the most important consideration in any relationship.”',
              steps=['แต่ละบทนำ = ประโยค paraphrase โจทย์ + thesis ที่บอกจุดยืนและเหตุผล 2 ข้อแบบย่อ',
                     'ห้ามเปิดด้วย “The world is gradually changing.” หรือ “According to the statement”',
                     'ใช้คำเปรียบเทียบอย่างน้อย 1 ครั้ง (rather than / more … than / unlike)'],
              compare='เทียบกับบทนำฉบับปรับปรุงของ Essay 3 และ Essay 4 ใน Improved_Opinion_Essays.docx'),
    error='จดย่อหน้าที่ตอบ “purpose of paragraph” ผิด และหน้าที่ที่ถูกต้อง',
)
D[15] = dict(
    title='Scanning + Short answer + Numbers', focusR='Scanning + Short answer (≤ 3 คำ)', focusW='Numbers & quantities + body with evidence',
    goal='ตอบคำถามแบบเขียนคำตอบสั้นได้ตรงคำในบทความ สะกดถูก ไม่เกินจำนวนคำ',
    read=[B(232, 236, 'No More Than Three Words: “The Neanderthals”, “The Orient Express” + เฉลย (ตรงกับ short answer ของ KKU)'),
          B(149, 158, 'ภาษาบรรยายตัวเลข/แนวโน้ม (increase, decline, fluctuate, level off + ตารางคำบุพบท) — อ่านเฉพาะตารางคำ')],
    reading=dict(lesson='L_SHORTANS', passages=['W11'], bookTask='All that IELTS หน้า 232–236: NMT3W 6 ข้อ'),
    grammar='G11',
    task=dict(kind='paragraph', topic='IE5', minutes=20, words='130–150',
              prompt='Workers’ skills matter more than an education degree. Do you agree or disagree?',
              steps=['เขียน body paragraph 1 ย่อหน้า ใช้หลักฐาน/ตัวอย่างอาชีพเฉพาะ (แพทย์ วิศวกร โปรแกรมเมอร์)',
                     'ใช้ภาษาจำนวนอย่างน้อย 2 แบบ เช่น a large proportion of, the number of … has increased',
                     'ห้ามแต่งสถิติแล้วอ้างองค์กรจริง ใช้ “many”, “a growing number of” แทนได้'],
              compare='เทียบกับ Essay 5 (Skills vs Degree) ใน Improved_Opinion_Essays.docx'),
    error='จดคำตอบสั้นที่ผิดเพราะสะกด/เกินจำนวนคำ/ใช้คำไม่ตรงบทความ',
)
D[16] = dict(
    title='Inference, Purpose & Tone + Hedging', focusR='Inference / Author’s purpose / Tone', focusW='Hedging & modals',
    goal='อนุมานจากหลักฐาน ไม่เดาเกินข้อความ และเขียนอ้างความเห็นอย่างระมัดระวัง',
    read=[B(242, 246, 'Multiple Choice: เคล็ดลับ + แบบฝึก “Orinoco River”, “Freezing rain” + เฉลย'),
          B(36, 37, 'ตัวอย่าง Band 8: ใช้ may / can เพื่อไม่ฟันธงเกินไป')],
    reading=dict(lesson='L_INFER', passages=['W12'], bookTask='All that IELTS หน้า 242–246: MC 5 ข้อ'),
    grammar='G12',
    task=dict(kind='paragraph', topic='SMART', minutes=20, words='120',
              prompt='Smartphones should be banned in classrooms. Do you agree or disagree?',
              steps=['แก้ประโยคฟันธงเกินจริง 4 ประโยคให้มี hedging: (1) Smartphones always distract students. (2) All teachers hate phones. (3) Banning phones will solve every learning problem. (4) Students never use phones for learning.',
                     'เขียน 1 ย่อหน้า 120 คำ ใช้ may / tend to / is likely to / evidence suggests อย่างน้อย 3 ครั้ง'],
              compare='ดูย่อหน้าตัวอย่าง “Smartphones in classrooms” ที่แสดงหลังเขียน'),
    error='จดข้อ inference ที่ผิดเพราะ “เดาเกิน” — คำไหนในตัวเลือกที่แรงกว่าบทความ (always / all / only)',
)
D[17] = dict(
    title='Fact vs Opinion + Concession', focusR='Fact vs opinion + writer’s view', focusW='Conditionals & concession',
    goal='แยกข้อเท็จจริงกับความเห็นของผู้เขียน และเขียนประโยคยอมรับ–โต้แย้งโดยไม่เปลี่ยนจุดยืน',
    read=[B(76, 78, 'สำนวนเปิดย่อหน้าฝ่ายไม่เห็นด้วย (Those against the idea of …, However, these arguments miss …)'),
          B(29, 29, 'คำเชื่อมแสดงการยอมรับ: Even though / Although / In spite of / Despite')],
    reading=dict(lesson='L_FACTOP', passages=['W13']),
    grammar='G13',
    task=dict(kind='sentences', topic='CONCEDE', minutes=15, words='4 ประโยค',
              prompt='เขียนประโยค concession + rebuttal 1 ประโยคต่อโจทย์ (4 โจทย์จริง)',
              steps=['R5 Online courses are preferable to face-to-face courses.',
                     'R7 Big salary is much more important than job satisfaction.',
                     'R13 National university entrance examination should be abolished.',
                     'R16 Man is preferable when working alone than working with a team.',
                     'รูปแบบ: Although some argue that …, this view overlooks the fact that … / Admittedly, …; however, …'],
              compare='ดูประโยคตัวอย่างที่แสดงหลังเขียน'),
    error='จดประโยคในบทความที่เข้าใจผิดว่าเป็น fact ทั้งที่เป็น opinion (ดูคำว่า should, I believe, arguably)',
)
D[18] = dict(
    title='Reading Test 3', focusR='Full test 6 passages / 69 ข้อ / 120 นาที', focusW='—',
    goal='ใช้ skimming/scanning/inference ภายใต้เวลาจริง',
    read=[APP('ก่อนสอบ: ทบทวนสรุปกลยุทธ์ทุกทักษะในคู่มือ (5 นาที)', 'guide'),
          APP('หลังสอบ: ดูกราฟทักษะ เทียบ Test 1–3', 'stats')],
    test='T3',
    error='passage ที่ใช้เวลาเกิน 15 นาที (สั้น) หรือ 35 นาที (ยาว) และสาเหตุ',
)
D[19] = dict(
    title='Writing 60 นาที (ข้อสอบจริง R14) + ทบทวนสัปดาห์', focusR='ทบทวนข้อผิดสัปดาห์ 3', focusW='Essay เต็ม: R14',
    goal='เขียน essay เต็ม 60 นาที เน้นตัวอย่างที่เป็นรูปธรรม',
    read=[B(61, 64, 'Tips ระหว่างเขียน A–D: จำประโยคเปิดย่อหน้า + ตัวอย่างต้องเป็นรูปธรรม'),
          B(380, 383, 'Checklist ตรวจงาน (หลังเขียน)')],
    essay=dict(topic='R14', minutes=60),
    review=dict(days=[13, 14, 15, 16, 17, 18]),
    error='ตัวอย่างใน essay เป็นรูปธรรมพอหรือยัง (มีใคร/ที่ไหน/ผลอะไร)?',
)
D[20] = dict(
    title='อ่านบทความวิจัย + Noun phrases', focusR='Academic/research passages (IMRaD)', focusW='Nominalisation + summary',
    goal='อ่านบทความวิจัยแบบรู้โครง: วัตถุประสงค์ → วิธีการ → ผล → ข้อจำกัด แล้วสรุปเป็นภาษาตัวเอง',
    read=[B(236, 240, 'Summary completion: “Global warming…”, “Role of an architect” + เฉลย'),
          B(86, 87, 'Participle: N + V-ing / N + V3 (ทำประโยควิชาการให้กระชับ)')],
    reading=dict(lesson='L_RESEARCH', passages=['W14'], bookTask='All that IELTS หน้า 236–240: Summary 5 ข้อ'),
    grammar='G14',
    task=dict(kind='summary', topic='W14', minutes=15, words='60–80',
              prompt='สรุปบทความ W14 (โครงการ อสม. ควบคุมความดันโลหิตสูง) เป็นภาษาอังกฤษ 60–80 คำ',
              steps=['ประโยค 1: วัตถุประสงค์และรูปแบบการศึกษา', 'ประโยค 2: ผลหลัก', 'ประโยค 3: ข้อจำกัด/ข้อเสนอแนะ',
                     'ห้ามลอกประโยคจากบทความเกิน 4 คำติดกัน'],
              compare='เทียบกับ model summary ที่แสดงหลังเขียน'),
    error='จดส่วนของบทความวิจัย (Methods/Results/Discussion) ที่หาข้อมูลไม่เจอเร็ว',
)
D[21] = dict(
    title='Sentence types + Reading ผสม (หนังสือ Passage 1)', focusR='Mixed practice: main idea เร็ว', focusW='Sentence types & combining',
    goal='เขียนประโยคได้ 4 แบบ (simple / compound / complex / compound-complex) โดยไม่มีข้อผิดโครงสร้าง',
    read=[B(64, 65, 'ประโยคความรวม/ความซ้อน “When S V, S V as S V”'),
          B(84, 84, 'สรุป 8 โครงสร้างไวยากรณ์ทำคะแนนสูง (อ่านกรอบสรุป)'),
          B(248, 249, 'Mock IELTS Passage 1 “The periodic table – History” Q1–13 (ทำ 20 นาที) — เฉลยหน้า 256')],
    reading=dict(lesson='L_MIX_MAIN', passages=['W15'], bookTask='All that IELTS หน้า 248–249: Passage 1 (Q1–13) 20 นาที, เฉลยหน้า 256'),
    grammar='G15',
    task=dict(kind='sentences', topic='R4', minutes=15, words='5 ประโยค',
              prompt='Students perform better in school when they are rewarded rather than punished. (ข้อสอบจริง R4 — เตรียมไอเดียสำหรับวันที่ 22–27)',
              steps=['เขียน 5 ประโยคเกี่ยวกับโจทย์นี้: 1 simple, 1 compound (…, but …), 2 complex (Although/Because/When …), 1 มี relative clause',
                     'ทุกประโยคต้องสนับสนุนจุดยืนเดียวกัน (เลือกก่อนเขียน)'],
              compare='ดูไอเดียและ outline ของ R4 ในคลัง Essay'),
    error='ประโยคยาวที่เขียนแล้วกลายเป็น run-on — เขียนฉบับแก้',
)
D[22] = dict(
    title='Introduction & Thesis (เริ่มประกอบ essay R4)', focusR='Mixed practice: vocabulary in context', focusW='Introduction + thesis',
    goal='เขียนบทนำ 2–3 ประโยคที่ paraphrase โจทย์และบอกจุดยืนชัดเจนภายใน 5 นาที',
    read=[B(42, 49, 'โครงสร้างบทนำ: general statement → support → issue (paraphrase) → thesis + pattern ฉุกเฉิน'),
          B(72, 74, 'สำนวนขึ้นบทนำ + ประโยคใจความหลัก'),
          B(250, 252, 'Mock IELTS Passage 2 “Genetic disorders” Q14–27 (ทำ 20 นาที) — เฉลยหน้า 256–257')],
    reading=dict(lesson='L_MIX_VOCAB', passages=['W16'], bookTask='All that IELTS หน้า 250–252: Passage 2 (Q14–27) 20 นาที'),
    grammar='G16',
    task=dict(kind='parts', topic='R4', part='intro', minutes=20, words='50–60',
              prompt='Students perform better in school when they are rewarded rather than punished. Do you agree or disagree?',
              steps=['Brainstorm 3 นาที: เหตุผล 2 ข้อที่ไม่ซ้ำมุม', 'เขียน Introduction 50–60 คำ (paraphrase + thesis + preview เหตุผล 2 ข้อ)',
                     'ถ้ายังมีเวลา: เขียนบทนำสั้น ๆ ให้ R10 และ R11 อย่างละ 2 ประโยค'],
              compare='เทียบกับบทนำ model R4 ในคลัง Essay'),
    error='บทนำมีคำที่ลอกจากโจทย์กี่คำ? เปลี่ยนเป็น paraphrase',
)
D[23] = dict(
    title='Topic sentence + Supporting ideas (Body 1 ของ R4)', focusR='Mixed practice: inference', focusW='Body paragraph (PEEL / EEEE)',
    goal='เขียน body paragraph ที่มี topic sentence ชัด อธิบาย ยกตัวอย่าง และเชื่อมกลับจุดยืน',
    read=[B(49, 53, 'Body: topic sentence + supporting sentences + สูตร EEEE (Explanation, Evidence, Example, Effect)'),
          B(74, 78, 'Magic Words ที่ใช้เริ่มเนื้อหา (ฝ่ายเห็นด้วย / ไม่เห็นด้วย)'),
          B(254, 255, 'Mock IELTS Passage 3 “The solar car” Q28–40 (ทำ 20 นาที) — เฉลยหน้า 257')],
    reading=dict(lesson='L_MIX_INFER', passages=['W17'], bookTask='All that IELTS หน้า 254–255: Passage 3 (Q28–40) 20 นาที'),
    grammar='G17',
    task=dict(kind='parts', topic='R4', part='body1', minutes=20, words='100–120',
              prompt='R4 — Body paragraph 1',
              steps=['Point: topic sentence เหตุผลที่ 1', 'Explain: อธิบาย 1–2 ประโยค', 'Example: ตัวอย่างรูปธรรม (โรงเรียน/ห้องเรียน/งานวิจัยแบบทั่วไป)', 'Link: เชื่อมกลับจุดยืน'],
              compare='เทียบกับ Body 1 ของ model R4'),
    error='ประโยคใน Body 1 ที่ไม่เกี่ยวกับ topic sentence (ลบทิ้ง)',
)
D[24] = dict(
    title='Brainstorming + Body 2 ของ R4', focusR='Mixed practice: reference', focusW='Supporting ideas & examples',
    goal='คิดไอเดีย 2 ด้านได้ใน 2 นาที และเขียน Body 2 คนละมุมกับ Body 1',
    read=[B(57, 60, 'Tips ก่อนเขียน: เข้าใจโจทย์ 20 วินาที → Brainstorm 1–2 นาที (ขอบเขต ตัวเอง/ครอบครัว/ประเทศ/มนุษยชาติ) → Organising'),
          B(384, 397, 'ภาคผนวก II Power Essay Brainstorming: อ่านหัวข้อแบบ Agree/Disagree #2, #7, #9, #10, #14, #15, #17, #18, #25, #27'),
          B(257, 260, 'คำแปล Mock IELTS — เช็กศัพท์ที่ไม่รู้จาก Passage 1–3')],
    reading=dict(lesson='L_MIX_REF', passages=['W18']),
    grammar='G18',
    task=dict(kind='parts', topic='R4', part='body2', minutes=20, words='100–120 + 4 outlines',
              prompt='R4 — Body paragraph 2 + outline ด่วน 4 หัวข้อ',
              steps=['เขียน Body 2 (มุมต่างจาก Body 1 เช่น แรงจูงใจระยะยาว / สุขภาพจิต / ความสัมพันธ์ครู–นักเรียน)',
                     'Outline ด่วน (2 นาที/หัวข้อ): R8 Young people are the best change makers. / R9 Thailand should not open to international tourist. / R13 National university entrance examination should be abolished. / R16 Man is preferable when working alone than working with a team. — เขียนแค่จุดยืน + เหตุผล 2 ข้อ'],
              compare='เทียบกับ Body 2 ของ model R4 และไอเดียในคลัง Essay'),
    error='ไอเดียที่ “นอกโจทย์” (ตอบคนละคำถาม) จากการ brainstorm วันนี้',
)
D[25] = dict(
    title='Reading Test 4', focusR='Full test 6 passages / 69 ข้อ / 120 นาที', focusW='—',
    goal='รักษาความเร็วและความแม่นยำตลอด 120 นาที',
    read=[APP('ก่อนสอบ: ทวนแผนเวลา', 'guide'), APP('หลังสอบ: เทียบกราฟทักษะ Test 1–4', 'stats')],
    test='T4',
    error='ทักษะที่ยังผิดซ้ำตั้งแต่ Test 1 (ถ้ามี) → แผนแก้',
)
D[26] = dict(
    title='Writing 60 นาที (ข้อสอบจริง R6) + ทบทวนสัปดาห์', focusR='ทบทวนข้อผิดสัปดาห์ 4', focusW='Essay เต็ม: R6',
    goal='เขียน essay เต็ม 60 นาที ใช้ intro/body ที่ฝึกในสัปดาห์นี้',
    read=[B(42, 55, 'ทวนโครงสร้าง Intro–Body–Conclusion ก่อนเขียน 3 นาที'), B(380, 383, 'Checklist ตรวจงาน')],
    essay=dict(topic='R6', minutes=60),
    review=dict(days=[20, 21, 22, 23, 24, 25]),
    error='เทียบ essay วันนี้กับวันที่ 5 และ 12: ดีขึ้นด้านไหน',
)
D[27] = dict(
    title='Conclusion + ประกอบ essay R4 เต็มเรื่อง', focusR='Long text strategy', focusW='Conclusion + full essay assembly',
    goal='เขียนบทสรุปที่ย้ำจุดยืนด้วยคำใหม่ + รวม essay เต็ม 270–300 คำ',
    read=[B(54, 55, 'การเขียนบทสรุป: วิธีสรุป 1 (ความเห็น + สรุปประเด็น) / วิธีสรุป 2 (ความเห็น + ข้อเสนอ)'),
          B(79, 82, 'สำนวนจบเนื้อหา + คำที่ปรากฏบ่อยใน Essay'),
          B(61, 68, 'Tips ระหว่างเขียน A–H: ห้ามภาษาพูด, ใช้วรรคตอนให้ถูก')],
    reading=dict(lesson='L_LONG', passages=['W19']),
    grammar='G19',
    task=dict(kind='parts', topic='R4', part='assemble', minutes=25, words='270–300',
              prompt='R4 — เขียน Conclusion แล้วรวม Intro + Body 1 + Body 2 + Conclusion เป็น essay เต็ม',
              steps=['เขียน Conclusion 40–50 คำ: In conclusion + ย้ำจุดยืนด้วยคำใหม่ + สรุปเหตุผล 2 ข้อ (ไม่เพิ่มเหตุผลใหม่)',
                     'รวมทั้ง 4 ส่วน แก้คำเชื่อมระหว่างย่อหน้าให้ลื่น',
                     'ตรวจด้วย Checklist 10 ข้อ (ภาคผนวก I)'],
              compare='เทียบกับ model R4 ทั้งเรื่อง'),
    error='นับคำ essay R4: ___ คำ ถ้าเกิน 330 ให้ตัดส่วนที่ซ้ำ ถ้าต่ำกว่า 260 ให้เพิ่มตัวอย่าง',
)
D[28] = dict(
    title='Opinion essay 6.0 vs 7.0 + ข้อผิดที่คนไทยพบบ่อย', focusR='Mixed: NOT / EXCEPT questions', focusW='R10 (ส่วนที่ 1)',
    goal='เห็นความต่างระหว่าง essay ระดับ 6.0 กับ 7.0 แล้วนำมาใช้กับ essay ของตัวเอง',
    read=[B(94, 105, 'Day 6: เขียน Agree/Disagree ระดับ 6.0 (จำกัดจำนวนรถในเมือง) vs 7.0 (ย้ายออกจากบ้านหลังจบ ม.ปลาย) ทีละ Step')],
    reading=dict(lesson='L_NOT', passages=['W20']),
    grammar='G20',
    task=dict(kind='parts', topic='R10', part='A', minutes=25, words='~150',
              prompt='When learning a language, studying grammar is more important than practising conversation skills. (ข้อสอบจริง 2020)',
              steps=['วางแผน 5 นาที (จุดยืน + เหตุผล 2 ข้อ + ตัวอย่าง)', 'เขียน Introduction + Body 1 (≈150 คำ) ใน 20 นาที'],
              compare='เทียบหลังเขียนส่วนที่ 2 ในวันพรุ่งนี้'),
    error='ข้อผิดแบบ “คนไทย” ที่เจอในงานตัวเอง (เช่น I am agree, there have, ขาด -s)',
)
D[29] = dict(
    title='Coherence & Cohesion (จบ R10)', focusR='Mixed: purpose & organisation', focusW='Cohesion + R10 (ส่วนที่ 2)',
    goal='ทำให้ essay อ่านลื่น: คำเชื่อมถูกตรรกะ ไม่ซ้ำ และอ้างอิงชัด',
    read=[B(26, 31, 'ทวน: การเชื่อมระหว่างย่อหน้า / ภายในย่อหน้า / ตารางคำเชื่อม'),
          S('guide', '“คำเชื่อม (Cohesive devices): ใช้ให้หลากหลาย อย่าใช้ซ้ำ” + ศัพท์ 50 คำข้อ 21–46')],
    reading=dict(lesson='L_PURPOSE', passages=['W21']),
    grammar='G21',
    task=dict(kind='parts', topic='R10', part='B', minutes=25, words='~150',
              prompt='R10 — เขียน Body 2 + Conclusion แล้วตรวจคำเชื่อมทั้งเรื่อง',
              steps=['เขียน Body 2 (มุมต่างจาก Body 1) และ Conclusion', 'วงกลมคำเชื่อมทุกคำ: ห้ามซ้ำเกิน 1 ครั้ง และต้องตรงความสัมพันธ์ (เพิ่ม/ขัดแย้ง/ผล/ตัวอย่าง)'],
              compare='เทียบกับ model R10 ในคลัง Essay'),
    error='คำเชื่อมที่ใช้ซ้ำมากที่สุดใน essay และคำแทน 2 คำ',
)
D[30] = dict(
    title='Counterpoint โดยไม่เสียจุดยืน (เริ่ม R11)', focusR='Mixed: tone & attitude', focusW='Stance consistency + R11 (ส่วนที่ 1)',
    goal='ยอมรับอีกฝ่ายได้ 1 ประโยคแล้วโต้กลับ โดย essay ยังเห็นด้วย/ไม่เห็นด้วยทั้งเรื่อง',
    read=[S('improved', 'Essay 4 (Telling the truth): บทวิเคราะห์ “ไม่ได้เลือกจุดยืนชัดเจน” — อ่านข้อ 1 Task Response'),
          B(118, 126, 'Day 8: ข้อดี/ข้อเสียของการท่อง Pattern + Pattern บทนำ/เนื้อหา (ใช้เป็นโครง ไม่ใช่ท่องทั้งก้อน)')],
    reading=dict(lesson='L_TONE', passages=['W22']),
    grammar='G22',
    task=dict(kind='parts', topic='R11', part='A', minutes=25, words='~150',
              prompt='Education is the single most important factor in the development of a country.',
              steps=['ระวังคำว่า “the single most important” — เป็นข้ออ้างที่แรงมาก จะ agree หรือ disagree ต้องตอบตรงขอบเขตนี้',
                     'วางแผน 5 นาที แล้วเขียน Introduction + Body 1 (มีประโยค concession + rebuttal 1 ประโยค)'],
              compare='เทียบหลังจบส่วนที่ 2 พรุ่งนี้'),
    error='ประโยคใน essay ที่ทำให้จุดยืน “ไม่ชัด” (ลบหรือเขียนใหม่)',
)
D[31] = dict(
    title='Lexical resource: Collocation + Formal style (จบ R11)', focusR='Mixed: paraphrase matching', focusW='Collocations + R11 (ส่วนที่ 2)',
    goal='ใช้คำที่ “เข้าคู่กันเป็นธรรมชาติ” และภาษาทางการ แทนคำยากที่ใช้ผิด',
    read=[S('improved', 'ตาราง “ประโยคที่เขียน | ปัญหา | ที่ควรเขียน” 14 รายการ (Essay 4) + หลักข้อ 3 “คำศัพท์หลากหลาย ไม่ซ้ำ”'),
          B(31, 33, 'Lexical Resource (6.0 vs 8.0) + ห้ามใช้คำกำกวม a lot of / very / something / good')],
    reading=dict(lesson='L_PARA', passages=['W23']),
    grammar='G23',
    task=dict(kind='parts', topic='R11', part='B', minutes=25, words='~150',
              prompt='R11 — Body 2 + Conclusion + อัปเกรดคำศัพท์',
              steps=['เขียน Body 2 + Conclusion', 'หาคำ important / good / bad / a lot of ในงาน แล้วเปลี่ยนเป็นคำที่แม่นกว่า (crucial, beneficial, detrimental, a substantial number of)'],
              compare='เทียบกับ model R11'),
    error='collocation ผิดที่เจอในงานตัวเอง (เช่น make a crime → commit a crime)',
)
D[32] = dict(
    title='Reading Test 5', focusR='Full test 6 passages / 69 ข้อ / 120 นาที', focusW='—',
    goal='ทำข้อสอบระดับยากขึ้นโดยรักษาแผนเวลา',
    read=[APP('ก่อนสอบ: ทวนแผนเวลา', 'guide'), APP('หลังสอบ: เทียบกราฟทักษะ Test 1–5', 'stats')],
    test='T5',
    error='ข้อที่ผิดเพราะ “รีบ” vs “ไม่รู้ศัพท์” vs “ตีความผิด” — นับแต่ละแบบ',
)
D[33] = dict(
    title='Writing 60 นาที (ข้อสอบจริง R9) + ทบทวนสัปดาห์', focusR='ทบทวนข้อผิดสัปดาห์ 5', focusW='Essay เต็ม: R9',
    goal='เขียน essay ประเด็นสังคม/เศรษฐกิจ ด้วยตัวอย่างที่เกี่ยวกับประเทศไทย',
    read=[B(126, 132, 'Day 8 body patterns ตามธีม (สุขภาพ สิ่งแวดล้อม เศรษฐกิจ …) — ใช้เป็นคลังไอเดีย'), B(380, 383, 'Checklist ตรวจงาน')],
    essay=dict(topic='R9', minutes=60),
    review=dict(days=[27, 28, 29, 30, 31, 32]),
    error='ส่วนที่ใช้เวลามากที่สุดตอนเขียน (วางแผน/เขียน/ตรวจ) และวิธีลดเวลา',
)
D[34] = dict(
    title='Grammar correction intensive', focusR='Long text + time management', focusW='แก้ข้อผิดในงานเขียนจริง',
    goal='ตรวจและแก้ไวยากรณ์ในย่อหน้าจริงได้เร็ว (ใช้ Checklist 10 ข้อ)',
    read=[S('improved', 'ต้นฉบับ “พี่เขียนเอง” ของ Essay 5 (Skills vs Degree): หาข้อผิดเองก่อน แล้วค่อยอ่าน “วิเคราะห์ปัญหาของต้นฉบับ”'),
          B(68, 70, 'Check Test ระดับ 5.5: ดูการแก้แต่ละจุดพร้อมเลขข้อ checklist'),
          B(380, 383, 'ภาคผนวก I ทั้ง 10 ข้อ')],
    reading=dict(lesson='L_LONGTIME', passages=['W24']),
    grammar='G24',
    task=dict(kind='rewrite', topic='IE5', minutes=25, words='10 จุด + 1 ย่อหน้า',
              prompt='แก้ต้นฉบับ Essay 5 (Skills vs Degree) ให้ถูก 10 จุด แล้วเขียนย่อหน้าที่อ่อนที่สุดของ essay วันที่ 33 ใหม่',
              steps=['คัดลอกต้นฉบับย่อหน้า Body 1 จาก Improved_Opinion_Essays.docx (หรือดูในแอป) แล้วแก้ 10 จุด',
                     'เปิด essay วันที่ 33 → เลือกย่อหน้าที่อ่อนที่สุด → เขียนใหม่ 100–130 คำ'],
              compare='เทียบกับ “วิเคราะห์ปัญหาของต้นฉบับ” และฉบับปรับปรุงของ Essay 5'),
    error='3 ข้อผิดที่ยังเกิดซ้ำตั้งแต่สัปดาห์แรก',
)
D[35] = dict(
    title='Integration 1: Reading จับเวลา + Essay 40 นาที (R13)', focusR='Timed: 2 short texts (12 นาที/บท)', focusW='Timed essay 40 นาที: R13',
    goal='ทำ passage สั้นให้ทันเวลา 12 นาที/บท และเขียน essay เต็มใน 40 นาที',
    read=[B(126, 132, 'Day 8 body patterns: หัวข้อการศึกษา/ผลกระทบต่อผู้อื่น — คลังไอเดีย (อ่านหลังเขียน)')],
    reading=dict(lesson='L_TIMED', passages=['W25', 'W26'], timed=24),
    grammar='G25',
    task=dict(kind='essay', topic='R13', minutes=40, words='250–300',
              prompt='National university entrance examination should be abolished. (ข้อสอบจริง ธ.ค. 2020)',
              steps=['วางแผน 5 นาที → เขียน 30 นาที → ตรวจ 5 นาที', 'ใช้ timer ในแอป ห้ามหยุดเวลา'],
              compare='เทียบกับ model R13'),
    error='เวลา Reading จริงต่อบท: ___ / ___ นาที',
)
D[36] = dict(
    title='Integration 2: Long text 30 นาที + Essay 40 นาที (R15)', focusR='Timed: 1 long text (30 นาที)', focusW='Timed essay 40 นาที: R15',
    goal='ทำบทความยาว + short answer ให้จบใน 30 นาที',
    read=[B(389, 389, 'ภาคผนวก II #12 (ทำงาน part-time ระหว่างเรียน) — ไอเดียเรื่องผลกระทบต่อชีวิตนักศึกษา'),
          S('guide', 'Essay 1 “Technology and Stress” — ดูวิธีเขียนเหตุผลด้านสุขภาพจิต')],
    reading=dict(lesson='L_TIMED', passages=['W27'], timed=30),
    grammar='G26',
    task=dict(kind='essay', topic='R15', minutes=40, words='250–300',
              prompt='Online learning has negative impact on students life. (ข้อสอบจริง ก.พ. 2021)',
              steps=['วางแผน 5 → เขียน 30 → ตรวจ 5 นาที'], compare='เทียบกับ model R15'),
    error='short answer ที่ผิด: เกินจำนวนคำ? สะกด? ใช้คำไม่ตรง?',
)
D[37] = dict(
    title='Integration 3: 2 short texts + Essay 40 นาที (R16)', focusR='Timed: 2 short texts', focusW='Timed essay 40 นาที: R16',
    goal='ความเร็วคงที่ในบทสั้น + essay ประเด็นการทำงาน',
    read=[B(61, 64, 'Tips A–C: ประโยคเปิดย่อหน้า + คำศัพท์สำคัญเฉพาะตัว (อ่านก่อนเขียน 3 นาที)')],
    reading=dict(lesson='L_TIMED', passages=['W28', 'W29'], timed=24),
    grammar='G27',
    task=dict(kind='essay', topic='R16', minutes=40, words='250–300',
              prompt='Man is preferable when working alone than working with a team. (ข้อสอบจริง มี.ค. 2021)',
              steps=['โจทย์เขียนไม่สมบูรณ์ทางไวยากรณ์ → paraphrase ให้ถูก เช่น “Some people believe that individuals work more effectively alone than in a team.”',
                     'วางแผน 5 → เขียน 30 → ตรวจ 5 นาที'],
              compare='เทียบกับ model R16'),
    error='ประโยคที่เขียนตามโจทย์ผิดไวยากรณ์ (ลอกโจทย์) — แก้ให้ถูก',
)
D[38] = dict(
    title='Integration 4: Long text + Essay 40 นาที (R7) เทียบตัวอย่างจริง', focusR='Timed: 1 long text', focusW='Timed essay 40 นาที: R7',
    goal='เขียนโจทย์ที่มีตัวอย่างในเอกสาร แล้วเทียบกับ 2 ฉบับ (Image (1) และ Improved)',
    read=[S('image', 'หลังเขียน: ตัวอย่าง “Big salary…” (291 คำ)', 'หน้า 1', 1),
          S('improved', 'หลังเขียน: Essay 1 ฉบับปรับปรุง + จุดที่ปรับปรุง')],
    reading=dict(lesson='L_TIMED', passages=['W30'], timed=30),
    grammar='G28',
    task=dict(kind='essay', topic='R7', minutes=40, words='250–300',
              prompt='Big salary is much more important than job satisfaction.',
              steps=['ห้ามเปิดตัวอย่างก่อนเขียนเสร็จ', 'วางแผน 5 → เขียน 30 → ตรวจ 5 นาที', 'หลังเขียน: ทำเครื่องหมาย 5 จุดที่ตัวอย่างเขียนดีกว่า แล้วแก้งานตัวเอง'],
              compare='เทียบกับ Image (1).pdf, Improved Essay 1 และ model R7'),
    error='5 จุดที่ตัวอย่างดีกว่างานของเรา (collocation / ตัวอย่าง / คำเชื่อม)',
)
D[39] = dict(
    title='Reading Test 6 (ชุดสุดท้ายก่อน Mock)', focusR='Full test 6 passages / 69 ข้อ / 120 นาที', focusW='—',
    goal='ซ้อมเหมือนจริง: เริ่ม 09.00 น. ถ้าทำได้ ใช้กระดาษคำตอบ ไม่ดูมือถือ',
    read=[APP('ก่อนสอบ: ทวนแผนเวลา + ข้อควรระวังในคู่มือ', 'guide'), APP('หลังสอบ: เทียบกราฟ Test 1–6', 'stats')],
    test='T6',
    error='สรุป 3 กลยุทธ์ที่จะใช้ใน Mock (เช่น ข้ามข้อยากก่อน, ตอบ short answer ทันที)',
)
D[40] = dict(
    title='Writing 60 นาที (ข้อสอบจริง R8) + ทบทวนสัปดาห์', focusR='ทบทวนข้อผิดสัปดาห์ 6', focusW='Essay เต็ม: R8',
    goal='essay เต็มก่อน Mock + เตรียมอุปกรณ์/เวลา 3 วันข้างหน้า',
    read=[B(380, 383, 'Checklist 3 นาทีสุดท้าย (ท่องให้ได้ 10 ข้อ)'), APP('คู่มือ → Template essay + คำเชื่อม (ทวน 5 นาที)', 'guide')],
    essay=dict(topic='R8', minutes=60),
    review=dict(days=[34, 35, 36, 37, 38, 39]),
    error='เตรียม Mock: ตั้งนาฬิกา 09.00–12.00 น. สำหรับ 16–18 พ.ย.',
)
D[41] = dict(
    title='Full Mock 1 (Reading 120 + Writing 60)', focusR='Mock M1 — 6 passages / 69 ข้อ', focusW='Mock essay: R5',
    goal='จำลองวันสอบจริง 3 ชั่วโมงต่อเนื่อง (09.00–12.00 น.)',
    read=[APP('ห้ามเปิดเอกสารระหว่างสอบ — หลังสอบอ่านเฉลย + ดูผลแยกทักษะ', 'stats')],
    test='M1', essay=dict(topic='R5', minutes=60),
    error='จุดที่ “หมดแรง/เสียสมาธิ” ช่วงไหนของ 3 ชั่วโมง และวิธีแก้',
)
D[42] = dict(
    title='Full Mock 2 (Reading 120 + Writing 60)', focusR='Mock M2 — 6 passages / 69 ข้อ', focusW='Mock essay: R1',
    goal='จำลองสอบครั้งที่ 2 แก้จุดที่พลาดจาก Mock 1',
    read=[APP('หลังสอบ: เทียบผล Mock 1 กับ Mock 2', 'stats')],
    test='M2', essay=dict(topic='R1', minutes=60),
    error='สิ่งที่ทำได้ดีขึ้นจาก Mock 1 และสิ่งที่ยังพลาด',
)
D[43] = dict(
    title='Full Mock 3 (Reading 120 + Writing 60 หัวข้อใหม่)', focusR='Mock M3 — 6 passages / 69 ข้อ', focusW='Mock essay: หัวข้อที่ไม่เคยเห็น',
    goal='ฝึกรับมือหัวข้อที่ไม่เคยเห็น (Writing ชอบออกแนวการศึกษาและ trend)',
    read=[APP('หลังสอบ: สรุปผล 3 Mock ในหน้า “สถิติ”', 'stats')],
    test='M3', essay=dict(topic='RX', minutes=60),
    error='สรุปแผนวันสอบ: ลำดับ passage, เวลา, วิธีวางแผน essay',
)
D[44] = dict(
    title='Error Review — ปิดจุดอ่อน', focusR='ทำข้อที่เคยผิดซ้ำ', focusW='Final grammar review + rewrite',
    goal='ทบทวนเฉพาะสิ่งที่ผิด ไม่เพิ่มเนื้อหาใหม่',
    read=[APP('สมุดข้อผิดพลาด: ทำ “ทำซ้ำข้อที่ผิด” ให้ครบอย่างน้อย 30 ข้อ', 'errors'),
          B(380, 383, 'Checklist 10 ข้อ (รอบสุดท้าย)'),
          S('guide', 'ส่วนที่ 1: เทคนิคสำคัญที่ต้องจำ (รอบสุดท้าย)')],
    blocks=[('vocabreview', 20), ('retry', 30), ('writing', 35), ('errors', 5)],
    grammar='G29',
    task=dict(kind='rewrite', topic=None, minutes=20, words='100–150',
              prompt='เลือกย่อหน้าที่อ่อนที่สุดจาก essay Mock 1–3 แล้วเขียนใหม่ + เขียน intro/conclusion template ของตัวเองจากความจำ',
              steps=['เปิด Writing Studio ดู essay วันที่ 41–43', 'เขียนใหม่ 1 ย่อหน้า 100–150 คำ',
                     'เขียน template บทนำ 2 ประโยค และบทสรุป 2 ประโยค จากความจำ แล้วเทียบกับคู่มือ'],
              compare='เทียบ template กับคู่มือ → “Template essay”'),
    error='Top 5 ข้อผิดที่ต้องระวังพรุ่งนี้และวันสอบ',
)
D[45] = dict(
    title='Light Review — ทบทวนเบา ๆ แล้วพัก', focusR='Passage สั้น 1 บท (เบา)', focusW='Template phrases',
    goal='ไม่ทำข้อสอบหนัก: ทวน template + คำศัพท์ แล้วพักผ่อนให้เต็มที่',
    read=[APP('คู่มือ → “Checklist วันสอบ” (สิ่งที่ต้องเตรียม + แผนเวลา)', 'guide'),
          S('guide', 'ตัวอย่าง Essay ที่ชอบที่สุด 1 เรื่อง (อ่านเพื่อความมั่นใจ ไม่ต้องท่อง)')],
    blocks=[('vocabreview', 15), ('reading', 15), ('writing', 15)],
    reading=dict(lesson='L_LIGHT', passages=['W31']),
    grammar='G30',
    task=dict(kind='sentences', topic=None, minutes=10, words='thesis + outline',
              prompt='เขียน thesis statement + outline 4 ย่อหน้า (หัวข้อสั้น ๆ) ให้โจทย์ที่ถนัด 1 เรื่อง ใน 10 นาที แล้วหยุด',
              steps=['เลือกโจทย์จริงที่เขียนแล้วรู้สึกมั่นใจ', 'เขียนแค่โครง ไม่เขียนเต็ม', 'จากนั้นปิดหนังสือ พักผ่อน นอนเร็ว'],
              compare=''),
    error='เตรียมของวันสอบ: บัตรประชาชน, ใบสมัคร/ยืนยัน, ดินสอ 2B/ปากกา, ยางลบ, นาฬิกา (ตรวจกฎของสนามสอบ)',
)


def build_days(vocab_plan):
    days = []
    for d in range(1, 46):
        x = dict(D[d])
        dt = START + timedelta(days=d - 1)
        x['d'] = d
        x['date'] = dt.isoformat()
        x['wd'] = WD[dt.weekday()]
        x['dateTh'] = f'{dt.day} {TH_MONTH[dt.month]} {dt.year + 543}'
        x['phase'] = phase_of(d)
        if d in (4, 11, 18, 25, 32, 39):
            x['type'] = 'test'
        elif d in (41, 42, 43):
            x['type'] = 'mock'
        elif d == 44:
            x['type'] = 'review'
        elif d == 45:
            x['type'] = 'light'
        elif dt.weekday() == 6:
            x['type'] = 'sunday'
        elif 35 <= d <= 38:
            x['type'] = 'integration'
        else:
            x['type'] = 'weekday'
        if 'blocks' not in x:
            x['blocks'] = {'test': SATURDAY, 'mock': MOCK, 'sunday': SUNDAY, 'integration': INTEGRATION}.get(x['type'], WEEKDAY)
        x['blocks'] = [{'k': k, 'min': m} for k, m in x['blocks']]
        x['minutes'] = sum(b['min'] for b in x['blocks'])
        x['newWords'] = len(vocab_plan.get(str(d), []))
        days.append(x)
    return days
