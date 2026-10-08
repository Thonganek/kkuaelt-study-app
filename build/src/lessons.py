# -*- coding: utf-8 -*-
"""Reading-skill lessons (Thai), small model answers and the in-app guide."""

# Each lesson: title, steps (list), signals (list of English cue words, optional), trap (Thai), drill (what to do in the passage)
RL = {}
RL['L_FORMAT'] = dict(
    title='รู้จักข้อสอบ Reading KKU-AELT',
    steps=['ข้อสอบ Reading มี 6 passages รวม 69 ข้อ เวลา 2 ชั่วโมง (ตามคู่มือการสอบของศูนย์ฯ)',
           'Passage 1–4 = ข้อความสั้น/ข่าว (Short text/News) ตัวเลือก 4 ข้อ เลือกคำตอบที่ถูกที่สุด 1 ข้อ',
           'Passage 5–6 = บทความยาว (Long text) มีทั้ง 4 ตัวเลือกและ Short answer (เขียนเป็นวลี/ประโยคสั้น)',
           'แผนเวลาแนะนำ: บทสั้น 10–12 นาที/บท (≈45 นาที) → บทยาว 30 นาที/บท (≈60 นาที) → เผื่อตรวจ 10–15 นาที',
           'วิธีทำทุก passage: อ่านคำถามก่อน → skim ชื่อเรื่อง+ประโยคแรกของแต่ละย่อหน้า → scan หาคำตอบ → ยืนยันด้วยหลักฐานในบทความ'],
    trap='อย่าแปลทุกคำ อย่าใช้ความรู้เดิมตอบแทนข้อความ — คำตอบที่ถูกต้อง “มีหลักฐานในบทความ” เสมอ',
    drill='ทำ W01 แบบไม่จับเวลา ทุกข้อให้ระบุว่าหลักฐานอยู่ย่อหน้าไหน (¶) ก่อนกดส่ง')
RL['L_PREVIEW'] = dict(
    title='Previewing & Predicting — ดูภาพรวมก่อนอ่าน',
    steps=['อ่านชื่อเรื่อง + หัวข้อย่อย (ถ้ามี) แล้วถามตัวเองว่า “บทความนี้น่าจะพูดถึงอะไร”',
           'อ่านประโยคแรกของทุกย่อหน้า (มักเป็น topic sentence) และประโยคสุดท้ายของบทความ',
           'เดาโครงเรื่อง: ปัญหา→สาเหตุ→ทางแก้? / ข้อดี–ข้อเสีย? / เปรียบเทียบ?',
           'จากนั้นค่อยอ่านคำถาม แล้วรู้ทันทีว่าควรกลับไปย่อหน้าไหน'],
    signals=['title', 'subheading', 'first sentence', 'however', 'in conclusion'],
    trap='การ preview ใช้เวลา 1–2 นาทีเท่านั้น ถ้าอ่านละเอียดตั้งแต่แรกจะเสียเวลา',
    drill='ก่อนเปิดคำถาม W02 ให้เขียนคาดเดาโครงเรื่อง 1 บรรทัด แล้วเทียบหลังทำเสร็จ')
RL['L_SCAN'] = dict(
    title='Scanning — หาข้อมูลเฉพาะอย่างรวดเร็ว',
    steps=['ขีดเส้นใต้ “คำค้น” ในคำถาม: ตัวเลข ปี ชื่อคน/สถานที่ คำที่ขึ้นต้นด้วยตัวใหญ่',
           'กวาดสายตาหา “รูปร่าง” ของคำค้น (ตัวเลข, ตัวพิมพ์ใหญ่) ไม่ต้องอ่านทุกคำ',
           'เมื่อเจอแล้ว อ่านประโยครอบ ๆ 1–2 ประโยคเพื่อยืนยัน',
           'ระวังคำถามที่ใช้คำพ้องความหมาย (paraphrase) แทนคำในบทความ เช่น “rose” = “increased”'],
    signals=['numbers', 'dates', 'names', 'percent', 'between … and …'],
    trap='ตัวเลขหลายตัวในย่อหน้าเดียว — ตรวจว่าเป็นตัวเลข “ของอะไร” “ปีไหน” ให้ตรงคำถาม',
    drill='W03: จับเวลา 10 นาที ข้อไหนเจอคำตอบไม่ถึง 30 วินาทีให้ทำเครื่องหมาย ✓')
RL['L_ERRORS'] = dict(
    title='วิเคราะห์ข้อผิดอย่างเป็นระบบ',
    steps=['เปิดหน้า “สถิติ” ดูความแม่นยำแยกทักษะจาก Test 1 และ W01–W03',
           'จัดข้อผิดเป็น 3 แบบ: (1) ไม่รู้ศัพท์ (2) หาหลักฐานไม่เจอ/หมดเวลา (3) ตีความผิด/เดาเกิน',
           'แบบ (1) → เพิ่มศัพท์ลง flashcards / แบบ (2) → ฝึก skimming–scanning / แบบ (3) → ฝึก inference + ตัดตัวเลือก',
           'วันนี้ทำ W04 แบบผสมทุกทักษะ แล้วจดว่าข้อผิดเป็นแบบไหน'],
    trap='อย่าดูแค่คะแนนรวม — คะแนนแยกทักษะบอกว่าต้องฝึกอะไรต่อ',
    drill='หลังส่ง W04 ให้บันทึกประเภทข้อผิดในสมุดข้อผิดพลาด')
RL['L_TOPIC_MAIN'] = dict(
    title='Topic vs Main idea',
    steps=['Topic = “เรื่องอะไร” ตอบได้ด้วยคำนามวลี เช่น “teenage sleep”',
           'Main idea = “ผู้เขียนพูดอะไรเกี่ยวกับ topic” เป็นประโยคเต็ม เช่น “Teenagers who sleep less perform worse at school.”',
           'หา main idea: ดู topic sentence (มักเป็นประโยคแรก) แต่ถ้ามี However/But ต่อมา ประเด็นหลักมักอยู่หลังคำนั้น',
           'ตรวจตัวเลือก: กว้างเกิน (พูดถึงเรื่องทั้งโลก) / แคบเกิน (แค่รายละเอียดเดียว) / ไม่มีในบทความ → ตัดทิ้ง'],
    signals=['however', 'but', 'in fact', 'the main reason', 'overall'],
    trap='ตัวเลือกที่ “จริงตามบทความ” อาจไม่ใช่ main idea ถ้ามันเป็นแค่ตัวอย่างหรือรายละเอียด',
    drill='ก่อนตอบ W05 เขียน main idea แต่ละย่อหน้าเป็นภาษาไทยสั้น ๆ 1 บรรทัด')
RL['L_IMPLIED'] = dict(
    title='Implied main idea & Best title',
    steps=['ถ้าย่อหน้าไม่มี topic sentence ให้รวมรายละเอียดทุกประโยคแล้วถามว่า “ทั้งหมดนี้ชี้ไปที่อะไร”',
           'Best title ต้องครอบคลุมทั้งบทความ ไม่ใช่แค่ย่อหน้าเดียว และไม่กว้างจนพูดถึงเรื่องอื่น',
           'ทดสอบตัวเลือกชื่อเรื่อง: ถ้าใช้เป็นชื่อบทความนี้ ผู้อ่านจะคาดหวังเนื้อหาตรงกับที่อ่านไหม'],
    signals=['all of these', 'together', 'this suggests', 'in short'],
    trap='ชื่อเรื่องที่มีคำตรงกับบทความมากที่สุด “ไม่จำเป็น” ต้องถูก (word-match trap)',
    drill='W06: เขียนชื่อเรื่องของตัวเองก่อนดูตัวเลือก + ทำ Heading “Onyx” ในหนังสือ')
RL['L_DETAILS'] = dict(
    title='Supporting details — หลัก vs รอง',
    steps=['Major detail = สนับสนุน main idea โดยตรง (เหตุผล/ขั้นตอน/ผลลัพธ์)',
           'Minor detail = ขยาย major detail (ตัวอย่าง ตัวเลข ชื่อ)',
           'ดูคำสัญญาณ: for example / such as (ตัวอย่าง) — in addition / also (เพิ่ม) — as a result / therefore (ผล)',
           'คำถาม “NOT mentioned” ให้ตรวจทีละตัวเลือก ตัวที่หาไม่เจอในบทความคือคำตอบ'],
    signals=['for example', 'such as', 'in addition', 'furthermore', 'as a result', 'first / second / finally'],
    trap='ตัวเลือกที่ใช้คำจากบทความแต่ “สลับเหตุ–ผล” เป็นกับดักที่พบบ่อย',
    drill='W07: วงกลมคำสัญญาณทุกคำ แล้วตอบว่าแต่ละรายละเอียดสนับสนุนประเด็นไหน')
RL['L_REFERENCE'] = dict(
    title='Reference words — คำนี้หมายถึงอะไร',
    steps=['ย้อนกลับไปหาคำนามที่อยู่ก่อนหน้า (มักอยู่ในประโยคเดียวกันหรือประโยคก่อนหน้า)',
           'เช็กจำนวน: it/this = เอกพจน์, they/these/those = พหูพจน์',
           'this/such/which อาจหมายถึง “ทั้งความคิด/ประโยคก่อนหน้า” ไม่ใช่คำเดียว',
           'ทดสอบ: แทนคำตอบลงในประโยค ถ้าความหมายลงตัว = ถูก'],
    signals=['it', 'they', 'this', 'these', 'which', 'such', 'the former', 'the latter', 'one / ones'],
    trap='คำนามที่อยู่ “ใกล้ที่สุด” ไม่จำเป็นต้องเป็นคำตอบ — ตรวจความหมายด้วย',
    drill='W08: ทุกข้อ reference ให้เขียนประโยคใหม่โดยแทนคำตอบ แล้วอ่านดูว่าลื่นไหม')
RL['L_CONTEXT'] = dict(
    title='Context clues — เดาความหมายจากบริบท',
    steps=['Definition: ประโยคให้คำนิยามตรง ๆ (is defined as, refers to, means, เครื่องหมาย — หรือ ( ))',
           'Synonym/restatement: or, that is, in other words',
           'Antonym/contrast: but, however, unlike, whereas — คำศัพท์มีความหมายตรงข้ามกับอีกส่วน',
           'Example: such as, including — ดูตัวอย่างแล้วสรุปความหมาย',
           'Word parts: un-/in-/dis- (ไม่), re- (อีก), -ive/-al (adj), -tion/-ment (noun)'],
    signals=['refers to', 'that is', 'in other words', 'unlike', 'such as'],
    trap='เลือกความหมายที่ “ถูกในพจนานุกรม” แต่ไม่เข้ากับบริบทประโยคนั้น — ต้องแทนลงประโยคทุกครั้ง',
    drill='W09: ก่อนดูตัวเลือก ให้เขียนความหมายที่เดาเป็นภาษาไทยก่อน')
RL['L_SKIM'] = dict(
    title='Skimming & Paragraph function',
    steps=['Skim 2–3 นาที: ชื่อเรื่อง + ประโยคแรก/สุดท้ายของแต่ละย่อหน้า',
           'ตั้งชื่อหน้าที่ของแต่ละย่อหน้า: introduce problem / give example / explain cause / present solution / contrast view / conclude',
           'คำถาม “Which paragraph…” ให้ใช้ป้ายหน้าที่ที่จดไว้แทนการอ่านใหม่',
           'โครงบทความที่พบบ่อย: problem–solution, cause–effect, compare–contrast, chronological'],
    signals=['one solution', 'another reason', 'in contrast', 'this has led to', 'finally'],
    trap='ย่อหน้าที่มีตัวเลขเยอะไม่จำเป็นต้องเป็น “ข้อมูลหลัก” อาจเป็นแค่ตัวอย่าง',
    drill='W10: จดป้ายหน้าที่ย่อหน้า ¶1–¶7 ก่อนเปิดคำถาม + ทำ TFNG “Mars”, “Taste” ในหนังสือ')
RL['L_SHORTANS'] = dict(
    title='Short answer (ไม่เกิน 3 คำ)',
    steps=['อ่านคำสั่ง: “NO MORE THAN THREE WORDS” = เขียนได้ 1–3 คำ ใช้คำจากบทความ',
           'หาคำค้นในคำถาม → scan → คัดลอกคำจากบทความ “ตามตัวสะกด”',
           'ตรวจไวยากรณ์ของคำตอบให้เข้ากับคำถาม (เอกพจน์/พหูพจน์, a/the)',
           'ในแอปนี้ระบบตรวจคำตอบที่ใกล้เคียง ถ้าขึ้นว่าผิดแต่ความหมายเท่ากัน ให้กด “นับว่าถูก” และจดไว้'],
    signals=['numbers', 'names', 'terms in quotation marks', 'called', 'known as'],
    trap='เขียนเกินจำนวนคำ หรือเขียนคำของตัวเองที่ไม่อยู่ในบทความ = ผิดในข้อสอบจริง',
    drill='W11: ทุกข้อ short answer นับคำก่อนส่ง + ทำ NMT3W ในหนังสือหน้า 232–236')
RL['L_INFER'] = dict(
    title='Inference, Purpose & Tone',
    steps=['Inference = สิ่งที่ “ต้องจริง” จากข้อความ แม้ไม่ได้เขียนตรง ๆ — หาประโยคหลักฐานก่อนทุกครั้ง',
           'Purpose: ถามว่า “ผู้เขียนใส่ประโยค/ตัวอย่างนี้ไว้เพื่ออะไร” (to illustrate / to contrast / to support / to warn)',
           'Tone: ดูคำคุณศัพท์/กริยาวิเศษณ์ที่แสดงความรู้สึก เช่น promising (บวก), concerning (กังวล), cautiously (ระมัดระวัง)',
           'ตัดตัวเลือกที่ใช้คำแรงเกินบทความ: always, all, never, only, completely'],
    signals=['suggests', 'implies', 'may', 'appears', 'unfortunately', 'promising', 'however'],
    trap='ตัวเลือกที่ “น่าจะจริงในโลกจริง” แต่บทความไม่ได้สนับสนุน = ผิด',
    drill='W12: เขียนเลข ¶ ของหลักฐานข้างคำตอบ inference ทุกข้อ + ทำ MC ในหนังสือหน้า 242–246')
RL['L_FACTOP'] = dict(
    title='Fact vs Opinion + มุมมองผู้เขียน',
    steps=['Fact = ตรวจสอบได้ (ตัวเลข เหตุการณ์ ผลการศึกษา)',
           'Opinion = ความเห็น/การประเมิน มีคำว่า should, must, I believe, arguably, best, worst, unfortunately',
           'คำถาม “The writer would most likely agree…” ให้ดูประโยคที่แสดงจุดยืนของผู้เขียน (มักอยู่ย่อหน้าแรก/สุดท้าย)',
           'แยก “ความเห็นของคนที่ถูกอ้างถึง” ออกจาก “ความเห็นของผู้เขียน”'],
    signals=['should', 'I believe', 'arguably', 'clearly', 'critics claim', 'supporters argue'],
    trap='ประโยคที่มีตัวเลขก็อาจเป็น opinion ได้ ถ้ามีการประเมิน เช่น “an alarming 40%”',
    drill='W13: ติดป้าย F/O ให้ทุกประโยคในย่อหน้า 2 ก่อนตอบ')
RL['L_RESEARCH'] = dict(
    title='อ่านบทความวิจัย (Background–Methods–Results–Discussion)',
    steps=['Background: ปัญหาและช่องว่างความรู้ → ตอบคำถาม “ทำไมต้องศึกษา”',
           'Methods: ใคร (sample) กี่คน ที่ไหน รูปแบบ (RCT, cohort, cross-sectional) วัดอะไร',
           'Results: ตัวเลขหลัก เปรียบเทียบกลุ่ม (significant / not significant)',
           'Discussion/Limitations: ผู้เขียนตีความอย่างไร และยอมรับข้อจำกัดอะไร',
           'คำถามแบบ short answer มักถามจำนวนผู้เข้าร่วม ระยะเวลา ชื่อเครื่องมือ'],
    signals=['aimed to', 'participants', 'randomly assigned', 'compared with', 'significantly', 'limitation'],
    trap='อย่าสับสน “ผลที่พบ” (results) กับ “ข้อเสนอแนะ” (implications)',
    drill='W14: ระบุส่วน Background/Methods/Results/Discussion ก่อนตอบ แล้วเขียน summary 60–80 คำ')
RL['L_MIX_MAIN'] = dict(
    title='ฝึกผสม: Main idea ให้เร็ว (≤ 30 วินาที/ย่อหน้า)',
    steps=['ทำ W15 ใน 20 นาที แล้วทำ Passage 1 ในหนังสือ (20 นาที)',
           'ใช้เทคนิค Heading: อ่านประโยคแรก + ประโยคหลัง however แล้วตัดสินทันที',
           'คำถาม TFNG ในหนังสือ: T = ตรงความหมาย 100%, F = ขัดแย้ง, NG = ไม่มีข้อมูล'],
    trap='Heading list ในหนังสือมีตัวเลือกเกิน ห้ามใช้ซ้ำ',
    drill='จับเวลาแยก 2 ช่วง: แอป 20 นาที + หนังสือ 20 นาที')
RL['L_MIX_VOCAB'] = dict(
    title='ฝึกผสม: Vocabulary in context',
    steps=['ทำ W16 (20 นาที) + Passage 2 ในหนังสือ (20 นาที)',
           'ข้อศัพท์: เดาความหมายจาก clue ก่อนดูตัวเลือก แล้วแทนลงประโยค',
           'ตาราง (table completion) ในหนังสือ: ดูหัวตารางเพื่อรู้ชนิดคำที่ต้องเติม'],
    trap='ตัวเลือกที่เป็น “อีกความหมายหนึ่ง” ของคำเดียวกันเป็นกับดักบ่อย',
    drill='จดศัพท์ใหม่จาก Passage 2 อย่างน้อย 5 คำลงสมุด')
RL['L_MIX_INFER'] = dict(
    title='ฝึกผสม: Inference ภายใต้เวลา',
    steps=['ทำ W17 (20 นาที) + Passage 3 ในหนังสือ (20 นาที)',
           'ข้อ inference: หาประโยคหลักฐาน 1 ประโยค แล้วเลือกตัวเลือกที่ “ห่างจากหลักฐานน้อยที่สุด”',
           'Summary completion ในหนังสือ: หาจุดเริ่มต้นของ summary ในบทความก่อน'],
    trap='ข้อที่ไม่แน่ใจ อย่าใช้เวลาเกิน 90 วินาที — ทำเครื่องหมายแล้วกลับมาทีหลัง',
    drill='ตรวจคำตอบหนังสือกับเฉลยหน้า 257 และจดเหตุผลที่ผิด')
RL['L_MIX_REF'] = dict(
    title='ฝึกผสม: Reference + ทบทวนศัพท์จาก Mock หนังสือ',
    steps=['ทำ W18 (25 นาที) โดยเน้นข้อ reference และ detail',
           'ใช้เวลาที่เหลือ 15 นาที อ่านคำแปล Mock ในหนังสือ (หน้า 257–260) เฉพาะย่อหน้าที่ตอบผิด'],
    trap='this/these มักชี้ไปที่ “ความคิดทั้งประโยค” ก่อนหน้า',
    drill='จดคู่ “ประโยคอังกฤษ ↔ คำแปล” ที่ทำให้เข้าใจผิด 3 คู่')
RL['L_LONG'] = dict(
    title='บทความยาว: วางแผนก่อนลงมือ',
    steps=['Skim 3 นาที จดป้ายหน้าที่ย่อหน้า', 'ตอบคำถามตามลำดับย่อหน้า (คำถามมักเรียงตามบทความ)',
           'Short answer ทำทันทีเมื่ออ่านถึงย่อหน้านั้น', 'ข้อ main idea/title ทำท้ายสุด'],
    trap='บทความยาวทำให้ลืมว่าข้อมูลอยู่ไหน — ป้ายย่อหน้าช่วยได้มาก',
    drill='W19: จับเวลา 25 นาที')
RL['L_NOT'] = dict(
    title='คำถาม NOT / EXCEPT / LEAST',
    steps=['ขีดเส้นใต้ NOT/EXCEPT ในคำถามทุกครั้ง', 'ตรวจทีละตัวเลือก: เจอในบทความ = ✗ ตัดทิ้ง', 'ตัวเลือกสุดท้ายที่หาไม่เจอหรือขัดแย้ง = คำตอบ'],
    trap='อ่านคำถามเร็วแล้วเลือกตัวที่ “ถูกตามบทความ” — ซึ่งเป็นคำตอบที่ผิดในข้อ NOT',
    drill='W20: ข้อ NOT ให้เขียน ¶ ของตัวเลือกที่เจอทั้ง 3 ตัว')
RL['L_PURPOSE'] = dict(
    title='Purpose & Organisation',
    steps=['คำถาม “Why does the author mention X?” → X เป็นตัวอย่าง/หลักฐาน/การเปรียบเทียบของประเด็นไหน',
           'คำถามโครงสร้าง: problem→solution / cause→effect / chronological / comparison',
           'ใช้ป้ายหน้าที่ย่อหน้าที่ skim ไว้'],
    signals=['to illustrate', 'to emphasise', 'to contrast', 'to explain why'],
    trap='ตอบเนื้อหาของ X แทนที่จะตอบ “เหตุผลที่ผู้เขียนพูดถึง X”',
    drill='W21: จด purpose ของทุกย่อหน้า')
RL['L_TONE'] = dict(
    title='Tone & Attitude',
    steps=['หา adjectives/adverbs ที่แสดงการประเมิน (promising, troubling, cautiously, encouraging)',
           'แยกน้ำเสียง: positive / negative / neutral / cautious / critical / optimistic',
           'ดูประโยคสรุปของผู้เขียน (ย่อหน้าสุดท้าย) มักบอกทัศนคติชัดที่สุด'],
    signals=['promising', 'worrying', 'remarkable', 'questionable', 'cautiously optimistic'],
    trap='ตัวเลือกที่สุดโต่ง (furious, enthusiastic) มักผิดในบทความวิชาการ ซึ่งใช้น้ำเสียงพอประมาณ',
    drill='W22: ขีดเส้นใต้คำแสดงทัศนคติทุกคำ')
RL['L_PARA'] = dict(
    title='Paraphrase matching',
    steps=['คำถามส่วนใหญ่ “ไม่ใช้คำเดียวกับบทความ” — หาคำพ้องความหมายหรือโครงสร้างที่เปลี่ยน',
           'ตัวอย่าง: “rose sharply” = “increased considerably”; “a lack of” = “insufficient”',
           'ระวังคำที่ตรงกันเป๊ะแต่ความหมายต่าง (word-match trap)'],
    trap='เลือกตัวเลือกเพราะเห็นคำเดียวกับบทความ โดยไม่ตรวจความหมายทั้งประโยค',
    drill='W23: เขียนคู่ paraphrase (คำถาม ↔ บทความ) ของ 3 ข้อ')
RL['L_LONGTIME'] = dict(
    title='บทความยาว + บริหารเวลา 30 นาที',
    steps=['0–3 นาที skim + ป้ายย่อหน้า', '3–25 นาที ตอบตามลำดับ (short answer ทำทันที)', '25–30 นาที ข้อที่ข้ามไว้ + ตรวจการสะกด'],
    trap='ติดข้อเดียวนานเกิน 2 นาที = เสียเวลาข้ออื่น',
    drill='W24: จับเวลา 30 นาทีเหมือนจริง')
RL['L_TIMED'] = dict(
    title='จับเวลาแบบวันสอบ',
    steps=['บทสั้น: 12 นาที/บท (อ่าน 4 + ตอบ 7 + ตรวจ 1)', 'บทยาว: 30 นาที/บท', 'ข้อยาก: ทำเครื่องหมาย ข้ามไปก่อน กลับมาทีหลัง',
           'ห้ามเว้นว่าง — ถ้าไม่รู้ให้ตัดตัวเลือกแล้วเดาอย่างมีเหตุผล (ตรวจกติกาการให้คะแนนของสนามสอบ)'],
    trap='ใช้เวลาเกินกับบทแรก ทำให้บทยาวท้าย ๆ ไม่ทัน',
    drill='เปิด timer ในแอปทุกครั้ง และจดเวลาจริงลงสมุดข้อผิดพลาด')
RL['L_LIGHT'] = dict(
    title='อ่านเบา ๆ เพื่อความมั่นใจ',
    steps=['อ่าน passage สั้น 1 บท ไม่จับเวลา', 'ทวนลำดับขั้น: คำถาม → skim → scan → หลักฐาน', 'จบแล้วพัก ไม่ทำข้อสอบเพิ่ม'],
    trap='อย่าทำ Mock เพิ่มในวันนี้ ความเหนื่อยจะส่งผลต่อวันสอบ',
    drill='W31: ทำแบบสบาย ๆ')
RL['L_TEST'] = dict(
    title='กลยุทธ์ทำข้อสอบเต็ม 120 นาที',
    steps=['ก่อนเริ่ม: ดูภาพรวมทั้ง 6 passages 1 นาที', 'Passage 1–4 (สั้น): ไม่เกิน 12 นาที/บท รวม ≈ 45 นาที',
           'Passage 5–6 (ยาว): ไม่เกิน 30 นาที/บท รวม ≈ 60 นาที', 'เหลือ 10–15 นาทีกลับไปข้อที่ทำเครื่องหมาย ⚑',
           'ใช้แถบหมายเลขข้อเพื่อดูว่าข้อไหนยังไม่ตอบ ก่อนกดส่ง'],
    trap='ห้ามเปิดเฉลยระหว่างทำ เวลาเดินต่อแม้ปิดไฟล์ (ระบบจำเวลาสิ้นสุด)',
    drill='หลังส่ง: ดูผลแยก passage + แยกทักษะ แล้วจดลงสมุดข้อผิดพลาด')

# Small model answers for tasks without an essay-bank entry
MODELS_SMALL = {
    'SMART': {
        'title': 'ย่อหน้าตัวอย่าง: Smartphones should be banned in classrooms (Agree, ใช้ hedging)',
        'paras': ['Smartphones tend to be a significant source of distraction in classrooms, which is why I believe they should be banned during lessons. When phones are within reach, students are likely to check notifications even if they do not intend to, and each interruption may reduce their ability to follow complex explanations. Evidence from classroom observations suggests that students who keep their phones on their desks often recall less of a lecture than those who leave them in their bags. Although phones can occasionally support learning, teachers can provide the same resources through shared computers or printed materials. A clear ban would therefore help most students concentrate more effectively.'],
        'notes': ['tend to / are likely to / may / suggests / often = hedging ทำให้ข้ออ้างไม่ฟันธงเกินหลักฐาน',
                  'Although … , … = concession + rebuttal ภายในย่อหน้า โดยไม่เปลี่ยนจุดยืน'],
    },
    'CONCEDE': {
        'title': 'ประโยคตัวอย่าง concession + rebuttal',
        'paras': ['R5 (Disagree): Although online courses offer flexibility, they cannot fully replace the immediate feedback and peer interaction that face-to-face classes provide.',
                  'R7 (Disagree): Admittedly, a high salary provides financial security; however, it rarely compensates for the stress of doing work that one finds meaningless.',
                  'R13 (Disagree): It is true that a single entrance examination puts heavy pressure on students, but abolishing it would remove the most transparent way to compare applicants from different schools.',
                  'R16 (Disagree): While some tasks require quiet concentration, most complex problems today are solved more effectively by teams that combine different skills.'],
        'notes': ['โครง: Although / Admittedly / It is true that / While + ข้อดีของอีกฝ่าย → but / however / this overlooks + เหตุผลของเรา',
                  'ประโยคแบบนี้ใช้ได้ 1 ครั้งในย่อหน้า Body เพื่อแสดงความคิดรอบด้าน แต่จุดยืนทั้ง essay ต้องไม่เปลี่ยน'],
    },
}

BLOCK_INFO = {
    'vocab': ('คำศัพท์', 'อ่านคำ + ความหมาย + ตัวอย่าง → ปิดความหมายแล้วทวน → ทำ Quiz 20 ข้อ → ติดดาวคำที่ยังจำไม่ได้'),
    'reading': ('Reading', 'อ่านบทเรียนทักษะ → ทำ passage ในแอป (และหนังสือถ้ามี) → ส่ง → อ่านคำอธิบายทุกข้อที่ผิด'),
    'writing': ('Writing / Grammar', 'อ่านบทเรียน grammar → ทำ Quiz → ทำงานเขียนของวัน → ตรวจด้วย checklist → ดูตัวอย่าง'),
    'errors': ('สมุดข้อผิดพลาด', 'ทบทวนข้อที่ผิดวันนี้ (ระบบรวบรวมให้) + จดสิ่งที่เรียนรู้ 1–3 บรรทัด'),
    'test': ('Reading Test 120 นาที', 'ทำข้อสอบเต็ม 6 passages / 69 ข้อ จับเวลาต่อเนื่อง ห้ามดูเฉลยระหว่างทำ'),
    'review': ('ตรวจผล + จดข้อผิด', 'อ่านคำอธิบายทุกข้อที่ผิด ดูผลแยกทักษะ จดลงสมุดข้อผิดพลาด'),
    'essay': ('Writing 60 นาที', 'วางแผน 10 นาที → เขียน 40 นาที → ตรวจ 10 นาที (Checklist) แล้วจึงดูตัวอย่าง'),
    'weekly': ('ทบทวนข้อผิดของสัปดาห์', 'ทำซ้ำข้อที่ผิดในสัปดาห์นี้ (ระบบรวบรวมให้อัตโนมัติ)'),
    'vocabreview': ('ทวนศัพท์', 'Quiz ทบทวนจากศัพท์ที่เรียนไปแล้ว (เน้นคำที่ติดดาว)'),
    'retry': ('ทำข้อที่เคยผิดซ้ำ', 'ทำซ้ำข้อที่ยังไม่ถูกจาก Test/Mock ทั้งหมด'),
}

GUIDE = {}
GUIDE['exam'] = dict(title='ข้อมูลข้อสอบ KKU-AELT', blocks=[
    {'h': 'โครงสร้างการสอบ (PBT)', 'list': [
        'สอบรวม 3 ชั่วโมง: Part I Reading 2 ชั่วโมง + Part II Writing 1 ชั่วโมง (ปฏิทิน PBT 2569 ของศูนย์ CELEx)',
        'ต้องทำ Reading ก่อน เมื่อถึง 11.00 น. จึงทำส่วน Writing ได้ (ปฏิทิน PBT 2569)',
        'Reading: Passage 1–6 รวม 69 ข้อ — Passage 1–4 ข้อความสั้น/ข่าว ตัวเลือก 4 ข้อ; Passage 5–6 บทความยาว มีทั้งตัวเลือกและ short answer (คู่มือการสอบ Online ปี 2564)',
        'Writing: โจทย์ข้อเดียวสั้น ๆ ถามความเห็นต่อประเด็นที่กำหนด เขียน essay อย่างน้อย 250 คำ (คู่มือการสอบ Online ปี 2564)',
        'เกณฑ์ผ่านระบบ 7 ระดับ: ปริญญาโท ระดับ 4 ขึ้นไป / ปริญญาเอก ระดับ 5 ขึ้นไป (คะแนนรวมทักษะการอ่านและการเขียน)',
        'ค่าสมัคร 600 บาท สมัครและพิมพ์ใบชำระเงินออนไลน์ ชำระที่ธนาคารไทยพาณิชย์',
    ]},
    {'h': '⚠ ตรวจวันสอบของคุณ', 'p': 'แผนนี้ตั้งวันสอบเป้าหมายเป็นเสาร์ 21 พ.ย. 2569 ตามที่คุณกำหนด แต่ปฏิทิน PBT 2569 ของศูนย์ฯ ระบุรอบเดือนพฤศจิกายนเป็น “เสาร์ 14 พ.ย. 2569” (รับสมัคร 21–31 ต.ค. 2569, ประกาศผล 26 พ.ย.) และรอบถัดไป “เสาร์ 12 ธ.ค. 2569” (รับสมัคร 20–30 พ.ย.) โปรดตรวจวันสอบในหลักฐานการสมัครของคุณ ถ้าสอบ 14 พ.ย. ให้ใช้ “แผนย่อสำหรับสอบ 14 พ.ย.” ด้านล่าง'},
    {'h': 'แผนย่อ ถ้าวันสอบจริงคือ 14 พ.ย.', 'list': [
        'ทำ Day 1–31 ตามปกติ (10 ต.ค.–9 พ.ย.)',
        '10 พ.ย. (อ.) → ทำ Day 38 Full Mock 1 แทน Day 32',
        '11 พ.ย. (พ.) → ทำ Day 39 Full Mock 2 แทน Day 33',
        '12 พ.ย. (พฤ.) → ทำ Day 41 Error Review',
        '13 พ.ย. (ศ.) → ทำ Day 42 Light Review แล้วพัก',
        '14 พ.ย. (ส.) → วันสอบ (Day 32–37, 40 และ Test 6 ใช้ทบทวนต่อได้หากสอบรอบ 12 ธ.ค.)',
    ]},
    {'h': 'สิ่งที่แผนนี้ไม่ได้อ้าง', 'list': [
        'ข้อสอบในแอปแต่งขึ้นใหม่เพื่อการฝึก ไม่ใช่ข้อสอบจริงหรือข้อสอบที่ศูนย์ฯ รับรอง ชื่อบุคคล ตัวเลข และโครงการเฉพาะในบทอ่านเป็นสถานการณ์สมมติ',
        'การแบ่งข้อ 8/8/9/10/17/17 ต่อ passage และ short answer ไม่เกิน 3 คำ เป็นการออกแบบแบบฝึกตามโครง 6 passages/69 ข้อ ไม่ได้อ้างว่าทุกรอบเหมือนกัน',
        'คะแนนร้อยละในแอปใช้ติดตามพัฒนาการ ไม่สามารถแปลงเป็น band ทางการได้',
    ]},
])
GUIDE['reading'] = dict(title='กลยุทธ์ Reading', blocks=[
    {'h': 'ลำดับขั้นทุก passage', 'list': ['อ่านคำถาม (ไม่ต้องอ่านตัวเลือก) 30–60 วินาที', 'Skim: ชื่อเรื่อง + ประโยคแรกแต่ละย่อหน้า', 'Scan หาคำค้นของแต่ละข้อ', 'ยืนยันด้วยประโยคหลักฐาน → เลือก/เขียนคำตอบ', 'ข้อยากทำเครื่องหมาย ⚑ แล้วไปต่อ']},
    {'h': 'แผนเวลา 120 นาที', 'table': [['ส่วน', 'เวลา', 'หมายเหตุ'], ['Passage 1–4 (สั้น)', '10–12 นาที/บท', 'รวม ≈ 45 นาที'], ['Passage 5–6 (ยาว)', '≈ 30 นาที/บท', 'short answer ทำทันทีที่อ่านถึง'], ['ตรวจ/ข้อที่ข้าม', '10–15 นาที', 'ห้ามเว้นว่าง']]},
    {'h': 'ประเภทคำถามและวิธีคิด', 'table': [['ประเภท', 'สัญญาณในคำถาม', 'วิธีคิด'],
        ['Main idea / Title', 'main idea, best title, mainly about', 'ครอบคลุมทั้งเรื่อง ไม่กว้าง/แคบเกิน'],
        ['Detail', 'According to the passage', 'scan คำค้น → ประโยคหลักฐาน'],
        ['NOT / EXCEPT', 'NOT mentioned, EXCEPT', 'ตัดตัวที่เจอในบทความ'],
        ['Reference', 'What does “it” refer to', 'ย้อนหาคำนาม + แทนค่า'],
        ['Vocabulary', 'closest in meaning to', 'clue รอบคำ + แทนค่า'],
        ['Inference', 'It can be inferred / suggests', 'ต้องจริงจากหลักฐาน ไม่เดาเกิน'],
        ['Purpose', 'Why does the author mention', 'หน้าที่ของ X ในย่อหน้า'],
        ['Tone', 'attitude, tone', 'คำคุณศัพท์/กริยาวิเศษณ์ประเมินค่า'],
        ['Short answer', 'NO MORE THAN THREE WORDS', 'คัดคำจากบทความ สะกดถูก นับคำ']]},
])
GUIDE['essay'] = dict(title='โครง Essay + Template', blocks=[
    {'h': 'โครง 4 ย่อหน้า (จาก Opinion_Essay_Guide.docx)', 'table': [['ย่อหน้า', 'ความยาว', 'เนื้อหา'],
        ['1 Introduction', '2–3 ประโยค (≈50 คำ)', 'Paraphrase โจทย์ + Thesis: I strongly agree/disagree that … because …'],
        ['2 Body 1', '5–7 ประโยค', 'Topic sentence (เหตุผล 1) → อธิบาย → ตัวอย่าง (For instance, …) → เชื่อมกลับจุดยืน'],
        ['3 Body 2', '5–7 ประโยค', 'Furthermore/Moreover + เหตุผล 2 คนละมุม → อธิบาย → ตัวอย่าง (+ Additionally, เหตุผลสั้นข้อ 3)'],
        ['4 Conclusion', '2–3 ประโยค', 'In conclusion, + สรุปเหตุผล 2 ข้อ + ย้ำจุดยืนด้วยคำใหม่ (ไม่เพิ่มเหตุผลใหม่)']]},
    {'h': 'แผนเวลา Writing 60 นาที', 'list': ['0–10 นาที: อ่านโจทย์ ขีดเส้นใต้คำสำคัญ เลือกจุดยืน brainstorm เหตุผล 2 ข้อ + ตัวอย่าง', '10–50 นาที: เขียน 4 ย่อหน้า (บทนำ 5 นาที / body ละ 15 นาที / สรุป 5 นาที)', '50–60 นาที: นับคำ (≥ 250) + ตรวจ Checklist 10 ข้อ']},
    {'h': 'Template (ปรับคำให้เข้ากับโจทย์ — อย่าท่องทั้งก้อน)', 'list': [
        'Intro: It is often argued that [paraphrase]. I strongly [agree/disagree] with this view because [reason 1] and [reason 2].',
        'Body 1: First and foremost, [reason 1]. This is because … For instance, … Therefore, …',
        'Body 2: Furthermore, [reason 2]. … To illustrate, … As a result, …',
        'Concession (ถ้าจำเป็น): Admittedly, …; however, …',
        'Conclusion: In conclusion, [restate stance in new words] since [reason 1] and [reason 2]. I therefore firmly believe that …']},
    {'h': 'ห้ามใช้', 'list': ['คำย่อ (don’t → do not), ภาษาพูด, อีโมจิ, คำถามในบทความ', 'ประโยคเปิดที่ไม่เกี่ยว: “The world is gradually changing.”', '“This essay will focus on two reasons as follows …” (เสียคำโดยไม่ได้เนื้อหา)', 'ประโยคขึ้นต้นด้วย Because … ที่ไม่มีประโยคหลัก (fragment)', 'สลับจุดยืนไปมา (เห็นด้วยบ้างไม่เห็นด้วยบ้าง)']},
])
GUIDE['connectors'] = dict(title='คำเชื่อม (All that IELTS หน้า 28–30)', blocks=[
    {'h': 'เลือกจำ 2 คำต่อหน้าที่', 'table': [['หน้าที่', 'คำเชื่อม'],
        ['เพิ่มเติม', 'Furthermore, / Moreover, / In addition, / Another key point is that'],
        ['ขัดแย้ง', 'However, / Nevertheless, / In contrast, / On the other hand,'],
        ['ยอมรับ (concession)', 'Although S V / Even though S V / Despite N / In spite of N'],
        ['เหตุผล', 'because S V / because of N / due to N / as S V'],
        ['ผลลัพธ์', 'Therefore, / As a result, / Consequently, / Hence, / As such,'],
        ['ตัวอย่าง', 'For example, / For instance, / To illustrate, / such as N'],
        ['ขยายความ', 'In other words, / That is, / In fact, / Indeed,'],
        ['สรุป', 'In conclusion, / To sum up, / Overall, / On balance,']]},
])
GUIDE['checklist'] = dict(title='Checklist 10 ข้อ (All that IELTS หน้า 68–69, 380–383)', blocks=[
    {'h': 'ตรวจก่อนส่งทุกครั้ง', 'list': ['Tense ถูกต้องหรือไม่ (ตัวอย่างอดีตใช้ past)', 'ใช้กริยาโดยเฉพาะ “be” ซ้ำ หรือกริยาตกหรือไม่', 'Article นำหน้านามถูกต้องหรือไม่ (รวมเอกพจน์/พหูพจน์)', 'ประธานกับกริยาเข้ากันหรือไม่ (เติม s บุรุษที่ 3)', 'Preposition ถูกต้องหรือไม่', 'สกรรมกริยา/อกรรมกริยาสลับกันหรือไม่ (increase ไม่ใช้ was increased)', 'Active และ Passive ถูกหรือไม่ (children are allowed to …)', 'คำเชื่อมเหมาะสมหรือไม่', 'การสะกดคำและตัวพิมพ์ใหญ่–เล็ก', 'เครื่องหมายมหัพภาค (.) ครบทุกประโยค']},
    {'h': 'ตรวจโครง (เพิ่มเติมจากเอกสารของคุณ)', 'list': ['บทนำ paraphrase โจทย์ ไม่ลอก', 'จุดยืนชัดเจนและไม่เปลี่ยน', 'Body 2 เหตุผลคนละมุมกับ Body 1', 'ตัวอย่างเป็นรูปธรรม อธิบายว่า “ทำไม/ส่งผลอย่างไร”', 'บทสรุปไม่เพิ่มเหตุผลใหม่', 'จำนวนคำ ≥ 250 (เป้า 270–310)']},
])
GUIDE['examday'] = dict(title='Checklist วันสอบ', blocks=[
    {'h': 'คืนก่อนสอบ', 'list': ['ตรวจวัน/เวลา/สถานที่สอบในหลักฐานการสมัคร', 'เตรียมบัตรประชาชน/บัตรที่ใช้ยืนยันตัวตนตามประกาศของศูนย์ฯ', 'เตรียมอุปกรณ์ที่อนุญาต (ตรวจตามประกาศของสนามสอบ)', 'นอนให้พอ ไม่อ่านหนักหลัง 20.00 น.']},
    {'h': 'ระหว่างสอบ', 'list': ['Reading ก่อน: แผนเวลา 45 / 60 / 15 นาที', 'Writing: 10 วางแผน / 40 เขียน / 10 ตรวจ', 'เขียน ≥ 250 คำ นับคร่าว ๆ จากจำนวนบรรทัด', 'ใช้ Checklist 10 ข้อในการตรวจ 3–5 นาทีสุดท้าย']},
])
GUIDE['sources'] = dict(title='แหล่งข้อมูลที่ใช้', blocks=[
    {'h': 'เอกสารของคุณ (อยู่โฟลเดอร์เดียวกับไฟล์นี้)', 'list': [
        'All that IELTS คู่มือเตรียมสอบ IELTS ใหม่ล่าสุด (1).pdf — Writing Task 2 หน้า 21–132, Reading หน้า 206–260, ภาคผนวก หน้า 380–397 (เลขหน้าในแผนเป็นเลขหน้าที่พิมพ์ในหนังสือ; ลิงก์จะเปิด PDF หน้าที่ตรงกัน เพราะไฟล์สแกนมีหน้าซ้ำ: PDF = หน้า+2 สำหรับหน้า ≤ 67, +4 สำหรับหน้า 68–181, +6 ตั้งแต่หน้า 182)',
        'Aelt Writing 0421.pdf — หัวข้อ Writing ข้อสอบจริง (หน้า PDF 1–3; หน้า 4–8 ซ้ำกับหน้า 3)',
        'Image (1).pdf — ตัวอย่าง essay “Big salary…” 291 คำ (หน้า 2 ซ้ำหน้า 1)',
        'Opinion_Essay_Guide.docx — โครงสร้าง 4 ย่อหน้า ศัพท์ 50 คำ ตัวอย่าง 5 เรื่อง',
        'Improved_Opinion_Essays.docx — ต้นฉบับ vs ฉบับปรับปรุง 5 เรื่อง + บทวิเคราะห์']},
    {'h': 'แหล่งข้อมูลทางการ (ตรวจ 7 ต.ค. 2569)', 'links': [
        ['ปฏิทิน KKU-AELT PBT 2569 (CELEx)', 'https://kkuaelt.kku.ac.th/img/img/2569/Calendar/2026%20PBT%20calendar.pdf'],
        ['คู่มือการใช้งานระบบสอบ KKU-AELT แบบออนไลน์ (2564) — คำอธิบายข้อสอบหน้า 2', 'https://kkuaelt.kku.ac.th/img/img/2564/T-11-2021/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%83%E0%B8%8A%E0%B9%89%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B8%A3%E0%B8%B0%E0%B8%9A%E0%B8%9A%E0%B8%AA%E0%B8%AD%E0%B8%9A%E0%B9%81%E0%B8%A5%E0%B8%B0%E0%B8%82%E0%B9%89%E0%B8%AD%E0%B8%9B%E0%B8%8F%E0%B8%B4%E0%B8%9A%E0%B8%B1%E0%B8%95%E0%B8%B4%E0%B8%AA%E0%B9%8D%E0%B8%B2%E0%B8%AB%E0%B8%A3%E0%B8%B1%E0%B8%9A%E0%B8%9C%E0%B8%B9%E0%B9%89%E0%B9%80%E0%B8%82%E0%B9%89%E0%B8%B2%E0%B8%AA%E0%B8%AD%E0%B8%9A%20Online%20KKU-AELT..pdf']]},
])
