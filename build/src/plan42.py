# -*- coding: utf-8 -*-
"""42-day plan: Day 1 = Sat 10 Oct 2026 ... Day 42 = Fri 20 Nov 2026 (exam Sat 21 Nov).

The 45-day content in plan_days.py was written for a Wed 7 Oct start. The learner starts on Sat 10 Oct,
so every old Day n becomes new Day n-3 on the *same calendar date* (Saturday tests, Sunday essays and the
phase dates are unchanged). Nothing from old Days 1-3 (7-9 Oct) is dropped - it is merged where the skill fits:

  old 1  exam intro + research words  -> new 1 (before Test 1)     W01 passage -> new 3 (mixed practice)
         Grammar diagnostic G01       -> new 2 (after the diagnostic essay)
         baseline paragraph (GE1)     -> new 14 (paragraph with a concession)
  old 2  W02 Previewing               -> new 4 (with Topic vs Main idea)    G02 fragments/run-ons -> new 6 (with punctuation)
         essay analysis + 3 theses    -> new 4 (before topic sentences)    book pp. 25-35 -> new 3
  old 3  W03 Scanning                 -> new 12 (with Scanning + Short answer)   G03 tense/SVA -> new 5 (with passive)
         paraphrase 5 prompts         -> new 10 (with word forms)          book pp. 35-40 -> new 11, Guide part 2 -> new 10
  old 2-4 vocabulary (60 words)       -> +3 words/day on new days 3-25 (sublist-1 words early), total still 740
"""
import copy
import json
from datetime import date, timedelta

import plan_days as P

START = date(2026, 10, 10)
NDAYS = 42
SHIFT = 3
WD, TH_MONTH, FILES, SRC_NAME, B, S, APP = P.WD, P.TH_MONTH, P.FILES, P.SRC_NAME, P.B, P.S, P.APP

PHASES = copy.deepcopy(P.PHASES)
for p in PHASES:
    a, b = p['days']
    p['days'] = (max(1, a - SHIFT), b - SHIFT)
PHASES[0]['range'] = '10–12 ต.ค.'


def phase_of(d):
    for p in PHASES:
        if p['days'][0] <= d <= p['days'][1]:
            return p['id']


def _fix(text, pairs):
    for a, b in pairs:
        assert a in text, (a, text[:60])
        text = text.replace(a, b)
    return text


O = copy.deepcopy(P.D)
D = {n - SHIFT: copy.deepcopy(O[n]) for n in range(SHIFT + 1, 46)}

# day-number references inside the old texts
D[3]['task']['prompt'] = _fix(D[3]['task']['prompt'], [('วันที่ 5', 'วันที่ 2')])
D[3]['task']['steps'][0] = _fix(D[3]['task']['steps'][0], [('วันที่ 5', 'วันที่ 2')])
D[9]['error'] = _fix(D[9]['error'], [('วันที่ 5', 'วันที่ 2')])
D[18]['task']['prompt'] = _fix(D[18]['task']['prompt'], [('วันที่ 22–27', 'วันที่ 19–24')])
D[23]['error'] = _fix(D[23]['error'], [('วันที่ 5 และ 12', 'วันที่ 2 และ 9')])
D[31]['task']['prompt'] = _fix(D[31]['task']['prompt'], [('วันที่ 33', 'วันที่ 30')])
D[31]['task']['steps'] = [_fix(s, [('วันที่ 33', 'วันที่ 30')]) if 'วันที่ 33' in s else s for s in D[31]['task']['steps']]
D[41]['task']['steps'][0] = _fix(D[41]['task']['steps'][0], [('วันที่ 41–43', 'วันที่ 38–40')])
for n, x in D.items():
    if x.get('review'):
        x['review']['days'] = [d - SHIFT for d in x['review']['days'] if d - SHIFT >= 1]

o1, o2, o3 = O[1], O[2], O[3]

# ---- Day 1 (Sat 10 Oct): exam intro + Reading Test 1 ----
D[1].update(
    title='เปิดตัว + Reading Test 1 — Diagnostic เต็มรูปแบบ',
    goal='รู้จักรูปแบบข้อสอบ KKU-AELT แล้วทำ Reading เต็มชุดครั้งแรกเพื่อหาจุดอ่อนรายทักษะ (ไม่ต้องกังวลคะแนน)',
    read=[APP('ก่อนสอบ: คู่มือในแอป → “ข้อมูลข้อสอบ” + “กลยุทธ์ทำข้อสอบ 120 นาที” (10 นาที)', 'guide'),
          o1['read'][4],
          APP('หลังสอบ: อ่านคำอธิบายเฉลยทุกข้อที่ผิด แล้วดูกราฟแยกทักษะในหน้า “สถิติ”', 'stats')],
    error='จดคะแนน Diagnostic: Reading Test 1 __/69 + ทักษะที่ผิดมากที่สุด 2 อันดับ และ passage ที่ใช้เวลามากเกินไป',
)

# ---- Day 2 (Sun 11 Oct): diagnostic essay + grammar diagnostic ----
D[2].update(
    title='Writing Diagnostic 60 นาที + Grammar Diagnostic',
    focusR='—', focusW='Essay เต็ม: ข้อสอบจริง R3 + Grammar diagnostic',
    goal='เขียน essay เต็มครั้งแรกภายใต้เวลาจริง (งานตั้งต้นไว้เทียบตอน Mock) แล้ววัดพื้นฐาน Grammar 15 ข้อ',
    read=[o1['read'][1], o1['read'][2], o1['read'][3]] + D[2]['read'],
    grammar='G01',
    blocks=[('essay', 60), ('writing', 20), ('vocabreview', 15)],
    review=dict(days=[1]),
    error='จาก checklist: ข้อผิดที่เจอบ่อยที่สุดใน essay นี้ 3 อย่าง + คะแนน Grammar G01 __/15 และหัวข้อที่ผิด',
)
D[2]['read'][0] = dict(D[2]['read'][0], what='ก่อนเขียน: ' + D[2]['read'][0]['what'])

# the first Sunday review also covers Test 1 and the grammar diagnostic
D[9]['review']['days'] = list(range(1, 9))

# ---- Day 3 (Mon 12 Oct): + W01 warm-up passage, + scoring criteria pages ----
D[3]['reading']['passages'] = ['W01'] + D[3]['reading']['passages']
D[3]['reading']['lesson'] = ['L_FORMAT', D[3]['reading']['lesson']]
D[3]['read'] = D[3]['read'] + [o2['read'][0]]
D[3]['blocks'] = [('vocab', 15), ('reading', 50), ('writing', 30), ('errors', 5)]

# ---- Day 4 (Tue 13 Oct): + Previewing (W02) + essay analysis / thesis statements ----
D[4]['title'] = 'Previewing + Topic vs Main idea + Thesis & Relative clauses'
D[4]['focusR'] = 'Previewing & predicting + Topic vs Main idea'
D[4]['focusW'] = 'วิเคราะห์ essay ตัวอย่าง + thesis + topic sentences'
D[4]['goal'] = 'ดูภาพรวมก่อนอ่าน แล้วแยก topic กับ main idea ให้ได้ทุกย่อหน้า + เขียน thesis และ topic sentence ที่ชัดเจน'
D[4]['reading']['passages'] = ['W02'] + D[4]['reading']['passages']
D[4]['reading']['lesson'] = ['L_PREVIEW', D[4]['reading']['lesson']]
D[4]['read'] = [o2['read'][1], o2['read'][2]] + D[4]['read']
t = D[4]['task']
D[4]['task'] = dict(
    kind='sentences', topic=t['topic'], minutes=30, words='3 thesis + 2 topic sentences + 3 ประโยค',
    prompt='ส่วนที่ 1: วิเคราะห์ essay ตัวอย่าง “Big salary…” แล้วเขียน thesis statement ให้โจทย์จริง 3 ข้อ · ส่วนที่ 2: ' + t['prompt'],
    steps=['ส่วนที่ 1 — ' + s for s in o2['task']['steps']] + ['ส่วนที่ 2 — ' + s for s in t['steps']],
    compare=t['compare'] + ' · ดูตัวอย่าง thesis ของ R1, R4, R5 และบทวิเคราะห์ essay ตัวอย่างที่แสดงหลังเขียน',
    show={'intro': ['R1', 'R4', 'R5'], 'models': ['IMG']},
)
D[4]['blocks'] = [('vocab', 15), ('reading', 50), ('writing', 40), ('errors', 5)]

# ---- Day 5 (Wed 14 Oct): + Tense & SVA with Passive ----
D[5]['grammar'] = ['G03', D[5]['grammar']]
D[5]['focusW'] = 'Tense & Subject–verb agreement + Passive voice'
D[5]['blocks'] = [('vocab', 15), ('reading', 40), ('writing', 40), ('errors', 5)]

# ---- Day 6 (Thu 15 Oct): + Fragments / run-ons with connectors & punctuation ----
D[6]['grammar'] = ['G02', D[6]['grammar']]
D[6]['focusW'] = 'Fragment / Run-on / Comma splice + Connectors & punctuation'
D[6]['blocks'] = [('vocab', 15), ('reading', 40), ('writing', 40), ('errors', 5)]
D[6]['error'] = D[6]['error'] + ' · ' + o2['error']

# ---- Day 10 (Mon 19 Oct): + paraphrasing the prompt (synonyms + word forms) ----
t = D[10]['task']
D[10]['task'] = dict(
    kind='paragraph', topic=t['topic'], minutes=30, words='5 ประโยค + 130–150 คำ',
    prompt='ส่วนที่ 1: ' + o3['task']['prompt'] + ' · ส่วนที่ 2: ' + t['prompt'],
    steps=['ส่วนที่ 1 — ' + s for s in o3['task']['steps']] + ['ส่วนที่ 2 — ' + s for s in t['steps']],
    compare=t['compare'] + ' · ดูตัวอย่าง paraphrase ของ R2, R6, R11, R13, R14 ที่แสดงหลังเขียน',
    show={'paraphrase': ['R2', 'R6', 'R11', 'R13', 'R14']},
)
D[10]['focusW'] = 'Paraphrase โจทย์ + Word forms'
D[10]['read'] = D[10]['read'] + [o3['read'][1]]
D[10]['blocks'] = [('vocab', 15), ('reading', 40), ('writing', 40), ('errors', 5)]

# ---- Day 11 (Tue 20 Oct): band descriptors before writing introductions ----
D[11]['read'] = D[11]['read'] + [o3['read'][0]]

# ---- Day 12 (Wed 21 Oct): + Scanning (W03) ----
D[12]['reading']['passages'] = ['W03'] + D[12]['reading']['passages']
D[12]['reading']['lesson'] = ['L_SCAN', D[12]['reading']['lesson']]
D[12]['blocks'] = [('vocab', 15), ('reading', 50), ('writing', 30), ('errors', 5)]

# ---- Day 14 (Fri 23 Oct): + the first full paragraph (technology & stress) with a concession ----
t = D[14]['task']
D[14]['task'] = dict(
    kind='paragraph', topic=t['topic'], minutes=35, words='4 ประโยค + 120–150 คำ',
    prompt='ส่วนที่ 1: ' + t['prompt'] + ' · ส่วนที่ 2: ' + o1['task']['prompt'],
    steps=['ส่วนที่ 1 — ' + s for s in t['steps']] + [
        'ส่วนที่ 2 — เลือกจุดยืนเดียว แล้วเขียน 1 ย่อหน้า 120–150 คำ: ประโยคจุดยืน → เหตุผล 1 + ตัวอย่าง → เหตุผล 2 → ประโยคปิด',
        'ส่วนที่ 2 — ใส่ประโยค concession 1 ประโยค (Admittedly, …; however, …) แล้วเทียบกับ Essay 1 “Technology and Stress”'],
    compare=t['compare'] + ' · ' + o1['task']['compare'],
    show={'models': ['GE1']},
)
D[14]['focusW'] = 'Conditionals & concession + ย่อหน้าเต็ม'
D[14]['blocks'] = [('vocab', 15), ('reading', 40), ('writing', 45), ('errors', 5)]

# model hints that build.py used to patch onto the old numbering
D[18]['task']['show'] = {'ideas': ['R4']}
D[21]['task']['show'] = {'ideas': ['R8', 'R9', 'R13', 'R16']}

TEST_DAYS = (1, 8, 15, 22, 29, 36)
MOCK_DAYS = (38, 39, 40)
REVIEW_DAY, LIGHT_DAY = 41, 42
INTEGRATION = range(32, 36)
LIGHT_VOCAB_DAYS = [d - SHIFT for d in (22, 23, 27, 28, 30, 31)]
PARTS = {'R4': [[d - SHIFT, lab] for d, lab in ((22, 'Introduction'), (23, 'Body 1'), (24, 'Body 2'))],
         'R10': [[28 - SHIFT, 'ส่วนที่ 1 (Intro + Body 1)']], 'R11': [[30 - SHIFT, 'ส่วนที่ 1 (Intro + Body 1)']]}
EXTRA_WORD_DAYS = [d for d in range(3, 26) if (START + timedelta(days=d - 1)).weekday() != 6]


def remap_vocab(old):
    """old: {old_day(str): [entries]} -> new {new_day(str): [entries]} (740 words, none dropped)."""
    new = {'1': old['1']}
    for n in range(5, 46):
        if str(n) in old:
            new[str(n - SHIFT)] = list(old[str(n)])
    extra = old['2'] + old['3'] + old['4']
    assert len(extra) == 3 * len(EXTRA_WORD_DAYS), (len(extra), len(EXTRA_WORD_DAYS))
    for i, d in enumerate(EXTRA_WORD_DAYS):
        new[str(d)] = new.get(str(d), []) + extra[3 * i:3 * i + 3]
    return {k: new[k] for k in sorted(new, key=int)}


def build_days(vocab):
    days = []
    for d in range(1, NDAYS + 1):
        x = copy.deepcopy(D[d])
        dt = START + timedelta(days=d - 1)
        x['d'] = d
        x['date'] = dt.isoformat()
        x['wd'] = WD[dt.weekday()]
        x['dateTh'] = f'{dt.day} {TH_MONTH[dt.month]} {dt.year + 543}'
        x['phase'] = phase_of(d)
        if d in TEST_DAYS:
            x['type'] = 'test'
        elif d in MOCK_DAYS:
            x['type'] = 'mock'
        elif d == REVIEW_DAY:
            x['type'] = 'review'
        elif d == LIGHT_DAY:
            x['type'] = 'light'
        elif dt.weekday() == 6:
            x['type'] = 'sunday'
        elif d in INTEGRATION:
            x['type'] = 'integration'
        else:
            x['type'] = 'weekday'
        if 'blocks' not in x:
            x['blocks'] = {'test': P.SATURDAY, 'mock': P.MOCK, 'sunday': P.SUNDAY, 'integration': P.INTEGRATION}.get(x['type'], P.WEEKDAY)
        x['blocks'] = [{'k': k, 'min': m} for k, m in x['blocks']]
        x['minutes'] = sum(b['min'] for b in x['blocks'])
        x['newWords'] = len(vocab.get(str(d), []))
        days.append(x)
    assert days[0]['wd'] == 'เสาร์' and days[-1]['date'] == '2026-11-20'
    assert all(x['type'] != 'test' or x['wd'] == 'เสาร์' for x in days)
    return days
