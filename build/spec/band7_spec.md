# Band 7 content spec (Days 41–58 of the 60-day course)

Target learner: Thai adult preparing for KKU-AELT (Khon Kaen University Academic English Language Test) who wants **Band 7, the top of the 7-level scale**. Everything in this stage must be clearly harder than the existing 42-day material (CEFR C1, approaching C2 for the long passages). The app is untimed, so difficulty comes from the language and the questions, not from time pressure.

All files are UTF-8 JSON written with `ensure_ascii=False, indent=1` into `build/content/band7/`. Re-load every file you write and check it against the rules below before reporting back.

Samples of the existing data format (copy the field names exactly):
- `build/content/band7/_sample_short_passage.json`, `_sample_long_passage.json` (a passage with its questions)
- `build/content/band7/_sample_essay.json`, `_sample_grammar.json`, `_sample_lessons.json`
- `build/content/band7/_existing_titles.txt` — titles and essay prompts already in the course. Do not reuse these topics or titles.

## Exam format (KKU-AELT Reading)

A Reading test = 6 passages, 69 questions, always in this order:

| Passage | kind | words | questions |
|---|---|---|---|
| P1 | short | 380–480 | 8 multiple choice |
| P2 | short | 380–480 | 8 multiple choice |
| P3 | short | 400–500 | 9 multiple choice |
| P4 | short | 420–520 | 10 multiple choice |
| P5 | long | 950–1150 | 12 multiple choice + 5 short answer (17) |
| P6 | long | 950–1150 | 12 multiple choice + 5 short answer (17) |

The existing tests average 306 words (short) and 819 words (long). Band 7 passages are longer and denser.

## Passage rules

- Genres: P1–P4 are news reports, feature articles, official notices, editorials, research summaries. P5–P6 are academic articles (introduction → argument/evidence → counter-evidence or limitations → conclusion), organised in 7–10 paragraphs.
- Register: C1 academic. Use nominalisation, hedged claims (may, appears to, is likely to), concession (Although…, While…, Admittedly…), embedded and reduced relative clauses, and some low-frequency academic vocabulary that can be guessed from context. Avoid slang.
- Content must be internally consistent and plausible. People, institutions, projects and statistics are **fictional** (invent names, e.g. "a 2024 study at a university in northern Thailand", "Dr. Narin Chaiyasit"). Do not attribute invented findings to real named organisations or real people. Thailand/ASEAN contexts are welcome but not required.
- `paragraphs` is a list of plain-text paragraphs (no numbering, no markdown).
- Each passage object: `id`, `kind` ("short" or "long"), `genre`, `domain`, `title`, `paragraphs`, `questions`. Daily passages (B01–B10) also have `focus` (English, which Band 7 skill the passage drills) and `skill_tip_en` (one English sentence of strategy advice).

## Question rules

Multiple choice: `{"type":"mc","skill":…,"q":…,"options":[4 strings],"answer":0-3,"explain":…}`
Short answer: `{"type":"short","skill":"short answer","q":"… (Answer in NO MORE THAN THREE WORDS from the passage.)","answers":[accepted variants],"explain":…}`

`skill` must be one of: main idea, title, topic, detail, negative detail, vocabulary, reference, inference, purpose, tone, organization, fact/opinion, paraphrase, short answer.

Band 7 difficulty requirements:
- At least 40% of the multiple-choice questions in each passage are inference, purpose, tone, paraphrase, organization or fact/opinion. Every passage has at least one inference question.
- Correct options **paraphrase** the text; they never copy the key phrase word for word.
- Every distractor is tempting for a specific reason: it reuses words from the passage but changes the meaning, is true but does not answer the question, overgeneralises (all, always, only), reverses cause and effect, confuses who said what, or is a claim the author reports but rejects. No obviously absurd options.
- The four options are similar in length and grammar. "All/none of the above" is not allowed.
- Vocabulary questions test words with more than one meaning or low-frequency words whose sense depends on context.
- Reference questions point to a pronoun or summary noun (this trend, such measures) whose referent is at least one sentence away.
- Questions follow the order of the text (except main idea/title, which go first or last).
- Spread the answer key: in each passage use each of A–D at least once where the number of questions allows, with no runs of three identical letters. Across the 59 multiple-choice questions of a test, each letter is correct 14–16 times.
- Short answer: the answer must be copied **exactly** from the passage and be 1–3 words. `answers` lists every acceptable variant (with/without article, singular/plural). Questions must have exactly one defensible answer.
- `explain` is in Thai (2–4 sentences): cite the paragraph as ¶n, quote the English evidence in “…”, and say briefly why the most tempting distractor is wrong.

## Essay prompts (Writing)

KKU-AELT Writing: one short opinion prompt, essay of at least 250 words. For Band 7 the model essays are 320–380 words, four paragraphs (Introduction, Body 1, Body 2, Conclusion), with a clear position, one concession + rebuttal, precise examples, varied cohesion and C1 vocabulary — but natural, not showy.

Essay object fields (copy `_sample_essay.json`): `id`, `prompt` (short, exam-style), `prompt_fixed` (grammatical version + "Do you agree or disagree?"), `th_explain`, `keywords` [{en, th}] (8), `paraphrases` (3), `stance` ("agree"/"disagree"), `stance_reason_th`, `ideas` {agree:[3×{reason, explain, example}], disagree:[3×{…}]}, `outline` {intro, body1, body2, conclusion}, `model` [4 paragraphs], `phrases` [{en, th}] (6–8 Band 7 phrases from the model), plus `band7_th`: a Thai list (4–6 strings) of what makes this model a Band 7 essay (e.g. how the concession is handled).
