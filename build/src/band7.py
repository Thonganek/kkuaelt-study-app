# -*- coding: utf-8 -*-
"""Band 7 stage: turns the 42-day plan into 60 days.

Days 1-40   the 42-day plan (Days 38-40 = Full Mock 1-3, the checkpoint before Band 7)
Days 41-58  Band 7 stage: content from build/content/band7/ + the 300 academic words
Days 59-60  the old Day 41 (Error Review) and Day 42 (Light Review)
"""
import copy
import json
import re
from pathlib import Path

CONTENT = Path(__file__).resolve().parent.parent / 'content' / 'band7'
TEST_IDS = ['A1', 'A2', 'A3', 'AM1', 'AM2']
Q_COUNTS = [8, 8, 9, 10, 17, 17]
SKILLS = {'main idea', 'title', 'topic', 'detail', 'negative detail', 'vocabulary', 'reference', 'inference',
          'purpose', 'tone', 'organization', 'fact/opinion', 'paraphrase', 'short answer'}
PHASE = 'P10'
STAGE_TH = 'ยกระดับสู่ Band 7'


def read(name):
    return json.loads((CONTENT / name).read_text(encoding='utf-8'))


def app(what, link):
    return dict(src='app', pages='', pdf=None, what=what, link=link)


NUMBERS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
           'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']


def add_variants(q):
    """Accept 14% / 14 percent for '14 per cent' and digits for number words (and the reverse)."""
    out = list(q['answers'])
    for a in q['answers']:
        forms = {a}
        if 'per cent' in a:
            forms |= {a.replace(' per cent', '%'), a.replace('per cent', 'percent')}
        for n, word in enumerate(NUMBERS):
            for f in list(forms):
                forms.add(re.sub(rf'\b{word}\b', str(n), f, flags=re.I))
                forms.add(re.sub(rf'(?<![\d.]){n}(?![\d.%])', word, f))
        out += [f for f in sorted(forms) if f not in out]
    q['answers'] = out


def check_passage(p, n_questions=None):
    text = ' '.join(p['paragraphs']).lower()
    assert p['kind'] in ('short', 'long') and p['title'] and p['paragraphs'], p['id']
    if n_questions is not None:
        assert len(p['questions']) == n_questions, (p['id'], len(p['questions']))
    for i, q in enumerate(p['questions'], 1):
        where = f"{p['id']}.{i}"
        assert q['skill'] in SKILLS, (where, q['skill'])
        assert q['q'] and q['explain'], where
        if q['type'] == 'mc':
            assert len(q['options']) == 4 and q['answer'] in (0, 1, 2, 3), where
        else:
            assert q['type'] == 'short' and q['answers'], where
            first = re.sub(r'\s+', ' ', q['answers'][0].lower())
            assert first in re.sub(r'\s+', ' ', text) and len(first.split()) <= 3, (where, q['answers'][0])
            add_variants(q)


def load():
    tests = [read(f'test_{t}.json') for t in TEST_IDS]
    for t, tid in zip(tests, TEST_IDS):
        assert t['id'] == tid and len(t['passages']) == 6, tid
        for i, (p, n) in enumerate(zip(t['passages'], Q_COUNTS), 1):
            assert p['id'] == f'{tid}P{i}', p['id']
            check_passage(p, n)
    daily = read('daily_B01-B05.json') + read('daily_B06-B10.json')
    assert [p['id'] for p in daily] == [f'B{i:02d}' for i in range(1, 11)]
    for p in daily:
        check_passage(p, 12)
    essays = read('essays.json')
    assert sorted(essays) == ['BE1', 'BE2', 'BE3', 'BE4', 'BE5']
    grammar = read('grammar.json')
    assert sorted(grammar) == ['G31', 'G32', 'G33', 'G34', 'G35']
    for g in grammar.values():
        assert g['lesson'] and len(g['quiz']) == 10 and all(len(q['options']) == 4 for q in g['quiz'])
    lessons = read('lessons.json')
    assert sorted(lessons) == ['L_B7_INFER', 'L_B7_NOT', 'L_B7_ORG', 'L_B7_PARA', 'L_B7_STANCE']
    return tests, {p['id']: p for p in daily}, essays, grammar, lessons


def task(kind, topic, words, prompt, steps, compare):
    return dict(kind=kind, topic=topic, minutes=35, words=words, prompt=prompt, steps=steps, compare=compare)


# Band 7 weekdays: (day, passage, lesson, grammar, task, title, focusW)
WEEKDAYS = [
    (43, 'B01', 'L_B7_INFER', 'G31',
     task('rewrite', 'BE1', '120–150', 'ยกระดับบทนำและ Body 1 ของ essay BE1 (Day 42) ให้เป็นระดับ Band 7',
          ['เปิด essay BE1 ที่เขียนไว้ใน Day 42', 'เขียนบทนำใหม่: paraphrase โจทย์ด้วยนามวลี (nominal style) แล้วตามด้วย thesis ที่บอกเหตุผล 2 ข้อชัดเจน',
           'เขียน topic sentence ของ Body 1 ใหม่ให้เฉพาะเจาะจง และเพิ่มตัวอย่างที่เป็นรูปธรรม 1 ตัวอย่าง'],
          'เทียบกับ model BE1 และหัวข้อ “ทำไมตัวอย่างนี้อยู่ระดับ Band 7”'),
     'Multi-step inference + Nominal style', 'Rewrite: บทนำ + Body 1 ระดับ Band 7'),
    (44, 'B02', 'L_B7_STANCE', 'G32',
     task('paragraph', 'BE2', '150–180', 'เขียน Body paragraph 1 ย่อหน้าสำหรับโจทย์ BE2 โดยใช้ participle หรือ reduced relative clause อย่างน้อย 2 จุด',
          ['เลือกจุดยืนต่อโจทย์ BE2 แล้วเลือกเหตุผลที่หนักแน่นที่สุด 1 ข้อ', 'topic sentence → อธิบาย → ตัวอย่างเฉพาะ → ประโยคปิดที่เชื่อมกลับจุดยืน',
           'ขีดเส้นใต้ประโยคที่ใช้ participle / reduced relative clause แล้วตรวจว่าประธานของ clause ถูกต้อง (ไม่เป็น dangling modifier)'],
          'เทียบกับ Body ใน model BE2'),
     'Author’s stance + Participle clauses', 'Body paragraph BE2 + participle clauses'),
    (45, 'B03', 'L_B7_PARA', 'G33',
     task('paragraph', 'BE2', '150–180', 'เขียนย่อหน้า concession + rebuttal สำหรับโจทย์ BE2 ใช้โครงสร้างเน้นความ (cleft หรือ inversion) 1 ครั้ง',
          ['ยอมรับข้อโต้แย้งของอีกฝ่าย 1–2 ประโยค (Admittedly, … / It is true that …)', 'หักล้างด้วยเหตุผลและหลักฐาน แล้วกลับมายืนยันจุดยืน',
           'ใช้ cleft (What matters most is …) หรือ inversion (Not only … but …) 1 ครั้งในจุดที่ต้องการเน้นจริง ๆ'],
          'เทียบกับย่อหน้าที่มี concession ใน model BE2'),
     'Paraphrased detail + Emphasis', 'Concession + rebuttal BE2'),
    (46, 'B04', 'L_B7_NOT', 'G34',
     task('summary', None, '120–150', 'สรุปบทอ่าน B04 ด้วยคำของตัวเอง แยกให้ชัดว่าข้อเสนอใดเป็นของใคร และผู้เขียนเห็นด้วยแค่ไหน',
          ['ใช้ reporting verb อย่างน้อย 3 คำ (argue, contend, acknowledge, concede, claim)', 'ห้ามลอกวลีจากบทอ่านเกิน 3 คำติดกัน',
           'ปิดท้ายด้วย 1 ประโยคที่บอกจุดยืนของผู้เขียนบทความ โดยใช้ hedging ให้พอดี'],
          'เทียบกับคำอธิบายข้อ tone / purpose ของ B04'),
     'NOT/EXCEPT + Reporting verbs', 'Summary ด้วย reporting verbs'),
    (47, 'B05', 'L_B7_ORG', 'G35',
     task('rewrite', 'BE1', '320–380', 'ประกอบ essay BE1 ฉบับสมบูรณ์ระดับ Band 7 จากงาน Day 42–43',
          ['รวมบทนำและ Body 1 ฉบับใหม่ (Day 43) กับ Body 2 และบทสรุป', 'ตรวจ cohesion: ใช้ this/these + summary noun เชื่อมความคิด และเลี่ยงการใช้คำซ้ำ',
           'ตรวจด้วย Checklist 10 ข้อ แล้วนับคำ (เป้า 320–380 คำ)'],
          'เทียบ essay ทั้งเรื่องกับ model BE1'),
     'Paragraph organisation + Advanced cohesion', 'Essay BE1 ฉบับ Band 7'),
    (50, 'B06', 'L_B7_INFER', None,
     task('rewrite', 'BE2', '120–150', 'ยกระดับบทนำและบทสรุปของ essay BE2 (Day 49)',
          ['บทนำ: paraphrase โจทย์โดยไม่ใช้คำเดิมเกิน 2 คำติดกัน + thesis ที่มีเหตุผล 2 ข้อ', 'บทสรุป: ย้ำจุดยืนด้วยคำใหม่ + ผลที่ตามมา (implication) 1 ประโยค ไม่เพิ่มเหตุผลใหม่',
           'อ่านออกเสียงทั้งสองย่อหน้าเพื่อตรวจความลื่น'],
          'เทียบกับบทนำและบทสรุปของ model BE2'),
     'Multi-step inference', 'Rewrite: บทนำ + บทสรุป BE2'),
    (51, 'B07', 'L_B7_STANCE', None,
     task('paragraph', 'BE3', '150–180', 'เขียน Body paragraph สำหรับโจทย์ BE3 ที่มีตัวอย่างเฉพาะเจาะจงและ hedging ที่พอดี',
          ['เลือกจุดยืนต่อโจทย์ BE3', 'ใช้ตัวอย่างที่มีรายละเอียด (ใคร ทำอะไร ผลเป็นอย่างไร) แทนตัวอย่างกว้าง ๆ',
           'ใช้ hedging (tend to, is likely to) กับข้อสรุปที่ไม่แน่นอน และ boosting (clearly) เฉพาะเมื่อมีหลักฐานชัด'],
          'เทียบกับ Body ใน model BE3'),
     'Author’s stance and tone', 'Body paragraph BE3'),
    (52, 'B08', 'L_B7_PARA', None,
     task('summary', None, '120–150', 'สรุปบทอ่าน B08 ด้วยการ paraphrase ทั้งหมด',
          ['จดใจความหลักของแต่ละย่อหน้าเป็นภาษาไทยก่อน แล้วปิดบทอ่าน', 'เขียนสรุปภาษาอังกฤษจากโน้ตภาษาไทย โดยไม่เปิดบทอ่าน',
           'เปิดบทอ่านตรวจว่าไม่มีวลีที่ซ้ำเกิน 3 คำติดกัน และข้อมูลถูกต้อง'],
          'เทียบกับคำอธิบายข้อ paraphrase ของ B08'),
     'Paraphrased detail', 'Summary แบบ paraphrase ล้วน'),
    (53, 'B09', 'L_B7_NOT', None,
     task('paragraph', 'BE3', '150–180', 'เขียนย่อหน้าโต้แย้งฝั่งตรงข้ามของโจทย์ BE3 แล้วหักล้าง',
          ['สรุปเหตุผลที่ดีที่สุดของฝั่งตรงข้ามอย่างยุติธรรม', 'หักล้างด้วยหลักฐานหรือข้อจำกัดของเหตุผลนั้น',
           'ใช้คำเชื่อมแสดงความขัดแย้งให้หลากหลาย (whereas, by contrast, nevertheless) และตรวจว่าแต่ละคำตรงความหมาย'],
          'เทียบกับย่อหน้า concession ใน model BE3'),
     'NOT/EXCEPT + Counter-argument', 'Counter-argument BE3'),
    (54, 'B10', 'L_B7_ORG', None,
     task('analysis', 'BE3', 'thesis 3 แบบ + outline', 'เตรียม essay BE3: เขียน thesis 3 แบบ แล้วเลือกแบบที่ดีที่สุดทำ outline 4 ย่อหน้า',
          ['เขียน thesis 3 แบบ: เห็นด้วย / ไม่เห็นด้วย / เห็นด้วยบางส่วนอย่างมีเงื่อนไข', 'เลือก thesis ที่มีหลักฐานสนับสนุนมากที่สุด',
           'ทำ outline: บทนำ → เหตุผล 1 + ตัวอย่าง → เหตุผล 2 + concession → บทสรุป'],
          'เทียบ outline กับ model BE3 (หลังเขียน essay ใน Day 56)'),
     'Paragraph organisation', 'Thesis + outline BE3'),
]
TESTS = {41: ('A1', 'test'), 48: ('A2', 'test'), 55: ('A3', 'test'), 57: ('AM1', 'mock'), 58: ('AM2', 'mock')}
MOCK_ESSAY = {57: 'BE4', 58: 'BE5'}
ESSAY_DAYS = {42: ('BE1', [38, 39, 40, 41]), 49: ('BE2', [43, 44, 45, 46, 47, 48]), 56: ('BE3', [50, 51, 52, 53, 54, 55])}
VOCAB_DAYS = [41, 43, 44, 45, 46, 47, 48, 50, 51, 52, 53, 54, 55, 57, 58]


def stage_day(d, **kw):
    return dict(d=d, wd='', dateTh=STAGE_TH, phase=PHASE, **kw)


def assemble(data, academic, untime):
    tests, daily, essays, grammar, lessons = load()
    old = data['days']
    for pid in daily:
        assert pid not in data['passages'], pid
    by_id = {t['id']: t for t in tests}
    new = []
    for d in range(41, 59):
        if d in TESTS:
            tid, kind = TESTS[d]
            t = by_id[tid]
            n = TEST_IDS.index(tid) + 1
            if kind == 'test':
                x = stage_day(d, type='test', test=tid, title=f'{t["title"]} — ข้อสอบระดับยาก',
                              focusR='Band 7 Test: 6 passages / 69 ข้อ (ยากกว่า Test 1–6)', focusW='—',
                              goal='ทำข้อสอบระดับ Band 7 ให้ครบทุกข้อ หาหลักฐานทุกข้อก่อนตอบ แล้ววิเคราะห์ว่าข้อที่ผิดเป็นทักษะใด',
                              error=f'เทียบคะแนนแยกทักษะของ {tid} กับ Test ก่อนหน้า: ทักษะที่ยังต่ำกว่า 70% และแผนแก้',
                              blocks=[dict(k='test', min=150), dict(k='vocab', min=20), dict(k='review', min=25)],
                              read=[app('ก่อนเริ่ม: คู่มือ → “ข้อมูลข้อสอบ” หัวข้อหลักสูตร 60 Day เป้าหมาย Band 7', 'guide/exam'),
                                    app(f'ทำ {t["title"]} แบบไม่จำกัดเวลา แล้วจดเวลาที่ใช้', f'test/{tid}'),
                                    app('หลังสอบ: อ่านคำอธิบายทุกข้อที่ผิด แล้วดูผลแยกทักษะในหน้า “สถิติ”', 'stats')])
            else:
                eid = MOCK_ESSAY[d]
                x = stage_day(d, type='mock', test=tid, essay=dict(topic=eid, minutes=60),
                              title=f'{t["title"]} (Reading + Writing ระดับ Band 7)',
                              focusR=f'{t["title"]} — 6 passages / 69 ข้อ', focusW=f'Mock essay: {eid}',
                              goal='จำลองวันสอบระดับ Band 7: Reading ต่อด้วย Writing โดยไม่จำกัดเวลา แล้วจดเวลาที่ใช้ไว้เทียบ',
                              error='เทียบกับ Full Mock Day 38–40: ทักษะที่ดีขึ้น 2 เรื่อง และจุดอ่อนที่เหลือ 2 เรื่อง',
                              blocks=[dict(k='test', min=150), dict(k='essay', min=60), dict(k='review', min=25), dict(k='vocab', min=20)],
                              read=[app(f'ทำ {t["title"]} แล้วเขียน essay {eid} ต่อทันที', f'test/{tid}'),
                                    app(f'หลังเขียนเอง: เปิด model {eid} ดูว่าอะไรทำให้เป็นระดับ Band 7', f'writing/{eid}')])
            new.append(x)
        elif d in ESSAY_DAYS:
            eid, rdays = ESSAY_DAYS[d]
            new.append(stage_day(d, type='sunday', essay=dict(topic=eid, minutes=60), review=dict(days=rdays),
                                 title=f'Essay Band 7: {eid} + ทบทวนข้อผิด Day {rdays[0]}–{rdays[-1]}',
                                 focusR=f'ทบทวนข้อผิด Day {rdays[0]}–{rdays[-1]}', focusW=f'Essay เต็ม: {eid} (เป้า 320–380 คำ)',
                                 goal='เขียน essay ระดับ Band 7: จุดยืนชัด เหตุผล 2 ข้อพร้อมตัวอย่างเฉพาะ และ concession + rebuttal 1 จุด',
                                 error=f'เทียบ essay {eid} กับ model: จุดที่ยังห่างจาก Band 7 มากที่สุด 2 เรื่อง',
                                 blocks=[dict(k='essay', min=60), dict(k='weekly', min=20), dict(k='vocabreview', min=15)],
                                 read=[app('คู่มือ → Template essay + คำเชื่อม (ทวนก่อนเขียน)', 'guide/essay'),
                                       app(f'หลังเขียนเอง: เปิด model {eid} ดูหัวข้อ “ทำไมตัวอย่างนี้อยู่ระดับ Band 7”', f'writing/{eid}')]))
        else:
            spec = next(w for w in WEEKDAYS if w[0] == d)
            _, pid, lid, gid, tk, focus, focus_w = spec
            p = daily[pid]
            read_items = [app(f'บทเรียน “{lessons[lid]["title"]}” แล้วทำ {pid}: {p["title"]}', f'day/{d}/reading')]
            if gid:
                read_items.append(app(f'Grammar ขั้นสูง: {grammar[gid]["title_th"]}', f'day/{d}/writing'))
            read_items.append(app(f'งานเขียน: {focus_w}', f'day/{d}/writing'))
            new.append(stage_day(d, type='weekday', reading=dict(lesson=lid, passages=[pid]), grammar=gid, task=tk,
                                 title=f'Band 7: {focus}', focusR=f'{pid} — {p["focus"]}', focusW=focus_w,
                                 goal=f'ทำ {pid} ให้ถูกอย่างน้อย 9/12 ข้อ โดยระบุหลักฐาน (¶) ทุกข้อ และทำงานเขียน: {focus_w}',
                                 error=f'จดข้อที่ผิดใน {pid} พร้อมเหตุผลว่าตัวลวงหลอกได้อย่างไร',
                                 blocks=[dict(k='vocab', min=20), dict(k='reading', min=45), dict(k='writing', min=35), dict(k='errors', min=10)],
                                 read=read_items))

    # academic words: 20 per vocabulary day of the Band 7 stage, mixed parts of speech
    assert len(academic) == 20 * len(VOCAB_DAYS)
    lists = {d: [] for d in VOCAB_DAYS}
    for i, w in enumerate(academic):
        lists[VOCAB_DAYS[i % len(VOCAB_DAYS)]].append(w)
    for d, ws in lists.items():
        data['vocab'][str(d)] = ws
    for x in new:
        x['newWords'] = len(lists.get(x['d'], []))
        x['minutes'] = sum(b['min'] for b in x['blocks'])

    # Days 59-60: the former Error Review and Light Review
    review, light = copy.deepcopy(old[40]), copy.deepcopy(old[41])
    review['d'], light['d'] = 59, 60
    review['task']['prompt'] = review['task']['prompt'].replace('essay Mock 1–3', 'essay Mock ทั้ง 5 ชุด')
    review['task']['steps'] = [s.replace('essay วันที่ 38–40', 'essay จาก Mock Day 38–40 และ Band 7 Mock Day 57–58') for s in review['task']['steps']]
    for gid, d in (('G29', 59), ('G30', 60)):
        data['grammar'][gid]['day'] = d
    data['passages']['W31']['day'] = 60
    days = old[:40] + new + [review, light]
    assert [x['d'] for x in days] == list(range(1, 61))

    # content
    for t in tests:
        d = next(k for k, v in TESTS.items() if v[0] == t['id'])
        for p in t['passages']:
            assert p['id'] not in data['passages'], p['id']
            data['passages'][p['id']] = dict(p, day=d)
        data['tests'][t['id']] = dict(id=t['id'], title=t['title'], day=d, passages=[p['id'] for p in t['passages']])
    for d, pid, *_ in WEEKDAYS:
        data['passages'][pid] = dict(daily[pid], day=d)
    for gid, g in grammar.items():
        data['grammar'][gid] = dict(g, id=gid, day=min(w[0] for w in WEEKDAYS if w[3] == gid))
    data['lessons'].update(lessons)
    for eid, e in essays.items():
        data['essays'][eid] = dict(e, id=eid)
        data.setdefault('topics', {})[eid] = {'label': 'โจทย์ฝึกระดับ Band 7 (แต่งใหม่ ไม่ใช่ข้อสอบจริง)'}

    # phases
    phases = data['phases']
    for p in phases:
        if p['id'] == 'P8':
            p['days'] = [59, 59]
        if p['id'] == 'P9':
            p['days'] = [60, 60]
    at = next(i for i, p in enumerate(phases) if p['id'] == 'P8')
    phases.insert(at, dict(id=PHASE, name='Band 7', th=STAGE_TH, days=[41, 58],
                           goal='ข้อสอบระดับยาก 5 ชุด · บทอ่านยาก 10 บท · Grammar ขั้นสูง · Essay ระดับ Band 7 · Academic Vocabulary 300 คำ'))
    for p in phases:
        a, b = p['days']
        p['range'] = f'Day {a}' if a == b else f'Day {a}–{b}'
    data['days'] = days
    return days
