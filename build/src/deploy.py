# -*- coding: utf-8 -*-
"""Install the new version into the learner's folder; keep the previous version under build/old_v1/."""
import shutil, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
SCR = Path(__file__).resolve().parent.parent
DEST = Path(r'C:/Users/ACE/Desktop/kkuaelt')
OUT = SCR / 'out'
OLD = DEST / 'build' / 'old_v1'

files = ['KKU-AELT_45_Day_Study_Plan.html', 'KKU-AELT_45_Day_Plan.csv', 'KKU-AELT_45_Day_Plan.md', 'README_เริ่มอ่านที่นี่.md']
first = not OLD.exists()
if first:
    OLD.mkdir(parents=True)
    for f in files:
        if (DEST / f).exists():
            shutil.move(str(DEST / f), str(OLD / f))
    src_old = OLD / 'build_src'
    src_old.mkdir()
    for item in list((DEST / 'build').iterdir()):
        if item.name == 'old_v1':
            continue
        shutil.move(str(item), str(src_old / item.name))
    print('moved previous version to', OLD)
for f in files:
    shutil.copy2(OUT / f, DEST / f)
src = DEST / 'build' / 'src'
if src.exists():
    shutil.rmtree(src)
shutil.copytree(SCR / 'build2', src, ignore=shutil.ignore_patterns('__pycache__', 'deploy.py', '*_backup*', 'restyle_patch*.py', 'shots_design.py'))
for d in ('content', 'spec', 'verify'):
    if (DEST / 'build' / d).exists():
        shutil.rmtree(DEST / 'build' / d)
    shutil.copytree(SCR / d, DEST / 'build' / d)
(DEST / 'build' / 'README_build.md').write_text(
    '# วิธีสร้างไฟล์ใหม่\n\n'
    'ซอร์สอยู่ใน `src/` (แผนรายวัน `plan_days.py`, บทเรียน `lessons.py`, แอป `js/` + `style.css` + `template.html`) และเนื้อหาใน `content/` (ข้อสอบ ศัพท์ grammar essay)\n\n'
    '```\ncd build/src\npython build.py          # สร้าง build/out/KKU-AELT_45_Day_Study_Plan.html\npython export_tables.py  # ตาราง .md และ .csv\npython test_full.py      # ทดสอบคลิกทุกวัน (ต้องมี playwright)\n```\n\n'
    '`verify/` เก็บผลการตรวจเฉลยแบบ blind (ผู้ตรวจไม่เห็นเฉลย) ของข้อสอบทุกชุด\n'
    '`old_v1/` คือเวอร์ชันก่อนหน้า (HTML เดิม + ซอร์สเดิม + บันทึกการอ่านหนังสือ)\n', encoding='utf-8')
print('installed to', DEST)
for f in files:
    print(' ', f, (DEST / f).stat().st_size, 'bytes')
