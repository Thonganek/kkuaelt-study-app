# Essay bank spec — KKU-AELT 45-day plan

Learner: Thai university lecturer. KKU-AELT Writing = one short prompt asking for an opinion; write an essay of AT LEAST 250 words in 60 minutes
(practice target 270–310 words). The learner's materials (Opinion_Essay_Guide.docx) teach a 4-paragraph opinion essay:
Intro (paraphrase prompt + clear thesis with total agree/disagree) → Body 1 (reason 1: topic sentence, explanation, example, link back)
→ Body 2 (reason 2, different angle; may add a short reason 3 with "Additionally") → Conclusion (restate stance in new words + summarise both reasons, no new ideas).
They should pick ONE side clearly; a single concession sentence followed by a rebuttal is acceptable but the essay must never switch sides.
Avoid: contractions, informal words, rhetorical questions, "The world is gradually changing", "This essay will focus on two reasons as follows", "According to the statement", "Because…" fragments.

## Output (strict JSON, UTF-8)
```json
{"essays": [
 {"id": "R3",
  "prompt": "Native English speaker is better teacher than non-native English speaker.",
  "prompt_fixed": "A native English speaker is a better teacher than a non-native English speaker. Do you agree or disagree?",
  "th_explain": "ภาษาไทย 3–5 ประโยค: โจทย์ถามอะไร ขอบเขต คำสำคัญ กับดักที่ควรระวัง",
  "keywords": [{"en": "native speaker", "th": "เจ้าของภาษา"}],
  "paraphrases": ["Many people assume that teachers who grew up speaking English are more effective than those who learned it as a second language.", "..."],
  "stance": "disagree",
  "stance_reason_th": "ทำไมฝั่งนี้เขียนง่าย/มีน้ำหนักกว่า",
  "ideas": {
    "agree": [{"reason": "...", "explain": "...", "example": "..."}],
    "disagree": [{"reason": "...", "explain": "...", "example": "..."}]
  },
  "outline": {"intro": "...", "body1": "...", "body2": "...", "conclusion": "..."},
  "model": ["Intro paragraph ...", "Body 1 ...", "Body 2 ...", "Conclusion ..."],
  "phrases": [{"en": "...", "th": "..."}]
 }
]}
```
- `ideas`: exactly 3 for each side; `reason` = a topic-sentence-ready claim; `explain` = 1–2 sentences; `example` = a concrete, plausible example (no invented statistics attributed to real organisations; generic examples like "a rural school in Khon Kaen" are fine).
- `outline`: one English skeleton sentence (or two) per paragraph, matching `stance`.
- `model`: 4 paragraphs, 270–310 words total, natural B2+/C1 academic English (clear rather than showy), total stance = `stance`, uses varied connectors, 1 concession+rebuttal sentence allowed in a body paragraph. Paraphrase the prompt; never copy it word for word.
- `keywords`: 6–8 items; `phrases`: 5 useful phrases from the model with Thai meanings.
- `prompt` must be copied EXACTLY as given to you (even if ungrammatical); `prompt_fixed` is your grammatical version ending with "Do you agree or disagree?".

## Quality check (mandatory)
Count words of each model with python and keep 270–310. Validate JSON with python (run WITHOUT -I). Report a table (id, stance, model word count) — not the JSON.
