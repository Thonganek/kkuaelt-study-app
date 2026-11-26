/* ============================================================
   Full course edition: Day 1–42 at your own pace — no dates, no time limits.
   Timers are stopwatches (time used), tests never submit on their own.
   ============================================================ */
function calendarMode() { return false; }
function dayBanners(d) {
  return d === NDAYS && allDaysDone() ? `<div class="banner info">${ico('spark')}<span>ครบ ${NDAYS} Day แล้ว — ใช้หน้า “ข้อผิดพลาด” และ “คำศัพท์” ทบทวนต่อได้</span></div>` : '';
}

/* ---------- stopwatch timers ---------- */
function swUsed(t) { return t ? (t.acc || 0) + (t.run ? Date.now() - t.run : 0) : 0; }
function timerStart(key, minutes, label) {
  S.timers[key] = { acc: 0, run: Date.now(), label };
  S.ui.activeTimer = key; save(); tick(); toast('เริ่มจับเวลา (ไม่จำกัดเวลา): ' + label);
}
function timerLeft(key) { const t = S.timers[key]; return t ? swUsed(t) / 1000 : null; }
function timerPause(key) {
  const t = S.timers[key]; if (!t) return;
  if (t.run) { t.acc = swUsed(t); t.run = null; } else t.run = Date.now();
  save(); tick();
}
function timerStop(key) {
  const t = S.timers[key];
  if (t && S.quiz[key]) S.quiz[key].usedSec = Math.round(swUsed(t) / 1000);
  delete S.timers[key]; if (S.ui.activeTimer === key) S.ui.activeTimer = null; save(); tick();
}
function onTimerEnd() { }
function tick() {
  const dock = $('#dock');
  const key = S.ui.activeTimer && S.timers[S.ui.activeTimer] ? S.ui.activeTimer : null;
  if (!key) dock.hidden = true;
  else {
    const t = S.timers[key];
    dock.hidden = false; dock.classList.remove('low');
    $('#dockLabel').textContent = t.label; $('#dockTime').textContent = fmtTime(swUsed(t) / 1000);
    $('#dockPause').textContent = t.run ? 'พัก' : 'ต่อ'; $('#dockPause').hidden = false;
  }
  $$('[data-timer]').forEach(el => { const t = S.timers[el.dataset.timer]; el.textContent = t ? 'ใช้ไป ' + fmtTime(swUsed(t) / 1000) + (t.run ? '' : ' (พัก)') : ''; el.classList.remove('low'); });
}
function timerBtn(key, min, label) {
  const t = S.timers[key];
  const txt = !t ? ico('clock') + ' จับเวลา (แนะนำ ≈ ' + min + ' นาที)' : t.run ? ico('pause') + ' พัก' : ico('play') + ' จับเวลาต่อ';
  return `<span class="row"><span class="small" data-timer="${esc(key)}"></span><button class="btn sm" data-act="timer" data-key="${esc(key)}" data-min="${min}" data-label="${esc(label)}">${txt}</button></span>`;
}
ACT.timer = el => {
  const k = el.dataset.key;
  if (S.timers[k]) { S.ui.activeTimer = k; timerPause(k); } else timerStart(k, +el.dataset.min, el.dataset.label);
  const span = el.closest('span.row'); if (span) span.outerHTML = timerBtn(k, +el.dataset.min, el.dataset.label);
  tick();
};
ACT.startTest = el => {
  const tid = el.dataset.t; const key = 'T:' + tid; const st = qstate(key);
  if (!st.end) { st.startAt = Date.now(); st.end = st.startAt; S.timers[key] = { acc: 0, run: Date.now(), label: DATA.tests[tid].title }; S.ui.activeTimer = key; }
  save(true); if (location.hash === '#/test/' + tid) render(); else location.hash = '#/test/' + tid;
};
ACT.testExit = el => {
  const k = S.ui.activeTimer; if (k && k.startsWith('T:') && S.timers[k] && S.timers[k].run) timerPause(k);
  location.hash = +el.dataset.d ? '#/day/' + el.dataset.d : '#/plan';
};
// opening an unfinished test starts its stopwatch again where it stopped; closing the page stops it
function resumeTestClock() {
  const m = location.hash.match(/^#\/test\/([A-Za-z0-9]+)/); if (!m || !DATA.tests[m[1]]) return;
  const key = 'T:' + m[1]; const st = S.quiz[key]; if (!st || !st.end || st.done) return;
  if (!S.timers[key]) S.timers[key] = { acc: (st.usedSec || 0) * 1000, run: null, label: DATA.tests[m[1]].title };
  if (!S.timers[key].run) S.timers[key].run = Date.now();
  S.ui.activeTimer = key; save(); tick();
}
window.addEventListener('hashchange', resumeTestClock);
window.addEventListener('pagehide', () => {
  Object.keys(S.timers).forEach(k => { const t = S.timers[k]; if (k.startsWith('T:') && t.run) { t.acc = swUsed(t); t.run = null; } });
  save(true);
});

/* ---------- one-time upgrades of saved progress ---------- */
// countdown timers from earlier editions become paused stopwatches with the time already used
function upgradeTimers(state) {
  for (const [k, t] of Object.entries(state.timers || {})) {
    if (t && t.acc == null && t.end != null) {
      const left = t.paused != null ? t.paused : Math.max(0, t.end - Date.now());
      state.timers[k] = { acc: Math.max(0, (t.dur || 0) * 1000 - left), run: null, label: t.label };
    }
  }
  return state;
}
// each vocabulary day gained 8–9 academic words, so the old vocabulary quizzes no longer match.
// Archive them, keep the step ticked as done, and let the new quiz start fresh.
function upgradeVocabulary(state) {
  if (state.vocabRevision === DATA.meta.vocabRevision) return state;
  const archive = { revision: state.vocabRevision || '740-words', quiz: {}, retry: {}, resolved: {} };
  for (const key of Object.keys(state.quiz || {})) {
    const m = key.match(/^(V|VR):(\d+)$/); if (!m) continue;
    const step = m[1] === 'V' ? 'vocab' : 'vocabreview';
    if (state.quiz[key].done) { const dd = (state.done ||= {})[m[2]] ||= {}; if (dd[step] == null) dd[step] = true; }
    archive.quiz[key] = state.quiz[key]; delete state.quiz[key];
  }
  for (const kind of ['retry', 'resolved']) {
    for (const key of Object.keys(state[kind] || {})) {
      if (/^V(R)?\d+s\d+\./.test(key)) { archive[kind][key] = state[kind][key]; delete state[kind][key]; }
    }
  }
  if (Object.keys(archive.quiz).length) (state.vocabHistory ||= []).push(archive);
  state.vocabRevision = DATA.meta.vocabRevision;
  return state;
}
S = upgradeVocabulary(upgradeTimers(S));
save(true);
resumeTestClock();

/* ---------- header / side card / runway ---------- */
function updateCountdown() {
  const done = DAYS.filter(x => dayProgress(x.d).done).length; const tn = todayNum(); const pr = dayProgress(tn);
  $('#countdown').innerHTML = `<span class="pulse"></span>ไม่จำกัดเวลา · <b>${done}/${NDAYS}</b> Day`;
  const sc = $('#sideCard'); if (!sc) return;
  sc.innerHTML = `<div class="lbl">หลักสูตรเต็ม · ไม่จำกัดเวลา</div><div class="big">${done}<small style="font-size:1rem;font-weight:500"> / ${NDAYS} Day</small></div><div class="lbl">ทำตามจังหวะของตัวเอง</div><div class="bar"><i style="width:${pct(done, NDAYS)}%"></i></div><div class="lbl">${allDaysDone() ? 'ครบทุก Day' : `ต่อที่ Day ${tn} (${pr.n}/${pr.total} ขั้น)`}</div>`;
}
function runway(d) {
  const tn = rawTodayNum(); let cells = '';
  for (const x of DAYS) {
    const pr = dayProgress(x.d);
    const cls = ['rw', x.type === 'test' ? 'test' : x.type === 'mock' ? 'mock' : x.type === 'sunday' ? 'sun' : '', pr.done ? 'done' : '', x.d === d ? 'cur' : '', x.d === tn ? 'today' : ''].filter(Boolean).join(' ');
    cells += `<a class="${cls}" href="#/day/${x.d}" title="Day ${x.d} · ${pr.done ? 'เสร็จแล้ว' : pr.n + '/' + pr.total + ' ขั้น'} · ${esc(x.title)}" aria-label="Day ${x.d}"></a>`;
  }
  const lab = (n, end) => `<span style="grid-column:${end ? (n - 5) + ' / ' + (n + 1) : n + ' / span 7'};${end ? 'text-align:right' : ''}">Day ${n}</span>`;
  return `<div class="runway"><div class="rw-head"><div class="tile-label">${ico('calendar')} เส้นทาง ${NDAYS} Day · ไม่จำกัดเวลา</div><div class="rw-legend"><span><i style="background:var(--sky)"></i>Reading Test</span><span><i style="background:var(--teal)"></i>Mock</span><span><i style="background:var(--emerald)"></i>Essay + ทวนสัปดาห์</span><span><i style="background:var(--surface-3)"></i>วันเรียนปกติ</span></div></div>
  <div class="rw-track" style="--n:${NDAYS}">${cells}<span class="rw-flag">${ico('flag')}<span>จบหลักสูตร</span></span></div>
  <div class="rw-scale" style="--n:${NDAYS}">${[1, 15, 29].map(n => lab(n)).join('')}${lab(NDAYS, true)}</div></div>`;
}

/* ---------- to-do ---------- */
function viewTodo() {
  const cd = curDay(); const all = allDaysDone();
  const doneN = DAYS.filter(x => dayProgress(x.d).done).length;
  const left = DAYS.filter(x => !dayProgress(x.d).done).map(x => ({ d: x.d, min: remainMin(x.d) }));
  const steps = left.reduce((s, x) => s + DAY(x.d).blocks.filter(b => !blockDone(x.d, b.k)).length, 0);
  const mins = left.reduce((s, x) => s + x.min, 0);
  let h = `<div class="card"><div class="row"><div><div class="daynum">ไม่จำกัดเวลา · ไม่ผูกกับวันที่ · ทำเสร็จเมื่อไรก็ติ๊ก</div><h1>ที่ต้องทำ</h1></div><span class="spacer"></span>${all ? `<span class="chip ok">${ico('spark')} ครบทั้ง ${NDAYS} Day แล้ว</span>` : `<a class="btn pri" href="#/day/${cd}">${ico('play')} ทำต่อ: Day ${cd} — ${esc(DAY(cd).title)}</a>`}</div>
  <p class="muted">หน้า “วันนี้” เปิด Day แรกที่ยังไม่เสร็จให้เอง จะทำวันละกี่ Day ก็ได้ ขั้นที่ทำในแอป (ส่ง quiz / ส่งข้อสอบ / เขียนงาน / จดบันทึก) ระบบนับให้อัตโนมัติ</p>
  <div class="grid g4" style="margin-top:10px">
    <div class="kpi"><div class="v">${doneN}/${NDAYS}</div><div class="l">Day ที่ทำเสร็จแล้ว</div><progress max="${NDAYS}" value="${doneN}"></progress></div>
    <div class="kpi"><div class="v">${left.length}</div><div class="l">Day ที่ยังต้องทำ · ${steps} ขั้น</div></div>
    <div class="kpi"><div class="v">${Math.round(mins / 6) / 10}<small> ชม.</small></div><div class="l">เวลาโดยประมาณของงานที่เหลือ (ไม่ใช่เวลาจำกัด)</div></div>
    <div class="kpi"><div class="v">${ALLWORDS.length}</div><div class="l">คำศัพท์ในหลักสูตร (Academic +${DATA.meta.academicWords})</div></div>
  </div></div>`;
  const upto = Math.max(1, cd - 1);
  h += `<div class="card"><div class="row"><h2 style="margin:0">เลือกสถานะแต่ละ Day</h2><span class="spacer"></span><label class="small row" style="gap:6px">ทำเสร็จแล้วตั้งแต่ Day 1 ถึง <select id="upto" class="sel">${DAYS.map(x => `<option value="${x.d}" ${x.d === upto ? 'selected' : ''}>Day ${x.d}</option>`).join('')}</select></label><button class="btn sm" data-act="markUpTo">${ico('check')} ติ๊กเสร็จทั้งช่วง</button></div>
  <p class="small muted">กดปุ่ม ✓ ของแต่ละช่องเพื่อสลับ “เสร็จแล้ว / ยังไม่เสร็จ” · กดที่ตัวเลขเพื่อเปิด Day นั้น · 1 แถว = 1 รอบ (Reading Test → Essay → วันเรียนปกติ 5 Day)</p>${dayGrid()}</div>`;
  if (left.length) {
    const first = left.slice(0, 7), rest = left.slice(7);
    h += `<div class="card"><h2>งานที่ยังต้องทำ (${left.length} Day)</h2><p class="small muted">เรียงตาม Day · ขั้นสีฟ้ากดเพื่อเริ่มทำได้ทันที · ขั้นสีเขียวทำแล้ว · นาทีเป็นค่าประมาณ</p>${first.map(x => todoDay(x, cd)).join('')}${rest.length ? `<details class="more"><summary>ดูอีก ${rest.length} Day (Day ${rest[0].d}–${rest[rest.length - 1].d})</summary>${rest.map(x => todoDay(x, cd)).join('')}</details>` : ''}</div>`;
  }
  return h;
}

/* ---------- plan ---------- */
function viewPlan() {
  const tn = rawTodayNum(); const f = S.ui.planF || 'all';
  const list = t => DAYS.filter(x => x.type === t).map(x => x.d).join(', ');
  let h = `<div class="card"><div class="row"><div><div class="daynum">KKU-AELT · หลักสูตรเต็ม · ไม่จำกัดเวลา</div><h1>หลักสูตร ${NDAYS} Day (Day 1–${NDAYS})</h1></div><span class="spacer"></span><button class="btn noprint" data-act="print">${ico('printer')} พิมพ์ตาราง</button><button class="btn noprint" data-act="csv">${ico('download')} CSV (Excel)</button></div>
  <p class="muted">Reading 60% + Writing 40% · ทำตามลำดับ Day ตามจังหวะของตัวเอง ไม่มีวันหมดเขต ข้อสอบและแบบฝึกไม่ตัดเวลา · นาทีในตารางเป็นค่าประมาณ ใช้วางแผนเท่านั้น</p>
  <div class="grid g4" style="margin-top:10px">
    <div class="kpi"><div class="v">${ALLWORDS.length}</div><div class="l">คำศัพท์ (AWL + ศัพท์หัวข้อ ${ALLWORDS.length - DATA.meta.academicWords} + Academic ${DATA.meta.academicWords})</div></div>
    <div class="kpi"><div class="v">${Object.keys(DATA.passages).length}</div><div class="l">บทอ่าน (รายวัน ${Object.keys(DATA.passages).filter(x => x.startsWith('W')).length} + ชุดเต็ม ${Object.keys(DATA.tests).length}×6)</div></div>
    <div class="kpi"><div class="v">${Object.values(DATA.passages).reduce((s, p) => s + p.questions.length, 0)}</div><div class="l">ข้อ Reading พร้อมเฉลยภาษาไทย</div></div>
    <div class="kpi"><div class="v">${Object.keys(DATA.grammar).length}</div><div class="l">บท Grammar พร้อม quiz</div></div>
  </div></div>`;
  h += `<div class="card"><h2>รูปแบบของแต่ละ Day</h2><div class="tablewrap"><table class="t"><tr><th>ประเภท</th><th>ลำดับขั้น</th></tr>
  <tr><td>วันเรียนปกติ</td><td>คำศัพท์ → Reading → Writing/Grammar → สมุดข้อผิดพลาด</td></tr>
  <tr><td>Reading Test <span class="small muted">(Day ${list('test')})</span></td><td>Reading Test เต็มชุด → คำศัพท์ → ตรวจผล</td></tr>
  <tr><td>Essay + ทวนสัปดาห์ <span class="small muted">(Day ${list('sunday')})</span></td><td>Essay เต็ม → ทำซ้ำข้อผิด → ทวนศัพท์</td></tr>
  <tr><td>รวมทักษะ <span class="small muted">(Day ${list('integration')})</span></td><td>คำศัพท์ → Reading บทสั้น/ยาว → Essay เต็ม → ข้อผิด</td></tr>
  <tr><td>Full Mock <span class="small muted">(Day ${list('mock')})</span></td><td>Reading Test → Essay → ตรวจผล → คำศัพท์</td></tr>
  <tr><td>ทบทวน <span class="small muted">(Day ${list('review')}, ${list('light')})</span></td><td>ทวนศัพท์ → ทำข้อผิดซ้ำ → Writing</td></tr></table></div></div>`;
  h += `<div class="card"><h2>ช่วงการเรียน</h2><div class="tablewrap"><table class="t"><tr><th>ช่วง</th><th>Day</th><th>เป้าหมาย</th></tr>${PHASES.map(p => `<tr><td>${phaseChip(p.id)} ${esc(p.th)}</td><td>${esc(p.range)}</td><td>${esc(p.goal)}</td></tr>`).join('')}</table></div></div>`;
  h += `<div class="card noprint"><h2>สถานะรายวัน</h2>${dayGrid()}</div>`;
  const fb = [['all', 'ทั้งหมด']].concat(PHASES.map(p => [p.id, p.name]));
  h += `<div class="card"><h2>ตารางราย Day</h2><div class="filters noprint">${fb.map(([k, l]) => `<button class="${f === k ? 'on' : ''}" data-act="planF" data-f="${k}">${esc(l)}</button>`).join('')}</div>
  <div class="tablewrap"><table class="t plan"><tr><th>Day</th><th>หัวข้อ</th><th>อ่านอะไร (เลขหน้าในหนังสือ)</th><th>ศัพท์</th><th>Reading</th><th>Writing</th><th>ข้อสอบใน Day นี้</th><th>≈ นาที</th><th>สถานะ</th></tr>`;
  DAYS.filter(d => f === 'all' || d.phase === f).forEach(d => {
    const pr = dayProgress(d.d);
    h += `<tr class="${d.d === tn ? 'today' : ''} ${pr.done ? 'done' : ''}"><td><a class="daylink" href="#/day/${d.d}">Day ${d.d}</a>${phaseChip(d.phase)}</td><td><b>${esc(d.title)}</b></td><td><ul style="margin:0;padding-left:1rem">${d.read.map(it => `<li>${esc(shortRead(it))}</li>`).join('')}</ul></td><td>${esc(vocabShort(d.d))}</td><td>${esc(readingShort(d))}</td><td>${esc(taskShort(d))}${d.grams.map(id => DATA.grammar[id] ? `<div class="small muted">Grammar: ${esc(DATA.grammar[id].title_th)}</div>` : '').join('')}</td><td class="small">${esc(examShort(d.d))}</td><td>${d.minutes}</td><td class="nowrap">${pr.n}/${pr.total} ${chkBtn(d.d, pr)}</td></tr>`;
  });
  return h + `</table></div></div>`;
}
ACT.csv = () => {
  const rows = [['Day', 'ช่วง', 'หัวข้อ', 'อ่านอะไร', 'ศัพท์', 'Reading', 'Writing', 'Grammar', 'ข้อสอบใน Day นี้', 'นาที (ประมาณ)', 'สถานะ']];
  DAYS.forEach(d => { const p = dayProgress(d.d); rows.push([d.d, PHASE[d.phase].name, d.title, d.read.map(shortRead).join(' | '), vocabShort(d.d), readingShort(d), taskShort(d), d.grams.map(id => DATA.grammar[id] ? DATA.grammar[id].title_th : id).join(' + '), examShort(d.d), d.minutes, p.done ? 'เสร็จแล้ว' : `ยังไม่เสร็จ (${p.n}/${p.total})`]); });
  download('KKU-AELT_Full_Course.csv', '﻿' + rows.map(r => r.map(c => '"' + String(c).replace(/"/g, '""') + '"').join(',')).join('\r\n'), 'text/csv');
};

/* ---------- vocabulary: filter for the 300 academic words ---------- */
function vocabFiltered() {
  const q = (S.ui.vq || '').trim().toLowerCase(); const f = S.ui.vf || 'all'; const dd = +(S.ui.vd || 0);
  return ALLWORDS.filter(w => (!dd || w.day === dd) && (f === 'all' || (f === 'avl' && w.src === 'AVL') || (f === 'star' && S.vstat[w.w] === 2) || (f === 'known' && S.vstat[w.w] === 1) || (f === 'new' && !S.vstat[w.w])) && (!q || w.w.toLowerCase().includes(q) || (w.th || '').includes(q) || (w.fam || '').toLowerCase().includes(q)));
}

/* ---------- settings / backup ---------- */
function viewSettings() {
  const st = S.settings;
  return `<div class="card"><h1>ตั้งค่าและสำรองข้อมูล</h1>
  <h3>หลักสูตร</h3><p><b>หลักสูตรเต็ม ${NDAYS} Day · ไม่จำกัดเวลา</b> — ไม่ผูกกับวันที่ หน้า “วันนี้” เปิด Day แรกที่ยังทำไม่เสร็จ ข้อสอบไม่ตัดเวลาและไม่ส่งอัตโนมัติ</p>
  <h3>ธีม</h3><div class="row">${[['light', 'Iron Man · สว่าง'], ['dark', 'JARVIS HUD · มืด']].map(([v, l]) => `<button class="btn sm ${(st.theme === 'dark' ? 'dark' : 'light') === v ? 'pri' : ''}" data-act="setTheme" data-v="${v}">${l}</button>`).join('')}</div>
  <h3>ขนาดตัวอักษร</h3><div class="row">${[['s', 'เล็ก'], ['m', 'ปกติ'], ['l', 'ใหญ่'], ['xl', 'ใหญ่มาก']].map(([v, l]) => `<button class="btn sm ${st.font === v ? 'pri' : ''}" data-act="setFont" data-v="${v}">${l}</button>`).join('')}</div>
  <h3>สำรอง / กู้คืน</h3><p class="small muted">ข้อมูลทั้งหมด (คำตอบ งานเขียน บันทึก ดาวคำศัพท์) เก็บในเบราว์เซอร์นี้เท่านั้น ถ้าเปลี่ยนเครื่อง/เบราว์เซอร์ หรือล้างข้อมูลเบราว์เซอร์ ข้อมูลจะหาย — สำรองเป็นไฟล์ JSON เป็นระยะ · กู้คืนจากไฟล์สำรองของฉบับ 42 วันเดิมได้</p>
  <div class="row"><button class="btn pri" data-act="backup">${ico('download')} สำรองข้อมูล (.json)</button><label class="btn">${ico('upload')} กู้คืนจากไฟล์<input type="file" accept=".json,application/json" data-chg="restore" hidden></label><button class="btn" data-act="resetAll" style="color:var(--bad)">ลบข้อมูลทั้งหมด</button></div>
  <p class="small">สถานะการบันทึก: ${storageOK ? '<span class="chip ok">บันทึกอัตโนมัติได้</span>' : '<span class="chip no">บันทึกอัตโนมัติไม่ได้ — ใช้ปุ่มสำรองข้อมูล</span>'}</p></div>`;
}
ACT.backup = () => { const d = new Date(); download(`kkuaelt-full-backup-${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}.json`, JSON.stringify(S), 'application/json'); toast('ดาวน์โหลดไฟล์สำรองแล้ว'); };
INP.restore = el => {
  const f = el.files && el.files[0]; if (!f) return;
  const rd = new FileReader();
  rd.onload = () => {
    try {
      const s = JSON.parse(rd.result);
      if (!s || s.v !== 2) throw new Error('รูปแบบไฟล์ไม่ถูกต้อง');
      if (s.planId && s.planId !== DATA.meta.planId) throw new Error('ไฟล์นี้เป็นของแผนอื่น (เช่น แผน 6 วัน)');
      if (!confirm('แทนที่ข้อมูลปัจจุบันด้วยไฟล์สำรอง?')) return;
      S = upgradeVocabulary(upgradeTimers(migratePlan42(Object.assign(defaultState(), s, { plan42: s.plan42 || 0, vocabRevision: s.vocabRevision || 0 }))));
      S.settings = Object.assign(defaultState().settings, s.settings || {}, { ai: 1, bright: 1 });
      save(true); applySettings(); render(); toast('กู้คืนข้อมูลแล้ว');
    } catch (e) { alert('กู้คืนไม่ได้: ' + e.message); }
  };
  rd.readAsText(f);
};
