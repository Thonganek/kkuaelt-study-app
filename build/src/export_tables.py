# -*- coding: utf-8 -*-
"""Write the printable Markdown table and the Excel CSV of the 42-day plan from out/data.json."""
import json, csv, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
SCR = Path(__file__).resolve().parent.parent
OUTDIR = Path(sys.argv[1]) if len(sys.argv) > 1 else SCR / 'out'
D = json.loads((SCR / 'out' / 'data.json').read_text(encoding='utf-8'))
KIND = {'paragraph': 'ย่อหน้า', 'analysis': 'วิเคราะห์ + thesis', 'sentences': 'เขียนประโยค', 'intro': 'บทนำ', 'summary': 'สรุปความ', 'rewrite': 'แก้/เขียนใหม่', 'parts': 'ประกอบ essay ทีละส่วน', 'essay': 'Essay เต็ม (จับเวลา)'}
SRC = {'book': 'All that IELTS', 'aelt': 'Aelt Writing 0421.pdf', 'image': 'Image (1).pdf', 'guide': 'Opinion_Essay_Guide.docx', 'improved': 'Improved_Opinion_Essays.docx', 'app': 'ในแอป'}
PH = {p['id']: p for p in D['phases']}


def read_items(d):
    out = []
    for it in d['read']:
        if it['src'] == 'book':
            out.append(f"All that IELTS หน้า {it['pages']} (PDF {it['pdf']}{'–' + str(it['pdfEnd']) if it['pdfEnd'] != it['pdf'] else ''}): {it['what']}")
        elif it['src'] == 'app':
            out.append(f"ในแอป: {it['what']}")
        else:
            out.append(f"{SRC[it['src']]}{' ' + it['pages'] if it['pages'] else ''}: {it['what']}")
    return out


def vocab(d):
    n = len(D['vocab'].get(str(d['d']), []))
    if n:
        w = D['vocab'][str(d['d'])]
        return f"{n} คำใหม่: " + ', '.join(x['w'] for x in w)
    if d.get('review'):
        return 'ทวน ' + str(sum(len(D['vocab'].get(str(x), [])) for x in d['review']['days'])) + f" คำ (Day {', '.join(map(str, d['review']['days']))})"
    return 'ทวนคำที่ติดดาว' if d['type'] == 'review' else 'ทวนศัพท์วิจัย + สำนวน essay'


def reading(d):
    if d.get('test'):
        t = D['tests'].get(d['test'], {'title': d['test']})
        return f"{t['title']} — 6 passages / 69 ข้อ / 120 นาที"
    if d.get('reading'):
        s = ' + '.join(f"{pid} “{D['passages'][pid]['title']}” ({len(D['passages'][pid]['questions'])} ข้อ)" if pid in D['passages'] else pid for pid in d['reading']['passages'])
        s = ' + '.join(D['lessons'][l]['title'] for l in ([d['reading']['lesson']] if isinstance(d['reading']['lesson'], str) else d['reading']['lesson'])) + ': ' + s
        if d['reading'].get('bookTask'):
            s += ' + หนังสือ: ' + d['reading']['bookTask']
        return s
    return 'ทำซ้ำข้อ Reading ที่เคยผิด'


def grams(d):
    g = d.get('grammar')
    return [x for x in ([g] if isinstance(g, str) else g or []) if x in D['grammar']]


def writing(d):
    parts = []
    for gid in grams(d):
        g = D['grammar'][gid]
        parts.append(f"Grammar: {g['title_th']} (quiz {len(g['quiz'])} ข้อ)")
    if d.get('task'):
        t = d['task']; e = D['essays'].get(t.get('topic') or '')
        parts.append(f"{KIND.get(t['kind'], t['kind'])} {t['words']} ({t['minutes']} นาที): " + (f"[{t['topic']}] {e['prompt']}" if e else t['prompt']))
    if d.get('essay'):
        e = D['essays'].get(d['essay']['topic'], {})
        parts.append(f"Essay 60 นาที ≥ 250 คำ: [{d['essay']['topic']}] {e.get('prompt', '')}")
    return ' | '.join(parts) or '—'


def exams(d):
    x = []
    if D['vocab'].get(str(d['d'])):
        x.append(f"Quiz ศัพท์ {max(20, len(D['vocab'][str(d['d'])]))}")
    if d.get('reading'):
        x += [f"Reading {pid} {len(D['passages'][pid]['questions'])} ข้อ" for pid in d['reading']['passages'] if pid in D['passages']]
    if d.get('test'):
        x.append('Reading Test 69 ข้อ')
    for gid in grams(d):
        x.append(f"Grammar {len(D['grammar'][gid]['quiz'])} ข้อ")
    if d.get('task'):
        x.append('งานเขียน')
    if d.get('essay'):
        x.append('Essay 60 นาที')
    ks = [b['k'] for b in d['blocks']]
    if 'vocabreview' in ks:
        x.append('ทวนศัพท์ ' + ('40' if d['type'] == 'review' else '20' if d['type'] == 'light' else '30') + ' ข้อ')
    if 'weekly' in ks:
        x.append('ทำซ้ำข้อผิดสัปดาห์')
    if 'retry' in ks:
        x.append('ทำซ้ำข้อผิดทั้งหมด ≥ 30 ข้อ')
    return ' · '.join(x)


rows = []
for d in D['days']:
    rows.append([d['d'], d['date'], d['wd'], PH[d['phase']]['name'], d['title'], ' / '.join(read_items(d)), vocab(d), reading(d), writing(d), exams(d), d['minutes']])
with open(OUTDIR / 'KKU-AELT_42_Day_Plan.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Day', 'วันที่', 'วัน', 'ช่วง', 'หัวข้อ', 'อ่านอะไร (เลขหน้าหนังสือ / PDF)', 'ศัพท์', 'Reading', 'Writing / Grammar', 'ข้อสอบวันนี้', 'นาที'])
    w.writerows(rows)

md = ['# ตารางอ่าน KKU-AELT 42 วัน (Day 1–42)', '',
      '10 ต.ค. – 20 พ.ย. 2569 · วันสอบเป้าหมาย เสาร์ 21 พ.ย. 2569 (ตามที่กำหนด) — **ตรวจวันสอบจริง:** ปฏิทิน KKU-AELT PBT 2569 ระบุรอบพฤศจิกายน = เสาร์ 14 พ.ย. 2569 (ดูแผนย่อในแอป → คู่มือ → ข้อมูลข้อสอบ)', '',
      'กิจวัตร: จ.–ศ. คำศัพท์ 15 → Reading 40 → Writing/Grammar 30 → สมุดข้อผิด 5 นาที (บางวันในสัปดาห์แรก ๆ 100–110 นาที เพราะรวมเนื้อหาของ 7–9 ต.ค. ไว้) · เสาร์ Reading Test 120 นาที · อาทิตย์ Writing 60 นาที + ทวนข้อผิดของสัปดาห์ · 16–18 พ.ย. Full Mock 3 ชั่วโมง', '']
for p in D['phases']:
    md.append(f"## {p['name']} — {p['th']} ({p['range']}, Day {p['days'][0]}–{p['days'][1]})")
    md.append(f"เป้าหมาย: {p['goal']}")
    md.append('')
    for d in [x for x in D['days'] if x['phase'] == p['id']]:
        md.append(f"### Day {d['d']} · {d['wd']} {d['dateTh']} — {d['title']} ({d['minutes']} นาที)")
        md.append('- **อ่านอะไร:**')
        md += [f'  - {x}' for x in read_items(d)]
        md.append(f'- **ศัพท์:** {vocab(d)}')
        md.append(f'- **Reading:** {reading(d)}')
        md.append(f'- **Writing:** {writing(d)}')
        md.append(f'- **ข้อสอบวันนี้:** {exams(d)}')
        md.append(f"- **สมุดข้อผิดพลาด:** {d['error']}")
        md.append('')
(OUTDIR / 'KKU-AELT_42_Day_Plan.md').write_text('\n'.join(md), encoding='utf-8')
print('wrote CSV + MD to', OUTDIR)
