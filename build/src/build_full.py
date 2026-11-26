# -*- coding: utf-8 -*-
"""Build the full self-paced course: the 42-day plan without dates or time limits,
plus 300 extra academic words (build/content/vocab_academic.json).

Run from any directory: python build/src/build_full.py
Use --deploy to also update the GitHub Pages entry file KKU-AELT_42_Day_Study_Plan.html.
"""
import copy
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = ROOT / 'KKU-AELT_42_Day_Study_Plan_Original.html'
ACADEMIC = HERE.parent / 'content' / 'vocab_academic.json'
OUT = ROOT / 'KKU-AELT_Full_Course.html'
PLAN_ID = 'kkuaelt-full'
VOCAB_REVISION = 'academic-300-v1'

original = SOURCE.read_text(encoding='utf-8')
match = re.search(r'<script id="study-data" type="application/json">(.*?)</script>', original, re.S)
assert match, 'The original study data must be present.'
data = json.loads(match.group(1))
days = data['days']
assert len(days) == 42

# ---------------- 300 academic words, spread over the vocabulary days ----------------
academic = json.loads(ACADEMIC.read_text(encoding='utf-8'))
old_words = {w['w'].lower() for ws in data['vocab'].values() for w in ws}
assert len(academic) == 300, len(academic)
assert len({w['w'].lower() for w in academic}) == 300, 'duplicate academic words'
assert not old_words & {w['w'].lower() for w in academic}, old_words & {w['w'].lower() for w in academic}
for w in academic:
    assert all(w.get(k) for k in ('w', 'pos', 'th', 'fam', 'col', 'ex')), w
    w['src'] = 'AVL'
vocab_days = sorted(data['vocab'], key=int)
light = {str(d) for d in data['meta'].get('lightVocabDays', [])}
capacity = {d: 8 if d in light else 9 for d in vocab_days}
assert sum(capacity.values()) == 300, sum(capacity.values())
added = {d: [] for d in vocab_days}
i = 0
for w in academic:  # round-robin so each day mixes verbs, nouns and adjectives
    while len(added[vocab_days[i % len(vocab_days)]]) >= capacity[vocab_days[i % len(vocab_days)]]:
        i += 1
    added[vocab_days[i % len(vocab_days)]].append(w)
    i += 1
for d in vocab_days:
    data['vocab'][d].extend(added[d])
total_words = sum(len(v) for v in data['vocab'].values())
assert total_words == 1040, total_words
for day in days:
    n = len(data['vocab'].get(str(day['d']), []))
    if 'newWords' in day or n:
        day['newWords'] = n
    if n:
        for b in day['blocks']:
            if b['k'] == 'vocab':
                b['min'] += 5  # about nine more words to learn
    day['minutes'] = sum(b['min'] for b in day['blocks'])

# ---------------- no dates, no time limits ----------------
PHASE_TH = {p['id']: p['th'] for p in data['phases']}
for p in data['phases']:
    a, b = p['days']
    p['range'] = f'Day {a}' if a == b else f'Day {a}–{b}'
    p['th'] = p['th'].replace(' + จับเวลา', '')
    p['goal'] = p['goal'].replace('Reading จับเวลา + Writing จับเวลา', 'Reading + Writing เต็มรูปแบบ')

RULES = [
    (r'วางแผน 5 → เขียน 30 → ตรวจ 5 นาที', 'วางแผน → เขียน → ตรวจ'),
    (r'passage ที่ใช้เวลาเกิน 15 นาที \(สั้น\) หรือ 35 นาที \(ยาว\) และสาเหตุ', 'passage ที่ใช้เวลานานที่สุด และสาเหตุ'),
    (r'จำลองวันสอบจริง 3 ชั่วโมงต่อเนื่อง \(09\.00–12\.00 น\.\)', 'จำลองวันสอบจริง: Reading ต่อด้วย Writing โดยไม่จำกัดเวลา แล้วจดเวลาที่ใช้ไว้เทียบ'),
    (r'เตรียม Mock: ตั้งนาฬิกา 09\.00–12\.00 น\. สำหรับ 16–18 พ\.ย\.', 'เตรียม Full Mock 3 ชุดใน Day 38–40'),
    (r'Full test 6 passages / 69 ข้อ / 120 นาที', 'Full test 6 passages / 69 ข้อ'),
    (r'Writing Diagnostic 60 นาที', 'Writing Diagnostic'),
    (r'Writing 60 นาที', 'Writing Essay เต็ม'),
    (r'Essay 40 นาที', 'Essay เต็ม'),
    (r'Timed essay 40 นาที', 'Essay เต็ม'),
    (r'Timed: ', ''),
    (r'Reading จับเวลา', 'Reading ฝึกความเร็ว'),
    (r'Long text 30 นาที', 'Long text'),
    (r'เต็มเวลา 60 นาที', 'เต็ม'),
    (r'เต็ม 60 นาที', 'เต็ม'),
    (r'ให้ทันเวลา 12 นาที/บท', 'อย่างแม่นยำ'),
    (r'ให้จบใน 30 นาที', 'ให้ครบทุกข้อ'),
    (r'ตลอด 120 นาที', 'ตลอดทั้งชุด'),
    (r'และเขียน essay เต็มใน 40 นาที', 'และเขียน essay เต็ม'),
    (r'แผนเวลา 120 นาที', 'แผนเวลาวันสอบจริง'),
    (r'กลยุทธ์ทำข้อสอบ 120 นาที', 'กลยุทธ์ทำข้อสอบเต็มชุด'),
    (r'\s*(?:ภายใน|ใน)\s*\d+(?:–\d+)?\s*นาที', ''),
    (r'\s*\((?:ทำจริง |ทำ )?\d+(?:–\d+)?\s*นาที(?:/บท)?\)', ''),
    (r'(?<=\S) \d+(?:–\d+)? นาที(?=[ :,)]|$)', ''),
]


def untime(s):
    for pat, rep in RULES:
        s = re.sub(pat, rep, s)
    return re.sub(r'\s{2,}', ' ', s).strip()


changed = []


def fix(obj, key):
    if isinstance(obj.get(key), str):
        new = untime(obj[key])
        if new != obj[key]:
            changed.append((obj[key], new))
            obj[key] = new


for day in days:
    for k in ('title', 'goal', 'focusR', 'focusW', 'error'):
        fix(day, k)
    for it in day.get('read', []):
        fix(it, 'what')
    if day.get('reading'):
        day['reading'].pop('timed', None)
        fix(day['reading'], 'bookTask')
    if day.get('task'):
        fix(day['task'], 'prompt')
        day['task']['steps'] = [untime(s) for s in day['task'].get('steps', [])]
    day['wd'] = ''
    day['dateTh'] = PHASE_TH[day['phase']]
    day.pop('date', None)
if '--show-changes' in sys.argv[1:]:
    for a, b in changed:
        print('-', a, '\n+', b)

data['blockInfo']['test'][0] = 'Reading Test เต็มชุด'
data['blockInfo']['test'][1] = 'ทำข้อสอบเต็ม 6 passages / 69 ข้อ ไม่จำกัดเวลา มีนาฬิกาบอกเวลาที่ใช้ ห้ามดูเฉลยระหว่างทำ'
data['blockInfo']['essay'][0] = 'Writing Essay เต็ม'
data['blockInfo']['essay'][1] = 'วางแผน → เขียน → ตรวจด้วย Checklist แล้วจึงดูตัวอย่าง (วันสอบจริงมี 60 นาที: วางแผน 10 / เขียน 40 / ตรวจ 10)'
data['blockInfo']['vocab'][1] = data['blockInfo']['vocab'][1].replace('Quiz 20 ข้อ', 'Quiz ทุกคำของวัน')

exam = data['guide']['exam']['blocks']
data['guide']['exam']['blocks'] = [b for b in exam if 'วันสอบของคุณ' not in b.get('h', '') and 'แผนย่อ' not in b.get('h', '')]
data['guide']['exam']['blocks'].insert(0, dict(
    h='หลักสูตรเต็ม ไม่จำกัดเวลา',
    p=f'ทำ Day 1–42 ตามลำดับได้ตามจังหวะของตัวเอง ไม่ผูกกับวันที่และไม่มีวันหมดเขต ข้อสอบและแบบฝึกไม่ตัดเวลาหรือส่งอัตโนมัติ '
      f'มีนาฬิกาจับเวลาให้ดูว่าใช้เวลาไปเท่าไร (หยุดพักได้) · คำศัพท์รวม {total_words} คำ = AWL และศัพท์หัวข้อ 740 คำ '
      '+ Academic Vocabulary เพิ่ม 300 คำ · บทอ่าน 85 บท · Grammar 30 บท · Reading Test 6 ชุด · Full Mock 3 ชุด · '
      'เวลาที่เห็นในแผนเป็นค่าประมาณ ส่วนแผนเวลาในคู่มือคือเวลาของวันสอบจริง'))

data['meta'].update(planId=PLAN_ID, vocabRevision=VOCAB_REVISION, academicWords=len(academic),
                    totalWords=total_words, built='2026-11-26')

# ---------------- app code ----------------
js = '\n'.join((HERE / 'js' / name).read_text(encoding='utf-8')
               for name in ('core.js', 'quiz.js', 'day.js', 'views.js'))


def rep(old, new, count=1):
    global js
    assert js.count(old) == count, (js.count(old), old)
    js = js.replace(old, new)


rep("const LS_KEY = 'kkuaelt45.v2';",
    "const LS_KEY = 'kkuaelt-full.v2';\n"
    "// carry over progress from the earlier 42-day edition on first open\n"
    "try { if (!localStorage.getItem(LS_KEY) && localStorage.getItem('kkuaelt45.v2')) localStorage.setItem(LS_KEY, localStorage.getItem('kkuaelt45.v2')); } catch (e) { }")
rep("return { v: 2, done:", "return { v: 2, planId: DATA.meta.planId, vocabRevision: DATA.meta.vocabRevision, done:")
rep("Object.assign(d, s, { plan42: s.plan42 || 0 })", "Object.assign(d, s, { plan42: s.plan42 || 0, vocabRevision: s.vocabRevision || 0 })")
rep("essay: 'Essay เต็ม (จับเวลา)'", "essay: 'Essay เต็ม'")
# tests: no countdown, no auto-submit
rep("if (status === 'running' && Date.now() > st.end) { setTimeout(() => submitQuiz(key, true), 0); }", '')
rep("const used = st.startAt ? Math.min(120, Math.round(((st.at || Date.now()) - st.startAt) / 60000)) : null;",
    "const used = st.usedSec != null ? Math.max(1, Math.round(st.usedSec / 60)) : st.startAt ? Math.min(120, Math.round(((st.at || Date.now()) - st.startAt) / 60000)) : null;")
rep('6 passages · 69 ข้อ · 120 นาที — กด “เริ่มทำข้อสอบ” แล้วนาฬิกาจะเดินต่อเนื่อง (แม้ปิดไฟล์) เมื่อหมดเวลาระบบส่งคำตอบให้อัตโนมัติ',
    '6 passages · 69 ข้อ · <b>ไม่จำกัดเวลา</b> — ทำจนครบแล้วกด “ส่งข้อสอบ” เอง ระบบไม่ตัดเวลาและไม่ส่งให้อัตโนมัติ นาฬิกาแสดงเวลาที่ใช้ไป (ออกจากหน้าข้อสอบ = หยุดนาฬิกาไว้) · วันสอบจริงมีเวลา 120 นาที')
rep('<th>เวลาแนะนำ</th>', '<th>เวลาแนะนำในวันสอบจริง</th>')
rep('ทำต่อเนื่องเหมือนวันจริง — Reading 120 นาที แล้วต่อด้วย Writing 60 นาทีทันที (09.00–12.00 น. ถ้าทำได้)',
    'ทำ Reading ให้ครบ แล้วต่อด้วย Writing เหมือนวันสอบจริง ไม่จำกัดเวลา — ดูเวลาที่ใช้ไว้เทียบกับวันสอบจริง (Reading 120 + Writing 60 นาที)')
rep('เริ่มทำข้อสอบ (120 นาที)', 'เริ่มทำข้อสอบ (ไม่จำกัดเวลา)')
rep('ออก (เวลาเดินต่อ)', 'ออก (หยุดนาฬิกาไว้)')
rep('ต่อ Writing 60 นาที', 'ต่อ Writing Essay')
rep(': 69 ข้อ / 120 นาที`', ': 69 ข้อ`')
rep('<div class="small">6 passages / 69 ข้อ / 120 นาที</div>', '<div class="small">6 passages / 69 ข้อ · ไม่จำกัดเวลา</div>')
rep('<span class="chip">6 passages · 69 ข้อ · 120 นาที</span>', '<span class="chip">6 passages · 69 ข้อ · ไม่จำกัดเวลา</span>')
rep(" (6 passages / 69 ข้อ / 120 นาที)'", " (6 passages / 69 ข้อ)'")
rep('จับเวลา 60 นาที (≥ 250 คำ)', 'เต็ม (≥ 250 คำ)')
rep('Essay 60 นาที', 'Essay เต็ม', 5)
rep('แผน 60 นาที</b>', 'แผนเวลาวันสอบจริง 60 นาที (ฝึกในแอปไม่จำกัดเวลา)</b>')
rep("integration: 'จับเวลา'", "integration: 'รวมทักษะ'")
# estimated durations are a guide, not a limit
rep('${ico(\'clock\')} ${day.minutes} นาที</span>', '${ico(\'clock\')} ≈ ${day.minutes} นาที</span>')
rep('ขั้น ${i + 1}/${day.blocks.length} · ${b.min} นาที', 'ขั้น ${i + 1}/${day.blocks.length} · ≈ ${b.min} นาที')
rep('${ico(\'clock\')} ${task.minutes} นาที</span>', '${ico(\'clock\')} ≈ ${task.minutes} นาที</span>')
# the hero no longer counts down to an exam date
rep("""<div class="tile-label">${ico('flag')} นับถอยหลังวันสอบ</div><div class="stat-num">${n > 0 ? n : n === 0 ? '0' : '—'}<small> วัน</small></div><div class="sub small">${n > 0 ? 'สอบ ' + thDate(ex, true) : n === 0 ? 'วันนี้วันสอบ — สู้ ๆ' : 'ผ่านวันสอบแล้ว'}</div>""",
    """<div class="tile-label">${ico('flag')} หลักสูตรเต็ม</div><div class="stat-num">${doneDays}<small> / ${NDAYS} Day</small></div><div class="sub small">ไม่จำกัดเวลา · ทำตามจังหวะของตัวเอง</div>""")
rep('<span class="eb-plan"> · แผนเดิม ${esc(day.wd)} ${esc(day.dateTh)}</span>', '<span class="eb-plan"> · ${esc(day.dateTh)}</span>')
# vocabulary counts
rep('Quiz คำศัพท์ (20 ข้อ:', 'Quiz คำศัพท์ (${words.length} ข้อ:')
rep('<h1>คลังคำศัพท์ 740 คำ</h1>', '<h1>คลังคำศัพท์ ${ALLWORDS.length} คำ</h1>')
rep('รวมวันละ 20–23 คำ</p>', 'รวมวันละ 20–23 คำ + Academic Vocabulary เพิ่มวันละ 8–9 คำ (รวม ${DATA.meta.academicWords} คำ) · กรองเฉพาะชุดใหม่ได้ด้วยปุ่ม “Academic +300”</p>')
rep("[['all', 'ทั้งหมด'], ['star', 'ติดดาว'], ['known', 'จำได้แล้ว'], ['new', 'ยังไม่ระบุ']].map(([k, l]) => `<button class=\"${f === k",
    "[['all', 'ทั้งหมด'], ['avl', 'Academic +300'], ['star', 'ติดดาว'], ['known', 'จำได้แล้ว'], ['new', 'ยังไม่ระบุ']].map(([k, l]) => `<button class=\"${f === k")
rep('(เป้า 740)</div><progress max="740"', '(เป้า ${ALLWORDS.length})</div><progress max="${ALLWORDS.length}"')
assert js.rstrip().endswith('boot();')
js = js.rstrip()[:-len('boot();')] + '\n' + (HERE / 'js' / 'full_course.js').read_text(encoding='utf-8') + '\nboot();\n'

html = (HERE / 'template.html').read_text(encoding='utf-8')
html = html.replace('<title>KKU-AELT 42 วัน</title>', '<title>KKU-AELT หลักสูตรเต็ม</title>')
html = html.replace('ตารางอ่าน KKU-AELT 42 วัน (10 ต.ค.–20 พ.ย. 2569) พร้อมข้อสอบทุกวัน คำศัพท์ 740 คำ',
                    f'หลักสูตร KKU-AELT เต็ม 42 Day ไม่จำกัดเวลา พร้อมข้อสอบ คำศัพท์ {total_words} คำ')
html = html.replace('ตาราง 42 วัน', 'หลักสูตร 42 Day').replace('10 ต.ค.–20 พ.ย. 2569', 'ไม่จำกัดเวลา')
html = html.replace('__CSS__', (HERE / 'style.css').read_text(encoding='utf-8'))
html = html.replace('__DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c'))
html = html.replace('__JS__', js)
assert all(token not in html for token in ('__CSS__', '__DATA__', '__JS__'))
OUT.write_text(html, encoding='utf-8')
if '--deploy' in sys.argv[1:]:
    (ROOT / 'KKU-AELT_42_Day_Study_Plan.html').write_text(html, encoding='utf-8')
print(f'Created {OUT.name}: {len(days)} days, {total_words} words '
      f'({len(academic)} academic), {len(changed)} texts without time limits')
