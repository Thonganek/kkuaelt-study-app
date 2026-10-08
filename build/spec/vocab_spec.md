# Vocabulary entry spec — KKU-AELT 45-day plan

Learner: Thai university lecturer (Public Health / Medicine background) preparing for an academic English test
(reading research-style passages + writing an opinion essay). Thai is the learner's first language.

Input: scratchpad/spec/vocab_plan.json — {"<day>": [{"w": "<headword>", "src": "research|AWL1..AWL10|theme"}, ...]}.
Each day has 20 items. AWL items are Academic Word List headwords; "theme" items are topic words or essay phrases.

For EVERY item in your assigned days, produce an entry:
```json
{"w": "analyse", "pos": "v.", "th": "วิเคราะห์", "fam": "analysis (n.), analytical (adj.), analyst (n.)",
 "col": "analyse data / carefully analyse", "ex": "Researchers analysed data from 1,200 patients to identify risk factors."}
```
- `w`: copy the headword exactly as given (keep British spelling as given).
- `pos`: part of speech of the headword as usually used in academic texts: n. / v. / adj. / adv. / conj. / prep. / phr. (phrase) — use "n./v." when both are common.
- `th`: concise Thai meaning in the ACADEMIC sense (1–3 short senses separated by " / "). Accurate, natural Thai. For phrases give the Thai equivalent of the whole phrase.
- `fam`: 1–4 useful word-family members with POS (empty string "" for phrases or when none are useful).
- `col`: 1–2 common academic collocations separated by " / ".
- `ex`: one natural academic example sentence (8–18 words) using the headword (or a family form) — preferably about public health, medicine, AI, environment, education or society. Vary sentence structures. No invented attributions to real organisations.

Quality rules:
- Meanings must be correct for academic usage (e.g., "subject" in research = ผู้เข้าร่วมวิจัย, "significant" = มีนัยสำคัญ/สำคัญ; "found" (AWL9) = ก่อตั้ง, not the past of find; "converse" (AWL9) = ตรงกันข้าม (adj./n.), also สนทนา (v.); "depress" (AWL10) = ทำให้ลดลง / ทำให้หดหู่; "minor" = เล็กน้อย / ผู้เยาว์; "medium" = สื่อกลาง/ขนาดกลาง).
- Do not copy dictionary example sentences.
- Output JSON object keyed by day (string) → list of entries in the SAME ORDER as the plan.
- Validate with python (run without -I): every day in your range present, 20 entries per day, `w` matches the plan exactly in order, all fields non-empty except `fam` may be "". Print a summary.
- Do NOT paste the JSON in your final message; just report counts and any words you found tricky.
