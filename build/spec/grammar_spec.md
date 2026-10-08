# Grammar & writing-skill mini-lessons + quizzes — KKU-AELT 45-day plan

Learner: Thai university lecturer preparing for KKU-AELT (Reading 2 h + Writing 1 h; writing = opinion essay ≥ 250 words).
Each set is the learner's "Writing/Grammar" block for one day: read a short Thai lesson, then answer a quiz in the app
(auto-scored, Thai explanation shown after submitting).

## Output format (strict JSON, UTF-8)
```json
{"sets": [
  {"id": "G02", "day": 2, "title_th": "โครงสร้างประโยค: Fragment และ Run-on",
   "title_en": "Sentence structure: fragments and run-ons",
   "book": "All that IELTS หน้า 33–35 (ไวยากรณ์ 5 ข้อที่ห้ามผิด)",
   "lesson": [
     {"h": "หลักสำคัญ", "p": "ภาษาไทย 2–4 ประโยค ..."},
     {"h": "ตัวอย่าง", "ex": [["✗ Because many students work part-time.", "✓ Because many students work part-time, they have less time to study."], ["✗ ...", "✓ ..."]]},
     {"h": "จุดที่คนไทยพลาดบ่อย", "list": ["...", "..."]},
     {"h": "สูตรจำ", "p": "..."}
   ],
   "quiz": [
     {"type": "mc", "q": "Choose the grammatically correct sentence.", "options": ["...", "...", "...", "..."], "answer": 2,
      "explain": "คำอธิบายภาษาไทยเฉพาะข้อนี้ ..."}
   ]}
]}
```
- `lesson` blocks: each has `h` (Thai heading) and ONE of: `p` (paragraph, Thai, may include English words), `list` (array of strings), `ex` (array of [wrong, right] pairs — prefix ✗ and ✓), or `table` (array of rows, first row = header).
  Lessons: 180–400 Thai words total, concrete, with English examples on academic topics (health, education, environment, AI, society). Include the typical Thai-learner pitfalls. Precise and correct grammar terminology.
- `quiz` items: type "mc" only; exactly 4 options; `answer` 0-based; one unambiguous answer; Thai `explain` specific to the item (1–2 sentences, say why the right answer is right and the tempting wrong one wrong). Vary item formats: choose the correct sentence / fill the blank (use "____") / find the error (options are the underlined parts written as "A) ..." etc. — instead, write options as the 4 candidate segments) / choose the best rewrite / choose the best connector.
  Spread answers evenly over A–D. No "all/none of the above".
- Use academic topics in examples. Keep each item short (one sentence or two).

## Quality check (mandatory)
Re-solve every item; make sure only one option is correct in standard formal written English (British or American both fine but be consistent within an item). Validate the JSON with python (run python WITHOUT -I): count items per set, check 4 options, answer in 0..3, print answer distribution. Report a summary table in your final message (not the JSON).
