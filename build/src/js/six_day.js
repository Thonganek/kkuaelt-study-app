/* Six-day edition: fixed study window, isolated progress, full optional library. */
SHORT.essay = "Writing (Essay)";
function planEndDate() { return new Date(DATA.meta.end + 'T00:00:00'); }
function daysToPlanEnd() { return Math.round((planEndDate() - todayDate()) / 86400000); }
function dayBanners(d) {
  if (calendarMode() && calRawNum() < 1 && d === 1) return '<div class="banner info">แผนเริ่มพฤหัสบดี 8 ต.ค. 2569 — แสดง Day 1 ล่วงหน้า</div>';
  if (calendarMode() && calRawNum() > NDAYS) return '<div class="banner info">สิ้นสุดช่วง 8–13 ต.ค. 2569 แล้ว — เปิดทบทวนทั้ง 6 วันต่อได้ หรือนับตามความคืบหน้าในตั้งค่า</div>';
  return '';
}
function runway(d) {
  return `<div class="tile-label">${ico('calendar')} เส้นทาง 6 วัน · 8–13 ตุลาคม 2569</div><div class="six-runway">${DAYS.map(x => `<a class="${x.d === d ? 'cur' : ''} ${dayProgress(x.d).done ? 'done' : ''}" href="#/day/${x.d}"><b>Day ${x.d}</b><small>${x.dateTh.replace(' 2569', '')}</small></a>`).join('')}</div>`;
}
function updateCountdown() {
  const n = daysToPlanEnd(), done = DAYS.filter(x => dayProgress(x.d).done).length;
  $('#countdown').innerHTML = '<span class="pulse"></span>8–13 ต.ค. 2569 · <b>6 วัน</b>';
  const sc = $('#sideCard');
  if (sc) sc.innerHTML = `<div class="lbl">ช่วงอ่านหนังสือ</div><div class="big">8–13 <small style="font-size:1rem">ต.ค.</small></div><div class="lbl">2569 · ${n > 0 ? 'เหลือ ' + n + ' วันถึงวันสุดท้าย' : n === 0 ? 'วันสุดท้ายของแผน' : 'สิ้นสุดช่วงตามปฏิทินแล้ว'}</div><div class="bar"><i style="width:${pct(done, NDAYS)}%"></i></div><div class="lbl">ทำครบ ${done}/6 วัน · ${allDaysDone() ? 'ครบทุก Day' : 'ทำต่อ Day ' + todayNum()}</div>`;
}
function viewTodo() {
  const cd = curDay(), left = DAYS.filter(x => !dayProgress(x.d).done);
  const minutes = left.reduce((s, x) => s + remainMin(x.d), 0);
  let h = `<div class="card"><div class="row"><div><div class="daynum">8–13 ตุลาคม 2569 · แผนเร่งรัด 6 วัน</div><h1>ที่ต้องทำ</h1></div><span class="spacer"></span>${left.length ? `<a class="btn pri" href="#/day/${cd}">${ico('play')} ทำต่อ Day ${cd}</a>` : '<span class="chip ok">ครบทั้ง 6 วันแล้ว</span>'}</div><p class="muted">ติ๊กตามงานที่ทำจริง หน้า “วันนี้” เปิด Day แรกที่ยังไม่เสร็จให้เอง และเปิดทบทวนหลังวันที่ 13 ต.ค. ได้</p><div class="grid g4"><div class="kpi"><div class="v">${NDAYS - left.length}/6</div><div class="l">Day ที่เสร็จแล้ว</div></div><div class="kpi"><div class="v">${left.length}</div><div class="l">Day ที่เหลือ</div></div><div class="kpi"><div class="v">${minutes}</div><div class="l">นาทีที่ยังต้องใช้</div></div><div class="kpi"><div class="v">13 ต.ค.</div><div class="l">วันสุดท้ายของแผน 2569</div></div></div></div>`;
  h += `<div class="card"><div class="row"><h2>เลือกสถานะรายวัน</h2><span class="spacer"></span><label>เสร็จถึง <select id="upto" class="sel">${DAYS.map(x => `<option value="${x.d}" ${x.d === Math.max(1, cd - 1) ? 'selected' : ''}>Day ${x.d}</option>`).join('')}</select></label><button class="btn sm" data-act="markUpTo">ติ๊กเสร็จทั้งช่วง</button></div>${dayGrid()}</div>`;
  if (left.length) h += `<div class="card"><h2>งานที่เหลือในช่วง 8–13 ต.ค.</h2>${left.map(x => todoDay({d: x.d, min: remainMin(x.d)}, cd)).join('')}</div>`;
  return h;
}
function viewPlan() {
  const filter = S.ui.planF || 'all';
  let h = `<div class="card"><div class="row"><div><div class="daynum">KKU-AELT · 8–13 ตุลาคม 2569</div><h1>ตารางอ่าน 6 วัน</h1></div><span class="spacer"></span><button class="btn noprint" data-act="print">${ico('printer')} พิมพ์ตาราง</button><button class="btn noprint" data-act="csv">${ico('download')} CSV (Excel)</button></div><p class="muted">ทุกวันเริ่มจาก คำศัพท์ 100 คำ (75 นาที) → Reading → Writing → ทบทวนและจดข้อผิด · Day 5 เรียนศัพท์ก่อนเริ่ม Mock Reading 120 + Writing 60 นาทีต่อเนื่อง · แบ่งพักระหว่างขั้นได้</p><div class="grid g4"><div class="kpi"><div class="v">${DATA.meta.coreWords}</div><div class="l">ศัพท์ใหม่ ${DATA.meta.wordsPerDay} คำ/วัน × 6 วัน</div></div><div class="kpi"><div class="v">${planCum().p}</div><div class="l">บทอ่านในแผน รวม Test/Mock</div></div><div class="kpi"><div class="v">2</div><div class="l">Essay เต็ม · Day 4 และ Day 5</div></div><div class="kpi"><div class="v">${DAYS.reduce((s,x) => s+x.minutes, 0)}</div><div class="l">นาทีรวมทั้งแผน</div></div></div><p class="small muted">คลังเพิ่มเติมยังมีศัพท์ 740 คำ บทอ่าน 85 บท และ Grammar 30 บท เลือกทวนตามจุดอ่อนหลังจบงานหลักได้</p></div>`;
  h += `<div class="card"><h2>สถานะและปฏิทิน</h2>${dayGrid()}${runway(0)}</div>`;
  h += `<div class="card"><h2>ตารางรายวัน</h2><div class="filters noprint">${[['all','ทั้งหมด'], ...PHASES.map(p => [p.id,p.name])].map(([k,l]) => `<button class="${filter === k ? 'on' : ''}" data-act="planF" data-f="${k}">${esc(l)}</button>`).join('')}</div><div class="tablewrap"><table class="t plan"><tr><th>Day / วันที่</th><th>หัวข้อ</th><th>อ่านอะไร / หน้า</th><th>ศัพท์</th><th>Reading</th><th>Writing / Grammar</th><th>ลำดับ (นาที)</th><th>รวม</th><th>สถานะ</th></tr>${DAYS.filter(x => filter === 'all' || x.phase === filter).map(x => { const p = dayProgress(x.d); return `<tr><td><a href="#/day/${x.d}">Day ${x.d}</a><div class="small">${esc(x.wd)} ${x.dateTh}</div></td><td><b>${esc(x.title)}</b></td><td><ul>${x.read.map(r => `<li>${esc(shortRead(r))}</li>`).join('')}</ul></td><td>${esc(vocabShort(x.d))}</td><td>${esc(readingShort(x))}</td><td>${esc(taskShort(x))}${x.grams.map(g => `<div class="small">${esc(DATA.grammar[g].title_th)}</div>`).join('')}</td><td>${x.blocks.map(b => `${esc(SHORT[b.k])} ${b.min}`).join(' → ')}</td><td>${x.minutes}</td><td>${chkBtn(x.d,p)}</td></tr>`; }).join('')}</table></div></div>`;
  h += `<div class="card"><h2>คลังฝึกเพิ่มเติม</h2><p class="small muted">เนื้อหาทั้งหมดจากฉบับเดิม ใช้เพิ่มได้ตามเวลาที่มี</p><div class="row">${Object.values(DATA.tests).map(t => `<a class="btn sm" href="#/test/${t.id}">${esc(t.id)} · ${t.day ? 'Day ' + t.day : 'เพิ่มเติม'}</a>`).join('')}<a class="btn sm" href="#/vocab">ศัพท์ 740 คำ</a><a class="btn sm" href="#/guide/reading">บทเรียน Reading</a><a class="btn sm" href="#/writing">Writing Studio</a></div><details class="more"><summary>Grammar ทั้ง 30 บท พร้อม quiz</summary>${Object.keys(DATA.grammar).map(id => `<details class="more"><summary>${id} · ${esc(DATA.grammar[id].title_th)}</summary>${grammarBox(id)}</details>`).join('')}</details><details class="more"><summary>Reading รายวันทั้งหมด 31 บท</summary>${Object.keys(DATA.passages).filter(id => id.startsWith('W')).map(id => `<details class="more"><summary>${id} · ${esc(DATA.passages[id].title)}</summary>${renderPassage(id)}${renderQuiz('R:' + id)}</details>`).join('')}</details></div>`;
  return h;
}
function reviewWords(d) {
  const words = ALLWORDS.filter(w => w.day > 0 && w.day <= d);
  return {all: words, starred: words.filter(w => S.vstat[w.w] === 2), rest: words.filter(w => S.vstat[w.w] !== 2)};
}
// Keep reading/writing progress when replacing the earlier 20-word vocabulary sets.
function upgradeVocabulary(state) {
  if (state.vocabRevision === DATA.meta.vocabRevision) return state;
  const archive = {revision: state.vocabRevision || '80-word-plan', quiz: {}, done: {}, retry: {}, resolved: {}};
  for (const key of Object.keys(state.quiz || {})) {
    if (/^(V|VR):/.test(key)) { archive.quiz[key] = state.quiz[key]; delete state.quiz[key]; }
  }
  for (const [day, blocks] of Object.entries(state.done || {})) {
    for (const key of ['vocab', 'vocabreview']) {
      if (Object.hasOwn(blocks, key)) {
        (archive.done[day] ||= {})[key] = blocks[key]; delete blocks[key];
      }
    }
  }
  for (const kind of ['retry', 'resolved']) {
    for (const key of Object.keys(state[kind] || {})) {
      if (/^V(R)?\d+s\d+\./.test(key)) { archive[kind][key] = state[kind][key]; delete state[kind][key]; }
    }
  }
  if (['quiz', 'done', 'retry', 'resolved'].some(k => Object.keys(archive[k]).length)) {
    (state.vocabHistory ||= []).push(archive);
  }
  state.vocabRevision = DATA.meta.vocabRevision;
  return state;
}
S = upgradeVocabulary(S);
save(true);
function vocabFiltered() {
  const q = (S.ui.vq || '').trim().toLowerCase(), f = S.ui.vf || 'all', dd = +(S.ui.vd || 0);
  return ALLWORDS.filter(w => (dd === -1 ? w.day === 0 : !dd || w.day === dd) && (f === 'all' || f === 'star' && S.vstat[w.w] === 2 || f === 'known' && S.vstat[w.w] === 1 || f === 'new' && !S.vstat[w.w]) && (!q || w.w.toLowerCase().includes(q) || (w.th || '').includes(q) || (w.fam || '').toLowerCase().includes(q)));
}
function vocabList() {
  const ws = vocabFiltered(); if (!ws.length) return '<div class="empty-state">ไม่พบคำ</div>';
  if (S.ui.fcMode === 'bank') return flashcards('bank', ws);
  return [...new Set(ws.map(w => w.day))].map(d => `<h3>${d ? `<a href="#/day/${d}">Day ${d}</a> · ${DAY(d).dateTh}` : 'ศัพท์เพิ่มเติม ' + DATA.extraVocab.length + ' คำ · เลือกทวนตามเวลา'}</h3><div class="vgrid ${S.ui.hideTh ? 'hideth' : ''}">${ws.filter(w => w.day === d).map(vcard).join('')}</div>`).join('');
}
function viewVocab() {
  return `<div class="card"><h1>คลังคำศัพท์ 740 คำ</h1><p class="muted">แผน 6 วันมีศัพท์ใหม่วันละ ${DATA.meta.wordsPerDay} คำ รวม ${DATA.meta.coreWords} คำ ไม่ซ้ำกัน · ทวนคำสะสมใน Day 6 · อีก ${DATA.extraVocab.length} คำเป็นคลังเพิ่มเติม</p><div class="row noprint"><input type="search" placeholder="ค้นหา อังกฤษ/ไทย" value="${esc(S.ui.vq || '')}" data-inp="vsearch"><select data-chg="vday" class="sel"><option value="0">ทั้งหมด 740 คำ</option>${DAYS.map(({d}) => `<option value="${d}" ${+S.ui.vd === d ? 'selected' : ''}>Day ${d} · ${DATA.meta.wordsPerDay} คำหลัก</option>`).join('')}<option value="-1" ${+S.ui.vd === -1 ? 'selected' : ''}>ศัพท์เพิ่มเติม ${DATA.extraVocab.length} คำ</option></select><div class="filters">${[['all','ทั้งหมด'],['star','ติดดาว'],['known','จำได้แล้ว'],['new','ยังไม่ระบุ']].map(([k,l]) => `<button class="${(S.ui.vf || 'all') === k ? 'on' : ''}" data-act="vf" data-f="${k}">${l}</button>`).join('')}</div><button class="btn sm" data-act="hideTh">ซ่อน/แสดงความหมาย</button><button class="btn sm" data-act="fcMode" data-key="bank">บัตรคำ/รายการ</button></div></div><div class="card" id="vlist">${vocabList()}</div>`;
}
function viewSettings() {
  const st = S.settings;
  return `<div class="card"><h1>ตั้งค่าและสำรองข้อมูล</h1><h3>ช่วงอ่านหนังสือ</h3><p><b>พฤหัสบดี 8 ตุลาคม 2569 – อังคาร 13 ตุลาคม 2569</b> · รวม 6 วัน</p><p class="small muted">วันที่นี้เป็นช่วงอ่านหนังสือ วันสอบเป้าหมายเดิมในข้อมูลคือ ${thDate(examDate(),true)} ตารางฉบับนี้ไม่ได้กำหนดวันสอบใหม่</p><h3>วิธีนับ “วันนี้”</h3><div class="row">${[['progress','ตามความคืบหน้า'],['calendar','ตามปฏิทิน · Day 1 = 8 ต.ค.']].map(([v,l]) => `<button class="btn sm ${(st.dayMode || 'progress') === v ? 'pri' : ''}" data-act="setDayMode" data-v="${v}">${l}</button>`).join('')}</div><h3>ธีม</h3><div class="row">${[['light','สว่าง'],['dark','มืด']].map(([v,l]) => `<button class="btn sm ${st.theme === v ? 'pri' : ''}" data-act="setTheme" data-v="${v}">${l}</button>`).join('')}</div><h3>ขนาดตัวอักษร</h3><div class="row">${[['s','เล็ก'],['m','ปกติ'],['l','ใหญ่'],['xl','ใหญ่มาก']].map(([v,l]) => `<button class="btn sm ${st.font === v ? 'pri' : ''}" data-act="setFont" data-v="${v}">${l}</button>`).join('')}</div><h3>สำรอง / กู้คืน</h3><p class="small muted">ข้อมูลฉบับ 6 วันแยกจากฉบับเดิม บันทึกในเบราว์เซอร์นี้ และกู้คืนได้จากไฟล์สำรองของฉบับ 6 วันเท่านั้น</p><div class="row"><button class="btn pri" data-act="backup">สำรองข้อมูล (.json)</button><label class="btn">กู้คืนจากไฟล์<input type="file" accept=".json,application/json" data-chg="restore" hidden></label><button class="btn" data-act="resetAll">ลบข้อมูลฉบับนี้</button></div><p class="small">${storageOK ? 'บันทึกอัตโนมัติได้' : 'บันทึกอัตโนมัติไม่ได้ — ใช้ปุ่มสำรองข้อมูล'}</p></div>`;
}
ACT.testExit = el => { location.hash = +el.dataset.d ? '#/day/' + el.dataset.d : '#/plan'; };
ACT.csv = () => {
  const rows = [['Day','วันที่','วัน','หัวข้อ','อ่านอะไร','ศัพท์','Reading','Writing','Grammar','นาที','สถานะ']];
  DAYS.forEach(d => rows.push([d.d,d.date,d.wd,d.title,d.read.map(shortRead).join(' | '),vocabShort(d.d),readingShort(d),taskShort(d),d.grams.map(g => DATA.grammar[g].title_th).join(' + '),d.minutes,dayProgress(d.d).done ? 'เสร็จแล้ว' : 'ยังไม่เสร็จ']));
  download('KKU-AELT_6_Day_Plan_08-13_Oct_2569.csv', '\uFEFF' + rows.map(r => r.map(c => '"' + String(c).replace(/"/g,'""') + '"').join(',')).join('\r\n'), 'text/csv');
};
ACT.backup = () => download('KKU-AELT_6_Day_Backup_08-13_Oct_2569.json', JSON.stringify(S), 'application/json');
INP.restore = el => {
  const f = el.files && el.files[0]; if (!f) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const state = JSON.parse(reader.result);
      if (!state || state.v !== 2 || state.planId !== DATA.meta.planId) throw new Error('ใช้ไฟล์สำรองของแผน 6 วัน ช่วง 8–13 ต.ค. 2569 เท่านั้น');
      if (!confirm('แทนที่ข้อมูลฉบับ 6 วันด้วยไฟล์สำรองนี้?')) return;
      S = upgradeVocabulary(Object.assign(defaultState(), state, {vocabRevision: state.vocabRevision || 0})); S.settings = Object.assign(defaultState().settings, state.settings || {});
      save(true); applySettings(); render(); toast('กู้คืนข้อมูลแล้ว');
    } catch (e) { alert('กู้คืนไม่ได้: ' + e.message); }
  };
  reader.readAsText(f);
};
