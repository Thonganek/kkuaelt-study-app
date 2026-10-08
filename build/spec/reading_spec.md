# Reading content spec — KKU-AELT 45-day plan

Learner: a Thai university lecturer (Public Health / Medicine background) preparing for KKU-AELT
(Khon Kaen University Academic English Language Test). Official Reading format: 6 passages, 69 questions, 2 hours.
Passages 1–4 = short texts / news, multiple choice (4 options, one best answer).
Passages 5–6 = long texts, multiple choice (4 options) + short answer (write a word/phrase/short sentence).
Everything you write will be embedded in an interactive HTML study app that auto-scores answers
and shows your Thai explanations after submission.

## Output format (strict JSON, UTF-8)

A passage object:
```json
{
  "id": "T1P1",                      
  "kind": "short",                   
  "genre": "news report",            
  "domain": "Public Health",         
  "title": "Bangkok Offers Free Health Checks for Office Workers",
  "paragraphs": ["First paragraph text ...", "Second paragraph ..."],
  "questions": [
    {"type": "mc", "skill": "main idea",
     "q": "What is the main idea of the passage?",
     "options": ["...", "...", "...", "..."],
     "answer": 2,
     "explain": "คำอธิบายภาษาไทย ... อ้างหลักฐาน ¶2: \"...\" ตัวเลือก A ผิดเพราะ ..."},
    {"type": "short", "skill": "detail",
     "q": "What do researchers call the period of fast forgetting? (Answer in NO MORE THAN THREE WORDS from the passage.)",
     "answers": ["the forgetting curve", "forgetting curve"],
     "explain": "¶3: \"...\""}
  ]
}
```
- `kind`: "short" or "long".
- `genre`: one of: news report, announcement/notice, feature article, research news, opinion article, academic article, research summary.
- `domain`: one of: Public Health, Medicine, AI/Technology, Environment, Education, Society.
- `paragraphs`: plain text, no numbering (the app numbers them ¶1, ¶2 …). No markdown, no HTML.
- `answer`: 0-based index of the correct option (0=A, 1=B, 2=C, 3=D).
- `skill` must be one of exactly: "main idea", "topic", "title", "detail", "negative detail", "reference", "vocabulary", "inference", "purpose", "organization", "tone", "fact/opinion", "paraphrase", "short answer".
  (Short-answer questions use type "short" and skill "short answer".)
- Short-answer `answers`: 1–4 acceptable strings, lower-case is fine; the FIRST is the canonical answer and must appear verbatim in the passage (NO MORE THAN THREE WORDS). Add obvious variants (with/without article, singular/plural) as extra entries.
- `explain`: Thai, 1–3 sentences. Always cite the evidence with paragraph number (e.g. ¶4: "…quote…"). For tricky items, say briefly why the most tempting distractor is wrong.

## Writing the passages
- 100% original writing. Do not copy or closely paraphrase any published text.
- Level: CEFR B2–C1 academic English; use Academic Word List vocabulary naturally; varied sentence structures (relative clauses, passives, concession clauses, nominalisation) as in real academic/news texts.
- Facts: general background must be accurate. Specific statistics, surveys and studies may be illustrative, BUT attribute invented numbers only to generic/unnamed sources ("a 2023 survey of 1,200 students", "researchers at a university in northern Thailand") — NEVER attach invented figures or quotes to real named organisations (WHO, UNICEF, Thai Ministry of Public Health, real universities, real journals) or real people. Invented people must have generic plausible names and roles ("Dr. Siriporn Kaewmanee, a public health researcher").
- Word counts: follow the target given for each passage (±10%). Long texts: 7–8 paragraphs.
- Thai context is welcome (Thailand/Southeast Asia settings), but mix in global ones too.
- Titles: informative headline style for news; academic style for long texts.

## Things a previous version got wrong — do NOT do these
- Do NOT write meta-disclaimers inside passages ("This programme is a fictional example", "A fictional campus report…"). Passages must read like genuine news/academic texts; the app shows a single global note that practice texts are invented.
- Do NOT write template explanations. An `explain` must NOT paste a whole paragraph and must NOT end with a generic sentence reused across questions. Quote only the 1 sentence (or clause) that proves the answer, then explain the reasoning specific to THIS question (and, where useful, why the most tempting wrong option fails). Every explanation must be different.
- Do NOT make texts artificially short: respect the word targets.
- Do NOT make the correct option the longest or the most "balanced-sounding" one by habit; distractors must be genuinely tempting. Check with a script: the correct option should be the strictly longest in no more than ~10% of MC items.
- Do NOT let a passage's own title give away the answer to its "best title" / "main idea" question (the app displays the title).

## Writing the questions
- Stems should look like a real exam, e.g.:
  "What is the main idea of the passage?" / "Which of the following is the best title for the passage?" /
  "What is paragraph 3 mainly about?" / "According to the passage, …" / "Which of the following is NOT mentioned as …?" /
  "The word 'X' in paragraph 2 is closest in meaning to" / "What does 'they' in paragraph 4 refer to?" /
  "It can be inferred from paragraph 5 that …" / "Why does the author mention …?" / "What is the purpose of paragraph 6?" /
  "The author's attitude toward … can best be described as" / "How is the information in the passage organised?" /
  "Which statement is an opinion rather than a fact?"
- For vocabulary and reference questions, quote the word in single quotes and give the paragraph number; make sure that word appears in that paragraph exactly once (or say "in line …" style is not possible — so pick a word that appears once in that paragraph).
- Exactly 4 options, parallel in grammar and similar in length; no "all of the above"/"none of the above"/"both A and B".
- Exactly one defensible answer, clearly supported by the text. Distractors should be plausible: true-but-not-stated, opposite meaning, too broad/too narrow, word-match traps, misread numbers.
- Spread correct answers evenly over A–D within each passage (never more than 3 identical letters in a row; each letter used roughly equally).
- Order questions roughly in the order of the passage, with main-idea/title questions first or last.
- Short-answer questions only in long passages unless the day spec says otherwise.

## Quality check before you finish (mandatory)
1. Re-solve every question yourself using only the passage and confirm the key is correct and unique. Fix anything ambiguous.
2. Validate the file with Python: `python -c "import json;d=json.load(open(r'PATH',encoding='utf-8'));print('ok')"` (run python WITHOUT -I; any directory is fine).
   Also print, per passage: word count, number of questions, distribution of answers A–D, and check every mc question has 4 options and `answer` in 0..3, every short question has non-empty `answers` whose first item appears in the passage text (case-insensitive).
3. Report the summary table in your final message (ids, titles, word counts, question counts, answer distribution). Do NOT paste the full JSON into your final message.
