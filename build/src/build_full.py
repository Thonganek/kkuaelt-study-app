# -*- coding: utf-8 -*-
"""Build the 60-day self-paced KKU-AELT course aimed at Band 7.

Days 1-40 come from the 42-day plan (without dates or time limits), Days 41-58 are the
Band 7 stage (build/content/band7/ + 300 academic words), Days 59-60 are the final review.

Run from any directory: python build/src/build_full.py
The output KKU-AELT_Full_Course.html is the page served on GitHub Pages.
"""
import copy
import json
import re
import sys
from pathlib import Path

import band7

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = ROOT / 'KKU-AELT_42_Day_Study_Plan_Original.html'
ACADEMIC = HERE.parent / 'content' / 'vocab_academic.json'
OUT = ROOT / 'KKU-AELT_Full_Course.html'
PLAN_ID = 'kkuaelt-full'
VOCAB_REVISION = 'band7-60-v1'

original = SOURCE.read_text(encoding='utf-8')
match = re.search(r'<script id="study-data" type="application/json">(.*?)</script>', original, re.S)
assert match, 'The original study data must be present.'
data = json.loads(match.group(1))
days = data['days']
assert len(days) == 42

academic = json.loads(ACADEMIC.read_text(encoding='utf-8'))
old_words = {w['w'].lower() for ws in data['vocab'].values() for w in ws}
assert len(academic) == 300, len(academic)
assert len({w['w'].lower() for w in academic}) == 300, 'duplicate academic words'
assert not old_words & {w['w'].lower() for w in academic}, old_words & {w['w'].lower() for w in academic}
for w in academic:
    assert all(w.get(k) for k in ('w', 'pos', 'th', 'fam', 'col', 'ex')), w
    w['src'] = 'AVL'

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

# ---------------- 60 days: Band 7 stage on Days 41-58 ----------------
days = band7.assemble(data, academic, untime)
total_words = sum(len(v) for v in data['vocab'].values())
assert len(days) == 60 and total_words == 1040, (len(days), total_words)

data['blockInfo']['test'][0] = 'Reading Test เต็มชุด'
data['blockInfo']['test'][1] = 'ทำข้อสอบเต็ม 6 passages / 69 ข้อ ไม่จำกัดเวลา มีนาฬิกาบอกเวลาที่ใช้ ห้ามดูเฉลยระหว่างทำ'
data['blockInfo']['essay'][0] = 'Writing Essay เต็ม'
data['blockInfo']['essay'][1] = 'วางแผน → เขียน → ตรวจด้วย Checklist แล้วจึงดูตัวอย่าง (วันสอบจริงมี 60 นาที: วางแผน 10 / เขียน 40 / ตรวจ 10)'
data['blockInfo']['vocab'][1] = data['blockInfo']['vocab'][1].replace('Quiz 20 ข้อ', 'Quiz ทุกคำของวัน')

exam = data['guide']['exam']['blocks']
data['guide']['exam']['blocks'] = [b for b in exam if 'วันสอบของคุณ' not in b.get('h', '') and 'แผนย่อ' not in b.get('h', '')]
data['guide']['exam']['blocks'].insert(0, dict(
    h='หลักสูตร 60 Day เป้าหมาย Band 7 · ไม่จำกัดเวลา',
    p='KKU-AELT ประเมินผลเป็น 7 ระดับ หลักสูตรนี้ตั้งเป้าที่ Band 7 ซึ่งเป็นระดับสูงสุด · Day 1–37 ปูพื้นฐานและกลยุทธ์ · '
      'Day 38–40 Full Mock 3 ชุดเป็นจุดวัดผลก่อนเข้าช่วง Band 7 · Day 41–58 ช่วง Band 7: Reading Test ระดับยาก 3 ชุด, '
      'Band 7 Mock 2 ชุด, บทอ่านยากรายวัน 10 บท, Grammar ขั้นสูง 5 บท, Essay โจทย์ใหม่ 5 เรื่องพร้อมตัวอย่างระดับ Band 7 '
      f'และ Academic Vocabulary 300 คำ · Day 59–60 ทบทวนข้อผิดและทบทวนเบา ๆ · คำศัพท์รวม {total_words} คำ · '
      'ทำตามจังหวะของตัวเอง ไม่ผูกกับวันที่ ข้อสอบไม่ตัดเวลาและไม่ส่งอัตโนมัติ มีนาฬิกาบอกเวลาที่ใช้ · '
      'เวลาที่เห็นในแผนเป็นค่าประมาณ ส่วนแผนเวลาในคู่มือคือเวลาของวันสอบจริง'))

data['meta'].update(planId=PLAN_ID, vocabRevision=VOCAB_REVISION, academicWords=len(academic),
                    totalWords=total_words, built='2026-11-26', target='Band 7')

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
    """<div class="tile-label">${ico('flag')} เป้าหมาย Band 7</div><div class="stat-num">${doneDays}<small> / ${NDAYS} Day</small></div><div class="sub small">ไม่จำกัดเวลา · ทำตามจังหวะของตัวเอง</div>""")
rep('<span class="eb-plan"> · แผนเดิม ${esc(day.wd)} ${esc(day.dateTh)}</span>', '<span class="eb-plan"> · ${esc(day.dateTh)}</span>')
# vocabulary counts
rep('Quiz คำศัพท์ (20 ข้อ:', 'Quiz คำศัพท์ (${words.length} ข้อ:')
rep('<h1>คลังคำศัพท์ 740 คำ</h1>', '<h1>คลังคำศัพท์ ${ALLWORDS.length} คำ</h1>')
rep('รวมวันละ 20–23 คำ</p>', 'รวมวันละ 20–23 คำ · ช่วง Band 7 (Day 41–58) = Academic Vocabulary ${DATA.meta.academicWords} คำ วันละ 20 คำ · กรองเฉพาะชุดนี้ได้ด้วยปุ่ม “Academic +300”</p>')
rep("[['all', 'ทั้งหมด'], ['star', 'ติดดาว'], ['known', 'จำได้แล้ว'], ['new', 'ยังไม่ระบุ']].map(([k, l]) => `<button class=\"${f === k",
    "[['all', 'ทั้งหมด'], ['avl', 'Academic +300'], ['star', 'ติดดาว'], ['known', 'จำได้แล้ว'], ['new', 'ยังไม่ระบุ']].map(([k, l]) => `<button class=\"${f === k")
rep('(เป้า 740)</div><progress max="740"', '(เป้า ${ALLWORDS.length})</div><progress max="${ALLWORDS.length}"')
# Band grading under every full essay, and a Writing test tab in Writing Studio (build/src/js/writing_grade.js)
rep("${ico('download')} .txt</button></div>`;", "${ico('download')} .txt</button></div>${short ? '' : gradeBox(key)}`;")
rep("['models', 'ตัวอย่างจากเอกสารของคุณ']]", "['models', 'ตัวอย่างจากเอกสารของคุณ'], ['test', 'ข้อสอบ Writing · ตรวจ Band']]")
# Writing Studio opens any essay topic, including the Band 7 prompts BE1-BE5
rep("tab.startsWith('R')", "!!DATA.essays[tab]", 3)
# Band 7 mocks (AM1, AM2) behave like the original mocks
rep("tid.startsWith('M')", r"/^A?M\d/.test(tid)", 2)
# review days are no longer fixed at Day 9, 16, 23, 30, 37 and 41
SUNDAYS = "${DAYS.filter(x => x.type === 'sunday').map(x => x.d).join(', ')}"
REVIEW = "${DAYS.filter(x => x.type === 'review').map(x => x.d).join(', ')}"
rep('(Day 9, 16, 23, 30, 37) และ Day 41', f'(Day {SUNDAYS}) และ Day {REVIEW}')
rep('— Day 9, 16, 23, 30, 37 — และ Day 41', f'— Day {SUNDAYS} — และ Day {REVIEW}')
# essays written for the Band 7 stage explain what makes the model a Band 7 answer
rep("— ${esc(e.stance_reason_th)}</p>` : ''}",
    "— ${esc(e.stance_reason_th)}</p>` : ''}${e.band7_th ? `<p class=\"small\"><b>ทำไมตัวอย่างนี้อยู่ระดับ Band 7</b></p>"
    "<ul class=\"small\">${e.band7_th.map(x => `<li>${esc(x)}</li>`).join('')}</ul>` : ''}")
assert js.rstrip().endswith('boot();')
js = js.rstrip()[:-len('boot();')] + '\n' + '\n'.join(
    (HERE / 'js' / name).read_text(encoding='utf-8') for name in ('full_course.js', 'writing_grade.js')) + '\nboot();\n'

html = (HERE / 'template.html').read_text(encoding='utf-8')
html = html.replace('<title>KKU-AELT 42 วัน</title>', '<title>KKU-AELT 60 Day · Band 7</title>')
html = html.replace('ตารางอ่าน KKU-AELT 42 วัน (10 ต.ค.–20 พ.ย. 2569) พร้อมข้อสอบทุกวัน คำศัพท์ 740 คำ',
                    f'หลักสูตร KKU-AELT 60 Day เป้าหมาย Band 7 ไม่จำกัดเวลา พร้อมข้อสอบ 14 ชุด คำศัพท์ {total_words} คำ')
html = html.replace('ตาราง 42 วัน', 'หลักสูตร 60 Day').replace('10 ต.ค.–20 พ.ย. 2569', 'ไม่จำกัดเวลา')
html = html.replace('<span>42</span>', '<span>60</span>').replace('42-Day Study Studio', '60-Day · Band 7')
html = html.replace('__CSS__', (HERE / 'style.css').read_text(encoding='utf-8'))
html = html.replace('__DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c'))
html = html.replace('__JS__', js)
assert all(token not in html for token in ('__CSS__', '__DATA__', '__JS__'))
OUT.write_text(html, encoding='utf-8')
print(f'Created {OUT.name}: {len(days)} days, {total_words} words '
      f'({len(academic)} academic), {len(changed)} texts without time limits')
