/* ============================================================
   Quiz engine: reading, grammar, vocabulary, retry, full tests
   ============================================================ */
function qstate(key) {
  if (!S.quiz[key]) S.quiz[key] = { ans: {}, done: false, seed: 1, hist: [], ov: {}, flags: {} };
  const st = S.quiz[key]; st.ans = st.ans || {}; st.ov = st.ov || {}; st.flags = st.flags || {}; st.hist = st.hist || [];
  return st;
}

function qpeek(key) { return S.quiz[key] || { ans: {}, done: false, seed: 1, hist: [], ov: {}, flags: {} }; }

/* ---------- vocabulary question generator ---------- */
function stemOf(w) { const b = w.toLowerCase(); return b.length <= 5 ? b : b.slice(0, Math.max(5, b.length - 2)); }
function clozeOf(w) {
  const ex = w.ex || ''; const low = ex.toLowerCase(); const head = w.w.toLowerCase();
  if (head.includes(' ')) {
    const i = low.indexOf(head); if (i < 0) return null;
    return { blank: ex.slice(0, i) + '_____' + ex.slice(i + head.length), ans: ex.slice(i, i + head.length) };
  }
  const st = stemOf(head); const re = /[A-Za-z][A-Za-z'-]*/g; let m;
  while ((m = re.exec(ex))) {
    const tok = m[0], t = tok.toLowerCase();
    if (t === head || (t.startsWith(st) && t.length - head.length <= 5)) return { blank: ex.slice(0, m.index) + '_____' + ex.slice(m.index + tok.length), ans: tok };
  }
  return null;
}
function distractors(w, r, field) {
  const same = shuffle((DATA.vocab[w.day] || []).filter(x => x.w !== w.w), r);
  const rest = shuffle(ALLWORDS.filter(x => x.w !== w.w && x.day !== w.day), r).slice(0, 30);
  const out = []; const seen = new Set([String(w[field]).trim()]);
  for (const x of same.concat(rest)) { const v = String(x[field]).trim(); if (!seen.has(v)) { seen.add(v); out.push(x); } if (out.length === 3) break; }
  return out;
}
function genVocab(words, seed, prefix, n) {
  const r = rng(seed * 7919 + words.length * 31 + prefix.length);
  const pick = shuffle(words, r).slice(0, Math.min(n, words.length));
  return pick.map((w, i) => {
    let type = ['et', 'te', 'et', 'cl'][i % 4];
    const id = prefix + '.' + (i + 1);
    const base = { id, skill: 'vocab', word: w.w, src: 'คำศัพท์ Day ' + w.day, explain: `${w.w} (${w.pos}) = ${w.th}${w.ex ? ' — ' + w.ex : ''}` };
    if (type === 'cl') {
      const c = clozeOf(w);
      if (c) { const ds = distractors(w, r, 'w'); const opts = shuffle([c.ans].concat(ds.map(x => x.w)), r); return Object.assign(base, { type: 'mc', q: 'เติมคำในช่องว่าง: ' + c.blank, options: opts, answer: opts.indexOf(c.ans) }); }
      type = 'te';
    }
    if (type === 'te') { const ds = distractors(w, r, 'w'); const opts = shuffle([w.w].concat(ds.map(x => x.w)), r); return Object.assign(base, { type: 'mc', q: `คำใดมีความหมายว่า “${w.th}”`, options: opts, answer: opts.indexOf(w.w) }); }
    const ds = distractors(w, r, 'th'); const opts = shuffle([w.th].concat(ds.map(x => x.th)), r);
    return Object.assign(base, { type: 'mc', q: `“${w.w}” (${w.pos}) หมายถึงข้อใด`, options: opts, answer: opts.indexOf(w.th) });
  });
}
function vrCount(d) { const t = DAY(d).type; return t === 'review' ? 40 : t === 'light' ? 20 : 30; }
function reviewWords(d) {
  const day = DAY(d);
  let words;
  if (day.review) words = day.review.days.flatMap(x => (DATA.vocab[x] || []).map(w => Object.assign({ day: x }, w)));
  else if (day.type === 'review') words = ALLWORDS.slice();
  else if (day.type === 'light') words = ALLWORDS.filter(w => w.day === 1 || w.src === 'theme' && DATA.meta.lightVocabDays.includes(w.day));
  else words = [];
  const starred = words.filter(w => S.vstat[w.w] === 2), rest = words.filter(w => S.vstat[w.w] !== 2);
  return { all: words, starred, rest };
}
function getQuiz(key) {
  const i = key.indexOf(':'); const kind = key.slice(0, i), id = key.slice(i + 1);
  if (kind === 'R') { const p = DATA.passages[id]; if (!p) return null; return { key, kind: 'reading', title: p.title, day: PASSAGE_DAY[id], pids: [id], questions: p.questions.map((q, j) => Q[id + '.' + (j + 1)]) }; }
  if (kind === 'T') { const t = DATA.tests[id]; if (!t) return null; return { key, kind: 'test', title: t.title, day: t.day, pids: t.passages, questions: t.passages.flatMap(pid => DATA.passages[pid].questions.map((q, j) => Q[pid + '.' + (j + 1)])) }; }
  if (kind === 'G') { const g = DATA.grammar[id]; if (!g) return null; return { key, kind: 'grammar', title: g.title_th, day: g.day, questions: g.quiz.map((q, j) => Q[id + '.' + (j + 1)]) }; }
  if (kind === 'V') { const d = +id; const st = S.quiz[key] || { seed: 1 }; const w = (DATA.vocab[d] || []).map(x => Object.assign({ day: d }, x)); return { key, kind: 'vocab', title: 'Quiz คำศัพท์ Day ' + d, day: d, questions: genVocab(w, st.seed || 1, 'V' + d + 's' + (st.seed || 1), Math.max(20, w.length)) }; }
  if (kind === 'VR') {
    const d = +id; const st = S.quiz[key] || { seed: 1 }; const rw = reviewWords(d); const r = rng((st.seed || 1) * 104729 + d);
    const n = vrCount(d);
    const chosen = shuffle(rw.starred, r).concat(shuffle(rw.rest, r)).slice(0, n);
    return { key, kind: 'vocab', title: 'ทวนศัพท์ Day ' + d, day: d, questions: genVocab(chosen, st.seed || 1, 'VR' + d + 's' + (st.seed || 1), n) };
  }
  return null;
}
function normAns(s) { return String(s || '').toLowerCase().replace(/[’‘`]/g, "'").replace(/[^a-z0-9'%.\s-]/g, ' ').replace(/\b(the|a|an)\b/g, ' ').replace(/-/g, ' ').replace(/\s+/g, ' ').trim().replace(/\.$/, ''); }
function shortOK(q, a) {
  if (!a || wc(a) > 3 && !/\d/.test(a)) return false;
  const n = normAns(a); if (!n) return false; const sing = s => s.split(' ').map(x => x.replace(/(es|s)$/, '')).join(' ');
  const words = t => t.split(' ').filter(Boolean);
  return (q.answers || []).some(x => { const m = normAns(x); if (m === n || sing(m) === sing(n)) return true; const has = (' ' + sing(n) + ' ').includes(' ' + sing(m) + ' '); return has && words(n).length - words(m).length <= 2; });
}
function isRight(q, a, ov) { if (!q) return false; if (q.type === 'short') return !!(ov && ov[q.id]) || shortOK(q, a); return a !== undefined && a !== null && a !== '' && Number(a) === q.answer; }
function answered(a) { return a !== undefined && a !== null && String(a).trim() !== ''; }

function submitQuiz(key, auto) {
  const qz = getQuiz(key); const st = qstate(key);
  const miss = qz.questions.filter(q => !answered(st.ans[q.id])).length;
  if (!auto && miss && !confirm(`ยังไม่ได้ตอบ ${miss} ข้อ ต้องการส่งเลยหรือไม่?`)) return false;
  const score = qz.questions.filter(q => isRight(q, st.ans[q.id], st.ov)).length;
  Object.assign(st, { done: true, score, total: qz.questions.length, at: Date.now() });
  st.hist.push({ score, total: qz.questions.length, at: st.at });
  if (S.timers[key]) timerStop(key);
  qz.questions.forEach(q => { if (isRight(q, st.ans[q.id], st.ov)) delete S.resolved[q.id]; });
  save(true);
  if (auto) toast('หมดเวลา — ระบบส่งคำตอบให้อัตโนมัติ', 5000);
  else toast(`ส่งแล้ว: ได้ ${score}/${qz.questions.length} (${pct(score, qz.questions.length)}%)`);
  render(true);
  return true;
}
function recalc(key) { const qz = getQuiz(key), st = S.quiz[key]; if (!st || !st.done) return; st.score = qz.questions.filter(q => isRight(q, st.ans[q.id], st.ov)).length; if (st.hist.length) st.hist[st.hist.length - 1].score = st.score; }

ACT.pick = el => {
  const st = qstate(el.dataset.key); if (st.done) return;
  st.ans[el.dataset.q] = +el.dataset.i; save();
  const box = el.closest('.opts'); $$('.opt', box).forEach(o => o.classList.toggle('sel', o === el));
  const inp = $('input', el); if (inp) inp.checked = true;
  updateCount(el.dataset.key);
};
INP.short = el => { const st = qstate(el.dataset.key); if (st.done) return; st.ans[el.dataset.q] = el.value; save(); updateCount(el.dataset.key); };
ACT.submit = el => submitQuiz(el.dataset.key);
ACT.override = el => { const st = qstate(el.dataset.key); st.ov[el.dataset.q] = true; recalc(el.dataset.key); save(); render(true); };
ACT.resetQuiz = el => {
  const key = el.dataset.key; if (!confirm('เริ่มทำใหม่? คะแนนเดิมจะถูกเก็บในประวัติ')) return;
  const old = qstate(key); S.quiz[key] = { ans: {}, done: false, seed: (old.seed || 1) + (key.startsWith('V') ? 1 : 0), hist: old.hist, ov: {}, flags: {} };
  if (key.startsWith('T:')) { delete S.timers[key]; }
  save(); render(true);
};
ACT.flag = el => { const st = qstate(el.dataset.key); st.flags[el.dataset.q] = !st.flags[el.dataset.q]; save(); el.classList.toggle('on', !!st.flags[el.dataset.q]); const p = $(`.pal[data-q="${CSS.escape(el.dataset.q)}"]`); if (p) p.classList.toggle('f', !!st.flags[el.dataset.q]); };
function updateCount(key) {
  const qz = getQuiz(key); const st = qpeek(key);
  const n = qz.questions.filter(q => answered(st.ans[q.id])).length;
  $$(`[data-count="${CSS.escape(key)}"]`).forEach(e => e.textContent = `ตอบแล้ว ${n}/${qz.questions.length}`);
  qz.questions.forEach(q => { const p = $(`.pal[data-q="${CSS.escape(q.id)}"]`); if (p) p.classList.toggle('a', answered(st.ans[q.id])); });
  if (qz.pids) qz.pids.forEach((pid, i) => { const t = $(`.ptab[data-pi="${i}"] small`); if (t) { const qs = DATA.passages[pid].questions.map((x, j) => pid + '.' + (j + 1)); t.textContent = qs.filter(id => answered(st.ans[id])).length + '/' + qs.length; } });
}

function renderQ(key, q, num, st) {
  const done = st.done; const a = st.ans[q.id]; const ok = done && isRight(q, a, st.ov);
  let h = `<div class="q ${done ? (ok ? 'right' : 'wrong') : ''}" id="q-${esc(q.id)}"><div class="qhead"><span class="qn">${num}.</span><span class="qtext">${esc(q.q)}</span>`;
  h += `<span class="skilltag">${esc(SKILL_TH[q.skill] || q.skill || '')}</span>`;
  if (!done && key.startsWith('T:')) h += `<button class="flag ${st.flags[q.id] ? 'on' : ''}" title="ทำเครื่องหมายกลับมาดู" data-act="flag" data-key="${esc(key)}" data-q="${esc(q.id)}" aria-label="ทำเครื่องหมาย">${ico('flag')}</button>`;
  h += `</div>`;
  if (q.type === 'short') {
    h += `<div class="shortin"><input type="text" ${done ? 'disabled' : ''} value="${esc(a || '')}" data-inp="short" data-key="${esc(key)}" data-q="${esc(q.id)}" placeholder="พิมพ์คำตอบ (ไม่เกิน 3 คำ)" aria-label="คำตอบข้อ ${num}">`;
    if (done) h += ok ? '<span class="chip ok">' + ico('check') + ' ถูก</span>' : `<span class="chip no">${ico('x')}</span> <span class="small">คำตอบ: <b>${esc(q.answers[0])}</b></span> ${answered(a) ? `<button class="btn sm" data-act="override" data-key="${esc(key)}" data-q="${esc(q.id)}">ความหมายเท่ากัน — นับว่าถูก</button>` : ''}`;
    h += `</div>`;
  } else {
    h += `<div class="opts" role="radiogroup">` + q.options.map((o, i) => {
      let cls = 'opt'; if (!done && a === i) cls += ' sel';
      if (done) { if (i === q.answer) cls += ' ans'; else if (a === i) cls += ' bad'; }
      return `<label class="${cls}" ${done ? '' : `data-act="pick" data-key="${esc(key)}" data-q="${esc(q.id)}" data-i="${i}"`}><input type="radio" name="${esc(key + q.id)}" ${a === i ? 'checked' : ''} ${done ? 'disabled' : ''}><span class="L">${L(i)}</span><span>${esc(o)}</span></label>`;
    }).join('') + `</div>`;
  }
  if (done) h += `<div class="explain">${!ok && q.type !== 'short' ? `<b>เฉลย ${L(q.answer)}</b> · ` : ''}${esc(q.explain || '')}</div>`;
  return h + `</div>`;
}
function skillTable(qs, st) {
  const by = {}; qs.forEach(q => { const k = q.skill || 'other'; by[k] = by[k] || [0, 0]; by[k][1]++; if (isRight(q, st.ans[q.id], st.ov)) by[k][0]++; });
  return Object.entries(by).sort((a, b) => a[1][0] / a[1][1] - b[1][0] / b[1][1]).map(([k, v]) => `<span class="chip ${v[0] === v[1] ? 'ok' : v[0] / v[1] < .6 ? 'no' : ''}">${esc(SKILL_TH[k] || k)} ${v[0]}/${v[1]}</span>`).join(' ');
}
function renderQuizInner(key, opts = {}) {
  const qz = getQuiz(key); if (!qz) return '<p class="muted">ไม่พบชุดคำถาม</p>';
  const st = qpeek(key); st.ov = st.ov || {}; st.flags = st.flags || {}; st.hist = st.hist || []; let h = '';
  if (st.done) {
    h += `<div class="result"><div class="big">${st.score}/${st.total}</div><div><b>${pct(st.score, st.total)}%</b><div class="small muted">ส่งเมื่อ ${new Date(st.at).toLocaleString('th-TH')}${st.hist.length > 1 ? ' · ครั้งที่ ' + st.hist.length : ''}</div></div><div class="spacer"></div><button class="btn sm" data-act="resetQuiz" data-key="${esc(key)}">${ico('retry')} ทำใหม่${key.startsWith('V') ? ' (สุ่มข้อใหม่)' : ''}</button></div>`;
    if (qz.kind !== 'vocab') h += `<div class="row small" style="margin-bottom:8px">${skillTable(qz.questions, st)}</div>`;
  }
  h += `<div class="qlist">` + qz.questions.map((q, i) => renderQ(key, q, (opts.offset || 0) + i + 1, st)).join('') + `</div>`;
  if (!st.done) {
    const n = qz.questions.filter(q => answered(st.ans[q.id])).length;
    h += `<div class="quizbar"><button class="btn pri" data-act="submit" data-key="${esc(key)}">ส่งคำตอบ</button><span class="small muted" data-count="${esc(key)}">ตอบแล้ว ${n}/${qz.questions.length}</span>`;
    if (opts.minutes) h += `<span class="spacer"></span>${timerBtn('Q:' + key, opts.minutes, opts.label || qz.title)}`;
    h += `</div>`;
  }
  return h;
}
function renderQuiz(key, opts) { return `<div class="quizbox" data-key="${esc(key)}">${renderQuizInner(key, opts)}</div>`; }
function timerBtn(key, min, label) {
  const on = S.timers[key] && timerLeft(key) > 0;
  return `<span class="row"><span class="small" data-timer="${esc(key)}"></span><button class="btn sm" data-act="timer" data-key="${esc(key)}" data-min="${min}" data-label="${esc(label)}">${on ? ico('pause') + ' พัก/ต่อ' : ico('clock') + ' จับเวลา ' + min + ' นาที'}</button></span>`;
}
function renderPassage(pid, opts = {}) {
  const p = DATA.passages[pid]; if (!p) return `<div class="callout warn">ยังไม่มีบทอ่าน ${esc(pid)}</div>`;
  const words = p.paragraphs.reduce((s, x) => s + wc(x), 0);
  return `<article class="passage"><h3>${esc(p.title)}</h3><div class="meta small muted">${esc(p.genre || '')} · ${esc(p.domain || '')} · ${words} คำ · ${p.questions.length} ข้อ${opts.label ? ' · ' + esc(opts.label) : ''}</div>` +
    p.paragraphs.map((x, i) => `<p><span class="pn">¶${i + 1}</span>${esc(x)}</p>`).join('') + `</article>`;
}

/* ---------- wrong items & instant retry ---------- */
function wrongItems(filter = {}) {
  const out = [];
  for (const key in S.quiz) {
    const st = S.quiz[key]; if (!st.done) continue;
    const qz = getQuiz(key); if (!qz) continue;
    if (filter.days && !filter.days.includes(qz.day)) continue;
    qz.questions.forEach(q => { if (!isRight(q, st.ans[q.id], st.ov)) out.push({ key, q, a: st.ans[q.id], day: qz.day, kind: qz.kind, title: qz.title }); });
  }
  return out;
}
function renderRetryItem(it) {
  const q = it.q; const r = S.retry[q.id]; const solved = !!S.resolved[q.id];
  let h = `<div class="q ${r ? (r.ok ? 'right' : 'wrong') : ''}"><div class="qhead"><span class="qtext">${esc(q.q)}</span><span class="skilltag">${esc(SKILL_TH[q.skill] || q.skill || '')}</span></div><div class="tiny muted" style="margin-left:0">Day ${it.day || '-'} · ${esc(it.title || '')}${it.a !== undefined && it.a !== null && it.a !== '' ? ' · ครั้งก่อนตอบ: ' + esc(q.type === 'short' ? it.a : L(it.a) + ') ' + (q.options[it.a] || '')) : ' · ครั้งก่อนไม่ได้ตอบ'}</div>`;
  if (q.pid) h += `<details class="more small"><summary>ดูบทอ่าน “${esc(DATA.passages[q.pid].title)}”</summary>${renderPassage(q.pid)}</details>`;
  if (q.type === 'short') {
    h += `<div class="shortin"><input type="text" id="rt-${esc(q.id)}" value="${esc(r ? r.a : '')}" ${r ? 'disabled' : ''} placeholder="พิมพ์คำตอบ"><button class="btn sm" data-act="retryShort" data-q="${esc(q.id)}" ${r ? 'disabled' : ''}>ตรวจ</button></div>`;
  } else {
    h += `<div class="opts">` + q.options.map((o, i) => { let c = 'opt'; if (r) { if (i === q.answer) c += ' ans'; else if (r.a === i) c += ' bad'; } return `<label class="${c}" ${r ? '' : `data-act="retryPick" data-q="${esc(q.id)}" data-i="${i}"`}><span class="L">${L(i)}</span><span>${esc(o)}</span></label>`; }).join('') + `</div>`;
  }
  if (r) h += `<div class="explain">${r.ok ? ico('check') + ' ถูกแล้ว — ย้ายออกจากรายการข้อผิด' : ico('x') + ' ยังไม่ถูก' + (q.type === 'short' ? ' · คำตอบ: <b>' + esc(q.answers[0]) + '</b>' : ' · เฉลย <b>' + L(q.answer) + '</b>')} · ${esc(q.explain || '')} ${!r.ok ? `<button class="btn sm" data-act="retryAgain" data-q="${esc(q.id)}">ลองอีกครั้ง</button>` : ''}</div>`;
  else if (solved) h += `<div class="explain">${ico('check')} แก้แล้ว</div>`;
  return h + `</div>`;
}
const RETRY_INDEX = {};
function renderRetryList(items, ctx) {
  items.forEach(it => RETRY_INDEX[it.q.id] = it);
  if (!items.length) return `<div class="empty-state">${ico('spark')} ไม่มีข้อผิดค้างในช่วงนี้</div>`;
  const left = items.filter(it => !S.resolved[it.q.id]).length;
  return `<p class="small muted">${items.length} ข้อ · แก้แล้ว ${items.length - left} · คงเหลือ ${left}</p><div class="qlist">${items.map(renderRetryItem).join('')}</div>`;
}
function retryCheck(id, a) {
  const it = RETRY_INDEX[id]; if (!it) return; const ok = isRight(it.q, a, {});
  S.retry[id] = { a, ok, at: Date.now() }; if (ok) S.resolved[id] = true;
  save(); render(true);
}
ACT.retryPick = el => retryCheck(el.dataset.q, +el.dataset.i);
ACT.retryShort = el => { const v = (document.getElementById('rt-' + el.dataset.q) || {}).value; retryCheck(el.dataset.q, v); };
ACT.retryAgain = el => { delete S.retry[el.dataset.q]; save(); render(true); };

/* ---------- full test runner ---------- */
function testStatus(tid) { const st = S.quiz['T:' + tid]; if (!st) return 'new'; if (st.done) return 'done'; if (st.end) return 'running'; return 'new'; }
ACT.startTest = el => {
  const tid = el.dataset.t; const key = 'T:' + tid; const st = qstate(key);
  if (!st.end) { st.end = Date.now() + 120 * 60000; st.startAt = Date.now(); S.timers[key] = { end: st.end, dur: 7200, label: DATA.tests[tid].title, paused: null }; S.ui.activeTimer = key; }
  save(true); if (location.hash === '#/test/' + tid) render(); else location.hash = '#/test/' + tid;
};
ACT.ptab = el => { S.ui.tp = S.ui.tp || {}; S.ui.tp[el.dataset.t] = +el.dataset.pi; save(); render(); const b = $('.testbody'); if (b) b.classList.remove('showq'); };
ACT.pal = el => { S.ui.tp = S.ui.tp || {}; S.ui.tp[el.dataset.t] = +el.dataset.pi; save(); render(); setTimeout(() => { const b = $('.testbody'); if (b) b.classList.add('showq'); const q = document.getElementById('q-' + el.dataset.q); if (q) q.scrollIntoView({ block: 'center' }); }, 30); };
ACT.palToggle = () => { S.ui.palOpen = !S.ui.palOpen; save(); const p = $('.palette'); if (p) p.classList.toggle('open', !!S.ui.palOpen); };
ACT.paneToggle = () => { const b = $('.testbody'); if (b) b.classList.toggle('showq'); };
ACT.testExit = el => { location.hash = '#/day/' + el.dataset.d; };

function viewTest(tid) {
  const t = DATA.tests[tid]; if (!t) return `<div class="card">ไม่พบข้อสอบ</div>`;
  const key = 'T:' + tid; const st = qstate(key); const status = testStatus(tid);
  if (status === 'running' && Date.now() > st.end) { setTimeout(() => submitQuiz(key, true), 0); }
  if (status === 'new') return testIntro(tid);
  if (status === 'done') return testResults(tid);
  const pi = (S.ui.tp && S.ui.tp[tid]) || 0; const pid = t.passages[pi];
  let offset = 0; for (let i = 0; i < pi; i++) offset += DATA.passages[t.passages[i]].questions.length;
  const qs = DATA.passages[pid].questions.map((q, j) => Q[pid + '.' + (j + 1)]);
  let h = `<div class="testwrap"><div class="testtop"><button class="btn sm ghost" data-act="testExit" data-d="${t.day}">${ico('arrowl')} ออก (เวลาเดินต่อ)</button><b>${esc(t.title)}</b><span class="timer" data-timer="${esc(key)}"></span><span class="spacer"></span>
  <div class="ptabs">` + t.passages.map((p, i) => { const n = DATA.passages[p].questions.length; const a = DATA.passages[p].questions.filter((x, j) => answered(st.ans[p + '.' + (j + 1)])).length; return `<button class="ptab ${i === pi ? 'on' : ''}" data-act="ptab" data-t="${tid}" data-pi="${i}">P${i + 1} <small>${a}/${n}</small></button>`; }).join('') + `</div>
  <button class="btn sm panetoggle" data-act="paneToggle">${ico('swap')} บทความ/คำถาม</button><button class="btn sm panetoggle" data-act="palToggle">${ico('grid')} เลขข้อ</button><button class="btn sm pri" data-act="submit" data-key="${esc(key)}">ส่งข้อสอบ</button></div>
  <div class="testbody"><div class="pane-p">${renderPassage(pid, { label: 'Passage ' + (pi + 1) + ' / 6' })}</div><div class="pane-q"><h3 style="margin-top:0">Passage ${pi + 1}: ข้อ ${offset + 1}–${offset + qs.length}</h3>${qs.map((q, j) => renderQ(key, q, offset + j + 1, st)).join('')}
  <div class="quizbar">${pi > 0 ? `<button class="btn" data-act="ptab" data-t="${tid}" data-pi="${pi - 1}">${ico('arrowl')} Passage ${pi}</button>` : ''}${pi < 5 ? `<button class="btn pri" data-act="ptab" data-t="${tid}" data-pi="${pi + 1}">Passage ${pi + 2} ${ico('arrowr')}</button>` : `<button class="btn pri" data-act="submit" data-key="${esc(key)}">ส่งข้อสอบ</button>`}<span class="small muted" data-count="${esc(key)}"></span></div></div></div>
  <div class="palette ${S.ui.palOpen ? 'open' : ''}" aria-label="หมายเลขข้อ">`;
  let n = 0; t.passages.forEach((p, i) => DATA.passages[p].questions.forEach((x, j) => { n++; const id = p + '.' + (j + 1); h += `<button class="pal ${answered(st.ans[id]) ? 'a' : ''} ${st.flags[id] ? 'f' : ''}" data-act="pal" data-t="${tid}" data-pi="${i}" data-q="${esc(id)}" title="Passage ${i + 1}">${n}</button>`; }));
  h += `</div></div>`;
  setTimeout(() => updateCount(key), 0);
  return h;
}
function testIntro(tid) {
  const t = DATA.tests[tid]; const isMock = tid.startsWith('M');
  const rows = t.passages.map((pid, i) => { const p = DATA.passages[pid]; const w = p.paragraphs.reduce((s, x) => s + wc(x), 0); const sa = p.questions.filter(q => q.type === 'short').length; return `<tr><td>P${i + 1}</td><td>${esc(p.kind === 'long' ? 'ยาว' : 'สั้น')}</td><td>${p.questions.length}${sa ? ` (short answer ${sa})` : ''}</td><td>${w}</td><td>${i < 4 ? '10–12 นาที' : '≈ 30 นาที'}</td></tr>`; }).join('');
  return `<div class="card"><div class="daynum">Day ${t.day} · ${isMock ? 'Full Mock Exam' : 'Reading Test'}</div><h1>${esc(t.title)}</h1>
  <p>6 passages · 69 ข้อ · 120 นาที — กด “เริ่มทำข้อสอบ” แล้วนาฬิกาจะเดินต่อเนื่อง (แม้ปิดไฟล์) เมื่อหมดเวลาระบบส่งคำตอบให้อัตโนมัติ</p>
  <div class="tablewrap"><table class="t"><tr><th>Passage</th><th>ประเภท</th><th>จำนวนข้อ</th><th>คำ</th><th>เวลาแนะนำ</th></tr>${rows}</table></div>
  <div class="lesson"><b>${ico('bulb')} ${esc(DATA.lessons.L_TEST.title)}</b><ol>${DATA.lessons.L_TEST.steps.map(s => `<li>${esc(s)}</li>`).join('')}</ol><div class="trap">${ico('alert')}<span>${esc(DATA.lessons.L_TEST.trap)}</span></div></div>
  ${isMock ? '<div class="callout warn"><b>Mock:</b> ทำต่อเนื่องเหมือนวันจริง — Reading 120 นาที แล้วต่อด้วย Writing 60 นาทีทันที (09.00–12.00 น. ถ้าทำได้)</div>' : ''}
  <div class="row" style="margin-top:12px"><button class="btn pri" data-act="startTest" data-t="${tid}">${ico('play')} เริ่มทำข้อสอบ (120 นาที)</button><a class="btn" href="#/day/${t.day}">กลับไปหน้า Day ${t.day}</a></div></div>`;
}
function testResults(tid) {
  const t = DATA.tests[tid]; const key = 'T:' + tid; const st = qstate(key); const qz = getQuiz(key);
  const used = st.startAt ? Math.min(120, Math.round(((st.at || Date.now()) - st.startAt) / 60000)) : null;
  let rows = '', off = 0;
  t.passages.forEach((pid, i) => { const p = DATA.passages[pid]; const qs = p.questions.map((x, j) => Q[pid + '.' + (j + 1)]); const sc = qs.filter(q => isRight(q, st.ans[q.id], st.ov)).length; rows += `<tr><td>P${i + 1}</td><td>${esc(p.title)}</td><td>${sc}/${qs.length}</td><td>${pct(sc, qs.length)}%</td><td><button class="btn sm" data-act="scrollTo" data-id="rev-${pid}">ดูเฉลย</button></td></tr>`; });
  let h = `<div class="card"><div class="daynum">Day ${t.day} · ผลสอบ</div><h1>${esc(t.title)}</h1>
  <div class="result"><div class="big">${st.score}/${st.total}</div><div><b>${pct(st.score, st.total)}%</b><div class="small muted">${used != null ? 'ใช้เวลา ≈ ' + used + ' นาที · ' : ''}ส่งเมื่อ ${new Date(st.at).toLocaleString('th-TH')}</div></div><span class="spacer"></span><a class="btn" href="#/day/${t.day}">กลับ Day ${t.day}</a>${tid.startsWith('M') ? `<a class="btn pri" href="#/day/${t.day}/essay">ต่อ Writing 60 นาที ${ico('arrowr')}</a>` : ''}<button class="btn sm" data-act="resetQuiz" data-key="${esc(key)}">${ico('retry')} ทำใหม่</button></div>
  <h3>ผลแยกทักษะ (เรียงจากอ่อนสุด)</h3><div class="row small">${skillTable(qz.questions, st)}</div>
  <h3>ผลแยก passage</h3><div class="tablewrap"><table class="t"><tr><th></th><th>บทอ่าน</th><th>คะแนน</th><th>%</th><th></th></tr>${rows}</table></div>
  <p class="small muted">ข้อที่ผิดถูกเพิ่มเข้า “สมุดข้อผิดพลาด” อัตโนมัติ — ทำซ้ำได้ในวันอาทิตย์และวันที่ 44</p></div>`;
  t.passages.forEach((pid, i) => {
    const qs = DATA.passages[pid].questions.map((x, j) => Q[pid + '.' + (j + 1)]);
    h += `<div class="card" id="rev-${pid}"><details class="more" ${i === 0 ? '' : ''}><summary>Passage ${i + 1}: ${esc(DATA.passages[pid].title)} — ${qs.filter(q => isRight(q, st.ans[q.id], st.ov)).length}/${qs.length}</summary>${renderPassage(pid)}</details><div class="qlist">${qs.map((q, j) => renderQ(key, q, off + j + 1, st)).join('')}</div></div>`;
    off += qs.length;
  });
  return h;
}
