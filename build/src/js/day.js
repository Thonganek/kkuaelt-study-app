/* ============================================================
   Day view
   ============================================================ */
function readItem(it) {
  const name = (DATA.srcName[it.src] || it.src).replace(/_/g, ' '); let link = '';
  if (it.src !== 'app') {
    const file = DATA.files[it.src];
    if (it.pdf) link = `<a class="btn sm lk" href="${fileHref(file, it.pdf)}" target="_blank" rel="noopener" title="เปิด PDF หน้า ${it.pdf} (ไฟล์ต้องอยู่ในโฟลเดอร์เดียวกัน)" aria-label="เปิด PDF หน้า ${it.pdf}">${ico('file')} PDF น.${it.pdf}${it.pdfEnd && it.pdfEnd !== it.pdf ? '–' + it.pdfEnd : ''}</a>`;
    else link = `<a class="btn sm lk" href="${fileHref(file)}" target="_blank" rel="noopener" title="เปิดไฟล์" aria-label="เปิดไฟล์">${ico('file')} เปิดไฟล์</a>`;
    if (it.src === 'guide' || it.src === 'improved' || it.src === 'image') link += ` <a class="btn sm lk" href="#/writing/models" title="อ่านในแอป" aria-label="อ่านในแอป">${ico('eye')} ในแอป</a>`;
  } else if (it.link) link = `<a class="btn sm lk" href="#/${esc(it.link)}" title="เปิดในแอป" aria-label="เปิดในแอป">${ico('arrowr')} เปิด</a>`;
  const pages = it.src === 'book' && it.pages ? ' หน้า ' + esc(it.pages) : (it.pages ? ' ' + esc(it.pages) : '');
  if (it.src === 'app') return `<li>${srcBadge(it.src)}<div><b>${esc(it.what)}</b></div><span class="lks">${link}</span></li>`;
  return `<li>${srcBadge(it.src)}<div><b>${esc(name)}${pages}</b><div class="small">${esc(it.what)}</div></div><span class="lks">${link}</span></li>`;
}
function examsOf(d) {
  const day = DAY(d); const out = [];
  if (day.newWords) out.push({ label: `Quiz คำศัพท์ ${Math.max(20, day.newWords)} ข้อ`, key: 'V:' + d });
  if (day.reading) day.reading.passages.forEach(pid => { const p = DATA.passages[pid]; if (p) out.push({ label: `Reading ${pid}: ${p.questions.length} ข้อ`, key: 'R:' + pid }); });
  if (day.test && DATA.tests[day.test]) out.push({ label: `${DATA.tests[day.test].title}: 69 ข้อ / 120 นาที`, key: 'T:' + day.test });
  day.grams.forEach(id => { if (DATA.grammar[id]) out.push({ label: `Grammar quiz ${DATA.grammar[id].quiz.length} ข้อ (${DATA.grammar[id].title_th})`, key: 'G:' + id }); });
  if (day.task) out.push({ label: `Writing: ${KIND_TH[day.task.kind] || day.task.kind} ${day.task.words}${/[0-9]/.test(day.task.words) && !/ประโยค|จุด|×|outline|thesis/.test(day.task.words) ? ' คำ' : ''} (${day.task.minutes} นาที)`, essay: 'E:' + d, target: targetWords(day.task) });
  if (day.essay) out.push({ label: `Essay ${day.essay.topic} จับเวลา 60 นาที (≥ 250 คำ)`, essay: 'E:' + d, target: 250 });
  if (day.blocks.some(b => b.k === 'vocabreview')) out.push({ label: `ทวนศัพท์ ${vrCount(d)} ข้อ`, key: 'VR:' + d });
  if (day.blocks.some(b => b.k === 'weekly')) out.push({ label: 'ทำซ้ำข้อที่ผิดของสัปดาห์', block: 'weekly' });
  if (day.blocks.some(b => b.k === 'retry')) out.push({ label: 'ทำซ้ำข้อที่ผิดทั้งหมด (≥ 30 ข้อ)', block: 'retry' });
  return out;
}
function examStatus(x, d) {
  if (x.key) { const st = S.quiz[x.key]; if (st && st.done) return `<span class="chip ok">${st.score}/${st.total}</span>`; if (st && st.end && !st.done) return '<span class="chip warn">กำลังทำ</span>'; return '<span class="chip">ยังไม่ทำ</span>'; }
  if (x.essay) { const e = S.essays[x.essay]; const n = e ? wc(e.text) : 0; return n ? `<span class="chip ${n >= (x.target || 1) ? 'ok' : 'warn'}">${n} คำ</span>` : '<span class="chip">ยังไม่เขียน</span>'; }
  if (x.block) return blockDone(d, x.block) ? '<span class="chip ok">' + ico('check') + '</span>' : '<span class="chip">ยังไม่ทำ</span>';
  return '';
}
function targetWords(task) { const w = String(task.words || ''); const m = w.match(/(\d+)/); let n = m ? +m[1] : 0; if (n < 20) return 0; const x = w.match(/×\s*(\d+)/); if (x) n *= +x[1]; return n; }
function vocabSummary(d) {
  const day = DAY(d); const w = DATA.vocab[d];
  if (w && w.length) {
    const subs = [...new Set(w.filter(x => x.src && x.src.startsWith('AWL')).map(x => x.src.replace('AWL', 'AWL Sublist ')))];
    const th = w.filter(x => x.src === 'theme').map(x => x.w);
    return `<b>${w.length} คำใหม่</b>${d === 1 ? ' — ศัพท์งานวิจัยหลัก (significant, evidence, indicate …)' : ''}${subs.length ? '<div class="small">' + esc(subs.join(', ')) + ' (' + w.filter(x => x.src && x.src.startsWith('AWL')).length + ' คำ)</div>' : ''}${th.length ? '<div class="small">ศัพท์หัวข้อ/สำนวน: ' + esc(th.join(', ')) + '</div>' : ''}${day.type === 'test' ? '<div class="small muted">ทำหลังสอบ</div>' : day.type === 'mock' ? '<div class="small muted">ทำหลัง Mock (คำศัพท์วันนี้ใบ้หัวข้อ essay)</div>' : ''}`;
  }
  const rw = reviewWords(d); return rw.all.length ? `<b>ไม่มีคำใหม่</b> — ทวน ${rw.all.length} คำ${day.review ? ' จาก Day ' + day.review.days.join(', ') : ''}` : '—';
}
function readingSummary(day) {
  if (day.test && DATA.tests[day.test]) return `<b>${esc(DATA.tests[day.test].title)}</b><div class="small">6 passages / 69 ข้อ / 120 นาที</div>`;
  if (day.reading) return day.reading.passages.map(pid => { const p = DATA.passages[pid]; return p ? `<div><b>${esc(pid)}</b> ${esc(p.title)} <span class="small muted">(${p.questions.length} ข้อ · ${esc(p.domain)})</span></div>` : `<div>${esc(pid)}</div>`; }).join('') + `<div class="small">ทักษะ: ${esc(day.reading.lessons.map(l => DATA.lessons[l].title).join(' + '))}</div>` + (day.reading.bookTask ? `<div class="small">+ หนังสือ: ${esc(day.reading.bookTask)}</div>` : '');
  if (day.blocks.some(b => b.k === 'weekly' || b.k === 'retry')) return 'ทำซ้ำข้อ Reading ที่เคยผิด';
  return '—';
}
function writingSummary(day) {
  let h = '';
  day.grams.forEach(id => { if (DATA.grammar[id]) h += `<div>Grammar: ${esc(DATA.grammar[id].title_th)}</div>`; });
  if (day.task) h += `<div><b>${esc(KIND_TH[day.task.kind] || '')}</b> ${day.task.topic && DATA.essays[day.task.topic] ? '(' + esc(day.task.topic) + ') ' : ''}${esc(day.task.prompt)}</div>`;
  if (day.essay) { const e = DATA.essays[day.essay.topic]; h += `<div><b>Essay 60 นาที (${esc(day.essay.topic)})</b> ${esc(e ? e.prompt : '')}</div>`; }
  return h || '—';
}

const KIND = { vocab: ['k-teal', 'type'], reading: ['k-sky', 'news'], writing: ['k-emerald', 'pen'], errors: ['k-amber', 'note'], test: ['k-blue', 'list'], review: ['k-green', 'retry'], essay: ['k-emerald', 'pen'], weekly: ['k-amber', 'retry'], vocabreview: ['k-teal', 'cards'], retry: ['k-green', 'retry'] };
const SHORT = { vocab: 'คำศัพท์', reading: 'Reading', writing: 'Writing', errors: 'ข้อผิดพลาด', test: 'Reading Test', review: 'ตรวจผล', essay: 'Essay', weekly: 'ทวนข้อผิด', vocabreview: 'ทวนศัพท์', retry: 'ทำข้อผิดซ้ำ' };
const blockHref = (d, k) => `#/day/${d}/${k}`;
function nextBlock(d) { return DAY(d).blocks.find(b => !blockDone(d, b.k)) || null; }
function dayBanners(d) {
  const tn = rawTodayNum(); let h = '';
  if (d === 1 && tn < 1) h += `<div class="banner info">${ico('calendar')}<span>แผนเริ่มเสาร์ที่ 10 ต.ค. 2569 — ตอนนี้แสดง Day 1 ล่วงหน้า</span></div>`;
  if (tn > NDAYS && d === NDAYS) h += `<div class="banner info">${ico('spark')}<span>ครบ ${NDAYS} วันแล้ว — ใช้หน้า “ข้อผิดพลาด” และ “คำศัพท์” ทบทวนต่อได้</span></div>`;
  if (d === 36 || d === 32) h += `<div class="banner warn">${ico('alert')}<span>ปฏิทิน PBT 2569 ของศูนย์ฯ ระบุสอบรอบพฤศจิกายน <b>เสาร์ 14 พ.ย.</b> — ถ้าวันสอบจริงของคุณคือ 14 พ.ย. ให้ดู “แผนย่อ” ใน <a href="#/guide/exam">คู่มือ → ข้อมูลข้อสอบ</a></span></div>`;
  return h;
}
function daySwitch(d) {
  const opts = DAYS.map(x => `<option value="${x.d}" ${x.d === d ? 'selected' : ''}>Day ${x.d} · ${x.dateTh} — ${x.title}</option>`).join('');
  return `<div class="dayswitch noprint"><button class="iconbtn" data-act="go" data-href="#/day/${Math.max(1, d - 1)}" ${d === 1 ? 'disabled' : ''} aria-label="วันก่อนหน้า">${ico('arrowl')}</button><select data-chg="pickDay" aria-label="เลือกวัน">${opts}</select><button class="iconbtn" data-act="go" data-href="#/day/${Math.min(NDAYS, d + 1)}" ${d === NDAYS ? 'disabled' : ''} aria-label="วันถัดไป">${ico('arrowr')}</button></div>`;
}
function progressRing(n, total, id) {
  const R = 46, C = 2 * Math.PI * R; const done = n === total;
  return `<svg class="ring" viewBox="0 0 112 112" role="img" aria-label="ทำแล้ว ${n} จาก ${total} ขั้น"><defs><linearGradient id="${id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" style="stop-color:var(--sky)"/><stop offset="1" style="stop-color:var(--emerald)"/></linearGradient></defs><circle class="track" cx="56" cy="56" r="${R}" fill="none" stroke-width="10"/><circle cx="56" cy="56" r="${R}" fill="none" stroke="${done ? 'var(--good)' : `url(#${id})`}" stroke-width="10" stroke-linecap="round" stroke-dasharray="${(C * n / total).toFixed(1)} ${C.toFixed(1)}" transform="rotate(-90 56 56)"/><text x="56" y="60" text-anchor="middle">${n}/${total}</text><text class="sub2" x="56" y="76" text-anchor="middle">ขั้น</text></svg>`;
}
function taskWords(t) { const w = String(t.words || ''); return w + (/[0-9]/.test(w) && !/ประโยค|จุด|×|outline|thesis|คำ/.test(w) ? ' คำ' : ''); }
function brief(d, k) {
  const day = DAY(d);
  switch (k) {
    case 'vocab': { const w = DATA.vocab[d] || []; return `${w.length} คำใหม่${day.type === 'test' || day.type === 'mock' ? ' (ทำหลังสอบ)' : ''} · ${w.slice(0, 4).map(x => x.w).join(', ')} …`; }
    case 'reading': return (day.reading ? day.reading.passages : []).map(pid => `${pid} ${DATA.passages[pid] ? DATA.passages[pid].title : ''}`).join(' · ');
    case 'writing': return [day.grams.length ? 'Grammar: ' + day.grams.map(id => DATA.grammar[id] ? DATA.grammar[id].title_th : id).join(' + ') : '', day.task ? (KIND_TH[day.task.kind] || '') + ' ' + taskWords(day.task) : ''].filter(Boolean).join(' · ');
    case 'errors': return day.error;
    case 'test': { const t = DATA.tests[day.test]; return `${t ? t.title : day.test} · 6 passages · 69 ข้อ`; }
    case 'review': return 'อ่านเฉลยทุกข้อที่ผิด ดูผลรายทักษะ แล้วจดสมุดข้อผิดพลาด';
    case 'essay': { const e = DATA.essays[day.essay.topic]; return `${day.essay.topic}: ${e ? e.prompt : ''}`; }
    case 'weekly': return `ทำซ้ำข้อที่ผิดจาก Day ${day.review.days.join(', ')}`;
    case 'vocabreview': return `Quiz ทวนศัพท์จาก ${reviewWords(d).all.length} คำ (คำติดดาวขึ้นก่อน)`;
    case 'retry': return 'ทำซ้ำข้อที่ยังไม่ถูกจาก Test/Mock ทั้งหมด (≥ 30 ข้อ)';
  }
  return '';
}
function scoreOf(d, k) {
  const day = DAY(d); const q = key => S.quiz[key] && S.quiz[key].done ? S.quiz[key] : null; const f = s => s.score + '/' + s.total;
  if (k === 'vocab') { const s = q('V:' + d); return s ? f(s) : ''; }
  if (k === 'vocabreview') { const s = q('VR:' + d); return s ? f(s) : ''; }
  if (k === 'test') { const s = q('T:' + day.test); return s ? f(s) : ''; }
  if (k === 'reading' && day.reading) return day.reading.passages.map(pid => q('R:' + pid)).filter(Boolean).map(f).join(' · ');
  if (k === 'writing' || k === 'essay') { const e = S.essays['E:' + d]; const n = e ? wc(e.text) : 0; return n ? n + ' คำ' : ''; }
  return '';
}
function stepRow(d, b, i, nb) {
  const [kc, ic] = KIND[b.k] || ['k-sky', 'spark']; const done = blockDone(d, b.k); const info = DATA.blockInfo[b.k];
  const sc = scoreOf(d, b.k); const isNext = nb && nb.k === b.k;
  const st = done ? `<span class="pill ok">${ico('check')} ${esc(sc || 'เสร็จ')}</span>` : isNext ? `<span class="pill nx">เริ่ม ${ico('arrowr')}</span>` : sc ? `<span class="pill">${esc(sc)}</span>` : `<span class="go">${ico('arrowr')}</span>`;
  return `<a class="srow ${kc} ${done ? 'done' : ''} ${isNext ? 'next' : ''}" href="${blockHref(d, b.k)}" style="animation-delay:${120 + i * 50}ms"><span class="kchip">${ico(done ? 'check' : ic)}</span><span class="m"><span class="t"><b>${esc(info[0])}</b></span><span class="l"><span class="mn">${b.min} นาที</span> · ${esc(brief(d, b.k))}</span></span>${st}</a>`;
}
function viewDay(d, focus) {
  d = Math.min(NDAYS, Math.max(1, d | 0)); const day = DAY(d); S.ui.lastDay = d;
  if (focus && day.blocks.some(b => b.k === focus)) return viewBlock(d, focus);
  return viewDayBento(d);
}
let _cum = null;
function planCum() {
  if (_cum) return _cum;
  let w = 0, p = 0, wr = 0, es = 0; const by = {};
  for (const x of DAYS) {
    w += (DATA.vocab[x.d] || []).length;
    p += (x.reading ? x.reading.passages.length : 0) + (x.test && DATA.tests[x.test] ? DATA.tests[x.test].passages.length : 0);
    if (x.task || x.essay) wr++;
    if (x.essay || (x.task && x.task.kind === 'essay')) es++;
    by[x.d] = { w, p, wr, es };
  }
  return (_cum = { by, w, p, wr, es });
}
function dayQuizSets(d) {
  const day = DAY(d); const s = []; const qn = pid => DATA.passages[pid] ? DATA.passages[pid].questions.length : 0;
  if ((DATA.vocab[d] || []).length) s.push(['V:' + d, Math.max(20, DATA.vocab[d].length)]);
  if (day.reading) day.reading.passages.forEach(pid => s.push(['R:' + pid, qn(pid)]));
  if (day.test && DATA.tests[day.test]) s.push(['T:' + day.test, DATA.tests[day.test].passages.reduce((a, pid) => a + qn(pid), 0)]);
  day.grams.forEach(id => { if (DATA.grammar[id]) s.push(['G:' + id, DATA.grammar[id].quiz.length]); });
  if (day.blocks.some(b => b.k === 'vocabreview')) s.push(['VR:' + d, Math.min(vrCount(d), reviewWords(d).all.length)]);
  return s;
}
function heroStats(d) {
  const day = DAY(d); const C = planCum(); const c = C.by[d];
  const cell = (ic, label, val, unit, bar, sub) => `<div class="hs"><div class="hs-top">${ico(ic)}<span>${label}</span></div><div class="hs-val${String(val).length > 9 ? ' sm' : ''}">${val}${unit ? ` <small>${unit}</small>` : ''}</div><div class="hs-bar"><i style="width:${Math.max(0, Math.min(100, bar)).toFixed(1)}%"></i></div><div class="hs-sub">${sub}</div></div>`;
  let h = '';
  const nw = (DATA.vocab[d] || []).length;
  if (nw) h += cell('type', 'ศัพท์ใหม่', nw, 'คำ', 100 * c.w / C.w, `สะสม ${c.w} / ${C.w} คำ`);
  else h += cell('cards', 'ทวนศัพท์', reviewWords(d).all.length, 'คำ', 100 * c.w / C.w, `เรียนแล้ว ${c.w} / ${C.w} คำ`);
  const tp = day.test && DATA.tests[day.test] ? DATA.tests[day.test].passages : [];
  const rp = (day.reading ? day.reading.passages : []).concat(tp);
  const rq = rp.reduce((s, pid) => s + (DATA.passages[pid] ? DATA.passages[pid].questions.length : 0), 0);
  if (rp.length) h += cell('news', tp.length ? 'Reading Test' : 'ฝึกอ่าน', rp.length, `บท · ${rq} ข้อ`, 100 * c.p / C.p, `สะสม ${c.p} / ${C.p} บท`);
  else h += cell('retry', 'ฝึกอ่าน', 'ทวนข้อผิด', '', 100 * c.p / C.p, `อ่านแล้ว ${c.p} / ${C.p} บท`);
  if (day.essay) h += cell('pen', 'Essay 60 นาที', '≥ 250', 'คำ', 100 * c.es / C.es, `Essay เต็มชิ้นที่ ${c.es} / ${C.es}`);
  else if (day.task) {
    // long targets ("50–60 คำ + 5 ประโยค") keep the first part as the number and move the rest to the line below
    const [first, ...more] = String(day.task.words).split(' + ');
    const unit = /[0-9]/.test(first) && !/ประโยค|จุด|×|outline|thesis|คำ/.test(first) ? 'คำ' : '';
    h += cell('pen', 'ฝึกเขียน', esc(first), unit, 100 * c.wr / C.wr, `${more.length ? `<span class="more">+ ${esc(more.join(' + '))}</span>` : ''}${esc(KIND_TH[day.task.kind] || '')} · ชิ้นที่ ${c.wr} / ${C.wr}`);
  } else h += cell('pen', 'ฝึกเขียน', 'พักเขียน', '', 100 * c.wr / C.wr, `เขียนแล้ว ${c.wr} / ${C.wr} ชิ้น`);
  const sets = dayQuizSets(d); const tq = sets.reduce((s, x) => s + x[1], 0); const dn = sets.filter(x => S.quiz[x[0]] && S.quiz[x[0]].done).length;
  h += cell('list', 'ข้อสอบวันนี้', tq, 'ข้อ', sets.length ? 100 * dn / sets.length : 0, `ส่งแล้ว ${dn} / ${sets.length} ชุด`);
  return `<div class="hero-stats" aria-label="เป้าหมายวันนี้">${h}</div>`;
}
function viewDayBento(d) {
  const day = DAY(d); const pr = dayProgress(d); const ph = PHASE[day.phase]; const tn = todayNum(); const isToday = d === tn;
  const nb = nextBlock(d); const n = daysToExam(); const ex = examDate();
  const doneDays = DAYS.filter(x => dayProgress(x.d).done).length;
  let h = `<div class="dashwrap"><div class="pagehead"><div><div class="eyebrow">${isToday ? 'วันนี้ · ' : ''}${esc(day.wd)} ${esc(day.dateTh)}</div><h1>${isToday ? 'แผนวันนี้' : d < tn ? 'ย้อนดู Day ' + d : 'ดูล่วงหน้า Day ' + d}</h1></div><div class="row noprint">${isToday ? '' : `<a class="btn sm" href="#/today">${ico('target')} กลับวันนี้ · Day ${tn}</a>`}${daySwitch(d)}</div></div>`;
  h += dayBanners(d);
  h += `<div class="dash">`;
  // hero: what today is about + the numbers to hit
  h += `<section class="tile hero"><div class="foil" aria-hidden="true"></div><div class="shine" aria-hidden="true"></div><svg class="hero-core" viewBox="0 0 240 240" aria-hidden="true"><defs><radialGradient id="hcG"><stop offset="0" stop-color="#ffffff"/><stop offset=".26" stop-color="#cffafe"/><stop offset=".55" stop-color="#22d3ee" stop-opacity=".55"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></radialGradient><linearGradient id="hcL" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#67e8f9"/><stop offset=".5" stop-color="#a5f3fc"/><stop offset="1" stop-color="#fde68a"/></linearGradient></defs><circle class="core" cx="120" cy="120" r="44" fill="url(#hcG)"/><g class="orb o1"><circle cx="120" cy="120" r="62" fill="none" stroke="url(#hcL)" stroke-width="1.3" stroke-dasharray="3 7"/><circle cx="182" cy="120" r="3.6" fill="#a5f3fc"/></g><g class="orb o2"><ellipse cx="120" cy="120" rx="92" ry="34" fill="none" stroke="url(#hcL)" stroke-width="1" opacity=".75"/><circle cx="212" cy="120" r="3" fill="#fde68a"/><circle cx="28" cy="120" r="2.2" fill="#a5f3fc"/></g><g class="orb o3"><ellipse cx="120" cy="120" rx="34" ry="96" fill="none" stroke="url(#hcL)" stroke-width="1" opacity=".55"/><circle cx="120" cy="24" r="2.6" fill="#fef3c7"/></g><g class="ticks"><circle cx="120" cy="120" r="110" fill="none" stroke="rgba(165,243,252,.35)" stroke-width="1" stroke-dasharray="1 6"/></g></svg>
  <div class="hero-head"><div class="hero-num"><small>DAY</small><b>${String(d).padStart(2, '0')}</b><span>/ ${NDAYS}</span></div><div class="hero-top"><span class="glass">${esc(ph.name)}</span><span class="glass">${esc(TYPE_TH[day.type])}</span><span class="glass">${ico('clock')} ${day.minutes} นาที</span></div></div>
  <h2 class="hero-title">${esc(day.title)}</h2>
  <p class="hero-goal">${esc(day.goal)}</p>
  ${heroStats(d)}
  ${nb ? `<a class="hero-cta" href="${blockHref(d, nb.k)}">${ico('play')} ${pr.n ? 'ทำต่อ' : 'เริ่มเลย'}: ${esc(DATA.blockInfo[nb.k][0])} ${ico('arrowr')}</a>` : d < NDAYS ? `<a class="hero-cta" href="#/day/${d + 1}">${ico('check')} ครบแล้ว · ไป Day ${d + 1} ${ico('arrowr')}</a>` : `<span class="hero-cta">${ico('spark')} ครบ ${NDAYS} วัน</span>`}
  </section>`;
  // middle: countdown/progress + the day's steps
  h += `<div class="dcol"><div class="tile statpair"><div class="sp"><div class="tile-label">${ico('flag')} นับถอยหลังวันสอบ</div><div class="stat-num">${n > 0 ? n : n === 0 ? '0' : '—'}<small> วัน</small></div><div class="sub small">${n > 0 ? 'สอบ ' + thDate(ex, true) : n === 0 ? 'วันนี้วันสอบ — สู้ ๆ' : 'ผ่านวันสอบแล้ว'}</div></div><div class="sp"><div class="tile-label">${ico('chart')} ความคืบหน้า</div><div class="ringwrap">${progressRing(pr.n, pr.total, 'rg' + d)}<div><b>${pr.done ? 'ครบแล้ว' : 'เหลือ ' + (pr.total - pr.n) + ' ขั้น'}</b><div class="sub small">แผน ${doneDays}/${NDAYS} วัน</div></div></div></div></div>`;
  h += `<section class="tile stepstile"><div class="tile-label">${ico('list')} ขั้นตอนวันนี้<span class="spacer"></span><span class="pill">${pr.n}/${pr.total} เสร็จ</span></div><div class="steps-list">${day.blocks.map((b, i) => stepRow(d, b, i, nb)).join('')}</div></section></div>`;
  // right: what to read + today's focus
  const fr = day.focusR && day.focusR !== '—' ? day.focusR : '', fw = day.focusW && day.focusW !== '—' ? day.focusW : '';
  h += `<div class="dcol"><section class="tile readtile"><div class="tile-label">${ico('book')} วันนี้อ่านอะไร<span class="spacer"></span><span class="pill">${day.read.length} รายการ</span></div><ul class="readlist">${day.read.map(readItem).join('')}</ul>${fr || fw ? `<div class="focusbox"><div class="tile-label">${ico('target')} โฟกัสวันนี้</div>${fr ? `<div class="fx k-sky"><span class="kchip">${ico('news')}</span><div><small>Reading</small><b>${esc(fr)}</b></div></div>` : ''}${fw ? `<div class="fx k-emerald"><span class="kchip">${ico('pen')}</span><div><small>Writing</small><b>${esc(fw)}</b></div></div>` : ''}</div>` : ''}</section></div>`;
  h += `<section class="tile runtile noprint">${runway(d)}</section>`;
  h += `</div></div>`;
  return h;
}
function viewBlock(d, k) {
  const day = DAY(d); const i = day.blocks.findIndex(b => b.k === k); const b = day.blocks[i]; const info = DATA.blockInfo[k];
  const done = blockDone(d, k); const [kc, ic] = KIND[k] || ['k-sky', 'spark'];
  const noTimer = ['test', 'review', 'essay'].includes(k) || (k === 'reading' && day.reading && day.reading.timed);
  let inner = '';
  try { inner = { vocab: secVocab, reading: secReading, writing: secWriting, errors: secErrors, test: secTest, review: secReview, essay: secEssay, weekly: secWeekly, vocabreview: secVocabReview, retry: secRetry }[k](d, b); }
  catch (e) { inner = `<div class="callout warn">แสดงส่วนนี้ไม่ได้: ${esc(e.message)}</div>`; console.error(e); }
  let h = `<div class="blockhead ${kc}"><a class="iconbtn noprint" href="#/day/${d}" aria-label="กลับภาพรวม Day ${d}">${ico('arrowl')}</a><span class="kchip">${ico(done ? 'check' : ic)}</span><div style="min-width:0"><div class="eyebrow">Day ${d} · ${esc(day.dateTh)} · ขั้น ${i + 1}/${day.blocks.length} · ${b.min} นาที</div><h1>${esc(info[0])}</h1></div><span class="spacer"></span><div class="row noprint">${noTimer ? '' : timerBtn('B:' + d + ':' + k, b.min, 'Day ' + d + ' · ' + info[0])}<button class="btn sm ${done ? '' : 'pri'}" data-act="toggleBlock" data-d="${d}" data-k="${k}">${done ? ico('retry') + ' ยกเลิกเสร็จ' : ico('check') + ' ทำเสร็จแล้ว'}</button></div></div>`;
  h += `<nav class="stepper noprint" aria-label="ขั้นของวัน"><a href="#/day/${d}">${ico('grid')} ภาพรวม</a>${day.blocks.map((x, j) => { const dn = blockDone(d, x.k); return `<a class="${x.k === k ? 'on' : ''} ${dn ? 'done' : ''}" href="${blockHref(d, x.k)}" ${x.k === k ? 'aria-current="step"' : ''}><span class="dot">${dn ? ico('check') : j + 1}</span>${esc(SHORT[x.k] || x.k)}</a>`; }).join('')}</nav>`;
  h += dayBanners(d);
  h += `<section class="card section" id="sec-${k}"><p class="lead">${ico('bulb')}<span>${esc(info[1])}</span></p>${inner}</section>`;
  const prev = i > 0 ? day.blocks[i - 1] : null, next = i < day.blocks.length - 1 ? day.blocks[i + 1] : null;
  h += `<div class="stepnav noprint">${prev ? `<a class="btn" href="${blockHref(d, prev.k)}">${ico('arrowl')} ${esc(DATA.blockInfo[prev.k][0])}</a>` : `<a class="btn" href="#/day/${d}">${ico('grid')} ภาพรวม Day ${d}</a>`}${next ? `<a class="btn pri" href="${blockHref(d, next.k)}">ขั้นต่อไป: ${esc(DATA.blockInfo[next.k][0])} ${ico('arrowr')}</a>` : d < NDAYS ? `<a class="btn pri" href="#/day/${d + 1}">จบวันนี้ · ไป Day ${d + 1} ${ico('arrowr')}</a>` : `<span class="chip ok">${ico('spark')} ครบ ${NDAYS} วัน</span>`}</div>`;
  return h;
}
function runway(d) {
  const tn = rawTodayNum(); let cells = '';
  for (const x of DAYS) {
    const pr = dayProgress(x.d);
    const cls = ['rw', x.type === 'test' ? 'test' : x.type === 'mock' ? 'mock' : x.type === 'sunday' ? 'sun' : '', pr.done ? 'done' : '', x.d === d ? 'cur' : '', x.d === tn ? 'today' : ''].filter(Boolean).join(' ');
    cells += `<a class="${cls}" href="#/day/${x.d}" title="Day ${x.d} · ${esc(x.wd)} ${esc(x.dateTh)} · ${esc(x.title)}" aria-label="Day ${x.d}"></a>`;
  }
  const ex = examDate();
  const lab = (n, txt, end) => `<span style="grid-column:${end ? (n - 5) + ' / ' + (n + 1) : n + ' / span 7'};${end ? 'text-align:right' : ''}">${txt}</span>`;
  return `<div class="runway"><div class="rw-head"><div class="tile-label">${ico('calendar')} เส้นทาง ${NDAYS} วัน</div><div class="rw-legend"><span><i style="background:var(--sky)"></i>Reading Test</span><span><i style="background:var(--teal)"></i>Mock</span><span><i style="background:var(--emerald)"></i>Essay วันอาทิตย์</span><span><i style="background:var(--surface-3)"></i>วันธรรมดา</span></div></div>
  <div class="rw-track" style="--n:${NDAYS}">${cells}<span class="rw-flag">${ico('flag')}<span>สอบ ${ex.getDate()} ${TH_M[ex.getMonth()]}</span></span></div>
  <div class="rw-scale" style="--n:${NDAYS}">${[1, 15, 29].map(n => lab(n, shortDate(n))).join('')}${lab(NDAYS, shortDate(NDAYS), true)}</div></div>`;
}
function shortDate(n) { const x = dayDate(n); return x.getDate() + ' ' + TH_M[x.getMonth()]; }
INP.pickDay = el => { location.hash = '#/day/' + el.value; };

/* ---------- vocab section ---------- */
function vcard(w) {
  const st = S.vstat[w.w];
  return `<div class="vcard"><div class="tools">${canSpeak ? `<button class="iconbtn" data-act="speak" data-w="${esc(w.w)}" title="ฟังเสียง" aria-label="ฟังเสียง ${esc(w.w)}">${ico('volume')}</button>` : ''}<button class="star ${st === 2 ? 'on' : ''}" data-act="star" data-w="${esc(w.w)}" title="ติดดาว = ยังจำไม่ได้" aria-label="ติดดาว">${ico('star')}</button></div>
  <div><span class="w">${esc(w.w)}</span><span class="pos">${esc(w.pos || '')}</span>${st === 1 ? ' <span class="known small">' + ico('check') + ' จำได้</span>' : ''}</div><div class="th">${esc(w.th)}</div>${w.fam ? `<div class="fam">ครอบครัวคำ: ${esc(w.fam)}</div>` : ''}${w.col ? `<div class="col">คำที่มักใช้คู่: ${esc(w.col)}</div>` : ''}${w.ex ? `<div class="ex">${esc(w.ex)}</div>` : ''}</div>`;
}
ACT.star = el => { const w = el.dataset.w; S.vstat[w] = S.vstat[w] === 2 ? 0 : 2; save(); el.classList.toggle('on', S.vstat[w] === 2); };
ACT.hideTh = el => { S.ui.hideTh = !S.ui.hideTh; save(); render(true); };
function flashcards(key, words) {
  S.ui.fc = S.ui.fc || {}; const i = Math.min(words.length - 1, S.ui.fc[key] || 0); const w = words[i]; if (!w) return '';
  const flip = S.ui.fcFlip === key + i;
  return `<div class="fc"><div class="small muted">บัตรคำ ${i + 1}/${words.length} · คลิกบัตรเพื่อพลิก</div><div class="fcard" data-act="fcFlip" data-key="${esc(key)}" data-i="${i}" role="button" tabindex="0"><div class="w">${esc(w.w)}</div><div class="muted">${esc(w.pos || '')}</div>${flip ? `<div class="th">${esc(w.th)}</div><div class="small" style="margin-top:6px">${esc(w.ex || '')}</div>` : '<div class="small muted" style="margin-top:10px">(คิดความหมายก่อน แล้วคลิก)</div>'}</div>
  <div class="row" style="justify-content:center;margin-top:10px"><button class="btn sm" data-act="fcNav" data-key="${esc(key)}" data-n="${words.length}" data-dir="-1" aria-label="ก่อนหน้า">${ico('arrowl')}</button><button class="btn sm good" data-act="fcMark" data-key="${esc(key)}" data-w="${esc(w.w)}" data-v="1" data-n="${words.length}">${ico('check')} จำได้</button><button class="btn sm" data-act="fcMark" data-key="${esc(key)}" data-w="${esc(w.w)}" data-v="2" data-n="${words.length}">${ico('star')} ยังไม่จำ</button>${canSpeak ? `<button class="btn sm" data-act="speak" data-w="${esc(w.w)}" aria-label="ฟังเสียง">${ico('volume')}</button>` : ''}<button class="btn sm" data-act="fcNav" data-key="${esc(key)}" data-n="${words.length}" data-dir="1" aria-label="ถัดไป">${ico('arrowr')}</button></div></div>`;
}
ACT.fcFlip = el => { S.ui.fcFlip = S.ui.fcFlip === el.dataset.key + el.dataset.i ? null : el.dataset.key + el.dataset.i; render(true); };
ACT.fcNav = el => { S.ui.fc[el.dataset.key] = ((S.ui.fc[el.dataset.key] || 0) + (+el.dataset.dir) + (+el.dataset.n)) % (+el.dataset.n); S.ui.fcFlip = null; save(); render(true); };
ACT.fcMark = el => { S.vstat[el.dataset.w] = +el.dataset.v; S.ui.fc[el.dataset.key] = ((S.ui.fc[el.dataset.key] || 0) + 1) % (+el.dataset.n); S.ui.fcFlip = null; save(); render(true); };
ACT.fcMode = el => { S.ui.fcMode = S.ui.fcMode === el.dataset.key ? null : el.dataset.key; save(); render(true); };
function secVocab(d) {
  const words = (DATA.vocab[d] || []).map(w => Object.assign({ day: d }, w)); if (!words.length) return '<p class="muted">วันนี้ไม่มีคำใหม่</p>';
  const key = 'vd' + d; const fcOn = S.ui.fcMode === key;
  let h = `<div class="row noprint" style="margin-bottom:10px"><button class="btn sm" data-act="hideTh">${S.ui.hideTh ? ico('eye') + ' แสดงความหมาย' : ico('eyeoff') + ' ซ่อนความหมาย (ทดสอบตัวเอง)'}</button><button class="btn sm" data-act="fcMode" data-key="${key}">${fcOn ? ico('grid') + ' กลับไปแบบรายการ' : ico('cards') + ' โหมดบัตรคำ'}</button><span class="small muted">${ico('star')} = ยังจำไม่ได้ (จะถูกดึงมาทวนวันอาทิตย์และวันที่ 44)</span></div>`;
  h += fcOn ? flashcards(key, words) : `<div class="vgrid ${S.ui.hideTh ? 'hideth' : ''}">${words.map(vcard).join('')}</div>`;
  h += `<h3>Quiz คำศัพท์ (20 ข้อ: แปลความหมาย / เลือกคำ / เติมคำในประโยค)</h3>` + renderQuiz('V:' + d);
  return h;
}

/* ---------- reading section ---------- */
function lessonBox(lid) {
  const l = DATA.lessons[lid]; if (!l) return '';
  return `<div class="lesson"><b>${ico('bulb')} ${esc(l.title)}</b><ol>${l.steps.map(s => `<li>${esc(s)}</li>`).join('')}</ol>${l.signals ? `<div class="small">คำสัญญาณ: ${l.signals.map(s => `<span class="chip">${esc(s)}</span>`).join(' ')}</div>` : ''}<div class="trap small">${ico('alert')}<span>กับดัก: ${esc(l.trap)}</span></div><div class="small"><b>วันนี้ทำ:</b> ${esc(l.drill)}</div></div>`;
}
function secReading(d) {
  const day = DAY(d); const r = day.reading; let h = r.lessons.map(lessonBox).join('');
  if (r.bookTask) { const it = day.read.find(x => x.src === 'book' && r.bookTask.includes(x.pages.split('–')[0])); h += `<div class="callout"><b>${ico('book')} แบบฝึกในหนังสือ:</b> ${esc(r.bookTask)} ${it ? `<a class="btn sm" href="${fileHref(DATA.files.book, it.pdf)}" target="_blank" rel="noopener">เปิด PDF หน้า ${it.pdf}</a>` : ''}<div class="small muted">ทำในหนังสือแล้วตรวจกับเฉลยในหนังสือ (คำตอบอยู่ท้ายแต่ละแบบฝึก — ปิดครึ่งล่างของหน้าก่อนทำ)</div></div>`; }
  if (r.timed) h += `<div class="callout warn row"><b>จับเวลารวม ${r.timed} นาที</b> (${r.passages.length > 1 ? '12 นาที/บท' : 'บทยาว 30 นาที'}) — ไม่หยุดเวลา<span class="spacer"></span>${timerBtn('B:' + d + ':reading', r.timed, 'Day ' + d + ' · Reading จับเวลา')}</div>`;
  r.passages.forEach((pid, i) => {
    const p = DATA.passages[pid];
    h += `<h3>${r.passages.length > 1 ? 'บทที่ ' + (i + 1) + ': ' : ''}${esc(pid)}${p && p.focus ? ' — ' + esc(p.focus) : ''}</h3>`;
    if (p && p.skill_tip_en) h += `<p class="small"><b>Strategy:</b> ${esc(p.skill_tip_en)}</p>`;
    h += `<div class="readpair">${renderPassage(pid)}<div class="readq">${p ? renderQuiz('R:' + pid) : ''}</div></div>`;
  });
  return h;
}

/* ---------- grammar + writing ---------- */
function lessonBlocks(blocks) {
  return (blocks || []).map(b => {
    let x = `<div><b>${esc(b.h || '')}</b>`;
    if (b.p) x += `<p>${esc(b.p)}</p>`;
    if (b.list) x += `<ul>${b.list.map(s => `<li>${esc(s)}</li>`).join('')}</ul>`;
    if (b.ex) x += `<ul>${b.ex.map(p => `<li><span class="ex-wrong">${esc(p[0])}</span><br><span class="ex-right">${esc(p[1])}</span></li>`).join('')}</ul>`;
    if (b.table) x += `<div class="tablewrap"><table class="t">${b.table.map((r, i) => `<tr>${r.map(c => i === 0 ? `<th>${esc(c)}</th>` : `<td>${esc(c)}</td>`).join('')}</tr>`).join('')}</table></div>`;
    if (b.links) x += `<ul>${b.links.map(l => `<li><a href="${esc(l[1])}" target="_blank" rel="noopener">${esc(l[0])}</a></li>`).join('')}</ul>`;
    return x + '</div>';
  }).join('');
}
function grammarBox(gid) {
  const g = DATA.grammar[gid]; if (!g) return `<div class="callout warn">ยังไม่มีบทเรียน ${esc(gid)}</div>`;
  return `<h3>${ico('braces')} Grammar: ${esc(g.title_th)} <span class="small muted">(${esc(g.title_en)})</span></h3>${g.book ? `<p class="small">อ้างอิง: ${esc(g.book)}</p>` : ''}<details class="more" open><summary>บทเรียน (อ่าน 5 นาที)</summary><div class="lesson">${lessonBlocks(g.lesson)}</div></details><b>Quiz ${g.quiz.length} ข้อ</b>${renderQuiz('G:' + gid)}`;
}
function secWriting(d) {
  const day = DAY(d); let h = '';
  day.grams.forEach(id => { h += grammarBox(id); });
  if (day.task) h += `<h3>${ico('pen')} งานเขียนของวัน</h3>` + writingTask('E:' + d, day.task, d);
  return h;
}
const CHECK10 = DATA.guide.checklist.blocks[0].list;
const CHECK_STRUCT = DATA.guide.checklist.blocks[1].list;
function epeek(key) { const e = S.essays[key] || { text: '', outline: {}, chk: {}, rate: {} }; e.outline = e.outline || {}; e.chk = e.chk || {}; e.rate = e.rate || {}; return e; }
function essayState(key) { if (!S.essays[key]) S.essays[key] = { text: '', outline: {}, chk: {}, rate: {} }; const e = S.essays[key]; e.outline = e.outline || {}; e.chk = e.chk || {}; e.rate = e.rate || {}; return e; }
function topicBox(id) {
  const e = DATA.essays[id]; const t = DATA.topics[id]; if (!e) return '';
  return `<div class="prompt">${esc(e.prompt)}${/agree or disagree/i.test(e.prompt) ? '' : ' <span class="muted">Do you agree or disagree?</span>'}</div><div class="small muted">${esc(t ? t.label : '')}${e.prompt_fixed && e.prompt_fixed.replace(/ Do you agree or disagree\?$/, '') !== e.prompt ? ` · ถ้อยคำที่ถูกไวยากรณ์ (ใช้ช่วย paraphrase): <i>${esc(e.prompt_fixed)}</i>` : ''}</div>`;
}
const PARTS = DATA.meta.parts;
function previousParts(task, d) {
  if (task.kind !== 'parts') return '';
  const list = (PARTS[task.topic] || []).filter(([pd]) => pd < d); if (!list.length) return '';
  let total = 0;
  const body = list.map(([pd, lab]) => { const t = (S.essays['E:' + pd] || {}).text || ''; total += wc(t); return `<div class="model"><div class="lab">${esc(lab)} · Day ${pd} · ${wc(t)} คำ</div>${t ? t.split(/\n+/).map(p => `<p>${esc(p)}</p>`).join('') : '<p class="muted">(ยังไม่ได้เขียน)</p>'}</div>`; }).join('');
  return `<details class="more" open><summary>ส่วนที่เขียนไว้ก่อนหน้า (${total} คำ)</summary>${body}${task.part === 'assemble' ? `<button class="btn sm" data-act="pullParts" data-d="${d}" data-t="${esc(task.topic)}">⤵ คัดลอกทุกส่วนลงในช่องเขียนด้านล่าง</button>` : ''}</details>`;
}
ACT.pullParts = el => {
  const d = +el.dataset.d; const key = 'E:' + d; const e = essayState(key);
  if (e.text && e.text.trim() && !confirm('ช่องเขียนมีข้อความแล้ว ต้องการแทนที่ด้วยส่วนที่เขียนไว้?')) return;
  e.text = (PARTS[el.dataset.t] || []).map(([pd]) => ((S.essays['E:' + pd] || {}).text || '').trim()).filter(Boolean).join('\n\n') + '\n\n';
  save(true); render(true);
};
function writingTask(key, task, d) {
  const e = epeek(key); const n = wc(e.text); const target = targetWords(task);
  let h = `<div class="row"><span class="chip acc">${esc(KIND_TH[task.kind] || task.kind)}</span><span class="chip">เป้าหมาย ${esc(task.words)}</span><span class="chip mono">${ico('clock')} ${task.minutes} นาที</span></div>`;
  const eb = task.topic && DATA.essays[task.topic] && task.kind !== 'summary';
  h += eb ? topicBox(task.topic) + (task.prompt.slice(0, 25) === DATA.essays[task.topic].prompt.slice(0, 25) ? '' : `<p><b>${esc(task.prompt)}</b></p>`) : `<div class="prompt">${esc(task.prompt)}</div>`;
  if (task.steps && task.steps.length) h += `<ol>${task.steps.map(s => `<li>${esc(s)}</li>`).join('')}</ol>`;
  h += previousParts(task, d);
  h += editorBlock(key, task.minutes, target, task.kind === 'sentences' || task.kind === 'intro' || task.kind === 'summary' || task.kind === 'analysis', 'Day ' + d + ' · Writing');
  if (['paragraph', 'essay', 'parts', 'rewrite'].includes(task.kind)) h += checkBlock(key, task.kind === 'essay' || task.part === 'assemble');
  h += modelReveal(key, task, n, target);
  return h;
}
function editorBlock(key, minutes, target, short, label) {
  const e = epeek(key); const n = wc(e.text);
  return `<details class="more noprint"><summary>วางโครงก่อนเขียน (ไม่บังคับ)</summary><div class="outline">${[['i', 'จุดยืน + paraphrase'], ['b1', 'เหตุผล 1 + ตัวอย่าง'], ['b2', 'เหตุผล 2 + ตัวอย่าง'], ['c', 'ประโยคสรุป']].map(([k, l]) => `<textarea data-inp="outline" data-key="${esc(key)}" data-part="${k}" placeholder="${esc(l)}">${esc(e.outline[k] || '')}</textarea>`).join('')}</div></details>
  <textarea class="editor ${short ? 'short' : ''}" data-inp="essay" data-key="${esc(key)}" spellcheck="true" lang="en" placeholder="เขียนภาษาอังกฤษที่นี่ (บันทึกอัตโนมัติ)">${esc(e.text)}</textarea>
  <div class="row"><span class="wc ${target && n >= target ? 'ok' : n ? 'low' : ''}" data-wc="${esc(key)}">${n} คำ${target ? ' / เป้า ' + target : ''}</span><span class="small muted">บันทึกอัตโนมัติในเบราว์เซอร์นี้</span><span class="spacer"></span>${timerBtn('W:' + key, minutes, label)}<button class="btn sm" data-act="dlEssay" data-key="${esc(key)}">${ico('download')} .txt</button></div>`;
}
INP.essay = el => { const key = el.dataset.key; const e = essayState(key); e.text = el.value; e.at = Date.now(); const n = wc(e.text); const w = $(`[data-wc="${CSS.escape(key)}"]`); if (w) { const t = (w.textContent.match(/เป้า (\d+)/) || [])[1]; w.textContent = n + ' คำ' + (t ? ' / เป้า ' + t : ''); w.className = 'wc ' + (t && n >= +t ? 'ok' : n ? 'low' : ''); } save(); };
INP.outline = el => { const e = essayState(el.dataset.key); e.outline[el.dataset.part] = el.value; save(); };
INP.note = el => { S.notes[el.dataset.d] = el.value; save(); };
ACT.dlEssay = el => { const e = essayState(el.dataset.key); download(el.dataset.key.replace(':', '_') + '.txt', e.text || ''); };
ACT.chk = el => { const e = essayState(el.dataset.key); e.chk[el.dataset.i] = el.checked; save(); };
ACT.rate = el => { const e = essayState(el.dataset.key); e.rate[el.dataset.c] = +el.dataset.v; save(); render(true); };
function checkBlock(key, withRate) {
  const e = epeek(key);
  let h = `<details class="more"><summary>ตรวจงานด้วย Checklist (All that IELTS หน้า 68–69 / 380–383 + โครงสร้าง)</summary><div class="checks">` +
    CHECK10.concat(CHECK_STRUCT).map((c, i) => `<label><input type="checkbox" data-act="chk" data-key="${esc(key)}" data-i="${i}" ${e.chk[i] ? 'checked' : ''}> ${esc(c)}</label>`).join('') + `</div>`;
  if (withRate) h += `<div class="small"><b>ประเมินตัวเอง (1–5)</b> — ใช้ติดตามพัฒนาการ ไม่ใช่ band ทางการ</div>` + [['tr', 'ตอบโจทย์/จุดยืนชัด'], ['cc', 'โครงสร้างและคำเชื่อม'], ['lr', 'คำศัพท์/collocation'], ['gr', 'ไวยากรณ์']].map(([c, l]) => `<div class="rate"><span style="min-width:170px">${l}</span>${[1, 2, 3, 4, 5].map(v => `<button class="${e.rate[c] === v ? 'on' : ''}" data-act="rate" data-key="${esc(key)}" data-c="${c}" data-v="${v}">${v}</button>`).join('')}</div>`).join('');
  return h + `</details>`;
}
ACT.reveal = el => { const key = el.dataset.key; const e = essayState(key); const n = wc(e.text); const t = +el.dataset.t || 0; if (!e.revealed && t && n < t / 2 && !confirm('ยังเขียนไม่ถึงครึ่งของเป้าหมาย — แนะนำให้เขียนเองก่อน ต้องการดูตัวอย่างเลยหรือไม่?')) return; e.revealed = !e.revealed; save(); render(true); };
function modelReveal(key, task, n, target) {
  const e = epeek(key);
  const btn = `<button class="btn sm ${e.revealed ? '' : 'pri'}" data-act="reveal" data-key="${esc(key)}" data-t="${target}">${e.revealed ? ico('eyeoff') + ' ซ่อนตัวอย่าง' : ico('eye') + ' ดูตัวอย่าง/แนวคิดเพื่อเทียบ'}</button>`;
  let h = `<div class="row" style="margin-top:10px">${btn}${task.compare ? `<span class="small muted">${esc(task.compare)}</span>` : ''}</div>`;
  if (e.revealed) h += `<div style="margin-top:10px">${modelContent(task)}</div>`;
  return h;
}
function modelContent(task) {
  let h = '';
  const t = task.topic;
  if (task.show) {
    if (task.show.intro) h += `<h3>บทนำตัวอย่าง</h3>` + task.show.intro.map(id => DATA.essays[id] ? `<div class="model"><div class="lab">${id}</div><p>${esc(DATA.essays[id].model[0])}</p></div>` : '').join('');
    if (task.show.paraphrase) h += `<h3>ตัวอย่าง paraphrase</h3>` + task.show.paraphrase.map(id => DATA.essays[id] ? `<div class="model"><div class="lab">${id} · ${esc(DATA.essays[id].prompt)}</div>${DATA.essays[id].paraphrases.map(p => `<p>• ${esc(p)}</p>`).join('')}</div>` : '').join('');
    if (task.show.ideas) h += `<h3>ไอเดียตัวอย่าง</h3>` + task.show.ideas.map(id => DATA.essays[id] ? essayIdeas(id, true) : '').join('');
    if (task.show.models) h += task.show.models.map(id => DATA.models[id] ? docxModel(id) : '').join('');
  }
  if (!t) return h || '<p class="muted">ไม่มีตัวอย่างสำหรับงานนี้ — เทียบกับคู่มือ → Template essay</p>';
  if (DATA.essays[t]) h += essayView(t, task.part);
  else if (DATA.models[t]) h += docxModel(t);
  else if (t === 'W14' && DATA.passages.W14 && DATA.passages.W14.model_summary) h += `<div class="model"><div class="lab">Model summary</div><p>${esc(DATA.passages.W14.model_summary)}</p></div>`;
  return h;
}
function essayIdeas(id, compact) {
  const e = DATA.essays[id];
  const col = (k, lab) => `<div class="col"><b>${lab}</b><ol>${(e.ideas[k] || []).map(x => `<li><b>${esc(x.reason)}</b>${compact ? '' : `<div class="small">${esc(x.explain)}</div>`}<div class="small muted">ตัวอย่าง: ${esc(x.example)}</div></li>`).join('')}</ol></div>`;
  return `${compact ? `<p class="small"><b>${id}</b> ${esc(e.prompt)}</p>` : ''}<div class="ideas">${col('agree', ico('plus') + ' เหตุผลฝั่ง Agree')}${col('disagree', ico('minus') + ' เหตุผลฝั่ง Disagree')}</div>`;
}
function essayView(id, part) {
  const e = DATA.essays[id]; if (!e) return '';
  const labs = ['Introduction', 'Body 1', 'Body 2', 'Conclusion'];
  const hi = { intro: 0, body1: 1, body2: 2, A: [0, 1], B: [2, 3] }[part];
  const words = e.model.reduce((s, p) => s + wc(p), 0);
  return `<div class="lesson"><b>โจทย์นี้ถามอะไร</b><p>${esc(e.th_explain)}</p>${e.stance_reason_th ? `<p class="small">จุดยืนในตัวอย่าง: <b>${esc(e.stance)}</b> — ${esc(e.stance_reason_th)}</p>` : ''}
  <div class="small">คำสำคัญ: ${(e.keywords || []).map(k => `<span class="chip">${esc(k.en)} = ${esc(k.th)}</span>`).join(' ')}</div></div>
  <details class="more"><summary>Paraphrase โจทย์ (${(e.paraphrases || []).length})</summary>${(e.paraphrases || []).map(p => `<p>• ${esc(p)}</p>`).join('')}</details>
  <details class="more"><summary>ไอเดียทั้ง 2 ฝั่ง</summary>${essayIdeas(id)}</details>
  <details class="more"><summary>Outline 4 ย่อหน้า</summary><ul>${['intro', 'body1', 'body2', 'conclusion'].map((k, i) => `<li><b>${labs[i]}:</b> ${esc((e.outline || {})[k] || '')}</li>`).join('')}</ul></details>
  <details class="more" open><summary>Model essay (${words} คำ)</summary><div class="model">${e.model.map((p, i) => `<div class="lab">${labs[i]}${hi !== undefined && (hi === i || (Array.isArray(hi) && hi.includes(i))) ? ' ← ส่วนที่ฝึกวันนี้' : ''}</div><p>${esc(p)}</p>`).join('')}</div></details>
  ${(e.phrases || []).length ? `<details class="more"><summary>วลีที่ควรจำ</summary><ul>${e.phrases.map(p => `<li><b>${esc(p.en)}</b> — ${esc(p.th)}</li>`).join('')}</ul></details>` : ''}`;
}
function docxModel(id) {
  const m = DATA.models[id]; if (!m) return '';
  let h = `<div class="lesson"><b>${esc(m.title)}</b> <span class="small muted">(${esc(m.source)})</span>${m.topic ? `<p class="small">${esc(m.topic)}</p>` : ''}</div>`;
  if (m.original) h += `<details class="more"><summary>ต้นฉบับ “พี่เขียนเอง” (มีข้อผิด — ลองหาเอง)</summary><div class="model">${m.original.map(p => `<p>${esc(p)}</p>`).join('')}</div></details>`;
  if (m.analysis && m.analysis.length) h += `<details class="more"><summary>บทวิเคราะห์ปัญหาของต้นฉบับ</summary>${m.analysis.map(p => `<p class="small">${esc(p)}</p>`).join('')}${m.table ? `<div class="tablewrap"><table class="t">${m.table.map((r, i) => `<tr>${r.map(c => i ? `<td>${esc(c)}</td>` : `<th>${esc(c)}</th>`).join('')}</tr>`).join('')}</table></div>` : ''}</details>`;
  h += `<details class="more" open><summary>${m.original ? 'ฉบับปรับปรุง' : 'Essay ตัวอย่าง'}</summary><div class="model">${m.paras.map(p => /^\[.*\]$/.test(p) ? `<div class="lab">${esc(p.replace(/[\[\]]/g, ''))}</div>` : `<p>${esc(p)}</p>`).join('')}</div></details>`;
  if (m.notes && m.notes.length) h += `<details class="more"><summary>จุดที่ปรับปรุง / ข้อสังเกต</summary><ul>${m.notes.map(n => `<li>${esc(n)}</li>`).join('')}</ul></details>`;
  return h;
}

/* ---------- essay (timed 60) ---------- */
function secEssay(d) {
  const day = DAY(d); const id = day.essay.topic; const key = 'E:' + d;
  let h = topicBox(id);
  h += `<div class="lesson small"><b>${ico('clock')} แผน 60 นาที</b> 0–10 อ่านโจทย์ + เลือกจุดยืน + brainstorm เหตุผล 2 ข้อ · 10–50 เขียน 4 ย่อหน้า · 50–60 นับคำ (≥ 250) + ตรวจ Checklist 10 ข้อ — <b>ห้ามเปิดตัวอย่างก่อนเขียนเสร็จ</b>${day.type === 'mock' ? '<br><b>Mock:</b> เริ่มทันทีหลังส่ง Reading' : ''}</div>`;
  h += editorBlock(key, day.essay.minutes, 250, false, 'Day ' + d + ' · Essay ' + id);
  h += checkBlock(key, true);
  h += modelReveal(key, { topic: id, compare: id === 'R7' ? 'เทียบกับ Image (1).pdf และ Improved Essay 1 ด้วย' : '' }, wc(epeek(key).text), 250);
  return h;
}

/* ---------- errors & reviews ---------- */
function notesBox(d) { const day = DAY(d); return `<div class="callout"><b>บันทึกวันนี้:</b> ${esc(day.error)}</div><textarea class="notes" data-inp="note" data-d="${d}" placeholder="จดสิ่งที่ผิด สาเหตุ และวิธีแก้ (บันทึกอัตโนมัติ)">${esc(S.notes[d] || '')}</textarea>`; }
function secErrors(d) {
  const items = wrongItems({ days: [d] });
  return notesBox(d) + `<details class="more" ${items.length ? 'open' : ''}><summary>ข้อที่ผิดวันนี้ (${items.length}) — ทำซ้ำทันที</summary>${renderRetryList(items)}</details>`;
}
function secTest(d) {
  const tid = DAY(d).test; const t = DATA.tests[tid]; if (!t) return `<div class="callout warn">ยังไม่มีข้อสอบ ${esc(tid)}</div>`; const st = S.quiz['T:' + tid]; const s = testStatus(tid);
  let h = `<div class="row"><b>${esc(t.title)}</b><span class="chip">6 passages · 69 ข้อ · 120 นาที</span></div><ul class="small">${t.passages.map((pid, i) => `<li>P${i + 1} ${esc(DATA.passages[pid].kind === 'long' ? '(ยาว)' : '(สั้น)')} — ${esc(DATA.passages[pid].domain)}</li>`).join('')}</ul>`;
  if (s === 'new') h += `<div class="row"><a class="btn pri" href="#/test/${tid}">เปิดหน้าข้อสอบ ${ico('arrowr')}</a><span class="small muted">อ่านคำแนะนำแล้วกดเริ่ม</span></div>`;
  else if (s === 'running') h += `<div class="row"><span class="chip warn">กำลังทำ</span><span data-timer="T:${tid}"></span><a class="btn pri" href="#/test/${tid}">ทำต่อ ${ico('arrowr')}</a></div>`;
  else h += `<div class="result"><div class="big">${st.score}/${st.total}</div><b>${pct(st.score, st.total)}%</b><span class="spacer"></span><a class="btn" href="#/test/${tid}">ดูผลและเฉลยละเอียด ${ico('arrowr')}</a></div>`;
  return h;
}
function secReview(d) {
  const tid = DAY(d).test; const s = testStatus(tid);
  if (s !== 'done') return `<p class="muted">ทำข้อสอบให้เสร็จก่อน แล้วกลับมาที่ส่วนนี้</p>` + notesBox(d);
  const items = wrongItems({ days: [d] }).filter(x => x.kind === 'test');
  return `<p>ผิด ${items.length} ข้อ — อ่านคำอธิบายทีละข้อใน <a href="#/test/${tid}">หน้าผลสอบ</a> แล้วจดสรุปด้านล่าง</p>` + notesBox(d);
}
function secWeekly(d) {
  const days = DAY(d).review.days; const items = wrongItems({ days });
  return `<p class="small">รวมข้อที่ผิดจาก Day ${days.join(', ')} (Reading / Grammar / คำศัพท์) — ตอบใหม่ทีละข้อ ระบบบอกผลทันที ข้อที่ตอบถูกจะถูกย้ายออกจากรายการข้อผิด</p>` + renderRetryList(items.sort((a, b) => (a.kind === 'vocab') - (b.kind === 'vocab')).slice(0, 60));
}
function secVocabReview(d) {
  const rw = reviewWords(d);
  return `<p class="small">สุ่มจาก ${rw.all.length} คำ${DAY(d).review ? ' (Day ' + DAY(d).review.days.join(', ') + ')' : DAY(d).type === 'review' ? ` (ทั้งหมด ${ALLWORDS.length} คำ)` : ' (ศัพท์วิจัย + สำนวน essay)'} โดยดึงคำที่ติดดาว ★ (${rw.starred.length} คำ) ขึ้นก่อน</p>` + renderQuiz('VR:' + d);
}
function secRetry(d) {
  const items = wrongItems({}).filter(x => !S.resolved[x.q.id]).sort((a, b) => ({ test: 0, reading: 1, grammar: 2, vocab: 3 }[a.kind] - { test: 0, reading: 1, grammar: 2, vocab: 3 }[b.kind]));
  return `<p class="small">ข้อที่ยังไม่ได้แก้ทั้งหมด ${items.length} ข้อ (เรียง Test/Mock → Reading → Grammar → ศัพท์) — ทำให้ได้อย่างน้อย 30 ข้อ</p>` + renderRetryList(items.slice(0, 80));
}
