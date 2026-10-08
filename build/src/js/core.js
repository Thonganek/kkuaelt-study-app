'use strict';
/* ============================================================
   KKU-AELT 42-day plan — core: data index, state, utils, router
   ============================================================ */
const DATA = JSON.parse(document.getElementById('study-data').textContent);
const LS_KEY = 'kkuaelt45.v2';
const DAYS = DATA.days;
const DAY = n => DAYS[n - 1];
const NDAYS = DAYS.length;
// a day may carry several grammar sets / reading lessons
for (const d of DAYS) { d.grams = [].concat(d.grammar || []); if (d.reading) d.reading.lessons = [].concat(d.reading.lesson); }
const PHASES = DATA.phases;
const PHASE = Object.fromEntries(PHASES.map(p => [p.id, p]));
const PCOL = { P1: 'var(--p1)', P2: 'var(--p2)', P3: 'var(--p3)', P4: 'var(--p4)', P5: 'var(--p5)', P6: 'var(--p6)', P7: 'var(--p7)', P8: 'var(--p8)', P9: 'var(--p9)' };
const START = new Date(DATA.meta.start + 'T00:00:00');
const TYPE_TH = { weekday: 'วันธรรมดา', integration: 'Integration', test: 'Reading Test', sunday: 'Writing Day', mock: 'Full Mock', review: 'Error Review', light: 'Light Review' };
const KIND_TH = { paragraph: 'ย่อหน้า', analysis: 'วิเคราะห์ + thesis', sentences: 'เขียนประโยค', intro: 'บทนำ', summary: 'สรุปความ', rewrite: 'แก้/เขียนใหม่', parts: 'ประกอบ essay ทีละส่วน', essay: 'Essay เต็ม (จับเวลา)' };
const SKILL_TH = { 'main idea': 'Main idea', 'topic': 'Topic', 'title': 'Best title', 'detail': 'Detail', 'negative detail': 'NOT/EXCEPT', 'reference': 'Reference', 'vocabulary': 'Vocabulary in context', 'inference': 'Inference', 'purpose': 'Purpose', 'organization': 'Organisation', 'tone': 'Tone/attitude', 'fact/opinion': 'Fact/opinion', 'paraphrase': 'Paraphrase', 'short answer': 'Short answer', 'grammar': 'Grammar', 'vocab': 'คำศัพท์' };

/* ---------- index ---------- */
const Q = {};            // question id -> question (reading + grammar)
const PASSAGE_DAY = {};  // passage id -> day
const ALLWORDS = [];     // flat vocab list with day
for (const pid in DATA.passages) {
  const p = DATA.passages[pid];
  p.questions.forEach((q, i) => { Q[pid + '.' + (i + 1)] = Object.assign({}, q, { id: pid + '.' + (i + 1), pid, n: i + 1, src: p.title }); });
}
for (const gid in DATA.grammar) {
  const g = DATA.grammar[gid];
  g.quiz.forEach((q, i) => { Q[gid + '.' + (i + 1)] = Object.assign({}, q, { id: gid + '.' + (i + 1), gid, n: i + 1, skill: 'grammar', src: g.title_th }); });
}
for (const d of DAYS) {
  if (d.reading) d.reading.passages.forEach(pid => PASSAGE_DAY[pid] = d.d);
  if (d.test && DATA.tests[d.test]) DATA.tests[d.test].passages.forEach(pid => PASSAGE_DAY[pid] = d.d);
}
for (const day of Object.keys(DATA.vocab).map(Number).sort((a, b) => a - b)) {
  DATA.vocab[day].forEach(w => ALLWORDS.push(Object.assign({ day }, w)));
}
const WORD = Object.fromEntries(ALLWORDS.map(w => [w.w, w]));

/* ---------- state ---------- */
function defaultState() {
  return { v: 2, done: {}, quiz: {}, essays: {}, notes: {}, vstat: {}, resolved: {}, retry: {}, timers: {}, ui: {},
    settings: { font: 'm', theme: 'light', ai: 1, bright: 1, exam: DATA.meta.examDate }, plan42: 1 };
}
let storageOK = true;
let S = (() => {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (raw) { const s = JSON.parse(raw); const d = defaultState(); const m = Object.assign(d, s, { plan42: s.plan42 || 0 }); m.settings = Object.assign(defaultState().settings, s.settings || {}, { ai: (s.settings || {}).ai || 0, bright: (s.settings || {}).bright || 0 }); return m; }
  } catch (e) { storageOK = false; }
  return defaultState();
})();
// 8 Oct 2026: the plan was re-based from Wed 7 Oct (45 days) to Sat 10 Oct (42 days): old Day n = new Day n-3,
// old Days 1-3 were merged into new Days 1/2/4/10/14. Move day-keyed progress once; quizzes keyed by
// passage/test/grammar id need no change. Also applied to restored backups.
function migratePlan42(st) {
  if (st.plan42) return st;
  const to = n => n >= 4 ? n - 3 : ({ 1: 1, 2: 4, 3: 10 })[n];
  const essays = {}, notes = {}, done = {}, quiz = {};
  Object.keys(st.essays || {}).forEach(k => {
    const m = k.match(/^E:(\d+)$/); if (!m) { essays[k] = st.essays[k]; return; }
    const dest = 'E:' + (+m[1] === 1 ? 14 : to(+m[1])), cur = st.essays[k];
    essays[dest] = essays[dest] ? Object.assign({}, essays[dest], { text: (essays[dest].text || '') + '\n\n' + (cur.text || '') }) : cur;
  });
  Object.keys(st.notes || {}).forEach(k => { const v = st.notes[k], dest = String(to(+k)); if (v) notes[dest] = notes[dest] ? notes[dest] + '\n' + v : v; });
  Object.keys(st.done || {}).forEach(k => { if (+k >= 4) done[+k - 3] = st.done[k]; });
  Object.keys(st.quiz || {}).forEach(k => { const m = k.match(/^(V|VR):(\d+)$/); if (!m || k === 'V:1') quiz[k] = st.quiz[k]; });
  Object.keys(st.timers || {}).forEach(k => { if (k.startsWith('B:')) delete st.timers[k]; });
  Object.assign(st, { essays, notes, done, quiz, plan42: 1 }); st.ui = Object.assign({}, st.ui, { step: {}, lastDay: null });
  return st;
}
migratePlan42(S);
// the AI look ships dark by default; switch existing installs over once (they can toggle back)
if (!S.settings.ai) { S.settings.theme = 'dark'; S.settings.ai = 1; }
// 8 Oct 2026: the default became the bright light theme; switch existing installs over once (dark stays one click away)
if (!S.settings.bright) { S.settings.theme = 'light'; S.settings.bright = 1; }
let saveT = null;
function save(now) {
  clearTimeout(saveT);
  const run = () => {
    try { localStorage.setItem(LS_KEY, JSON.stringify(S)); storageOK = true; }
    catch (e) { storageOK = false; }
    const w = document.getElementById('storageWarn'); if (w) w.hidden = storageOK;
  };
  if (now) run(); else saveT = setTimeout(run, 250);
}

/* ---------- utils ---------- */
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
const L = i => 'ABCD'[i];
function ico(n, c) { return '<svg class="ico' + (c ? ' ' + c : '') + '" aria-hidden="true"><use href="#i-' + n + '"/></svg>'; }
function wc(t) { const m = String(t || '').trim().match(/[A-Za-z0-9][A-Za-z0-9'’-]*/g); return m ? m.length : 0; }
function pct(a, b) { return b ? Math.round(100 * a / b) : 0; }
function dayDate(n) { const x = new Date(START); x.setDate(x.getDate() + n - 1); return x; }
function todayDate() { const n = new Date(); return new Date(n.getFullYear(), n.getMonth(), n.getDate()); }
function todayNum() { const diff = Math.round((todayDate() - START) / 86400000) + 1; return Math.min(NDAYS, Math.max(1, diff)); }
function rawTodayNum() { return Math.round((todayDate() - START) / 86400000) + 1; }
function examDate() { return new Date((S.settings.exam || DATA.meta.examDate) + 'T00:00:00'); }
function daysToExam() { return Math.round((examDate() - todayDate()) / 86400000); }
const TH_M = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
const TH_WD = ['อาทิตย์', 'จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 'ศุกร์', 'เสาร์'];
function thDate(dt, withWd) { return (withWd ? TH_WD[dt.getDay()] + ' ' : '') + dt.getDate() + ' ' + TH_M[dt.getMonth()] + ' ' + (dt.getFullYear() + 543); }
function fmtTime(sec) { sec = Math.max(0, Math.round(sec)); const h = Math.floor(sec / 3600), m = Math.floor(sec % 3600 / 60), s = sec % 60; return (h ? h + ':' + String(m).padStart(2, '0') : m) + ':' + String(s).padStart(2, '0'); }
function fileHref(file, page) { return encodeURI(file).replace(/#/g, '%23') + (page ? '#page=' + page : ''); }
function rng(seed) { let s = (seed >>> 0) || 1; return () => { s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; }; }
function shuffle(a, r) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
function toast(msg, ms = 2600) { const t = $('#toast'); t.textContent = msg; t.hidden = false; clearTimeout(toast.t); toast.t = setTimeout(() => t.hidden = true, ms); }
function beep() { try { const C = window.AudioContext || window.webkitAudioContext; const c = new C(); const o = c.createOscillator(); const g = c.createGain(); o.connect(g); g.connect(c.destination); o.frequency.value = 880; g.gain.value = .08; o.start(); setTimeout(() => { o.stop(); c.close(); }, 700); } catch (e) { } }
const canSpeak = 'speechSynthesis' in window;
function speak(t) { try { const u = new SpeechSynthesisUtterance(t); u.lang = 'en-US'; u.rate = .9; speechSynthesis.cancel(); speechSynthesis.speak(u); } catch (e) { } }
function download(name, text, type = 'text/plain') { const b = new Blob([text], { type: type + ';charset=utf-8' }); const a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = name; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500); }
function srcBadge(src) { const n = { book: 'หนังสือ', aelt: 'AELT PDF', image: 'Image PDF', guide: 'Guide DOCX', improved: 'Improved DOCX', app: 'ในแอป' }[src] || src; return `<span class="src s-${esc(src)}">${esc(n)}</span>`; }
function phaseChip(pid) { const p = PHASE[pid]; return `<span class="chip pchip" style="--pc:${PCOL[pid]}">${esc(p.name)}</span>`; }

/* ---------- timers (persist via end timestamps) ---------- */
function timerStart(key, minutes, label) {
  S.timers[key] = { end: Date.now() + minutes * 60000, dur: minutes * 60, label, paused: null };
  S.ui.activeTimer = key; save(); tick(); toast('เริ่มจับเวลา ' + minutes + ' นาที: ' + label);
}
function timerLeft(key) { const t = S.timers[key]; if (!t) return null; if (t.paused != null) return t.paused / 1000; return (t.end - Date.now()) / 1000; }
function timerPause(key) { const t = S.timers[key]; if (!t) return; if (t.paused == null) { t.paused = Math.max(0, t.end - Date.now()); } else { t.end = Date.now() + t.paused; t.paused = null; } save(); tick(); }
function timerStop(key) { delete S.timers[key]; if (S.ui.activeTimer === key) S.ui.activeTimer = null; save(); tick(); }
function tick() {
  const dock = $('#dock');
  const key = S.ui.activeTimer && S.timers[S.ui.activeTimer] ? S.ui.activeTimer : null;
  if (!key) { dock.hidden = true; }
  else {
    const t = S.timers[key]; const left = timerLeft(key);
    dock.hidden = false; dock.classList.toggle('low', left < 300);
    $('#dockLabel').textContent = t.label; $('#dockTime').textContent = left > 0 ? fmtTime(left) : 'หมดเวลา';
    $('#dockPause').textContent = t.paused != null ? 'ต่อ' : 'พัก';
    $('#dockPause').hidden = key.startsWith('T:');
    if (left <= 0 && !t.rang) { t.rang = true; save(); beep(); toast('หมดเวลา: ' + t.label, 6000); onTimerEnd(key); }
  }
  $$('[data-timer]').forEach(el => { const k = el.dataset.timer; const left = timerLeft(k); el.textContent = left == null ? '' : (left > 0 ? fmtTime(left) : 'หมดเวลา'); el.classList.toggle('low', left != null && left < 300); });
}
function onTimerEnd(key) { if (key.startsWith('T:')) { const st = S.quiz[key]; if (st && !st.done) { submitQuiz(key, true); } } }

/* ---------- actions (event delegation) ---------- */
const ACT = {};
const INP = {};
document.addEventListener('click', e => {
  const el = e.target.closest('[data-act]'); if (!el) return;
  const fn = ACT[el.dataset.act]; if (fn) { fn(el, e); }
});
document.addEventListener('input', e => { const el = e.target.closest('[data-inp]'); if (el && INP[el.dataset.inp]) INP[el.dataset.inp](el, e); });
document.addEventListener('change', e => { const el = e.target.closest('[data-chg]'); if (el && INP[el.dataset.chg]) INP[el.dataset.chg](el, e); });

ACT.dockPause = () => S.ui.activeTimer && timerPause(S.ui.activeTimer);
ACT.dockStop = () => { const k = S.ui.activeTimer; if (!k) return; if (k.startsWith('T:') && !confirm('หยุดนับเวลาข้อสอบ? (ข้อสอบยังไม่ถูกส่ง)')) return; timerStop(k); };
ACT.timer = el => { const k = el.dataset.key; const t = S.timers[k]; if (t && timerLeft(k) > 0) { S.ui.activeTimer = k; timerPause(k); } else timerStart(k, +el.dataset.min, el.dataset.label); };
ACT.speak = el => speak(el.dataset.w);
ACT.go = el => { location.hash = el.dataset.href; };
ACT.scrollTo = el => { const t = document.getElementById(el.dataset.id); if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' }); };
ACT.print = () => window.print();

/* ---------- block status ---------- */
function blockAuto(d, k) {
  const day = DAY(d);
  switch (k) {
    case 'vocab': return !!(S.quiz['V:' + d] && S.quiz['V:' + d].done);
    case 'reading': return day.reading ? day.reading.passages.every(pid => S.quiz['R:' + pid] && S.quiz['R:' + pid].done) : false;
    case 'writing': { const g = day.grams.every(id => (S.quiz['G:' + id] || {}).done); const e = S.essays['E:' + d]; return !!(g && (!day.task || (e && wc(e.text) >= 20))); }
    case 'errors': return !!(S.notes[d] && S.notes[d].trim().length > 3);
    case 'test': return !!(S.quiz['T:' + day.test] && S.quiz['T:' + day.test].done);
    case 'review': return !!(S.quiz['T:' + day.test] && S.quiz['T:' + day.test].done && S.notes[d] && S.notes[d].trim().length > 3);
    case 'essay': { const e = S.essays['E:' + d]; return !!(e && wc(e.text) >= 200); }
    case 'weekly': { const it = wrongItems({ days: day.review.days }); return it.length > 0 && it.every(x => S.retry[x.q.id] || S.resolved[x.q.id]); }
    case 'vocabreview': return !!(S.quiz['VR:' + d] && S.quiz['VR:' + d].done);
    case 'retry': { const it = wrongItems({}); const n = it.filter(x => S.retry[x.q.id]).length; return it.length > 0 && n >= Math.min(30, it.length); }
  }
  return false;
}
function blockDone(d, k) { const m = S.done[d] && S.done[d][k]; if (m === true || m === false) return m; return blockAuto(d, k); }
function dayProgress(d) { const bl = DAY(d).blocks; const n = bl.filter(b => blockDone(d, b.k)).length; return { n, total: bl.length, done: n === bl.length }; }
ACT.toggleBlock = el => { const d = +el.dataset.d, k = el.dataset.k; S.done[d] = S.done[d] || {}; S.done[d][k] = !blockDone(d, k); save(); render(true); };
