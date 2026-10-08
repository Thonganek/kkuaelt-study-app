/* ============================================================
   Other views: plan, vocab bank, errors, writing, stats, guide, settings
   ============================================================ */
function shortRead(it) { const n = { book: 'หนังสือ', aelt: 'AELT PDF', image: 'Image PDF', guide: 'Guide', improved: 'Improved', app: 'แอป' }[it.src]; return `${n}${it.pages ? ' ' + it.pages : ''}: ${it.what}`; }
function examShort(d) { return examsOf(d).map(x => x.label.replace(/^Reading (W\d+): /, 'Reading $1 ')).join(' · '); }
function taskShort(day) {
  if (day.essay) { const e = DATA.essays[day.essay.topic]; return `Essay 60 นาที (${day.essay.topic}): ${e ? e.prompt : ''}`; }
  if (day.task) return `${KIND_TH[day.task.kind] || ''} ${day.task.words}: ${day.task.topic && DATA.essays[day.task.topic] ? '(' + day.task.topic + ') ' + DATA.essays[day.task.topic].prompt : day.task.prompt}`;
  return '—';
}
function readingShort(day) {
  if (day.test) return (DATA.tests[day.test] || { title: day.test }).title + ' (6 passages / 69 ข้อ / 120 นาที)';
  if (day.reading) return day.reading.passages.map(pid => DATA.passages[pid] ? pid + ' ' + DATA.passages[pid].title : pid).join(' + ') + (day.reading.bookTask ? ' + หนังสือ' : '');
  if (day.blocks.some(b => b.k === 'weekly' || b.k === 'retry')) return 'ทำซ้ำข้อที่ผิด';
  return '—';
}
function vocabShort(d) { const n = DAY(d).newWords; return n ? n + ' คำใหม่' : 'ทวน ' + reviewWords(d).all.length + ' คำ'; }

/* ---------- plan ---------- */
function viewPlan() {
  const tn = rawTodayNum(); const f = S.ui.planF || 'all';
  let h = `<div class="card"><div class="row"><div><div class="daynum">KKU-AELT · ${esc(shortDate(1))} – ${esc(DAY(NDAYS).dateTh)}</div><h1>ตารางอ่าน ${NDAYS} วัน (Day 1–${NDAYS})</h1></div><span class="spacer"></span><button class="btn noprint" data-act="print">${ico('printer')} พิมพ์ตาราง</button><button class="btn noprint" data-act="csv">${ico('download')} CSV (Excel)</button></div>
  <p class="muted">Reading 60% + Writing 40% · วันธรรมดา 90 นาที ทุกวัน · เสาร์ Reading จับเวลา 120 นาที · อาทิตย์ Writing 60 นาที + ตรวจข้อผิดของสัปดาห์ · 16–18 พ.ย. Full Mock 3 ชั่วโมง · วันสอบเป้าหมาย ${esc(thDate(examDate(), true))}</p>
  <div class="grid g4" style="margin-top:10px">
    <div class="kpi"><div class="v">${ALLWORDS.length}</div><div class="l">คำศัพท์ Academic (20–23 คำ/วัน × ${Object.keys(DATA.vocab).length} วัน)</div></div>
    <div class="kpi"><div class="v">${Object.keys(DATA.passages).length}</div><div class="l">บทอ่าน (รายวัน ${Object.keys(DATA.passages).filter(x => x.startsWith('W')).length} + ชุดเต็ม ${Object.keys(DATA.tests).length}×6)</div></div>
    <div class="kpi"><div class="v">${Object.values(DATA.passages).reduce((s, p) => s + p.questions.length, 0)}</div><div class="l">ข้อ Reading พร้อมเฉลยภาษาไทย</div></div>
    <div class="kpi"><div class="v">${DAYS.filter(d => d.essay || (d.task && d.task.kind === 'essay')).length + 3}</div><div class="l">Essay เต็ม (+ งานเขียนย่อทุกวัน)</div></div>
  </div></div>`;
  h += `<div class="card"><h2>กิจวัตรประจำวัน</h2><div class="tablewrap"><table class="t"><tr><th>วัน</th><th>ลำดับ (นาที)</th><th>รวม</th></tr>
  <tr><td>จันทร์–ศุกร์</td><td>คำศัพท์ 15 → Reading 40 → Writing/Grammar 30 → สมุดข้อผิดพลาด 5 <span class="muted">(10–13 พ.ย.: ศัพท์ 10 → Reading จับเวลา 30 → Essay จับเวลา 40 → ข้อผิด 10)</span></td><td>90</td></tr>
  <tr><td>เสาร์</td><td>Reading Test เต็มชุด 120 → คำศัพท์ 15 → ตรวจผล 15</td><td>150</td></tr>
  <tr><td>อาทิตย์</td><td>Writing จับเวลา 60 → ทำซ้ำข้อผิดของสัปดาห์ 20 → ทวนศัพท์ 15</td><td>95</td></tr>
  <tr><td>16–18 พ.ย.</td><td>Full Mock: Reading 120 → Writing 60 → ตรวจผล 20 → คำศัพท์ 15</td><td>215</td></tr>
  <tr><td>19 พ.ย. / 20 พ.ย.</td><td>Error Review 90 นาที / Light Review 45 นาทีแล้วพัก</td><td></td></tr></table></div></div>`;
  h += `<div class="card"><h2>ช่วงการเรียน</h2><div class="tablewrap"><table class="t"><tr><th>ช่วง</th><th>วันที่</th><th>Day</th><th>เป้าหมาย</th></tr>${PHASES.map(p => `<tr><td>${phaseChip(p.id)} ${esc(p.th)}</td><td>${esc(p.range)}</td><td>${p.days[0]}${p.days[1] !== p.days[0] ? '–' + p.days[1] : ''}</td><td>${esc(p.goal)}</td></tr>`).join('')}<tr><td><span class="chip no">สอบ</span></td><td>21 พ.ย.</td><td>—</td><td>Reading → Writing (ตรวจวันสอบจริง: ปฏิทินศูนย์ฯ ระบุรอบ พ.ย. = 14 พ.ย.)</td></tr></table></div></div>`;
  // calendar
  const calStart = new Date(2026, 9, 5); let cal = ['จ', 'อ', 'พ', 'พฤ', 'ศ', 'ส', 'อา'].map(x => `<div class="hd">${x}</div>`).join('');
  for (let i = 0; i < 49; i++) {
    const dt = new Date(calStart); dt.setDate(dt.getDate() + i);
    const n = Math.round((dt - START) / 86400000) + 1;
    if (n >= 1 && n <= NDAYS) { const day = DAY(n); const pr = dayProgress(n); cal += `<a class="cell ${n === tn ? 'today' : ''} ${pr.done ? 'done' : ''}" href="#/day/${n}"><span class="dn">D${n}</span><span class="dd">${dt.getDate()} ${TH_M[dt.getMonth()]}</span><span class="ty">${day.type === 'test' ? ico('news') + '<span>Test</span>' : day.type === 'mock' ? ico('target') + '<span>Mock</span>' : day.type === 'sunday' ? ico('pen') + '<span>Essay</span>' : day.type === 'review' ? ico('retry') + '<span>Review</span>' : day.type === 'light' ? ico('spark') + '<span>Light</span>' : ''}</span><span class="bar" style="background:${PCOL[day.phase]}"></span></a>`; }
    else if (dt.toISOString && dt.getMonth() === 10 && dt.getDate() === 21) cal += `<div class="cell exam"><span class="dn">สอบ</span><span class="dd">21 พ.ย.</span><span>เป้าหมาย</span></div>`;
    else cal += `<div class="cell empty"><span class="dd">${dt.getDate()} ${TH_M[dt.getMonth()]}</span>${dt.getMonth() === 10 && dt.getDate() === 14 ? '<span class="tiny">รอบ PBT ศูนย์ฯ</span>' : ''}</div>`;
  }
  h += `<div class="card noprint"><h2>ปฏิทิน</h2><div class="cal">${cal}</div><p class="small muted">สีแถบล่าง = ช่วงการเรียน · พื้นเขียว = ทำครบ · กรอบน้ำเงิน = วันนี้</p></div>`;
  // table
  const fb = [['all', 'ทั้งหมด']].concat(PHASES.map(p => [p.id, p.name]));
  h += `<div class="card"><h2>ตารางรายวัน</h2><div class="filters noprint">${fb.map(([k, l]) => `<button class="${f === k ? 'on' : ''}" data-act="planF" data-f="${k}">${esc(l)}</button>`).join('')}</div>
  <div class="tablewrap"><table class="t plan"><tr><th>Day / วันที่</th><th>หัวข้อ</th><th>อ่านอะไร (เลขหน้าในหนังสือ)</th><th>ศัพท์</th><th>Reading</th><th>Writing</th><th>ข้อสอบวันนี้</th><th>นาที</th><th>สถานะ</th></tr>`;
  DAYS.filter(d => f === 'all' || d.phase === f).forEach(d => {
    const pr = dayProgress(d.d);
    h += `<tr class="${d.d === tn ? 'today' : ''} ${pr.done ? 'done' : ''}"><td><a class="daylink" href="#/day/${d.d}">Day ${d.d}</a><div class="small">${esc(d.wd)} ${esc(d.dateTh)}</div>${phaseChip(d.phase)}</td><td><b>${esc(d.title)}</b></td><td><ul style="margin:0;padding-left:1rem">${d.read.map(it => `<li>${esc(shortRead(it))}</li>`).join('')}</ul></td><td>${esc(vocabShort(d.d))}</td><td>${esc(readingShort(d))}</td><td>${esc(taskShort(d))}${d.grams.map(id => DATA.grammar[id] ? `<div class="small muted">Grammar: ${esc(DATA.grammar[id].title_th)}</div>` : '').join('')}</td><td class="small">${esc(examShort(d.d))}</td><td>${d.minutes}</td><td>${pr.n}/${pr.total}</td></tr>`;
  });
  h += `</table></div></div>`;
  return h;
}
ACT.planF = el => { S.ui.planF = el.dataset.f; save(); render(true); };
ACT.csv = () => {
  const rows = [['Day', 'วันที่', 'วัน', 'ช่วง', 'หัวข้อ', 'อ่านอะไร', 'ศัพท์', 'Reading', 'Writing', 'Grammar', 'ข้อสอบวันนี้', 'นาที']];
  DAYS.forEach(d => rows.push([d.d, d.date, d.wd, PHASE[d.phase].name, d.title, d.read.map(shortRead).join(' | '), vocabShort(d.d), readingShort(d), taskShort(d), d.grams.map(id => DATA.grammar[id] ? DATA.grammar[id].title_th : id).join(' + '), examShort(d.d), d.minutes]));
  download('KKU-AELT_42_Day_Plan.csv', '﻿' + rows.map(r => r.map(c => '"' + String(c).replace(/"/g, '""') + '"').join(',')).join('\r\n'), 'text/csv');
};

/* ---------- vocab bank ---------- */
function vocabFiltered() {
  const q = (S.ui.vq || '').trim().toLowerCase(); const f = S.ui.vf || 'all'; const dd = +(S.ui.vd || 0);
  return ALLWORDS.filter(w => (!dd || w.day === dd) && (f === 'all' || (f === 'star' && S.vstat[w.w] === 2) || (f === 'known' && S.vstat[w.w] === 1) || (f === 'new' && !S.vstat[w.w])) && (!q || w.w.toLowerCase().includes(q) || (w.th || '').includes(q) || (w.fam || '').toLowerCase().includes(q)));
}
function vocabList() {
  const ws = vocabFiltered(); if (!ws.length) return '<div class="empty-state">ไม่พบคำ</div>';
  if (S.ui.fcMode === 'bank') return flashcards('bank', ws);
  let h = '', cur = 0;
  ws.forEach(w => { if (w.day !== cur) { if (cur) h += '</div>'; cur = w.day; h += `<h3><a href="#/day/${cur}">Day ${cur}</a> <span class="small muted">${esc(DAY(cur).dateTh)}</span></h3><div class="vgrid ${S.ui.hideTh ? 'hideth' : ''}">`; } h += vcard(w); });
  return h + '</div>';
}
function viewVocab() {
  const known = ALLWORDS.filter(w => S.vstat[w.w] === 1).length, star = ALLWORDS.filter(w => S.vstat[w.w] === 2).length;
  const learned = Object.keys(DATA.vocab).filter(d => S.quiz['V:' + d] && S.quiz['V:' + d].done).reduce((s, d) => s + DATA.vocab[d].length, 0);
  const f = S.ui.vf || 'all';
  return `<div class="card"><h1>คลังคำศัพท์ 740 คำ</h1><p class="muted">Day 1 = ศัพท์งานวิจัยหลัก 20 คำ · วันอื่น = Academic Word List (AWL) + ศัพท์หัวข้อ/สำนวน essay รวมวันละ 20–23 คำ</p>
  <div class="grid g4"><div class="kpi"><div class="v">${learned}</div><div class="l">คำที่ทำ quiz แล้ว</div></div><div class="kpi"><div class="v">${known}</div><div class="l">จำได้แล้ว</div></div><div class="kpi"><div class="v">${star}</div><div class="l">ติดดาว (ยังจำไม่ได้)</div></div><div class="kpi"><div class="v">${ALLWORDS.length}</div><div class="l">ทั้งหมด</div></div></div>
  <div class="row noprint" style="margin-top:12px"><input type="search" placeholder="ค้นหา อังกฤษ/ไทย" value="${esc(S.ui.vq || '')}" data-inp="vsearch" style="padding:8px 12px;border-radius:10px;border:1px solid var(--line-2);min-width:220px;background:var(--surface)">
  <select data-chg="vday" style="padding:8px;border-radius:10px;border:1px solid var(--line-2);background:var(--surface)"><option value="0">ทุกวัน</option>${Object.keys(DATA.vocab).map(d => `<option value="${d}" ${+S.ui.vd === +d ? 'selected' : ''}>Day ${d}</option>`).join('')}</select>
  <div class="filters" style="margin:0">${[['all', 'ทั้งหมด'], ['star', 'ติดดาว'], ['known', 'จำได้แล้ว'], ['new', 'ยังไม่ระบุ']].map(([k, l]) => `<button class="${f === k ? 'on' : ''}" data-act="vf" data-f="${k}">${l}</button>`).join('')}</div>
  <button class="btn sm" data-act="hideTh">${S.ui.hideTh ? ico('eye') + ' แสดงความหมาย' : ico('eyeoff') + ' ซ่อนความหมาย'}</button><button class="btn sm" data-act="fcMode" data-key="bank">${S.ui.fcMode === 'bank' ? ico('grid') + ' รายการ' : ico('cards') + ' บัตรคำ (ชุดที่กรอง)'}</button><button class="btn sm" data-act="vexport">${ico('download')} CSV คำที่ติดดาว</button></div></div>
  <div class="card" id="vlist">${vocabList()}</div>`;
}
INP.vsearch = el => { S.ui.vq = el.value; clearTimeout(INP.vsearch.t); INP.vsearch.t = setTimeout(() => { const c = $('#vlist'); if (c) c.innerHTML = vocabList(); }, 200); };
INP.vday = el => { S.ui.vd = +el.value; save(); render(true); };
ACT.vf = el => { S.ui.vf = el.dataset.f; save(); render(true); };
ACT.vexport = () => { const ws = ALLWORDS.filter(w => S.vstat[w.w] === 2); download('starred_words.csv', '﻿' + [['word', 'pos', 'thai', 'example', 'day']].concat(ws.map(w => [w.w, w.pos, w.th, w.ex, w.day])).map(r => r.map(c => '"' + String(c || '').replace(/"/g, '""') + '"').join(',')).join('\r\n'), 'text/csv'); };

/* ---------- errors ---------- */
function viewErrors() {
  const all = wrongItems({}); const open = all.filter(x => !S.resolved[x.q.id]);
  const f = S.ui.ef || 'all'; const sk = S.ui.es || '';
  const by = {}; open.forEach(x => { const k = x.q.skill || 'other'; by[k] = (by[k] || 0) + 1; });
  const list = (S.ui.eShowAll ? all : open).filter(x => (f === 'all' || (f === 'reading' && (x.kind === 'reading' || x.kind === 'test')) || x.kind === f) && (!sk || x.q.skill === sk)).sort((a, b) => b.day - a.day);
  const notes = Object.keys(S.notes).filter(d => S.notes[d] && S.notes[d].trim()).sort((a, b) => b - a);
  return `<div class="card"><h1>สมุดข้อผิดพลาด</h1><p class="muted">ทุกข้อที่ตอบผิดจาก Quiz/Reading/Test จะถูกรวบรวมที่นี่อัตโนมัติ — ตอบใหม่ให้ถูกเพื่อปิดข้อ</p>
  <div class="grid g4"><div class="kpi"><div class="v">${open.length}</div><div class="l">ข้อที่ยังไม่แก้</div></div><div class="kpi"><div class="v">${all.length - open.length}</div><div class="l">แก้แล้ว</div></div><div class="kpi"><div class="v">${open.filter(x => x.kind === 'test' || x.kind === 'reading').length}</div><div class="l">Reading</div></div><div class="kpi"><div class="v">${open.filter(x => x.kind === 'grammar').length + '/' + open.filter(x => x.kind === 'vocab').length}</div><div class="l">Grammar / ศัพท์</div></div></div>
  <h3>ทักษะที่ผิดบ่อย (ยังไม่แก้)</h3><div class="row small">${Object.entries(by).sort((a, b) => b[1] - a[1]).map(([k, v]) => `<button class="chip ${sk === k ? 'acc' : ''}" data-act="es" data-s="${esc(k)}">${esc(SKILL_TH[k] || k)} ${v}</button>`).join(' ') || '<span class="muted">—</span>'}</div>
  <div class="filters">${[['all', 'ทั้งหมด'], ['reading', 'Reading/Test'], ['grammar', 'Grammar'], ['vocab', 'คำศัพท์']].map(([k, l]) => `<button class="${f === k ? 'on' : ''}" data-act="ef" data-f="${k}">${l}</button>`).join('')}<button class="${S.ui.eShowAll ? 'on' : ''}" data-act="eAll">${S.ui.eShowAll ? 'แสดงเฉพาะที่ยังไม่แก้' : 'แสดงที่แก้แล้วด้วย'}</button></div></div>
  <div class="card">${renderRetryList(list.slice(0, 100))}${list.length > 100 ? '<p class="muted">แสดง 100 ข้อแรก — กรองตามทักษะเพื่อดูเพิ่ม</p>' : ''}</div>
  <div class="card"><h2>บันทึกรายวัน</h2>${notes.length ? notes.map(d => `<div class="lesson"><b><a href="#/day/${d}">Day ${d}</a></b> <span class="small muted">${esc(DAY(+d).title)}</span><p style="white-space:pre-wrap">${esc(S.notes[d])}</p></div>`).join('') : '<p class="muted">ยังไม่มีบันทึก</p>'}</div>`;
}
ACT.ef = el => { S.ui.ef = el.dataset.f; save(); render(true); };
ACT.es = el => { S.ui.es = S.ui.es === el.dataset.s ? '' : el.dataset.s; save(); render(true); };
ACT.eAll = () => { S.ui.eShowAll = !S.ui.eShowAll; save(); render(true); };

/* ---------- writing studio ---------- */
function viewWriting(tab) {
  tab = tab || 'mine';
  const tabs = [['mine', 'งานเขียนของฉัน'], ['bank', 'คลังหัวข้อ (' + Object.keys(DATA.essays).length + ')'], ['models', 'ตัวอย่างจากเอกสารของคุณ']];
  let h = `<div class="card"><h1>Writing Studio</h1><div class="tabs">${tabs.map(([k, l]) => `<a class="${tab === k || (tab.startsWith('R') && k === 'bank') ? 'on' : ''}" href="#/writing/${k}">${l}</a>`).join('')}</div>`;
  if (tab === 'mine') {
    const rows = DAYS.filter(d => d.task || d.essay).map(d => { const key = 'E:' + d.d; const e = S.essays[key]; const n = e ? wc(e.text) : 0; const tgt = d.essay ? 250 : targetWords(d.task); const r = e && e.rate ? Object.values(e.rate) : []; return `<tr><td><a href="#/day/${d.d}/${d.essay ? 'essay' : 'writing'}">Day ${d.d}</a><div class="small muted">${esc(d.dateTh)}</div></td><td>${d.essay ? 'Essay 60 นาที' : esc(KIND_TH[d.task.kind] || '')}</td><td class="small">${esc(taskShort(d))}</td><td><span class="wc ${tgt && n >= tgt ? 'ok' : n ? 'low' : ''}">${n}</span>${tgt ? ' / ' + tgt : ''}</td><td>${r.length ? (r.reduce((a, b) => a + b, 0) / r.length).toFixed(1) : '—'}</td></tr>`; }).join('');
    h += `<p class="muted">ทุกงานเขียนบันทึกในเบราว์เซอร์นี้ — กด “สำรองข้อมูล” ในหน้าตั้งค่าเป็นระยะ</p><div class="tablewrap"><table class="t"><tr><th>Day</th><th>ประเภท</th><th>โจทย์</th><th>คำ</th><th>ประเมินตนเอง</th></tr>${rows}</table></div><button class="btn" data-act="dlAll" style="margin-top:10px">${ico('download')} ดาวน์โหลดงานเขียนทั้งหมด (.txt)</button>`;
  } else if (tab === 'bank' || tab.startsWith('R')) {
    const cur = tab.startsWith('R') ? tab : null;
    h += `<p class="muted">หัวข้อจาก Aelt Writing 0421.pdf (คัดตามต้นฉบับ รวมถ้อยคำที่ผิดไวยากรณ์) + หัวข้อคาดการณ์ 1 ข้อ — แต่ละหัวข้อมีคำอธิบาย ไอเดีย 2 ฝั่ง outline และ model essay · แนะนำให้เขียนเองในวันที่กำหนดก่อนเปิดดู</p><div class="tablewrap"><table class="t"><tr><th>รหัส</th><th>โจทย์</th><th>แหล่งที่มา</th><th>ใช้ในวัน</th></tr>${Object.keys(DATA.essays).map(id => { const used = DAYS.filter(d => (d.essay && d.essay.topic === id) || (d.task && d.task.topic === id)).map(d => `<a href="#/day/${d.d}">${d.d}</a>`).join(', '); return `<tr><td><a href="#/writing/${id}"><b>${id}</b></a></td><td>${esc(DATA.essays[id].prompt)}</td><td class="small">${esc((DATA.topics[id] || {}).label || '')}</td><td>${used}</td></tr>`; }).join('')}</table></div>`;
    if (cur && DATA.essays[cur]) setTimeout(() => { const t = document.getElementById('topic'); if (t) t.scrollIntoView({ block: 'start' }); }, 30);
    if (cur && DATA.essays[cur]) h += `</div><div class="card" id="topic"><h2>${cur}: ${esc(DATA.essays[cur].prompt)}</h2>${essayView(cur)}`;
  } else if (tab === 'models') {
    h += `<p class="muted">ข้อความจาก Opinion_Essay_Guide.docx, Improved_Opinion_Essays.docx และ Image (1).pdf (คัดลอกมาให้อ่านในแอป)</p>` + Object.keys(DATA.models).filter(k => !['SMART', 'CONCEDE'].includes(k)).map(k => `<details class="more"><summary>${esc(DATA.models[k].title)}</summary>${docxModel(k)}</details>`).join('');
  }
  return h + `</div>`;
}
ACT.dlAll = () => { const t = DAYS.filter(d => S.essays['E:' + d.d] && S.essays['E:' + d.d].text).map(d => `===== Day ${d.d} (${d.dateTh}) — ${taskShort(d)} =====\n${S.essays['E:' + d.d].text}\n`).join('\n'); download('KKU-AELT_my_writing.txt', t || '(ยังไม่มีงานเขียน)'); };

/* ---------- stats ---------- */
function barChart(items, h = 220) {
  const W = 900, padL = 34, padB = 34, padT = 18, iw = W - padL - 10, ih = h - padB - padT, bw = Math.min(46, iw / items.length - 16);
  let s = `<svg class="chart" viewBox="0 0 ${W} ${h}" role="img" aria-label="กราฟคะแนน"><defs><linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" class="gs1"/><stop offset="1" class="gs2"/></linearGradient></defs>`;
  [0, 25, 50, 75, 100].forEach(v => { const y = padT + ih - ih * v / 100; s += `<line class="gl" x1="${padL}" x2="${W - 10}" y1="${y}" y2="${y}"/><text class="ax" x="${padL - 6}" y="${y + 4}" text-anchor="end">${v}</text>`; });
  items.forEach((it, i) => {
    const cx = padL + iw * (i + .5) / items.length; const v = it.value;
    if (v != null) { const bh = Math.max(2, ih * v / 100), x = cx - bw / 2, y = padT + ih - bh, r = Math.min(4, bh); s += `<path class="bar" d="M${x},${padT + ih} V${y + r} Q${x},${y} ${x + r},${y} H${x + bw - r} Q${x + bw},${y} ${x + bw},${y + r} V${padT + ih} Z"/><text class="vl" x="${cx}" y="${y - 5}" text-anchor="middle">${v}%</text>`; }
    else s += `<rect class="bar empty" x="${cx - bw / 2}" y="${padT + ih - 3}" width="${bw}" height="3" rx="1.5"/>`;
    s += `<text class="ax" x="${cx}" y="${h - 12}" text-anchor="middle">${esc(it.label)}</text><rect class="hit" x="${cx - iw / items.length / 2}" y="${padT}" width="${iw / items.length}" height="${ih}" data-tip="${esc(it.tip)}"/>`;
  });
  return s + `</svg>`;
}
function hbars(rows) {
  return `<div>${rows.map(r => `<div class="row" style="flex-wrap:nowrap;margin:4px 0" data-tip="${esc(r.tip)}"><span style="width:150px;flex:none" class="small">${esc(r.label)}</span><svg viewBox="0 0 200 14" style="flex:1;height:14px" preserveAspectRatio="none"><rect class="hb-track" x="0" y="2" width="200" height="10" rx="4"/><rect x="0" y="2" width="${2 * r.value}" height="10" rx="4" class="hb-fill"/></svg><span class="small" style="width:70px;text-align:right">${r.value}% <span class="muted">(${r.n})</span></span></div>`).join('')}</div>`;
}
function viewStats() {
  const daysDone = DAYS.filter(d => dayProgress(d.d).done).length;
  let qa = 0, qr = 0; const skill = {};
  for (const key in S.quiz) { const st = S.quiz[key]; if (!st.done) continue; const qz = getQuiz(key); if (!qz) continue; qz.questions.forEach(q => { qa++; const ok = isRight(q, st.ans[q.id], st.ov); if (ok) qr++; if (qz.kind === 'reading' || qz.kind === 'test') { const k = q.skill; skill[k] = skill[k] || [0, 0]; skill[k][1]++; if (ok) skill[k][0]++; } }); }
  const passDone = Object.keys(DATA.passages).filter(pid => (S.quiz['R:' + pid] || {}).done || Object.values(DATA.tests).some(t => t.passages.includes(pid) && (S.quiz['T:' + t.id] || {}).done)).length;
  const essays = DAYS.filter(d => S.essays['E:' + d.d]).map(d => ({ d: d.d, n: wc(S.essays['E:' + d.d].text) }));
  const full = essays.filter(e => e.n >= 250).length; const totalW = essays.reduce((s, e) => s + e.n, 0);
  const learned = Object.keys(DATA.vocab).filter(d => (S.quiz['V:' + d] || {}).done).reduce((s, d) => s + DATA.vocab[d].length, 0);
  const tests = Object.keys(DATA.tests).map(id => { const st = S.quiz['T:' + id]; const v = st && st.done ? pct(st.score, st.total) : null; return { label: id, value: v, tip: `${DATA.tests[id].title} (Day ${DATA.tests[id].day})${v != null ? ': ' + st.score + '/69' : ': ยังไม่ทำ'}` }; });
  const sk = Object.entries(skill).map(([k, v]) => ({ label: SKILL_TH[k] || k, value: pct(v[0], v[1]), n: v[0] + '/' + v[1], tip: `${SKILL_TH[k] || k}: ถูก ${v[0]} จาก ${v[1]} ข้อ` })).sort((a, b) => a.value - b.value);
  let h = `<div class="card"><h1>สถิติและความก้าวหน้า</h1><div class="grid g4">
  <div class="kpi"><div class="v">${daysDone}/${NDAYS}</div><div class="l">วันที่ทำครบทุกส่วน</div><progress max="${NDAYS}" value="${daysDone}"></progress></div>
  <div class="kpi"><div class="v">${learned}</div><div class="l">คำศัพท์ที่ทำ quiz แล้ว (เป้า 740)</div><progress max="740" value="${learned}"></progress></div>
  <div class="kpi"><div class="v">${passDone}</div><div class="l">บทอ่านที่ทำแล้ว (เป้า ≥ 25–30)</div><progress max="${Object.keys(DATA.passages).length}" value="${passDone}"></progress></div>
  <div class="kpi"><div class="v">${full}</div><div class="l">Essay ≥ 250 คำ (เป้า 12–15) · เขียนรวม ${totalW} คำ</div><progress max="16" value="${full}"></progress></div>
  </div><p class="small muted" style="margin-top:8px">ตอบคำถามทั้งหมด ${qa} ข้อ ถูก ${qr} ข้อ (${pct(qr, qa)}%)</p></div>`;
  h += `<div class="card"><h2>คะแนน Reading Test / Mock (% ถูก)</h2>${barChart(tests)}<details class="more small"><summary>ตารางข้อมูล</summary><table class="t"><tr><th>ชุด</th><th>Day</th><th>คะแนน</th><th>%</th></tr>${tests.map(t => `<tr><td>${t.label}</td><td>${DATA.tests[t.label].day}</td><td>${t.value != null ? S.quiz['T:' + t.label].score + '/69' : '—'}</td><td>${t.value != null ? t.value + '%' : '—'}</td></tr>`).join('')}</table></details><p class="small muted">ร้อยละใช้ดูแนวโน้มเท่านั้น ไม่แปลงเป็นระดับ (band) ของ KKU-AELT</p></div>`;
  h += `<div class="card"><h2>ความแม่นยำแยกทักษะ Reading (เรียงจากอ่อนสุด)</h2>${sk.length ? hbars(sk) : '<p class="muted">ยังไม่มีข้อมูล — ทำ Reading ก่อน</p>'}</div>`;
  h += `<div class="card"><h2>งานเขียน</h2>${essays.length ? `<div class="tablewrap"><table class="t"><tr><th>Day</th><th>งาน</th><th>คำ</th></tr>${essays.map(e => `<tr><td><a href="#/day/${e.d}">Day ${e.d}</a></td><td class="small">${esc(taskShort(DAY(e.d)))}</td><td>${e.n}</td></tr>`).join('')}</table></div>` : '<p class="muted">ยังไม่มีงานเขียน</p>'}</div>`;
  return h;
}
document.addEventListener('mouseover', e => { const el = e.target.closest('[data-tip]'); const tip = $('#tip'); if (!el) { tip.hidden = true; return; } tip.textContent = el.dataset.tip; tip.hidden = false; });
document.addEventListener('mousemove', e => { const tip = $('#tip'); if (!tip.hidden) { tip.style.left = Math.min(window.innerWidth - 270, e.clientX + 12) + 'px'; tip.style.top = (e.clientY + 14) + 'px'; } });

/* ---------- guide ---------- */
function viewGuide(tab) {
  const keys = Object.keys(DATA.guide); if (!DATA.guide[tab]) tab = 'exam';
  return `<div class="card"><h1>คู่มือ</h1><div class="tabs">${keys.map(k => `<a class="${k === tab ? 'on' : ''}" href="#/guide/${k}">${esc(DATA.guide[k].title)}</a>`).join('')}</div><div class="lesson">${lessonBlocks(DATA.guide[tab].blocks)}</div>
  ${tab === 'reading' ? '<h2>บทเรียนทักษะทั้งหมด</h2>' + Object.keys(DATA.lessons).map(k => `<details class="more"><summary>${esc(DATA.lessons[k].title)}</summary>${lessonBox(k)}</details>`).join('') : ''}</div>`;
}

/* ---------- settings ---------- */
function viewSettings() {
  const st = S.settings; const ex = st.exam;
  return `<div class="card"><h1>ตั้งค่าและสำรองข้อมูล</h1>
  <h3>วันสอบของฉัน (ใช้กับตัวนับถอยหลัง)</h3><div class="row">${[['2026-11-21', 'เสาร์ 21 พ.ย. 2569 (ตามแผน)'], ['2026-11-14', 'เสาร์ 14 พ.ย. 2569 (ปฏิทิน PBT ศูนย์ฯ)'], ['2026-12-12', 'เสาร์ 12 ธ.ค. 2569']].map(([v, l]) => `<button class="btn sm ${ex === v ? 'pri' : ''}" data-act="setExam" data-v="${v}">${l}</button>`).join('')}<input type="date" value="${esc(ex)}" data-chg="examDate" style="padding:6px;border-radius:8px;border:1px solid var(--line-2);background:var(--surface)"></div>
  <h3>ธีม</h3><div class="row">${[['light', 'Iron Man · สว่าง'], ['dark', 'JARVIS HUD · มืด']].map(([v, l]) => `<button class="btn sm ${(st.theme === 'dark' ? 'dark' : 'light') === v ? 'pri' : ''}" data-act="setTheme" data-v="${v}">${l}</button>`).join('')}</div>
  <h3>ขนาดตัวอักษร</h3><div class="row">${[['s', 'เล็ก'], ['m', 'ปกติ'], ['l', 'ใหญ่'], ['xl', 'ใหญ่มาก']].map(([v, l]) => `<button class="btn sm ${st.font === v ? 'pri' : ''}" data-act="setFont" data-v="${v}">${l}</button>`).join('')}</div>
  <h3>สำรอง / กู้คืน</h3><p class="small muted">ข้อมูลทั้งหมด (คำตอบ งานเขียน บันทึก ดาวคำศัพท์) เก็บในเบราว์เซอร์นี้เท่านั้น ถ้าเปลี่ยนเครื่อง/เบราว์เซอร์ หรือล้างข้อมูลเบราว์เซอร์ ข้อมูลจะหาย — สำรองเป็นไฟล์ JSON สัปดาห์ละครั้ง</p>
  <div class="row"><button class="btn pri" data-act="backup">${ico('download')} สำรองข้อมูล (.json)</button><label class="btn">${ico('upload')} กู้คืนจากไฟล์<input type="file" accept=".json,application/json" data-chg="restore" hidden></label><button class="btn" data-act="resetAll" style="color:var(--bad)">ลบข้อมูลทั้งหมด</button></div>
  <p class="small">สถานะการบันทึก: ${storageOK ? '<span class="chip ok">บันทึกอัตโนมัติได้</span>' : '<span class="chip no">บันทึกอัตโนมัติไม่ได้ — ใช้ปุ่มสำรองข้อมูล</span>'}</p></div>`;
}
function applySettings() {
  const r = document.documentElement; const dark = S.settings.theme === 'dark';
  r.dataset.theme = dark ? 'dark' : 'light'; r.dataset.font = S.settings.font || 'm';
  $$('.themetog, .themetog-m').forEach(b => { b.querySelector('use').setAttribute('href', dark ? '#i-sun' : '#i-moon'); const sp = b.querySelector('span'); if (sp) sp.textContent = dark ? 'โหมดสว่าง' : 'โหมดมืด'; b.title = dark ? 'สลับเป็นโหมดสว่าง' : 'สลับเป็นโหมดมืด'; });
}
ACT.toggleTheme = () => { S.settings.theme = S.settings.theme === 'dark' ? 'light' : 'dark'; applySettings(); save(); if (location.hash.startsWith('#/settings')) render(true); };

/* ---------- AI neural-network background (decorative, paused when hidden / in tests / reduced motion) ---------- */
function startNet() {
  const cv = document.getElementById('aiNet'); if (!cv || !cv.getContext) return;
  const ctx = cv.getContext('2d'); const reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  let W = 0, H = 0, nodes = [], last = 0; const mouse = { x: -1e4, y: -1e4 };
  const size = () => {
    const dpr = Math.min(2, window.devicePixelRatio || 1); W = innerWidth; H = innerHeight;
    cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const n = Math.round(Math.min(72, Math.max(22, W * H / 24000)));
    nodes = Array.from({ length: n }, (_, i) => ({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .28, vy: (Math.random() - .5) * .28, r: Math.random() * 1.5 + .7, c: i % 3 }));
  };
  const frame = t => {
    if (!document.hidden && !document.body.classList.contains('testing') && t - last > 33) {
      last = t; const light = document.documentElement.dataset.theme === 'light';
      const C = light ? ['185,28,28', '180,110,10', '8,145,178'] : ['248,113,113', '251,191,36', '103,232,249'];
      const A = light ? .2 : .55, R = 150, M = 190;
      ctx.clearRect(0, 0, W, H);
      for (const p of nodes) {
        p.x += p.vx; p.y += p.vy;
        if (p.x < -20) p.x = W + 20; else if (p.x > W + 20) p.x = -20;
        if (p.y < -20) p.y = H + 20; else if (p.y > H + 20) p.y = -20;
      }
      ctx.lineWidth = 1;
      for (let i = 0; i < nodes.length; i++) {
        const a = nodes[i];
        for (let j = i + 1; j < nodes.length; j++) {
          const b = nodes[j], dx = a.x - b.x, dy = a.y - b.y, d2 = dx * dx + dy * dy;
          if (d2 < R * R) { ctx.strokeStyle = `rgba(${C[a.c]},${((1 - Math.sqrt(d2) / R) * A * .55).toFixed(3)})`; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
        }
        const mx = a.x - mouse.x, my = a.y - mouse.y, m2 = mx * mx + my * my;
        if (m2 < M * M) { ctx.strokeStyle = `rgba(${C[0]},${((1 - Math.sqrt(m2) / M) * A).toFixed(3)})`; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke(); }
      }
      for (const p of nodes) { ctx.fillStyle = `rgba(${C[p.c]},${Math.min(1, A + .25)})`; ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832); ctx.fill(); }
    }
    if (!reduce) requestAnimationFrame(frame);
  };
  size();
  addEventListener('resize', () => { clearTimeout(startNet.t); startNet.t = setTimeout(size, 150); });
  addEventListener('pointermove', e => { mouse.x = e.clientX; mouse.y = e.clientY; }, { passive: true });
  document.addEventListener('pointerleave', () => { mouse.x = mouse.y = -1e4; });
  requestAnimationFrame(frame);
}
ACT.setExam = el => { S.settings.exam = el.dataset.v; save(); render(true); };
INP.examDate = el => { if (el.value) { S.settings.exam = el.value; save(); render(true); } };
ACT.setTheme = el => { S.settings.theme = el.dataset.v === 'dark' ? 'dark' : 'light'; applySettings(); save(); render(true); };
ACT.setFont = el => { S.settings.font = el.dataset.v; applySettings(); save(); render(true); };
ACT.backup = () => { const d = new Date(); download(`kkuaelt45-backup-${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}.json`, JSON.stringify(S), 'application/json'); toast('ดาวน์โหลดไฟล์สำรองแล้ว'); };
INP.restore = el => { const f = el.files && el.files[0]; if (!f) return; const rd = new FileReader(); rd.onload = () => { try { const s = JSON.parse(rd.result); if (!s || s.v !== 2) throw new Error('รูปแบบไฟล์ไม่ถูกต้อง'); if (!confirm('แทนที่ข้อมูลปัจจุบันด้วยไฟล์สำรอง?')) return; S = migratePlan42(Object.assign(defaultState(), s, { plan42: s.plan42 || 0 })); S.settings = Object.assign(defaultState().settings, s.settings || {}, { ai: 1, bright: 1 }); save(true); applySettings(); render(); toast('กู้คืนข้อมูลแล้ว'); } catch (e) { alert('กู้คืนไม่ได้: ' + e.message); } }; rd.readAsText(f); };
ACT.resetAll = () => { if (!confirm('ลบคำตอบ งานเขียน และบันทึกทั้งหมด?')) return; if (!confirm('ยืนยันอีกครั้ง — ลบแล้วกู้คืนไม่ได้ (ยกเว้นมีไฟล์สำรอง)')) return; S = defaultState(); save(true); applySettings(); render(); };

function viewMore() {
  const tiles = [['#/writing', 'pen', 'Writing Studio', 'งานเขียนทั้งหมด คลังหัวข้อ ตัวอย่าง'], ['#/stats', 'chart', 'สถิติ', 'คะแนน Test/Mock และทักษะ'], ['#/guide', 'book', 'คู่มือ', 'ข้อมูลข้อสอบ กลยุทธ์ template checklist'], ['#/settings', 'gear', 'ตั้งค่า', 'วันสอบ ธีม ขนาดตัวอักษร สำรองข้อมูล']];
  return `<div class="card"><h1>เมนู</h1><div class="grid g2">${tiles.map(([hr, ic, t, d]) => `<a class="kpi menu-tile" href="${hr}">${ico(ic)}<span><b>${t}</b><span class="small muted" style="display:block">${d}</span></span></a>`).join('')}</div></div>`;
}


/* ---------- router / layout ---------- */
function parseHash() { const h = (location.hash || '#/today').replace(/^#\/?/, ''); const p = h.split('/'); return { view: p[0] || 'today', a: p[1], b: p[2] }; }
let lastSig = '';
function render(keep) {
  const r = parseHash(); const y = window.scrollY; let html;
  try {
    switch (r.view) {
      case 'today': html = viewDay(todayNum(), r.a); break;
      case 'day': html = viewDay(+r.a || 1, r.b); break;
      case 'plan': html = viewPlan(); break;
      case 'vocab': html = viewVocab(); break;
      case 'errors': html = viewErrors(); break;
      case 'writing': html = viewWriting(r.a); break;
      case 'stats': html = viewStats(); break;
      case 'guide': html = viewGuide(r.a); break;
      case 'test': html = viewTest(r.a); break;
      case 'settings': html = viewSettings(); break;
      case 'more': html = viewMore(); break;
      default: html = viewDay(todayNum());
    }
  } catch (e) { console.error(e); html = `<div class="card"><h2>เกิดข้อผิดพลาด</h2><p>${esc(e.message)}</p><a class="btn" href="#/today">กลับหน้าวันนี้</a></div>`; }
  $('#main').innerHTML = html;
  document.body.classList.toggle('dash-on', !!$('#main .dashwrap')); fitDash();
  const nv = r.view === 'day' && +r.a === todayNum() ? 'today' : r.view;
  $$('[data-nav]').forEach(a => a.classList.toggle('on', a.dataset.nav === nv || (a.dataset.nav === 'more' && ['writing', 'stats', 'guide', 'settings'].includes(nv))));
  document.body.classList.toggle('testing', r.view === 'test' && testStatus(r.a) === 'running');
  const sig = location.hash;
  if (keep && sig === lastSig) window.scrollTo(0, y); else window.scrollTo(0, 0);
  lastSig = sig; tick(); updateCountdown();
}
// keep the day dashboard on one screen: compact first, and only let the page scroll if the hero still cannot fit
function fitDash() {
  const w = $('#main .dashwrap'); if (!w) return;
  w.classList.remove('tight', 'free', 'steps1', 'steps2');
  const hero = w.querySelector('.tile.hero'), cta = hero && hero.querySelector('.hero-cta'); if (!cta) return;
  const over = () => cta.getBoundingClientRect().bottom > hero.getBoundingClientRect().bottom - 12;
  if (over()) { w.classList.add('tight'); if (over()) w.classList.add('free'); }
  // every step row should stay visible: fall back to one-line notes before letting the list scroll
  // measured from layout boxes (offsetTop), so the rows' entrance animation cannot fake an overflow
  const overflows = el => { const last = el && el.lastElementChild; return !!last && last.offsetTop + last.offsetHeight > el.clientHeight + 2; };
  const sl = w.querySelector('.steps-list'); if (overflows(sl)) { w.classList.add('steps1'); if (overflows(sl)) w.classList.add('steps2'); }
  const rl = w.querySelector('.readtile .readlist'); if (rl) rl.classList.toggle('has-more', overflows(rl));
}
window.addEventListener('resize', () => { clearTimeout(fitDash.t); fitDash.t = setTimeout(fitDash, 120); });
if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => fitDash());
function updateCountdown() {
  const n = daysToExam(); const ex = examDate();
  $('#countdown').innerHTML = n > 0 ? `<span class="pulse"></span>T–<b>${n}</b> วัน<span class="cd-date"> · สอบ ${ex.getDate()} ${TH_M[ex.getMonth()]}</span>` : n === 0 ? '<span class="pulse"></span><b>วันนี้วันสอบ</b>' : 'ผ่านวันสอบแล้ว';
  const sc = $('#sideCard'); if (!sc) return;
  const dd = DAYS.filter(x => dayProgress(x.d).done).length; const tn = todayNum(); const pr = dayProgress(tn);
  sc.innerHTML = `<div class="lbl">นับถอยหลังวันสอบ</div><div class="big">${n > 0 ? n + ' <small style="font-size:1rem;font-weight:500">วัน</small>' : n === 0 ? 'วันนี้!' : '—'}</div><div class="lbl">${thDate(ex, true)}</div><div class="bar"><i style="width:${pct(dd, NDAYS)}%"></i></div><div class="lbl">ทำครบ ${dd}/${NDAYS} วัน · วันนี้ ${pr.n}/${pr.total} ขั้น</div>`;
}

window.addEventListener('hashchange', () => render());
document.addEventListener('visibilitychange', () => { if (!document.hidden) tick(); });
function boot() {
  applySettings();
  const w = $('#storageWarn'); if (w) w.hidden = storageOK;
  if (!location.hash) history.replaceState(null, '', '#/today');
  render(); setInterval(tick, 1000); startNet();
}
boot();
