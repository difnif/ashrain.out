// 시록고 강사도구 — 옮겨 오기: ① PC 강사도구 자료(data 폴더: mf.db + prints + scans) ② Claude와 만든 프린트 묶음(print.json 폴더)
// 이미 있는 코드는 건너뛴다(여러 번 해도 겹치지 않음). 파일은 teacher-tool/<uid>/tt/ 에, 기록은 tt_* 표에.
import { T as T0, all, must, put, log, nn } from "./sb";
// 넣기·고치기 전에 빈 값을 기본값으로
const T = (name) => {
  const q = T0(name);
  return new Proxy(q, { get(t, k) {
    if (k === "insert" || k === "upsert") return (rows, opt) => t[k](nn(name, rows), opt);
    const v = t[k]; return typeof v === "function" ? v.bind(t) : v;
  } });
};

const KST = (s) => {
  if (!s) return null;
  const t = String(s).trim().replace(" ", "T");
  return /[zZ]|[+-]\d\d:?\d\d$/.test(t) ? t : t + "+09:00";
};
const jparse = (s, d) => { if (s == null || s === "") return d; try { return JSON.parse(s); } catch { return d; } };
const MIME = { pdf: "application/pdf", png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", heic: "image/heic", webp: "image/webp", json: "application/json", html: "text/html" };
// 저장 공간 이름에 쓸 확장자(영문·숫자만)
const extOf = (name) => { const m = /\.([A-Za-z0-9]{1,5})$/.exec(String(name || "")); return m ? "." + m[1].toLowerCase() : ""; };
const mimeOf = (name) => MIME[(/\.([a-z0-9]+)$/i.exec(name) || [])[1]?.toLowerCase()] || "application/octet-stream";

// 끌어다 놓은 폴더 → [{path, file}] (path 는 고른 폴더 이름부터)
async function walkEntries(items) {
  const out = [];
  const walk = async (entry, prefix) => {
    if (entry.isFile) {
      const file = await new Promise((res, rej) => entry.file(res, rej));
      out.push({ path: prefix + entry.name, file });
    } else if (entry.isDirectory) {
      const reader = entry.createReader();
      for (;;) {
        const batch = await new Promise((res, rej) => reader.readEntries(res, rej));
        if (!batch.length) break;
        for (const e of batch) await walk(e, prefix + entry.name + "/");
      }
    }
  };
  for (const it of items) {
    const e = it.webkitGetAsEntry && it.webkitGetAsEntry();
    if (e) await walk(e, "");
  }
  return out;
}

// SQLite WAL 이 남아 있으면(PC 강사도구가 열려 있던 경우) 커밋된 쪽을 덮어써 최신 상태로
function applyWal(db, wal) {
  if (!wal || wal.length < 32) return db;
  const dv = new DataView(wal.buffer, wal.byteOffset, wal.byteLength);
  const magic = dv.getUint32(0);
  if (magic !== 0x377f0682 && magic !== 0x377f0683) return db;
  const ps = dv.getUint32(8);
  const salt1 = dv.getUint32(16), salt2 = dv.getUint32(20);
  const frames = [];
  let lastCommit = -1;
  for (let off = 32, i = 0; off + 24 + ps <= wal.length; off += 24 + ps, i++) {
    if (dv.getUint32(off + 8) !== salt1 || dv.getUint32(off + 12) !== salt2) break;
    frames.push({ pg: dv.getUint32(off), commit: dv.getUint32(off + 4), off: off + 24 });
    if (dv.getUint32(off + 4)) lastCommit = i;
  }
  if (lastCommit < 0) return db;
  let size = db.length;
  for (let i = 0; i <= lastCommit; i++) size = Math.max(size, frames[i].pg * ps);
  const out = new Uint8Array(size);
  out.set(db);
  for (let i = 0; i <= lastCommit; i++) out.set(wal.subarray(frames[i].off, frames[i].off + ps), (frames[i].pg - 1) * ps);
  const dbSize = frames[lastCommit].commit * ps;
  return out.subarray(0, dbSize || size);
}

async function openSqlite(bytes) {
  const [{ default: initSqlJs }, { default: wasmUrl }] = await Promise.all([import("sql.js"), import("sql.js/dist/sql-wasm.wasm?url")]);
  const SQL = await initSqlJs({ locateFile: () => wasmUrl });
  const db = new SQL.Database(bytes);
  const q = (sql) => {
    const res = db.exec(sql);
    if (!res.length) return [];
    const { columns, values } = res[0];
    return values.map((v) => Object.fromEntries(columns.map((c, i) => [c, v[i]])));
  };
  return { q, close: () => db.close() };
}
const tableCols = (q, t) => { try { return new Set(q(`PRAGMA table_info(${t})`).map((r) => r.name)); } catch { return new Set(); } };

// ── 무엇이 들었나 보기
async function scan(files) {
  const norm = files.map((f) => ({ ...f, path: f.path.replace(/\\/g, "/") }));
  const res = { pc: null, packages: [] };
  const dbf = norm.find((f) => /(^|\/)mf\.db$/.test(f.path));
  if (dbf) {
    const base = dbf.path.replace(/mf\.db$/, "");
    const wal = norm.find((f) => f.path === base + "mf.db-wal");
    let bytes = new Uint8Array(await dbf.file.arrayBuffer());
    if (wal && wal.file.size) bytes = applyWal(bytes, new Uint8Array(await wal.file.arrayBuffer()));
    const S = await openSqlite(bytes);
    const fileMap = new Map(norm.filter((f) => f.path.startsWith(base)).map((f) => [f.path.slice(base.length), f.file]));
    const cnt = (t) => { try { return S.q(`SELECT COUNT(*) n FROM ${t}`)[0].n; } catch { return 0; } };
    res.pc = { S, fileMap, base, n: { students: cnt("students"), prints: cnt("prints"), gradings: cnt("gradings"), scans: cnt("scans"), marks: cnt("marks"), class: cnt("class_records"), events: cnt("events"), transcripts: cnt("transcripts") } };
  }
  for (const f of norm.filter((x) => /(^|\/)print\.json$/.test(x.path))) {
    try {
      const j = JSON.parse(await f.file.text());
      if (j && j.kind === "ashrain.tt.package") {
        const base = f.path.replace(/print\.json$/, "");
        res.packages.push({ j, files: new Map(norm.filter((x) => x.path.startsWith(base)).map((x) => [x.path.slice(base.length), x.file])) });
      }
    } catch { /* 다른 json */ }
  }
  return res;
}

// 여러 파일 올리기 (동시에 4개)
async function putAll(jobs, onStep) {
  let i = 0, fail = [];
  const worker = async () => {
    while (i < jobs.length) {
      const j = jobs[i++];
      // 파일을 먼저 읽어 바이트로 보낸다(폴더에서 고른 파일을 그대로 넘기면 일부 환경에서 올리기가 끊김)
      try { const data = j.file instanceof Blob ? new Uint8Array(await j.file.arrayBuffer()) : j.file; await put(j.rel, data, j.type || mimeOf(j.rel)); }
      catch (e) { fail.push(j.rel + ": " + e.message); }
      onStep();
    }
  };
  await Promise.all([worker(), worker(), worker(), worker()]);
  return fail;
}

// ── Claude 프린트 묶음 → 보관함(shelf library)
async function importPackages(pkgs, ui) {
  const have = new Set((await all(() => T("tt_prints").select("code"))).map((r) => r.code));
  let done = 0, skipped = 0;
  const errors = [];
  for (const { j, files } of pkgs) {
    const p = j.print || {};
    const code = String(p.code || "").toUpperCase();
    ui.status(`프린트 묶음 ${done + skipped + 1}/${pkgs.length} · ${p.title || code}`);
    if (!/^[2-9A-HJKMNP-Z]{6}$/.test(code)) { errors.push(`${p.title || "?"}: 코드가 이상해요 (${code})`); continue; }
    if (have.has(code)) { skipped++; continue; }
    const jobs = [];
    const fl = j.files || {};
    const addFile = (src, rel) => { const f = files.get(src); if (f) jobs.push({ rel: `${code}/${rel}`, file: f }); return f ? `${code}/${rel}` : null; };
    const sheet = fl.sheet ? addFile(fl.sheet, "sheet.pdf") : null;
    if (!sheet) { errors.push(`${p.title || code}: 문제지 파일이 없어요`); continue; }
    const answer = fl.answer ? addFile(fl.answer, "answer.pdf") : null;
    const extras = [];
    (fl.extras || []).forEach((x, k) => { const rel = addFile(x.file, `extras/x${k + 1}${extOf(x.file)}`); if (rel) extras.push({ name: x.name || x.file.split("/").pop(), role: x.role || "기타", path: rel }); });
    for (const it of j.items || []) {
      if (it.png) addFile(it.png, it.png);
      if (it.answer_png) addFile(it.answer_png, it.answer_png);
      if (it.sol_png) addFile(it.sol_png, it.sol_png);
    }
    let n = 0;
    const fails = await putAll(jobs, () => ui.progress(++n, jobs.length));
    if (fails.length) { errors.push(`${p.title || code}: 파일 ${fails.length}개를 못 올렸어요 (${fails[0]})`); continue; }
    try {
      const row = must(await T("tt_prints").insert({
        code, title: p.title || code, sub: p.sub || "", kind: p.kind || "registered", template: p.template || "등록", label: p.label || "서답형",
        level: p.level || null, n_items: (j.items || []).length, n_choice: (j.items || []).filter((x) => x.choice).length, pages: p.pages || null,
        sources: p.sources || [], files: { sheet, answer, src: [], extras, sheet_name: fl.sheet_name || null, answer_name: fl.answer_name || null },
        name_boxes: p.name_boxes || [], options: p.options || {}, shelf: p.shelf || "library", created_at: KST(p.created_at) || undefined,
      }).select("id").single());
      const items = (j.items || []).map((it, k) => ({ print_id: row.id, seq: it.seq || k + 1, label: it.label ?? String(k + 1), src: it.src || null, src_no: it.src_no != null ? String(it.src_no) : null,
        choice: !!it.choice, hash: it.hash || null, png: it.png || null, answer: it.answer || "", answer_png: it.answer_png || null, sol_png: it.sol_png || null,
        points: it.points ?? null, topic: it.topic || "", tag: it.tag || "", rate: it.rate || "", scale: it.scale ?? null, page: it.page ?? null, bbox: it.bbox || null }));
      for (let k = 0; k < items.length; k += 200) must(await T("tt_print_items").insert(items.slice(k, k + 200)));
      log("library_import", null, row.id, { code, title: p.title, items: items.length });
      have.add(code);
      done++;
    } catch (e) { errors.push(`${p.title || code}: ${e.message}`); }
  }
  return { done, skipped, errors };
}

// ── PC 강사도구 자료 → tt_*
async function importPc(pc, ui) {
  const { S, fileMap } = pc;
  const q = S.q;
  const errors = [];
  const fileOf = (rel) => fileMap.get("prints/" + rel) || null;
  // 학생
  ui.status("학생 명단");
  const stOld = q("SELECT * FROM students ORDER BY id");
  const stNew = new Map((await all(() => T("tt_students").select("id,name"))).map((r) => [r.name, r.id]));
  const sMap = new Map();
  for (const s of stOld) {
    if (stNew.has(s.name)) { sMap.set(s.id, stNew.get(s.name)); continue; }
    const r = must(await T("tt_students").insert({ name: s.name, grade: s.grade || "", memo: s.memo || "", active: s.active !== 0, created_at: KST(s.created_at) || undefined, updated_at: KST(s.updated_at) || undefined }).select("id").single());
    sMap.set(s.id, r.id);
    stNew.set(s.name, r.id);
  }
  // 프린트
  const have = new Map((await all(() => T("tt_prints").select("id,code"))).map((r) => [r.code, r.id]));
  const pCols = tableCols(q, "prints");
  const prints = q("SELECT * FROM prints ORDER BY id");
  const pMap = new Map();
  const skipped = [];
  let pi = 0;
  for (const p of prints) {
    pi++;
    ui.status(`프린트 ${pi}/${prints.length} · ${p.title || p.code}`);
    if (have.has(p.code)) { pMap.set(p.id, { id: have.get(p.code), code: p.code, existed: true }); skipped.push(p.code); continue; }
    const code = p.code;
    const items = q(`SELECT * FROM print_items WHERE print_id=${Number(p.id)} ORDER BY seq`);
    const jobs = [];
    const add = (srcRel, dstRel) => { const f = srcRel && fileOf(srcRel); if (f) { jobs.push({ rel: `${code}/${dstRel}`, file: f }); return `${code}/${dstRel}`; } return null; };
    const sheet = add(p.pdf, "sheet.pdf");
    const answer = p.answer_pdf ? add(p.answer_pdf, "answer.pdf") : null;
    const extras = [];
    (jparse(pCols.has("extras") ? p.extras : null, []) || []).forEach((x, k) => {
      const fn = String(x.file || "").split("/").pop();
      const rel = add(x.file, `extras/x${k + 1}${extOf(fn)}`);      // 저장 공간 이름은 영문만 — 보이는 이름은 name 에
      if (rel) extras.push({ name: x.name || fn, role: x.role || "기타", path: rel });
    });
    for (const it of items) for (const k of ["png", "answer_png", "sol_png"]) if (it[k]) add(`${code}/${it[k]}`, it[k]);
    let n = 0;
    const fails = await putAll(jobs, () => ui.progress(++n, jobs.length));
    if (fails.length) errors.push(`${p.title || code}: 파일 ${fails.length}개를 못 올렸어요 (${fails[0]})`);
    try {
      const row = must(await T("tt_prints").insert({
        code, title: p.title || code, sub: p.sub || "", kind: pCols.has("kind") ? p.kind || "mathflat" : "mathflat", template: p.template || null, label: p.label || "서답형",
        level: pCols.has("level") ? p.level || null : null, n_items: p.n_items ?? items.length, n_choice: p.n_choice ?? items.filter((x) => x.choice).length, pages: p.pages ?? null,
        sources: jparse(p.sources, []), files: { sheet, answer, src: [], extras }, name_boxes: jparse(pCols.has("name_boxes") ? p.name_boxes : null, []) || [],
        options: jparse(p.options, {}) || {}, shelf: p.deleted ? "deleted" : "active", created_at: KST(p.created_at) || undefined, updated_at: KST(p.updated_at) || undefined,
      }).select("id").single());
      pMap.set(p.id, { id: row.id, code });
      const rows = items.map((it) => ({ print_id: row.id, seq: it.seq, src: it.src ?? null, src_no: it.src_no != null ? String(it.src_no) : null, choice: !!it.choice, hash: it.hash || null,
        png: it.png || null, answer: it.answer || "", label: it.label ?? null, points: it.points ?? null, topic: it.topic || "", answer_png: it.answer_png || null,
        tag: it.tag || "", rate: it.rate || "", sol_png: it.sol_png || null, scale: it.scale ?? null, origin: it.origin || null }));
      for (let k = 0; k < rows.length; k += 200) must(await T("tt_print_items").insert(rows.slice(k, k + 200)));
    } catch (e) { errors.push(`${p.title || code}: ${e.message}`); }
  }
  const P = (oid) => { const m = pMap.get(oid); return m ? m.id : null; };          // 전에 옮긴 프린트도 채점 기록은 이어서(겹치면 건너뜀)
  const isNew = (oid) => { const m = pMap.get(oid); return !!m && !m.existed; };
  const again = must(await T("tt_events").select("id").eq("kind", "pc_import").limit(1)).length > 0;
  // 출제 대상
  ui.status("출제 대상");
  const tg = q("SELECT * FROM print_targets").filter((t) => P(t.print_id) && sMap.get(t.student_id))
    .map((t) => ({ print_id: P(t.print_id), student_id: sMap.get(t.student_id), issued_at: KST(t.issued_at) || undefined }));
  for (let k = 0; k < tg.length; k += 500) must(await T("tt_targets").upsert(tg.slice(k, k + 500), { onConflict: "print_id,student_id", ignoreDuplicates: true }));
  // 채점 · 회차 · 기록 · 스캔본
  const gradings = q("SELECT * FROM gradings ORDER BY id");
  const gsCols = tableCols(q, "grading_sessions");
  const gMap = new Map();
  let gi = 0, nScans = 0;
  for (const g of gradings) {
    gi++;
    const pid = P(g.print_id), sid = sMap.get(g.student_id);
    if (!pid || !sid) continue;
    ui.status(`채점 기록 ${gi}/${gradings.length}`);
    try {
      const row = must(await T("tt_gradings").insert({ print_id: pid, student_id: sid, status: g.status || "open", mode: g.mode || "ox", created_at: KST(g.created_at) || undefined, updated_at: KST(g.updated_at) || undefined }).select("id").single());
      gMap.set(g.id, row.id);
      const ss = q(`SELECT * FROM grading_sessions WHERE grading_id=${Number(g.id)} ORDER BY no`).map((s) => ({ grading_id: row.id, no: s.no, round: gsCols.has("round") ? s.round || 1 : 1,
        kind: gsCols.has("kind") ? s.kind || "solve" : "solve", targets: gsCols.has("targets") ? jparse(s.targets, null) : null, started_at: KST(s.started_at) || undefined, ended_at: KST(s.ended_at), end_reason: s.end_reason || null }));
      if (ss.length) must(await T("tt_sessions").insert(ss));
      const ms = q(`SELECT * FROM marks WHERE grading_id=${Number(g.id)} ORDER BY id`).map((m) => ({ grading_id: row.id, session_no: m.session_no, seq: m.seq, result: m.result, answer: m.answer || "", at: KST(m.at) || undefined }))
        .filter((m) => ["O", "X", "U"].includes(m.result));
      for (let k = 0; k < ms.length; k += 500) must(await T("tt_marks").insert(ms.slice(k, k + 500)));
      const code = pMap.get(g.print_id).code;
      let k = 0;
      for (const sc of q(`SELECT * FROM scans WHERE grading_id=${Number(g.id)} AND deleted=0 ORDER BY id`)) {
        const f = fileMap.get("scans/" + sc.file);
        if (!f) continue;
        const fn = String(sc.file).split("/").pop();
        const rel = `${code}/scans/${row.id}/${String(++k).padStart(2, "0")}_pc${extOf(fn)}`;
        try {
          await put(rel, new Uint8Array(await f.arrayBuffer()), mimeOf(fn));
          must(await T("tt_scans").insert({ grading_id: row.id, path: rel, name: sc.name || fn, size: sc.size || f.size, mime: mimeOf(fn), pages: sc.pages || 1, created_at: KST(sc.created_at) || undefined }));
          nScans++;
        } catch (e) { errors.push(`스캔본 ${sc.name}: ${e.message}`); }
      }
    } catch (e) { if (!/duplicate|unique/i.test(e.message)) errors.push(`채점 ${g.id}: ${e.message}`); }
  }
  // 수업 기록
  ui.status("수업 기록");
  const cr = q("SELECT * FROM class_records").filter((r) => sMap.get(r.student_id) && P(r.print_id))
    .map((r) => ({ day: r.date, student_id: sMap.get(r.student_id), kind: r.kind, print_id: P(r.print_id), created_at: KST(r.created_at) || undefined }));
  for (let k = 0; k < cr.length; k += 500) { try { must(await T("tt_class_records").upsert(cr.slice(k, k + 500), { onConflict: "day,student_id,kind,print_id", ignoreDuplicates: true })); } catch (e) { errors.push("수업 기록: " + e.message); } }
  // 활동 로그 (옮긴 프린트에 딸린 것 + 학생 것)
  ui.status("활동 로그");
  const ev = again ? [] : q("SELECT * FROM events ORDER BY id").filter((e) => !e.print_id || P(e.print_id)).map((e) => ({ at: KST(e.at) || undefined, kind: e.kind,
    student_id: e.student_id ? sMap.get(e.student_id) || null : null, print_id: e.print_id ? P(e.print_id) : null, detail: { ...(jparse(e.detail, {}) || {}), from_pc: true } }));
  for (let k = 0; k < ev.length; k += 500) { try { must(await T("tt_events").insert(ev.slice(k, k + 500))); } catch (e) { errors.push("활동 로그: " + e.message); break; } }
  // 전사본
  ui.status("전사본");
  const tr = q("SELECT * FROM transcripts").map((t) => ({ item_key: t.item_key, print_id: t.print_id ? P(t.print_id) : null, seq: t.seq, level: t.level, question: t.question, solution: t.solution,
    corpus_id: t.corpus_id, source: t.source, batch: t.batch, updated_at: KST(t.updated_at) || undefined }));
  for (let k = 0; k < tr.length; k += 300) { try { must(await T("tt_transcripts").upsert(tr.slice(k, k + 300), { onConflict: "owner,item_key", ignoreDuplicates: true })); } catch (e) { errors.push("전사본: " + e.message); break; } }
  void isNew;
  log("pc_import", null, null, { students: sMap.size, prints: [...pMap.values()].filter((m) => !m.existed).length, skipped: skipped.length, gradings: gMap.size, scans: nScans });
  S.close();
  return { students: stOld.length, prints: [...pMap.values()].filter((m) => !m.existed).length, skipped, gradings: gMap.size, scans: nScans, errors };
}

export async function importView({ view, $, esc, toast, fmtCode }) {
  view.innerHTML = `<h1>옮겨 오기</h1>
    <div class="card"><h2>무엇을 옮기나요?</h2>
      <p class="sub small" style="margin:0 0 6px">① <b>PC 강사도구 자료</b> — PC 강사도구 폴더 안의 <b>data</b> 폴더(mf.db · prints · scans)를 통째로. 학생·프린트·채점 기록·스캔본·수업 기록·활동 로그·전사본이 옮겨져요. <b>PC 강사도구는 닫고</b> 하세요.</p>
      <p class="sub small" style="margin:0">② <b>Claude와 만든 프린트 묶음</b> — 「강사도구로 옮길 프린트」 폴더(프린트마다 print.json). 보관함에 들어가고, 쓸 때 코드로 꺼내 등록해요.</p>
      <p class="sub small" style="margin:6px 0 0">이미 있는 코드는 건너뛰어서 여러 번 해도 겹치지 않아요.</p>
      <div class="drop" id="imDrop" style="margin-top:12px"><b>폴더를 끌어다 놓거나 눌러서 고르기</b><span class="sub small">둘 다 한꺼번에 놓아도 돼요</span>
        <input type="file" id="imPick" webkitdirectory directory multiple hidden></div>
    </div><div id="imOut"></div>`;
  const out = $("#imOut");
  const dz = $("#imDrop"), pick = $("#imPick");
  const ui = {
    status: (t) => { const el = $("#imSt"); if (el) el.textContent = t; },
    progress: (a, b) => { const el = $("#imBar"); if (el) el.style.width = (b ? Math.round((a / b) * 100) : 0) + "%"; },
  };
  const run = async (files) => {
    if (!files.length) return;
    out.innerHTML = `<div class="card"><span class="busy"></span>폴더를 읽는 중… (파일 ${files.length}개)</div>`;
    let r;
    try { r = await scan(files); } catch (e) { out.innerHTML = `<div class="card" style="border-color:#fca5a5"><b>읽지 못했어요</b><div class="sub">${esc(e.message)}</div></div>`; return; }
    if (!r.pc && !r.packages.length) { out.innerHTML = `<div class="card" style="border-color:#fca5a5"><b>옮길 것을 찾지 못했어요</b><div class="sub small">mf.db 가 든 data 폴더나, print.json 이 든 프린트 묶음 폴더를 놓아 주세요.</div></div>`; return; }
    const n = r.pc && r.pc.n;
    out.innerHTML = `<div class="card"><h2>찾은 것</h2>
      ${r.pc ? `<div>PC 강사도구 자료 — 학생 ${n.students} · 프린트 ${n.prints} · 채점 ${n.gradings} (기록 ${n.marks}) · 스캔본 ${n.scans} · 수업 기록 ${n.class} · 활동 로그 ${n.events} · 전사본 ${n.transcripts}</div>` : ""}
      ${r.packages.length ? `<div>Claude 프린트 묶음 — ${r.packages.length}개 <span class="sub small">(${r.packages.slice(0, 6).map((p) => esc(p.j.print.title || "")).join(", ")}${r.packages.length > 6 ? " …" : ""})</span></div>` : ""}
      <div class="row" style="margin-top:12px"><button class="btn big" id="imGo">옮기기 시작</button><span class="sub small">창을 닫지 마세요 — 파일이 많으면 몇 분 걸려요</span></div>
      <div id="imRun" hidden style="margin-top:12px"><div class="sub small" id="imSt">…</div><div style="height:8px;background:#e2e8f0;border-radius:6px;overflow:hidden;margin-top:6px"><div id="imBar" style="height:8px;width:0;background:var(--acc);transition:width .2s"></div></div></div></div>`;
    $("#imGo").onclick = async () => {
      $("#imGo").disabled = true;
      $("#imRun").hidden = false;
      const lines = [];
      try {
        if (r.pc) {
          const a = await importPc(r.pc, ui);
          lines.push(`<b>PC 자료</b>: 학생 ${a.students}명 · 프린트 ${a.prints}개${a.skipped.length ? ` (이미 있던 ${a.skipped.length}개는 건너뜀: ${a.skipped.slice(0, 8).map(fmtCode).join(", ")}${a.skipped.length > 8 ? " …" : ""})` : ""} · 채점 ${a.gradings}건 · 스캔본 ${a.scans}개`);
          a.errors.forEach((e) => lines.push(`<span style="color:#b91c1c">${esc(e)}</span>`));
        }
        if (r.packages.length) {
          const b = await importPackages(r.packages, ui);
          lines.push(`<b>Claude 프린트</b>: 보관함에 ${b.done}개${b.skipped ? ` · 이미 있던 ${b.skipped}개는 건너뜀` : ""}`);
          b.errors.forEach((e) => lines.push(`<span style="color:#b91c1c">${esc(e)}</span>`));
        }
        out.innerHTML = `<div class="card" style="background:#f0fdf4;border-color:#bbf7d0"><h2>옮겼어요</h2>${lines.map((l) => `<div class="small">${l}</div>`).join("")}
          <div class="row" style="margin-top:10px"><a class="btn ghost" href="#/tt/prints">프린트함</a><a class="btn ghost" href="#/tt/register">보관함(프린트 등록)</a><a class="btn ghost" href="#/tt/students">학생</a></div></div>`;
        toast("옮기기를 마쳤어요");
      } catch (e) {
        out.insertAdjacentHTML("beforeend", `<div class="card" style="border-color:#fca5a5"><b>옮기다 멈췄어요</b><div class="sub">${esc(e.message)}</div><div class="sub small">다시 하면 이미 옮긴 코드는 건너뛰고 이어서 해요.</div></div>`);
        $("#imGo").disabled = false;
      }
    };
  };
  dz.onclick = () => pick.click();
  pick.onchange = () => { run([...pick.files].map((f) => ({ path: f.webkitRelativePath || f.name, file: f }))); pick.value = ""; };
  ["dragenter", "dragover"].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.classList.add("over"); }));
  ["dragleave", "drop"].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.classList.remove("over"); }));
  dz.addEventListener("drop", async (e) => run(await walkEntries([...e.dataTransfer.items])));
}
