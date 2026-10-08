# วิธีสร้างไฟล์ใหม่

ซอร์สอยู่ใน `src/` (แผนรายวัน `plan_days.py`, บทเรียน `lessons.py`, แอป `js/` + `style.css` + `template.html`) และเนื้อหาใน `content/` (ข้อสอบ ศัพท์ grammar essay)

```
cd build/src
python build.py          # สร้าง build/out/KKU-AELT_45_Day_Study_Plan.html
python export_tables.py  # ตาราง .md และ .csv
python test_full.py      # ทดสอบคลิกทุกวัน (ต้องมี playwright)
```

`verify/` เก็บผลการตรวจเฉลยแบบ blind (ผู้ตรวจไม่เห็นเฉลย) ของข้อสอบทุกชุด
`old_v1/` คือเวอร์ชันแรก (HTML เดิม + ซอร์สเดิม + บันทึกการอ่านหนังสือ) · `old_v2/` แบบเรียบ · `old_v3/` ธีมมืด Flight deck · `old_v4/` ธีม Hologram สว่าง · `old_v5/` แผน 45 วัน Bento โทนฟ้าเขียว · `old_v6/` แผน 42 วัน ธีม AI โทนม่วง · `old_v7/` ธีมเขียว–ฟ้าโหมดมืด · `old_v8/` โทนฟ้า–เขียวสว่าง · ปัจจุบัน = แผน 42 วัน + ธีม Iron Man (สว่าง) / JARVIS HUD (มืด)


## แผน 42 วัน
`src/plan42.py` แปลงแผน 45 วันใน `src/plan_days.py` (เริ่ม 7 ต.ค.) เป็นแผน 42 วันที่เริ่ม 10 ต.ค.: Day เดิม n = Day ใหม่ n−3 ในวันที่ปฏิทินเดียวกัน และรวมเนื้อหาของ Day เดิม 1–3 เข้ากับวันที่ทักษะเข้ากัน (ดู docstring ในไฟล์) · `build.py` ใช้ `plan42` สร้างไฟล์ `KKU-AELT_42_Day_Study_Plan.html`
