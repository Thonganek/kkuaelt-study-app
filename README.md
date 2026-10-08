# KKU-AELT 42-Day Study App

แอปเตรียมสอบ KKU-AELT แบบไฟล์เดียว (HTML ออฟไลน์) — แผน 42 วัน (10 ต.ค.–20 พ.ย. 2569, สอบ 21 พ.ย.) พร้อมข้อสอบทุกวัน

- **แอป:** เปิด `KKU-AELT_42_Day_Study_Plan.html` ด้วย Chrome / Edge ได้ทันที ไม่ต้องติดตั้ง
- **ตาราง:** `KKU-AELT_42_Day_Plan.md` (อ่าน/พิมพ์) และ `KKU-AELT_42_Day_Plan.csv` (Excel)
- **วิธีใช้ละเอียด:** [README_เริ่มอ่านที่นี่.md](README_เริ่มอ่านที่นี่.md)

## มีอะไรบ้าง

- คำศัพท์ 740 คำ (ศัพท์งานวิจัย + Academic Word List + ศัพท์หัวข้อ essay) พร้อม quiz
- บทอ่าน 85 บท: ฝึกรายวัน 31 บท + Reading Test เต็มชุด 6 ชุด + Full Mock 3 ชุด (69 ข้อ / 120 นาที) เฉลยภาษาไทยทุกข้อ
- Grammar 30 บทพร้อม quiz · งานเขียนทุกวัน + Essay จับเวลา · สมุดข้อผิดพลาดที่ทำซ้ำได้ · สถิติแยกทักษะ
- ความคืบหน้าบันทึกในเบราว์เซอร์ (localStorage) มีปุ่มสำรอง/กู้คืนเป็นไฟล์ JSON

## ไฟล์ที่ไม่ได้อยู่ใน repo

เอกสารต้นฉบับ 5 ไฟล์ (All that IELTS PDF, Aelt Writing 0421.pdf, Image (1).pdf, Opinion_Essay_Guide.docx, Improved_Opinion_Essays.docx) ไม่ได้อัปโหลด — หนังสือมีลิขสิทธิ์และไฟล์ใหญ่เกินขีดจำกัดของ GitHub
ถ้าวางไฟล์เหล่านี้ไว้โฟลเดอร์เดียวกับไฟล์ HTML ปุ่ม “เปิด PDF หน้า …” ในแอปจะเปิดหน้าหนังสือได้

## สร้างไฟล์ใหม่จากซอร์ส

```
cd build/src
python build.py          # ต้องมี python-docx และเอกสาร DOCX ตามพาธ SRC_DIR ใน build.py
python export_tables.py  # ตาราง .md / .csv
python test_full.py      # ทดสอบทุกวันทุกขั้นด้วย Playwright
```

- `build/src/plan_days.py` แผนเนื้อหา 45 วันเดิม · `build/src/plan42.py` แปลงเป็นแผน 42 วันที่เริ่ม 10 ต.ค.
- `build/content/` บทอ่าน ข้อสอบ ศัพท์ grammar essay (JSON) · `build/spec/` สเปกการออกเนื้อหา · `build/verify/` ผลตรวจเฉลยแบบ blind

ข้อสอบในแอปแต่งขึ้นใหม่เพื่อการฝึก ไม่ใช่ข้อสอบจริง และคะแนนร้อยละไม่ใช่ระดับคะแนนทางการ
