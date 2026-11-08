# -*- coding: utf-8 -*-
"""Build the six-day edition from the archived 42-day app.

Run from any directory: python build/src/build6.py
Use --deploy to also update the existing GitHub Pages entry filename.
"""
import copy
import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = ROOT / 'KKU-AELT_42_Day_Study_Plan_Original.html'
OUT = ROOT / 'KKU-AELT_6_Day_Study_Plan_08-13_Oct_2569.html'
START = dt.date(2026, 10, 8)
END = dt.date(2026, 10, 13)
PLAN_ID = 'kkuaelt6-2026-10-08'
WORDS_PER_DAY = 100
VOCAB_MINUTES = 75

original = SOURCE.read_text(encoding='utf-8')
match = re.search(r'<script id="study-data" type="application/json">(.*?)</script>', original, re.S)
assert match, 'The original study data must be present.'
data = json.loads(match.group(1))
old_days = copy.deepcopy(data['days'])
old_vocab = copy.deepcopy(data['vocab'])


def app(what, link='guide/reading'):
    return dict(src='app', pages='', pdf=None, what=what, link=link)


def book(first, last, pdf, what):
    return dict(src='book', pages=f'{first}–{last}', pdf=pdf,
                pdfEnd=pdf + last - first, what=what)


def task(kind, topic, minutes, words, prompt, steps, compare='เทียบกับ Outline และ Model ในคลังหัวข้อหลังเขียนเอง'):
    return dict(kind=kind, topic=topic, minutes=minutes, words=words,
                prompt=prompt, steps=steps, compare=compare)


# Reuse the existing questions, answers and page references; select a feasible core.
d1 = copy.deepcopy(old_days[0])
d1.update(title='วัดระดับ Reading + Writing',
          goal='เรียนศัพท์ 100 คำ → ทำ Reading Test 1 จับเวลา 120 นาที → เขียนย่อหน้าวัดระดับ แล้วเลือกจุดอ่อนเพื่อใช้โฟกัสในอีก 5 วัน',
          focusW='Writing Diagnostic: ย่อหน้า 100–120 คำ',
          task=task('paragraph', 'R3', 20, '100–120', data['essays']['R3']['prompt'],
                    ['เลือกจุดยืน แล้วเขียนเหตุผลสนับสนุน 1 ข้อเป็นย่อหน้า 100–120 คำภายใน 20 นาที',
                     'ใช้ topic sentence → อธิบายเหตุผล → ยกตัวอย่าง → สรุปเชื่อมกลับจุดยืน',
                     'เขียนด้วยตนเองก่อนเปิดตัวอย่าง เพื่อดูพื้นฐานการเขียนของตนเอง']),
          error='บันทึกคะแนน T1 __/69 ทักษะที่อ่อนที่สุด 2 เรื่อง และ passage ที่ใช้เวลามากเกินไป',
          blocks=[dict(k=k, min=m) for k, m in [('vocab', 15), ('test', 120), ('writing', 20), ('review', 20)]])
d1['read'].insert(-1, app('หลัง Reading: เขียนย่อหน้าวัดระดับ 100–120 คำใน 20 นาที', 'day/1/writing'))

d2 = copy.deepcopy(old_days[3])
d2.update(title='Main idea + โครงสร้างประโยคและบทนำ',
          goal='แยก topic กับ main idea และเขียนบทนำที่มีจุดยืนชัดเจน โดยแก้ fragment และ tense ที่ผิดบ่อย',
          focusR='Previewing + Topic vs Main idea', focusW='โครงประโยค + Tense/SVA + Thesis',
          grammar=['G02', 'G03', 'G16'],
          read=[book(222, 223, 228, 'หา main idea ของย่อหน้า และเลือก heading ให้พอดีกับใจความ'),
                dict(src='guide', pages='', pdf=None, what='ส่วนที่ 1: โครงสร้าง Opinion Essay 4 ย่อหน้า'),
                app('บทเรียน Previewing / Topic vs Main idea และ Grammar G02, G03, G16 ในขั้น Writing', 'day/2/reading')],
          task=task('intro', 'R4', 25, '60–80', data['essays']['R4']['prompt'],
                    ['เลือกจุดยืน แล้วเขียนเหตุผลสนับสนุน 2 ข้อเป็น outline สั้น ๆ',
                     'เขียนบทนำ 60–80 คำ: paraphrase โจทย์ + thesis ที่แสดงจุดยืน',
                     'ตรวจประธาน–กริยา tense และประโยคที่ไม่สมบูรณ์ก่อนเทียบตัวอย่าง']),
          error='จด main idea ที่เลือกผิด 1 ข้อ และประโยคที่แก้ fragment หรือ subject–verb agreement 2 ประโยค',
          blocks=[dict(k=k, min=m) for k, m in [('vocab', 15), ('reading', 50), ('writing', 65), ('errors', 10)]])

d3 = copy.deepcopy(old_days[11])
d3.update(title='Scanning + Short answer + Inference',
          goal='หาตัวเลขและข้อมูลเฉพาะ ตอบ short answer ตามคำสั่ง และแยกข้อสรุปที่มีหลักฐานออกจากการเดา',
          focusR='Scanning / Short answer / Inference', focusW='คำเชื่อม + เหตุผลและตัวอย่าง',
          reading=dict(lesson=['L_SCAN', 'L_SHORTANS', 'L_INFER'], passages=['W11', 'W12']),
          grammar=['G07'],
          read=[book(232, 236, 238, 'กลยุทธ์ Short answer และการหาข้อมูลเฉพาะ'),
                book(242, 246, 248, 'เทคนิค Multiple choice / Inference — อ่านเฉพาะกลยุทธ์'),
                app('ฝึกบทอ่าน W11 และ W12 พร้อมเฉลย แล้วเขียน Body paragraph', 'day/3/reading')],
          task=task('paragraph', 'R4', 25, '100–120', data['essays']['R4']['prompt'],
                    ['ต่อยอดจุดยืนและเหตุผลที่วางไว้ใน Day 2',
                     'เขียน Body 1: topic sentence → อธิบายเหตุผล → ยกตัวอย่าง → เชื่อมกลับจุดยืน',
                     'ตรวจคำเชื่อมและเครื่องหมายวรรคตอน โดยใช้ G07 เป็น checklist']),
          error='จด short answer ที่เกินจำนวนคำ หรือ inference ที่ไม่มีหลักฐาน พร้อมประโยคในบทอ่านที่ใช้ยืนยัน',
          blocks=[dict(k=k, min=m) for k, m in [('vocab', 15), ('reading', 65), ('writing', 45), ('errors', 10)]])

d4 = copy.deepcopy(old_days[31])
d4.pop('task', None)
d4.update(title='Reading จับเวลา + Essay เต็ม 60 นาที',
          goal='ฝึก Reading 2 บทภายใต้เวลา และเขียน essay อย่างน้อย 250 คำให้ครบ 4 ย่อหน้าใน 60 นาที',
          focusR='Reading จับเวลา 24 นาที + ตรวจเฉลย', focusW='Essay R13 เต็มเรื่อง + Checklist',
          grammar=None, essay=dict(topic='R13', minutes=60),
          read=[app('จับเวลา Reading W25–W26 รวม 24 นาที แล้วอ่านเฉลย', 'day/4/reading'),
                dict(src='aelt', pages='หน้า 3', pdf=3, pdfEnd=3, what='หัวข้อ R13: อ่านโจทย์ก่อนเขียนเอง'),
                book(68, 69, 72, 'Final Check: ใช้ตรวจหลังเขียน essay เสร็จ')],
          error='จดว่าเขียนครบ 250 คำใน 60 นาทีหรือไม่ และข้อผิดที่ต้องระวังใน Mock วันถัดไป 3 ข้อ',
          blocks=[dict(k=k, min=m) for k, m in [('vocab', 15), ('reading', 40), ('essay', 60), ('errors', 10)]])

d5 = copy.deepcopy(old_days[37])
d5.update(title='Full Mock — Reading 120 + Writing 60 นาที',
          goal='ทำ Mock M1 ต่อเนื่อง 3 ชั่วโมง แล้วตรวจผล 20 นาที เปรียบเทียบทักษะ Reading กับ Day 1',
          blocks=[dict(k=k, min=m) for k, m in [('vocab', 15), ('test', 120), ('essay', 60), ('review', 20)]],
          error='เปรียบเทียบ T1 กับ M1: ทักษะที่ดีขึ้น 2 เรื่อง จุดอ่อนที่เหลือ 2 เรื่อง และข้อผิดใน essay ที่ต้องแก้')

d6 = copy.deepcopy(old_days[40])
d6.update(title='ทบทวนข้อผิด + สรุปแม่แบบ แล้วพัก',
          goal='เรียนศัพท์ใหม่ 100 คำ ทวนศัพท์สะสม 600 คำ แก้ข้อผิดสำคัญจาก 5 วันแรก และสรุป checklist ที่ใช้ได้จริง',
          focusR='Reading เบา ๆ W31 + ทำซ้ำข้อผิดที่พบบ่อย', focusW='แก้งานเขียนจาก Day 5 + ทวน Template',
          reading=dict(lesson='L_LIGHT', passages=['W31']),
          grammar=['G30'], review=dict(days=[1, 2, 3, 4, 5, 6]),
          read=[app('หลังคำศัพท์: อ่าน W31 และทำคำถาม 6 ข้อ ใช้ประมาณ 15 นาที', 'day/6/reading'),
                app('เลือกข้อผิดสำคัญจาก T1, M1 และ Reading รายวัน ทำซ้ำไม่เกิน 30 ข้อ', 'errors'),
                app('ทวนโครง Essay และ checklist พร้อม Grammar G30', 'guide/essay')],
          task=task('rewrite', None, 20, '80–100', 'แก้ส่วนที่อ่อนที่สุดใน essay จาก Day 5 แล้วสรุปแม่แบบของตนเอง',
                    ['เปิดงาน Day 5 เลือกย่อหน้าที่จุดยืนหรือเหตุผลยังไม่ชัด แล้วเขียนใหม่ 80–100 คำ',
                     'สรุป thesis → เหตุผล 1 → เหตุผล 2 → conclusion เป็น outline สั้น ๆ',
                     'ตรวจคำเชื่อม ประธาน–กริยา จำนวนคำ และความสม่ำเสมอของจุดยืน'],
                    'เทียบงาน Day 5 กับ Model R5 และคู่มือ Template essay'),
          error='สรุปข้อควรระวังส่วนตัว 5 ข้อ และเรื่องที่ต้องทวนต่อหลังจบแผน',
          blocks=[dict(k=k, min=m) for k, m in [('vocab', 15), ('reading', 15), ('writing', 35), ('vocabreview', 15), ('retry', 30), ('errors', 10)]])

days = [d1, d2, d3, d4, d5, d6]
# Allocate 100 different words to each of the six days, in the original order.
all_vocab = [word for n in sorted(old_vocab, key=int) for word in old_vocab[n]]
vocab = {str(n): all_vocab[(n - 1) * WORDS_PER_DAY:n * WORDS_PER_DAY]
         for n in range(1, len(days) + 1)}
selected = {w['w'] for words in vocab.values() for w in words}
extra = [w for w in all_vocab if w['w'] not in selected]
assert all(len(words) == WORDS_PER_DAY for words in vocab.values())
assert len(selected) == 600 and len(extra) == 140

phase_specs = [
    ('P1', 'Diagnostic', 'วัดระดับ', 'ทดสอบ Reading และตั้งเป้าตามจุดอ่อน'),
    ('P2', 'Foundation', 'พื้นฐานการอ่านและเขียน', 'Main idea / Grammar / Thesis'),
    ('P3', 'Strategy', 'กลยุทธ์การอ่าน', 'Scanning / Short answer / Inference'),
    ('P6', 'Timed Practice', 'ฝึกจับเวลา', 'Reading + Essay เต็ม 60 นาที'),
    ('P7', 'Mock Exam', 'ข้อสอบจำลอง', 'Reading 120 + Writing 60 นาทีต่อเนื่อง'),
    ('P8', 'Review', 'ทบทวนและสรุป', 'แก้ข้อผิด / ทวนศัพท์ / สรุปแม่แบบ'),
]
phases = []
weekdays = ['จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 'ศุกร์', 'เสาร์', 'อาทิตย์']
for n, (day, spec) in enumerate(zip(days, phase_specs), 1):
    date = START + dt.timedelta(days=n - 1)
    pid, name, thai, goal = spec
    phases.append(dict(id=pid, name=name, th=thai, days=[n, n], range=f'{date.day} ต.ค.', goal=goal))
    vocab_block = next((b for b in day['blocks'] if b['k'] == 'vocab'), None)
    if vocab_block is not None:
        vocab_block['min'] = VOCAB_MINUTES
    else:
        day['blocks'].insert(0, dict(k='vocab', min=VOCAB_MINUTES))
    # Start every day with vocabulary, Reading, then Writing; review follows.
    order = {'vocab': 0, 'reading': 1, 'test': 1, 'writing': 2, 'essay': 2}
    day['blocks'].sort(key=lambda b: order.get(b['k'], 3))
    assert day['blocks'][0]['k'] == 'vocab'
    assert day['blocks'][1]['k'] in ('reading', 'test')
    assert day['blocks'][2]['k'] in ('writing', 'essay')
    day.update(d=n, date=date.isoformat(), wd=weekdays[date.weekday()],
               dateTh=f'{date.day} ต.ค. 2569', phase=pid,
               minutes=sum(b['min'] for b in day['blocks']), newWords=len(vocab.get(str(n), [])))
    day['type'] = ['test', 'weekday', 'weekday', 'integration', 'mock', 'review'][n - 1]

for group in ('passages', 'grammar', 'tests'):
    for item in data[group].values():
        item['day'] = 0  # optional library item, not a scheduled day
for day in days:
    for pid in (day.get('reading') or {}).get('passages', []):
        data['passages'][pid]['day'] = day['d']
    if day.get('test'):
        test = data['tests'][day['test']]
        test['day'] = day['d']
        for pid in test['passages']:
            data['passages'][pid]['day'] = day['d']
    gids = day.get('grammar') or []
    for gid in ([gids] if isinstance(gids, str) else gids):
        data['grammar'][gid]['day'] = day['d']

data.update(days=days, phases=phases, vocab=vocab, extraVocab=extra)
data['blockInfo']['vocab'][1] = data['blockInfo']['vocab'][1].replace('Quiz 20 ข้อ', 'Quiz 100 ข้อ')
data['meta'].update(start=START.isoformat(), end=END.isoformat(), planId=PLAN_ID,
                    built='2026-11-08', lightVocabDays=[], parts={}, coreWords=600,
                    wordsPerDay=WORDS_PER_DAY, vocabRevision='100-per-day-v1')
# The requested end of study is independent of the old target exam date.
data['guide']['exam']['blocks'] = [b for b in data['guide']['exam']['blocks']
                                  if 'วันสอบ' not in b['h'] and 'แผนย่อ' not in b['h']]
data['guide']['exam']['blocks'].insert(0, dict(h='แผนเร่งรัด 8–13 ตุลาคม 2569',
    p='Day 1 = พฤหัสบดี 8 ต.ค. · Day 6 = อังคาร 13 ต.ค. รวม 6 วัน เลือกเนื้อหาหลักจากแผนเดิม 42 วัน '
      'ทุกวันเริ่มจากคำศัพท์ → Reading → Writing แล้วจึงทบทวนและจดข้อผิด '
      'ศัพท์ใหม่วันละ 100 คำ รวม 600 คำ + Essay เต็ม 2 เรื่อง + Reading Test 1 ชุด + Full Mock 1 ชุด '
      'คลังศัพท์ 740 คำและบทเรียนเดิมใช้ฝึกเพิ่มเติมได้ วันสิ้นสุดแผนไม่ใช่การกำหนดวันสอบใหม่'))

js = '\n'.join((HERE / 'js' / name).read_text(encoding='utf-8')
               for name in ('core.js', 'quiz.js', 'day.js', 'views.js'))
js = js.replace("const LS_KEY = 'kkuaelt45.v2';", f"const LS_KEY = '{PLAN_ID}.v2';")
js = js.replace('return { v: 2, done:', 'return { v: 2, planId: DATA.meta.planId, vocabRevision: DATA.meta.vocabRevision, done:')
js = js.replace('Object.assign(d, s, { plan42: s.plan42 || 0 })',
                'Object.assign(d, s, { plan42: s.plan42 || 0, vocabRevision: s.vocabRevision || 0 })')
js = js.replace('const WORD = Object.fromEntries',
                'ALLWORDS.push(...DATA.extraVocab.map(w => Object.assign({ day: 0 }, w)));\nconst WORD = Object.fromEntries')
js = js.replace('const nb = nextBlock(d); const n = daysToExam(); const ex = examDate();',
                'const nb = nextBlock(d); const n = daysToPlanEnd(); const ex = planEndDate();')
js = js.replace('นับถอยหลังวันสอบ', 'สิ้นสุดแผนอ่าน')
js = js.replace("'สอบ ' + thDate(ex, true)", "'จบแผน ' + thDate(ex, true)")
js = js.replace('วันนี้วันสอบ — สู้ ๆ', 'วันสุดท้ายของแผน')
js = js.replace('ผ่านวันสอบแล้ว', 'สิ้นสุดช่วง 8–13 ต.ค. แล้ว')
js = js.replace('เสาร์ที่ 10 ต.ค. 2569', 'พฤหัสบดีที่ 8 ต.ค. 2569')
js = js.replace('แผนเดิม ${esc(day.wd)}', 'ตามแผน ${esc(day.wd)}')
js = js.replace('วันอาทิตย์ — Day 9, 16, 23, 30, 37 — และ Day 41', 'Day 6')
js = js.replace('วันอาทิตย์ (Day 9, 16, 23, 30, 37) และ Day 41', 'Day 6')
js = js.replace('Day ${t.day}', "${t.day ? 'Day ' + t.day : 'ฝึกเพิ่มเติม'}")
js = js.replace('href="#/day/${t.day}"', 'href="${t.day ? \'#/day/\' + t.day : \'#/plan\'}"')
js = js.replace("${tid.startsWith('M') ?", "${tid.startsWith('M') && t.day ?")
js = js.replace('(เป้า 740)', '(เป้า ${DATA.meta.coreWords} คำหลัก)').replace('max="740"', 'max="${DATA.meta.coreWords}"')
js = js.replace('Quiz คำศัพท์ (20 ข้อ:', 'Quiz คำศัพท์ (${words.length} ข้อ:')
js = js.replace('ทำหลัง Mock (คำศัพท์วันนี้ใบ้หัวข้อ essay)', 'เรียนก่อน Reading ตามลำดับประจำวัน')
js = js.replace('ทำหลังสอบ', 'เรียนก่อน Reading')
js = js.replace('(เป้า ≥ 25–30)', '(เป้า ${planCum().p} บทในแผน)').replace('(เป้า 12–15)', '(เป้า 2 เรื่อง)')
js = js.replace('max="16" value="${full}"', 'max="2" value="${full}"')
js = js.replace('(Day ${DATA.tests[id].day})', "(${DATA.tests[id].day ? 'Day ' + DATA.tests[id].day : 'ฝึกเพิ่มเติม'})")
js = js.replace('${DATA.tests[t.label].day}</td>', "${DATA.tests[t.label].day || 'ฝึกเพิ่มเติม'}</td>")
assert js.rstrip().endswith('boot();')
js = js.rstrip()[:-len('boot();')] + '\n' + (HERE / 'js' / 'six_day.js').read_text(encoding='utf-8') + '\nboot();\n'

html = (HERE / 'template.html').read_text(encoding='utf-8')
html = html.replace('42 วัน', '6 วัน').replace('42-Day', '6-Day').replace('<span>42</span>', '<span>6</span>')
html = html.replace('10 ต.ค.–20 พ.ย. 2569', '8–13 ตุลาคม 2569')
html = html.replace('__CSS__', (HERE / 'style.css').read_text(encoding='utf-8') + '''
.six-runway {display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px;margin-top:10px}
.six-runway a {padding:8px 4px;text-align:center;border:1px solid var(--line-2);border-radius:10px;background:var(--surface-2);font-size:12px}
.six-runway a.cur {border-color:var(--sky);box-shadow:inset 0 0 0 1px var(--sky)}
.six-runway a.done {background:var(--good);color:white}
.six-runway b,.six-runway small {display:block}.six-runway small {font-size:10px}
.dgrid {grid-template-columns:repeat(6,minmax(0,1fr))}
@media(max-width:600px){.six-runway {gap:4px}.six-runway a{font-size:11px}.dgrid{grid-template-columns:repeat(3,minmax(0,1fr))}}
''')
html = html.replace('__DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c'))
html = html.replace('__JS__', js)
assert all(token not in html for token in ('__CSS__', '__DATA__', '__JS__'))
assert len(days) == 6 and days[0]['date'] == '2026-10-08' and days[-1]['date'] == '2026-10-13'
OUT.write_text(html, encoding='utf-8')
if '--deploy' in sys.argv[1:]:
    (ROOT / 'KKU-AELT_42_Day_Study_Plan.html').write_text(html, encoding='utf-8')
print(f'Created {OUT.name}: {len(days)} days, {sum(d["minutes"] for d in days)} minutes, '
      f'{WORDS_PER_DAY} words/day, {len(selected)} core / {len(all_vocab)} total words')
