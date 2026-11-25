// 시록고 강사도구 — 옮겨 오기: ① PC 강사도구 자료(data 폴더: mf.db + prints + scans) ② Claude와 만든 프린트 묶음(print.json 폴더) ③ Claude 프린트 PDF
// 여러 번 해도 겹치지 않는다 — PC 자료는 새로 생긴 것만 더한다(프린트·학생·채점 차·표시·기록). 파일은 teacher-tool/<uid>/tt/ 에, 기록은 tt_* 표에.
// PC 자료 폴더는 이 브라우저에 기억해 두고(파일 시스템 접근 · Chrome), 강사도구를 열 때 PC에서 새로 등록한 것을 알아서 반영한다(pcAutoSync).
import { T as T0, all, must, put, log, nn, uid } from "./sb";
import { KST, jparse, applyWal, safeQuery, knownFromPc, cleanPrintMeta, cleanEventDetail, markKey, eventKey, scanKey, onlyNew, sessionPlan, gradingNewer, insidePcTool } from "./pccore.js";
import { guessLevel, stripNames } from "./logic.js";
// 넣기·고치기 전에 빈 값을 기본값으로
const T = (name) => {
  const q = T0(name);
  return new Proxy(q, { get(t, k) {
    if (k === "insert" || k === "upsert") return (rows, opt) => t[k](nn(name, rows), opt);
    const v = t[k]; return typeof v === "function" ? v.bind(t) : v;
  } });
};

const MIME = { pdf: "application/pdf", png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", heic: "image/heic", webp: "image/webp", json: "application/json", html: "text/html" };
// 저장 공간 이름에 쓸 확장자(영문·숫자만)
const extOf = (name) => { const m = /\.([A-Za-z0-9]{1,5})$/.exec(String(name || "")); return m ? "." + m[1].toLowerCase() : ""; };
const mimeOf = (name) => MIME[(/\.([a-z0-9]+)$/i.exec(name) || [])[1]?.toLowerCase()] || "application/octet-stream";

// 끌어다 놓은 폴더 → [{path, file}] (path 는 고른 폴더 이름부터)
// 항목(entry)은 놓는 순간에만 꺼낼 수 있어서 먼저 모두 꺼내 두고 걷는다
async function walkEntries(entries) {
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
  for (const e of entries) if (e) await walk(e, "");
  return out;
}
// 고른 폴더(파일 시스템 접근 핸들) → [{path, file}]
async function walkHandle(dir, prefix = "") {
  const out = [];
  const walk = async (d, pre) => {
    for await (const h of d.values()) {
      if (h.kind === "file") out.push({ path: pre + h.name, file: await h.getFile() });
      else await walk(h, pre + h.name + "/");
    }
  };
  await walk(dir, prefix + dir.name + "/");
  return out;
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

// PC 자료 열기: mf.db(+ 남은 WAL) → sqlite, 파일은 getFile("prints/…") 로 그때그때 (폴더 핸들이면 필요한 것만 읽음)
async function pcOpen(dbFile, walFile, getFile, base) {
  let bytes = new Uint8Array(await dbFile.arrayBuffer());
  if (walFile && walFile.size) bytes = applyWal(bytes, new Uint8Array(await walFile.arrayBuffer()));
  const S = await openSqlite(bytes);
  const q = safeQuery(S.q);
  const cnt = (t) => { try { return S.q(`SELECT COUNT(*) n FROM ${t}`)[0].n; } catch { return 0; } };
  return { S, q, getFile, base, sig: `${dbFile.size}:${dbFile.lastModified || 0}:${walFile ? walFile.size + ":" + (walFile.lastModified || 0) : "-"}`,
    n: { students: cnt("students"), prints: cnt("prints"), gradings: cnt("gradings"), scans: cnt("scans"), marks: cnt("marks"), class: cnt("class_records"), events: cnt("events"), transcripts: cnt("transcripts") } };
}

// 묶음이 zip 으로 왔으면 풀어서 같은 꼴로 (프린트 묶음 · data 폴더 압축 둘 다)
async function unzipAll(files) {
  const out = [];
  for (const f of files) {
    if (!/\.zip$/i.test(f.path)) { out.push(f); continue; }
    try {
      const { readZip } = await import("../../../lib/unzip");
      const base = f.path.replace(/\.zip$/i, "");
      for (const e of await readZip(await f.file.arrayBuffer())) {
        const name = e.name.replace(/\\/g, "/");
        out.push({ path: base + "/" + name, file: new File([e.data], name.split("/").pop()) });
      }
    } catch { out.push(f); }
  }
  return out;
}

// ── 무엇이 들었나 보기
async function scan(files0) {
  const files = await unzipAll(files0);
  const norm = files.map((f) => ({ ...f, path: f.path.replace(/\\/g, "/") }));
  const res = { pc: null, packages: [] };
  const dbf = norm.find((f) => /(^|\/)mf\.db$/.test(f.path));
  if (dbf) {
    const base = dbf.path.replace(/mf\.db$/, "");
    const wal = norm.find((f) => f.path === base + "mf.db-wal");
    const fileMap = new Map(norm.filter((f) => f.path.startsWith(base)).map((f) => [f.path.slice(base.length), f.file]));
    res.pc = await pcOpen(dbf.file, wal && wal.file, async (rel) => fileMap.get(rel) || null, base);
  }
  // 그 밖의 PDF (PC data 폴더 · 그 옆 「결과」 폴더 · 묶음 안의 것은 빼고) → Claude 프린트 PDF 후보
  const taken = (path) => (res.pc && insidePcTool(path, res.pc.base)) || res.packages.some((p) => path.startsWith(p.base));
  res.pdfs = () => norm.filter((x) => /\.pdf$/i.test(x.path) && !taken(x.path));
  for (const f of norm.filter((x) => /(^|\/)print\.json$/.test(x.path))) {
    try {
      const j = JSON.parse(await f.file.text());
      if (j && j.kind === "ashrain.tt.package") {
        const base = f.path.replace(/print\.json$/, "");
        res.packages.push({ j, base, files: new Map(norm.filter((x) => x.path.startsWith(base)).map((x) => [x.path.slice(base.length), x.file])) });
      }
    } catch { /* 다른 json */ }
  }
  const left = res.pdfs();
  res.claude = left.length ? await scanPdfs(left) : null;
  return res;
}

// ── Claude 프린트 PDF: 안에 든 등록 정보(코드)로 묶는다. 코드가 없으면 파일 이름으로 묶고 새 코드를 준다.
const ROLE_ANS = /정답|풀이|해설|answer/i, ROLE_MON = /모니터|monitor/i, ROLE_STU = /학생용|답안지|활동지/;
const stemOf = (name) => name.replace(/\.pdf$/i, "").replace(/[_\-\s]*(문제지|정답과\s*풀이|정답과\s*해설|정답지|빠른\s*정답|정답|풀이|해설|학생용|답안지|활동지|모니터\s*해설|최종|수정본?|v\d+|\(\d+\)|\d{6,8})[_\-\s]*/gi, " ").replace(/\s+/g, " ").trim();
async function scanPdfs(pdfs) {
  const B = await import("./engine/base.js");
  const groups = new Map(), skipped = [];
  for (const x of pdfs) {
    const name = x.path.split("/").pop();
    let man = null, text = "", pages = 0;
    try {
      const doc = await B.openPdf(new Uint8Array(await x.file.arrayBuffer()));
      pages = doc.numPages;
      try {
        const at = await doc.getAttachments();
        for (const k of Object.keys(at || {})) {
          if (!/\.json$/i.test(at[k].filename || k)) continue;
          try { const m = JSON.parse(new TextDecoder().decode(at[k].content).replace(/^\uFEFF/, "")); if (m && m.kind === "ashrain.print") man = m; } catch { /* */ }
        }
      } catch { /* 첨부 없음 */ }
      const tc = await (await doc.getPage(1)).getTextContent();
      text = tc.items.map((i) => i.str).join(" ");
      doc.destroy();
    } catch { skipped.push(name + " (PDF를 읽지 못함)"); continue; }
    const pm = /코드\s*([2-9A-HJKMNP-Z]{3})\s*-\s*([2-9A-HJKMNP-Z]{3})/.exec(text);
    const code = (man && /^[2-9A-HJKMNP-Z]{6}$/.test(String(man.code || "").toUpperCase()) && String(man.code).toUpperCase()) || (pm ? pm[1] + pm[2] : null);
    if (!man && !code && !/@\s*ashrain\.out/i.test(text)) { skipped.push(name); continue; }
    const mt = man ? `${man.title || ""} ${man.sub || ""}` : "";
    const role = ROLE_MON.test(name) ? "모니터해설" : ROLE_STU.test(name) ? "학생용" : ROLE_ANS.test(name) || ROLE_ANS.test(mt) ? "정답" : "문제지";
    const key = code || "stem:" + stemOf(name);
    if (!groups.has(key)) groups.set(key, { code, fresh: !code, title: "", sub: "", label: "", man: null, files: [] });
    const g = groups.get(key);
    g.files.push({ x, name, role, man, pages, t: x.file.lastModified || 0 });
    if (man && role === "문제지") { g.man = man; g.title = man.title || g.title; g.sub = man.sub || g.sub; g.label = man.label || g.label; }
    if (!g.title) g.title = (man && man.title) || stemOf(name) || name;
  }
  // 같은 역할이 여러 개면 가장 새것만 (옛 판은 건너뜀)
  const list = [...groups.values()].map((g) => {
    const by = new Map();
    for (const f of [...g.files].sort((a, b) => b.t - a.t)) if (!by.has(f.role)) by.set(f.role, f); else f.old = true;
    g.use = by;
    g.old = g.files.filter((f) => f.old).map((f) => f.name);
    return g;
  }).filter((g) => g.use.has("문제지") || (skipped.push(...g.files.map((f) => f.name + " (문제지 없음)")), false));
  return { groups: list, skipped };
}
async function importClaudePdfs(cl, ui) {
  const E = await import("./engine/register.js");
  const { knownNames } = await import("./backend.js");
  const { newCode } = await import("./logic.js");
  const have = new Set((await all(() => T("tt_prints").select("code"))).map((r) => r.code));
  const known = await knownNames();
  let done = 0, skipped = 0;
  const errors = [];
  let k = 0;
  for (const g of cl.groups) {
    k++;
    ui.status(`Claude 프린트 ${k}/${cl.groups.length} · ${g.title}`);
    let code = g.code;
    if (code && have.has(code)) { skipped++; continue; }
    if (!code) { do code = newCode(); while (have.has(code)); }
    try {
      const found = new Set();
      let boxes = [];
      const prep = async (f, stamp) => {
        let bytes = new Uint8Array(await f.x.file.arrayBuffer());
        const D = await E.readDoc(bytes);
        const fn = E.findNames(D, known);
        fn.removed.forEach((r) => found.add(r.text));
        if (f.role === "문제지") boxes = fn.boxes;
        bytes = await E.redactPages(bytes, D, fn.targets);
        if (stamp) bytes = await E.stampCode(bytes, code);
        return new Uint8Array(bytes);
      };
      const files = { sheet: `${code}/sheet.pdf`, answer: null, src: [], extras: [] };
      const s = g.use.get("문제지");
      await put(files.sheet, await prep(s, g.fresh), "application/pdf");
      const a = g.use.get("정답");
      if (a) { files.answer = `${code}/answer.pdf`; await put(files.answer, await prep(a, g.fresh), "application/pdf"); }
      let n = 0;
      for (const [role, f] of g.use) {
        if (role === "문제지" || role === "정답") continue;
        const rel = `${code}/extras/x${++n}.pdf`;
        await put(rel, await prep(f, g.fresh), "application/pdf");
        files.extras.push({ name: f.name, role, path: rel });
      }
      files.sheet_name = s.name; files.answer_name = a ? a.name : null;
      const strip = (t) => { let o = String(t || ""); for (const nm of [...found, ...known].filter((v) => v && v.length >= 2)) o = o.split(nm).join(" "); return o.replace(/\s{2,}/g, " ").trim(); };
      const made = new Date(s.t || Date.now());
      must(await T("tt_prints").insert({
        code, title: strip(g.title) || code, sub: strip(g.sub), kind: "registered", template: "등록", label: g.label || "서답형",
        n_items: g.man && Array.isArray(g.man.items) ? g.man.items.length : 0, pages: s.pages || 0,
        sources: [...g.use.values()].map((f) => strip(f.name)), files, name_boxes: boxes, shelf: "library",
        options: { library: { made: `${made.getFullYear()}-${String(made.getMonth() + 1).padStart(2, "0")}-${String(made.getDate()).padStart(2, "0")}`,
          for: [...found], roles: [...g.use.keys()], fresh_code: g.fresh, old: g.old } },
      }).select("id").single());
      log("library_import", null, null, { code, title: g.title, files: g.use.size, fresh: g.fresh });
      have.add(code);
      done++;
    } catch (e) { errors.push(`${g.title}: ${e.message}`); }
  }
  return { done, skipped, errors };
}

// 여러 파일 올리기 (동시에 4개)
async function putAll(jobs, onStep) {
  let i = 0, fail = [];
  const worker = async () => {
    while (i < jobs.length) {
      const j = jobs[i++];
      // 파일을 먼저 읽어 바이트로 보낸다(폴더에서 고른 파일을 그대로 넘기면 일부 환경에서 올리기가 끊김)
      try {
        const data = j.file instanceof Uint8Array ? j.file : typeof j.file?.arrayBuffer === "function" ? new Uint8Array(await j.file.arrayBuffer()) : j.file;
        await put(j.rel, data, j.type || mimeOf(j.rel));
      }
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

// ── PC 강사도구 자료 → tt_* : 여러 번 해도 새것만 더한다
// 프린트는 코드로, 학생은 이름으로, 채점은 (프린트, 학생)으로, 회차는 번호로, 채점 표시·활동 로그·스캔본은 내용으로 겹침을 가린다.
// 학생별로 만든 프린트(11/12판)는 시험지 이름 칸 · 정답지에 이름이 찍혀 있어서 이름 지운 판으로 넣는다(기본 프린트는 이름 없는 판).
// opts.only: 이 코드들만(시험용)
const chunked = async (ids, fn, n = 150) => { const out = []; for (let k = 0; k < ids.length; k += n) out.push(...(await fn(ids.slice(k, k + n)))); return out; };
const groupBy = (rows, key) => { const m = new Map(); for (const x of rows) { const k = x[key]; if (!m.has(k)) m.set(k, []); m.get(k).push(x); } return m; };

async function pcOnePrint(pc, p, items, ctx) {
  const { code, old, names, E, pCols, ui } = ctx;
  const found = new Set();
  const nameSet = () => new Set([...names, ...found]);
  let boxes = [];
  const prep = async (f, isSheet) => {
    const bytes0 = new Uint8Array(await f.arrayBuffer());
    const D = await E.readDoc(bytes0);
    try {
      const fn = E.findNames(D, nameSet());
      fn.removed.forEach((x) => found.add(x.text));
      if (isSheet) boxes = fn.boxes;
      return new Uint8Array(await E.redactPages(bytes0, D, fn.targets));
    } finally { try { D.doc.destroy(); } catch { /* 닫기 실패는 무시 */ } }
  };
  const fileOf = (rel) => (rel ? pc.getFile("prints/" + rel) : null);
  const jobs = [];
  const sf = await fileOf(p.pdf);
  if (!sf) throw new Error("시험지 PDF가 폴더에 없어요");
  ui.status(`${ctx.label} · 이름 지우는 중`);
  jobs.push({ rel: `${code}/sheet.pdf`, file: await prep(sf, true), type: "application/pdf" });
  const af = await fileOf(p.answer_pdf);
  if (af) jobs.push({ rel: `${code}/answer.pdf`, file: await prep(af, false), type: "application/pdf" });
  const extras = [];
  const ex = jparse(pCols.has("extras") ? p.extras : null, []) || [];
  for (const [k, x] of ex.entries()) {
    const fn = String(x.file || "").split("/").pop();
    const f = await fileOf(x.file);
    if (!f) continue;
    const rel = `${code}/extras/x${k + 1}${extOf(fn)}`;      // 저장 공간 이름은 영문만 — 보이는 이름은 name 에
    jobs.push({ rel, file: /\.pdf$/i.test(fn) ? await prep(f, false) : f });
    extras.push({ name: stripNames(x.name || fn, [...nameSet()]) || fn, role: x.role || "기타", path: rel });
  }
  for (const it of items) for (const k of ["png", "answer_png", "sol_png"]) {
    if (!it[k]) continue;
    const f = await fileOf(`${code}/${it[k]}`);
    if (f) jobs.push({ rel: `${code}/${it[k]}`, file: f });
  }
  ui.status(`${ctx.label} · 파일 ${jobs.length}개 올리는 중`);
  let n = 0;
  const fails = await putAll(jobs, () => ui.progress(++n, jobs.length));
  if (fails.length) throw new Error(`파일 ${fails.length}개를 못 올렸어요 (${fails[0]})`);
  const nm = [...nameSet()];
  const meta = cleanPrintMeta(p, nameSet());
  const kind = pCols.has("kind") && ["mathflat", "registered", "wrong"].includes(p.kind) ? p.kind : "mathflat";
  const row = {
    title: meta.title, sub: meta.sub, kind, template: p.template || "", label: p.label || "서답형",
    level: (pCols.has("level") && p.level) || guessLevel(meta.title, meta.sub, p.template), n_items: p.n_items ?? items.length,
    n_choice: p.n_choice ?? items.filter((x) => x.choice).length, pages: p.pages ?? 0, sources: meta.sources,
    files: { sheet: `${code}/sheet.pdf`, answer: af ? `${code}/answer.pdf` : null, src: [], extras }, name_boxes: boxes,
    options: { ...meta.options, from_pc: true }, shelf: p.deleted ? "deleted" : "active", updated_at: KST(p.updated_at) || undefined,
  };
  let pid = old && old.id;
  if (pid) must(await T("tt_prints").update(row).eq("id", pid));
  else pid = must(await T("tt_prints").insert({ code, ...row, created_at: KST(p.created_at) || undefined }).select("id").single()).id;
  const rows = items.map((it) => ({ print_id: pid, seq: it.seq, src: stripNames(it.src, nm) || null, src_no: it.src_no != null ? String(it.src_no) : null, choice: !!it.choice,
    hash: it.hash || null, png: it.png || null, answer: it.answer || "", label: it.label ?? null, points: it.points ?? null, topic: it.topic || "", answer_png: it.answer_png || null,
    tag: it.tag || "", rate: it.rate || "", sol_png: it.sol_png || null, scale: it.scale ?? null, origin: it.origin || null }));
  for (let k = 0; k < rows.length; k += 200) must(await T("tt_print_items").upsert(rows.slice(k, k + 200), { onConflict: "print_id,seq", ignoreDuplicates: true }));
  return { pid, anon: found.size > 0 };
}

export async function syncPc(pc, ui, opts = {}) {
  const q = pc.q;
  const errors = [];
  const r = { students: 0, prints: 0, repaired: 0, skipped: [], anon: 0, deleted: 0, targets: 0, gradings: 0, gradingsUpdated: 0, sessions: 0, marks: 0, scans: 0, classRecs: 0, events: 0, transcripts: 0, errors };
  const E = await import("./engine/register.js");
  const { knownNames } = await import("./backend.js");
  const names = knownFromPc(q, await knownNames().catch(() => []));
  // 학생 (이름으로)
  ui.status("학생 명단");
  const stOld = q("SELECT * FROM students ORDER BY id");
  const stNew = new Map((await all(() => T("tt_students").select("id,name"))).map((x) => [x.name, x.id]));
  const sMap = new Map();
  for (const s of stOld) {
    const nm = String(s.name || "").replace(/\s+/g, " ").trim();
    if (!nm) continue;
    if (stNew.has(nm)) { sMap.set(s.id, stNew.get(nm)); continue; }
    try {
      const row = must(await T("tt_students").insert({ name: nm, grade: s.grade || "", memo: s.memo || "", active: s.active !== 0, created_at: KST(s.created_at) || undefined, updated_at: KST(s.updated_at) || undefined }).select("id").single());
      sMap.set(s.id, row.id); stNew.set(nm, row.id); r.students++;
    } catch (e) { errors.push(`학생 ${nm}: ${e.message}`); }
  }
  // 프린트 (코드로) — 없으면 넣고, 넣다 만 것(문항이 모자람)은 다시, PC에서 지운 것은 웹에서도 지운 칸으로
  const web = new Map((await all(() => T("tt_prints").select("id,code,shelf,options"))).map((x) => [x.code, x]));
  const itemCount = new Map();
  for (const it of await all(() => T("tt_print_items").select("print_id"))) itemCount.set(it.print_id, (itemCount.get(it.print_id) || 0) + 1);
  const pCols = tableCols(q, "prints");
  const prints = q("SELECT * FROM prints ORDER BY id").filter((p) => !opts.only || opts.only.has(String(p.code || "").toUpperCase()));
  const pMap = new Map();
  let pi = 0;
  for (const p of prints) {
    pi++;
    const code = String(p.code || "").toUpperCase();
    if (!/^[2-9A-HJKMNP-Z]{6}$/.test(code)) { if (code) errors.push(`${p.title || "?"}: 코드가 이상해서 건너뛰었어요 (${p.code})`); continue; }
    const items = q(`SELECT * FROM print_items WHERE print_id=${Number(p.id)} ORDER BY seq`);
    const old = web.get(code);
    if (old && (itemCount.get(old.id) || 0) >= items.length) {
      pMap.set(p.id, { id: old.id, code, existed: true });
      r.skipped.push(code);
      if (p.deleted && old.shelf === "active" && old.options && old.options.from_pc) {
        try { must(await T("tt_prints").update({ shelf: "deleted", updated_at: KST(p.updated_at) || new Date().toISOString() }).eq("id", old.id)); r.deleted++; } catch (e) { errors.push(`${p.title || code}: ${e.message}`); }
      }
      continue;
    }
    const label = `프린트 ${pi}/${prints.length} · ${p.title || code}`;
    ui.status(label);
    try {
      const one = await pcOnePrint(pc, p, items, { code, old, names, E, pCols, ui, label });
      pMap.set(p.id, { id: one.pid, code, existed: false });
      if (old) r.repaired++; else r.prints++;
      if (one.anon) r.anon++;
    } catch (e) { errors.push(`${p.title || code}: ${e.message}`); }
  }
  const P = (oid) => { const m = pMap.get(oid); return m ? m.id : null; };
  const codeOf = (oid) => { const m = pMap.get(oid); return m ? m.code : null; };
  // 출제 대상
  ui.status("출제 대상");
  const tg = q("SELECT * FROM print_targets").filter((t) => P(t.print_id) && sMap.get(t.student_id))
    .map((t) => ({ print_id: P(t.print_id), student_id: sMap.get(t.student_id), issued_at: KST(t.issued_at) || undefined }));
  for (let k = 0; k < tg.length; k += 500) { try { must(await T("tt_targets").upsert(tg.slice(k, k + 500), { onConflict: "print_id,student_id", ignoreDuplicates: true })); } catch (e) { errors.push("출제 대상: " + e.message); } }
  r.targets = tg.length;
  // 채점 · 회차 · 표시 · 스캔본
  ui.status("채점 기록");
  const pids = [...new Set([...pMap.values()].map((m) => m.id))];
  const wg = pids.length ? await chunked(pids, (ids) => all(() => T("tt_gradings").select("id,print_id,student_id,status,updated_at").in("print_id", ids))) : [];
  const wgBy = new Map(wg.map((g) => [`${g.print_id}|${g.student_id}`, g]));
  const gids = wg.map((g) => g.id);
  const wSes = groupBy(gids.length ? await chunked(gids, (ids) => all(() => T("tt_sessions").select("grading_id,no,ended_at").in("grading_id", ids))) : [], "grading_id");
  const wMarks = groupBy(gids.length ? await chunked(gids, (ids) => all(() => T("tt_marks").select("grading_id,session_no,seq,result,at").in("grading_id", ids))) : [], "grading_id");
  const wScans = groupBy(gids.length ? await chunked(gids, (ids) => all(() => T("tt_scans").select("grading_id,name,size").in("grading_id", ids))) : [], "grading_id");
  const gsCols = tableCols(q, "grading_sessions");
  for (const g of q("SELECT * FROM gradings ORDER BY id")) {
    const pid = P(g.print_id), sid = sMap.get(g.student_id);
    if (!pid || !sid) continue;
    try {
      let w = wgBy.get(`${pid}|${sid}`);
      if (!w) {
        const row = must(await T("tt_gradings").insert({ print_id: pid, student_id: sid, status: g.status || "open", mode: g.mode || "ox", created_at: KST(g.created_at) || undefined, updated_at: KST(g.updated_at) || undefined }).select("id").single());
        w = { id: row.id, status: g.status || "open" };
        wgBy.set(`${pid}|${sid}`, w);
        r.gradings++;
      } else if (gradingNewer(g, w)) {
        must(await T("tt_gradings").update({ status: g.status || "open", updated_at: KST(g.updated_at) }).eq("id", w.id));
        r.gradingsUpdated++;
      }
      const gid = w.id;
      const sess = q(`SELECT * FROM grading_sessions WHERE grading_id=${Number(g.id)} ORDER BY no`);
      const plan = sessionPlan(sess, wSes.get(gid) || []);
      const toRow = (s) => ({ grading_id: gid, no: s.no, round: gsCols.has("round") ? s.round || 1 : 1, kind: gsCols.has("kind") ? s.kind || "solve" : "solve",
        targets: gsCols.has("targets") ? jparse(s.targets, null) : null, started_at: KST(s.started_at) || undefined, ended_at: KST(s.ended_at), end_reason: s.end_reason || null });
      if (plan.add.length) { must(await T("tt_sessions").insert(plan.add.map(toRow))); r.sessions += plan.add.length; }
      for (const s of plan.close) must(await T("tt_sessions").update({ ended_at: KST(s.ended_at), end_reason: s.end_reason || null }).eq("grading_id", gid).eq("no", s.no));
      const ms = q(`SELECT * FROM marks WHERE grading_id=${Number(g.id)} ORDER BY id`).filter((m) => ["O", "X", "U"].includes(m.result))
        .map((m) => ({ grading_id: gid, session_no: m.session_no, seq: m.seq, result: m.result, answer: m.answer || "", at: KST(m.at) || undefined }));
      const newMarks = onlyNew(ms, wMarks.get(gid) || [], markKey);
      for (let k = 0; k < newMarks.length; k += 500) must(await T("tt_marks").insert(newMarks.slice(k, k + 500)));
      r.marks += newMarks.length;
      const sc = q(`SELECT * FROM scans WHERE grading_id=${Number(g.id)} AND deleted=0 ORDER BY id`).map((x) => ({ ...x, name: x.name || String(x.file || "").split("/").pop(), size: x.size || 0 }));
      const newScans = onlyNew(sc, wScans.get(gid) || [], scanKey);
      let k = (wScans.get(gid) || []).length;
      for (const x of newScans) {
        const f = await pc.getFile("scans/" + x.file);
        if (!f) continue;
        const fn = String(x.file).split("/").pop();
        const rel = `${codeOf(g.print_id)}/scans/${gid}/${String(++k).padStart(2, "0")}_pc${extOf(fn)}`;
        try {
          const data = new Uint8Array(await f.arrayBuffer());
          await put(rel, data, mimeOf(fn));
          must(await T("tt_scans").insert({ grading_id: gid, path: rel, name: x.name, size: x.size || data.length, mime: mimeOf(fn), pages: x.pages || 1, created_at: KST(x.created_at) || undefined }));
          r.scans++;
        } catch (e) { errors.push(`스캔본 ${x.name}: ${e.message}`); }
      }
    } catch (e) { errors.push(`채점 ${g.id}: ${e.message}`); }
  }
  // 수업 기록
  ui.status("수업 기록");
  const cr = q("SELECT * FROM class_records").filter((x) => sMap.get(x.student_id) && P(x.print_id))
    .map((x) => ({ day: x.date, student_id: sMap.get(x.student_id), kind: x.kind, print_id: P(x.print_id), created_at: KST(x.created_at) || undefined }));
  for (let k = 0; k < cr.length; k += 500) { try { must(await T("tt_class_records").upsert(cr.slice(k, k + 500), { onConflict: "day,student_id,kind,print_id", ignoreDuplicates: true })); } catch (e) { errors.push("수업 기록: " + e.message); } }
  r.classRecs = cr.length;
  // 활동 로그 (옮긴 프린트에 딸린 것 + 학생 것) — 같은 때·같은 일은 한 번만
  ui.status("활동 로그");
  const allNames = new Set([...names]);
  const ev = q("SELECT * FROM events ORDER BY id").filter((e) => (!e.print_id || P(e.print_id)) && (!opts.only || e.print_id))
    .map((e) => ({ at: KST(e.at) || undefined, kind: e.kind, student_id: e.student_id ? sMap.get(e.student_id) || null : null, print_id: e.print_id ? P(e.print_id) : null,
      detail: { ...cleanEventDetail(e.kind, e.detail, allNames), from_pc: true } }));
  try {
    const wEv = await all(() => T("tt_events").select("at,kind,student_id,print_id").filter("detail->>from_pc", "eq", "true"));
    const newEv = onlyNew(ev, wEv, eventKey);
    for (let k = 0; k < newEv.length; k += 500) must(await T("tt_events").insert(newEv.slice(k, k + 500)));
    r.events = newEv.length;
  } catch (e) { errors.push("활동 로그: " + e.message); }
  // 전사본
  ui.status("전사본");
  const tr = q("SELECT * FROM transcripts").map((t) => ({ item_key: t.item_key, print_id: t.print_id ? P(t.print_id) : null, seq: t.seq, level: t.level, question: t.question, solution: t.solution,
    corpus_id: t.corpus_id, source: t.source, batch: t.batch, updated_at: KST(t.updated_at) || undefined }));
  for (let k = 0; k < tr.length; k += 300) { try { must(await T("tt_transcripts").upsert(tr.slice(k, k + 300), { onConflict: "owner,item_key", ignoreDuplicates: true })); } catch (e) { errors.push("전사본: " + e.message); break; } }
  r.transcripts = tr.length;
  r.changed = r.students + r.prints + r.repaired + r.deleted + r.gradings + r.gradingsUpdated + r.sessions + r.marks + r.scans + r.events;
  if (r.changed) log("pc_import", null, null, { students: r.students, prints: r.prints, repaired: r.repaired, anon: r.anon, deleted: r.deleted, gradings: r.gradings, marks: r.marks, scans: r.scans, events: r.events, errors: errors.length });
  try { pc.S.close(); } catch { /* 이미 닫힘 */ }
  return r;
}

// ── PC 자료 폴더 기억 (Chrome · Edge 파일 시스템 접근) — 이 브라우저에만, 계정마다 하나
// 강사도구를 열 때(또는 창으로 돌아올 때) mf.db 가 바뀌었으면 syncPc 로 새것만 더한다. SSD가 빠져 있으면 조용히 넘어간다.
const HDB = "tt-pc", HSTORE = "folders";
export const fsAccessOk = () => typeof window !== "undefined" && "showDirectoryPicker" in window && "indexedDB" in window;
function hdb() {
  return new Promise((res, rej) => {
    const r = indexedDB.open(HDB, 1);
    r.onupgradeneeded = () => r.result.createObjectStore(HSTORE);
    r.onsuccess = () => res(r.result);
    r.onerror = () => rej(r.error);
  });
}
async function hdo(mode, fn) {
  const db = await hdb();
  try {
    return await new Promise((res, rej) => {
      const tx = db.transaction(HSTORE, mode);
      const req = fn(tx.objectStore(HSTORE));
      tx.oncomplete = () => res(req ? req.result : undefined);
      tx.onerror = () => rej(tx.error);
      tx.onabort = () => rej(tx.error);
    });
  } finally { db.close(); }
}
export async function pcFolderGet() {
  try { const k = await uid(); return (await hdo("readonly", (st) => st.get(k))) || null; } catch { return null; }
}
async function pcFolderSet(rec) {
  try { const k = await uid(); await hdo("readwrite", (st) => st.put(rec, k)); } catch { /* 기억 못 해도 옮기기는 됨 */ }
}
export async function pcFolderForget() {
  try { const k = await uid(); await hdo("readwrite", (st) => st.delete(k)); } catch { /* 없음 */ }
}
const child = async (d, name, dir = false) => { try { return dir ? await d.getDirectoryHandle(name) : await d.getFileHandle(name); } catch { return null; } };
// 고른 폴더가 data 폴더이거나 그 위(강사도구 폴더)
async function dataDirOf(h) {
  if (!h || h.kind !== "directory") return null;
  if (await child(h, "mf.db")) return h;
  const d = await child(h, "data", true);
  return d && (await child(d, "mf.db")) ? d : null;
}
// 바뀌었는지는 mf.db·WAL 의 크기와 고친 때로 (내용은 읽지 않음)
async function pcPeek(h) {
  const data = await dataDirOf(h);
  if (!data) return null;
  const dbFile = await (await data.getFileHandle("mf.db")).getFile();
  const wh = await child(data, "mf.db-wal");
  const walFile = wh ? await wh.getFile() : null;
  return { data, dbFile, walFile, sig: `${dbFile.size}:${dbFile.lastModified || 0}:${walFile ? walFile.size + ":" + (walFile.lastModified || 0) : "-"}` };
}
async function pcFromPeek(pk) {
  const dirs = new Map([["", pk.data]]);
  const dirOf = async (path) => {
    if (dirs.has(path)) return dirs.get(path);
    const i = path.lastIndexOf("/");
    const parent = await dirOf(i < 0 ? "" : path.slice(0, i));
    const d = parent ? await child(parent, path.slice(i + 1), true) : null;
    dirs.set(path, d);
    return d;
  };
  const getFile = async (rel) => {
    const i = rel.lastIndexOf("/");
    const d = await dirOf(i < 0 ? "" : rel.slice(0, i));
    const fh = d ? await child(d, rel.slice(i + 1)) : null;
    return fh ? fh.getFile() : null;
  };
  return pcOpen(pk.dbFile, pk.walFile, getFile, pk.data.name + "/");
}
const whenStr = (iso) => { const d = new Date(iso); return isNaN(d) ? "" : `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`; };
export function pcSummary(a) {
  const parts = [];
  if (a.prints) parts.push(`새 프린트 ${a.prints}개${a.anon ? ` (그중 ${a.anon}개는 학생 이름을 지운 판)` : ""}`);
  if (a.repaired) parts.push(`넣다 만 프린트 ${a.repaired}개 다시`);
  if (a.deleted) parts.push(`PC에서 지운 프린트 ${a.deleted}개는 지운 칸으로`);
  if (a.students) parts.push(`학생 ${a.students}명`);
  if (a.gradings || a.gradingsUpdated) parts.push(`채점 ${a.gradings}건${a.gradingsUpdated ? ` (이어진 채점 ${a.gradingsUpdated}건)` : ""}`);
  if (a.marks) parts.push(`채점 표시 ${a.marks}개`);
  if (a.scans) parts.push(`스캔본 ${a.scans}개`);
  if (a.events) parts.push(`활동 로그 ${a.events}줄`);
  return parts.join(" · ");
}

// 강사도구 위쪽 띠 (화면이 바뀌어도 남도록 #tt-view 바깥)
function pcBar(view, esc) {
  let el = view.parentNode.querySelector("#tt-pcbar");
  const ensure = () => {
    if (!el) {
      el = document.createElement("div");
      el.id = "tt-pcbar";
      el.className = "card";
      el.style.cssText = "margin:0 0 14px;padding:10px 14px;background:var(--accbg);border-color:#99d5cc";
      view.parentNode.insertBefore(el, view);
    }
    return el;
  };
  return {
    show(html, btn, onBtn, closable) {
      const b = ensure();
      b.innerHTML = `<div class="row" style="gap:8px"><span class="small" style="flex:1;min-width:200px">${html}</span>${btn ? `<button class="btn small" data-a="go">${esc(btn)}</button>` : ""}${closable ? `<button class="btn ghost small" data-a="x">닫기</button>` : ""}</div>
        <div data-a="pg" hidden style="height:6px;background:#e2e8f0;border-radius:6px;overflow:hidden;margin-top:6px"><div style="height:6px;width:0;background:var(--acc);transition:width .2s"></div></div>`;
      if (btn) b.querySelector("[data-a=go]").onclick = () => onBtn();
      if (closable) b.querySelector("[data-a=x]").onclick = () => this.hide();
    },
    status(t) { const b = ensure(); const sp = b.querySelector("span"); if (sp) sp.textContent = t; },
    progress(a, n) { const b = ensure(); const pg = b.querySelector("[data-a=pg]"); if (!pg) return; pg.hidden = false; pg.firstElementChild.style.width = (n ? Math.round((a / n) * 100) : 0) + "%"; },
    hide() { if (el) { el.remove(); el = null; } },
  };
}

let pcBusy = false, pcLastLook = 0;
async function runPcSync(rec, bar, { toast, esc, manual }) {
  if (pcBusy) return null;
  pcBusy = true;
  try {
    let pk = null;
    try { pk = await pcPeek(rec.handle); } catch { pk = null; }
    if (!pk) { if (manual) bar.show("PC 강사도구 자료 폴더를 찾지 못했어요 — SSD가 꽂혀 있는지 봐 주세요", null, null, true); else bar.hide(); return null; }
    if (!manual && rec.sig && rec.sig === pk.sig) { bar.hide(); return null; }
    bar.show("PC 강사도구 자료를 맞추는 중…");
    const pc = await pcFromPeek(pk);
    const res = await syncPc(pc, { status: (t) => bar.status(t), progress: (a, n) => bar.progress(a, n) });
    const sum = pcSummary(res);
    await pcFolderSet({ ...rec, sig: res.errors.length ? rec.sig || null : pk.sig, at: new Date().toISOString(), last: sum || "새로 더할 것 없음" });
    if (res.errors.length) {
      bar.show(`PC 자료를 맞추다 ${res.errors.length}건을 못 옮겼어요 — ${esc(res.errors[0])}`, "다시", () => runPcSync(rec, bar, { toast, esc, manual: true }), true);
    } else if (res.changed) {
      bar.show(`PC 강사도구에서 반영했어요 — ${esc(sum)} · <a href="#/tt/prints">프린트함</a>`, null, null, true);
      toast("PC 강사도구에서 새로 등록한 것을 반영했어요");
    } else if (manual) {
      bar.show("PC 강사도구와 이미 같아요 — 새로 더할 것이 없어요", null, null, true);
    } else bar.hide();
    return res;
  } catch (e) {
    bar.show(`PC 자료를 맞추지 못했어요 — ${esc(e.message)}`, "다시", () => runPcSync(rec, bar, { toast, esc, manual: true }), true);
    return null;
  } finally { pcBusy = false; }
}
// 강사도구를 열 때 · 창으로 돌아올 때 (ui.js)
export async function pcAutoSync({ view, toast, esc, manual = false }) {
  if (pcBusy || !fsAccessOk()) return;
  if (!manual && Date.now() - pcLastLook < 20000) return;
  pcLastLook = Date.now();
  const rec = await pcFolderGet();
  if (!rec || !rec.handle || !rec.handle.queryPermission) return;
  const bar = pcBar(view, esc);
  let perm = "prompt";
  try { perm = await rec.handle.queryPermission({ mode: "read" }); } catch { return; }
  if (perm === "granted") return runPcSync(rec, bar, { toast, esc, manual });
  if (perm === "denied" && !manual) return;
  // 브라우저가 매번 묻는 경우 — 한 번 누르면 읽는다(「방문할 때마다 허용」을 고르면 다음부터는 묻지 않음)
  bar.show(`PC 강사도구 자료(${esc(rec.name || "data")} 폴더)에서 새로 등록한 것을 가져올까요?`, "가져오기", async () => {
    let p = "denied";
    try { p = await rec.handle.requestPermission({ mode: "read" }); } catch { p = "denied"; }
    if (p === "granted") runPcSync(rec, bar, { toast, esc, manual: true }); else bar.hide();
  }, true);
}
// 폴더 핸들 → PC 자료(없으면 null) — 시험·「지금 맞추기」에서도 씀
export async function pcOpenFolder(h) {
  const pk = await pcPeek(h);
  return pk ? pcFromPeek(pk) : null;
}
export { scan as scanFiles };
async function rememberPc(handle, pcBase, res) {
  if (!handle || !fsAccessOk()) return false;
  try {
    const pk = await pcPeek(handle);
    if (!pk) return false;
    await pcFolderSet({ handle, name: handle.name, base: pcBase, sig: res && !res.errors.length ? pk.sig : null, at: new Date().toISOString(), last: (res && pcSummary(res)) || "" });
    return true;
  } catch { return false; }
}

export async function importView({ view, $, esc, toast, fmtCode }) {
  view.innerHTML = `<h1>옮겨 오기</h1>
    <div id="imRem"></div>
    <div class="card"><h2>무엇을 옮기나요?</h2>
      <p class="sub small" style="margin:0 0 6px">① <b>PC 강사도구 자료</b> — PC 강사도구 폴더 안의 <b>data</b> 폴더(mf.db · prints · scans)를 통째로. 학생·프린트·채점 기록·스캔본·수업 기록·활동 로그·전사본이 옮겨져요.
        학생별로 만든 프린트는 <b>학생 이름을 지운 판</b>으로 넣어요. ${fsAccessOk() ? "놓은 폴더는 이 브라우저가 기억해 두었다가, <b>강사도구를 열 때마다 PC에서 새로 등록한 것을 알아서 더해요</b>(SSD가 꽂혀 있을 때)." : ""}</p>
      <p class="sub small" style="margin:0">② <b>Claude와 만든 프린트 묶음</b> — 「강사도구로 옮길 프린트」 폴더(프린트마다 print.json, zip 이어도 돼요). 보관함에 들어가고, 쓸 때 코드로 꺼내 등록해요.</p>
      <p class="sub small" style="margin:0">③ <b>Claude와 만든 프린트 PDF</b> — 받아 둔 문제지·정답 PDF를 한 폴더에 모아 통째로. PDF 안의 코드로 묶어 보관함에 넣고(옛 판은 가장 새것만), 코드가 없던 예전 프린트는 새 코드를 찍어요. 매쓰플랫·기출 PDF는 알아서 건너뛰어요.</p>
      <p class="sub small" style="margin:6px 0 0">여러 번 해도 겹치지 않아요 — 이미 있는 것은 건너뛰고 새로 생긴 것만 더해요.</p>
      <div class="drop" id="imDrop" style="margin-top:12px"><b>폴더를 끌어다 놓거나 눌러서 고르기</b><span class="sub small">둘 다 한꺼번에 놓아도 돼요</span>
        <input type="file" id="imPick" webkitdirectory directory multiple hidden></div>
      <div class="row" style="margin-top:8px"><span class="sub small">묶음이 zip 파일이면</span><button class="btn ghost small" id="imZipBtn">zip 파일 고르기</button><input type="file" id="imZip" accept=".zip" multiple hidden></div>
    </div><div id="imOut"></div>`;
  const out = $("#imOut");
  const dz = $("#imDrop"), pick = $("#imPick");
  const drawRem = async () => {
    const el = $("#imRem");
    if (!el) return;
    const rec = fsAccessOk() ? await pcFolderGet() : null;
    if (!rec || !rec.handle) { el.innerHTML = ""; return; }
    el.innerHTML = `<div class="card" style="background:var(--accbg);border-color:#99d5cc"><div class="row">
      <span class="small" style="flex:1;min-width:220px">기억한 PC 강사도구 자료: <b>${esc(rec.name || "data")}</b> 폴더${rec.at ? ` · 마지막으로 맞춘 때 ${esc(whenStr(rec.at))}` : ""}${rec.last ? `<br><span class="sub">${esc(rec.last)}</span>` : ""}</span>
      <button class="btn small" id="imRemGo">지금 맞추기</button><button class="btn ghost small" id="imRemX">잊기</button></div></div>`;
    $("#imRemGo").onclick = async () => { await pcAutoSync({ view, toast, esc, manual: true }); drawRem(); };
    $("#imRemX").onclick = async () => { await pcFolderForget(); toast("PC 자료 폴더를 잊었어요 — 다시 놓으면 또 기억해요"); drawRem(); };
  };
  drawRem();
  const ui = {
    status: (t) => { const el = $("#imSt"); if (el) el.textContent = t; },
    progress: (a, b) => { const el = $("#imBar"); if (el) el.style.width = (b ? Math.round((a / b) * 100) : 0) + "%"; },
  };
  // handles: 놓거나 고른 폴더의 핸들(약속) — PC 자료를 옮기면 그 폴더를 기억한다
  const run = async (files, handles = []) => {
    if (!files.length) return;
    out.innerHTML = `<div class="card"><span class="busy"></span>폴더를 읽는 중… (파일 ${files.length}개)</div>`;
    let r;
    try { r = await scan(files); } catch (e) { out.innerHTML = `<div class="card" style="border-color:#fca5a5"><b>읽지 못했어요</b><div class="sub">${esc(e.message)}</div></div>`; return; }
    if (!r.pc && !r.packages.length && !(r.claude && r.claude.groups.length)) { out.innerHTML = `<div class="card" style="border-color:#fca5a5"><b>옮길 것을 찾지 못했어요</b><div class="sub small">mf.db 가 든 data 폴더나, print.json 이 든 프린트 묶음 폴더를 놓아 주세요.</div></div>`; return; }
    const n = r.pc && r.pc.n;
    out.innerHTML = `<div class="card"><h2>찾은 것</h2>
      ${r.pc ? `<div>PC 강사도구 자료 — 학생 ${n.students} · 프린트 ${n.prints} · 채점 ${n.gradings} (기록 ${n.marks}) · 스캔본 ${n.scans} · 수업 기록 ${n.class} · 활동 로그 ${n.events} · 전사본 ${n.transcripts}</div>` : ""}
      ${r.packages.length ? `<div>Claude 프린트 묶음 — ${r.packages.length}개 <span class="sub small">(${r.packages.slice(0, 6).map((p) => esc(p.j.print.title || "")).join(", ")}${r.packages.length > 6 ? " …" : ""})</span></div>` : ""}
      ${r.claude && r.claude.groups.length ? `<div>Claude 프린트 PDF — <b>${r.claude.groups.length}개 프린트</b> (코드 있음 ${r.claude.groups.filter((g) => !g.fresh).length} · 코드 없어 새로 줌 ${r.claude.groups.filter((g) => g.fresh).length})
        <details><summary class="small">목록</summary><table class="t small">${r.claude.groups.map((g) => `<tr><td class="code">${g.code ? esc(fmtCode(g.code)) : "<span class='sub'>새 코드</span>"}</td><td>${esc(g.title)}</td><td class="sub">${[...g.use.keys()].map(esc).join(" · ")}${g.old.length ? ` · 옛 판 ${g.old.length}개 건너뜀` : ""}</td></tr>`).join("")}</table></details></div>` : ""}
      ${r.claude && r.claude.skipped.length ? `<div class="sub small">Claude 프린트가 아니어서(매쓰플랫·기출 등) 건너뛸 PDF ${r.claude.skipped.length}개</div>` : ""}
      <div class="row" style="margin-top:12px"><button class="btn big" id="imGo">옮기기 시작</button><span class="sub small">창을 닫지 마세요 — 파일이 많으면 몇 분 걸려요</span></div>
      <div id="imRun" hidden style="margin-top:12px"><div class="sub small" id="imSt">…</div><div style="height:8px;background:#e2e8f0;border-radius:6px;overflow:hidden;margin-top:6px"><div id="imBar" style="height:8px;width:0;background:var(--acc);transition:width .2s"></div></div></div></div>`;
    $("#imGo").onclick = async () => {
      if (pcBusy) { toast("PC 자료를 맞추는 중이에요 — 끝난 뒤에 다시 눌러 주세요"); return; }
      $("#imGo").disabled = true;
      $("#imRun").hidden = false;
      const lines = [];
      pcBusy = true;
      try {
        if (r.pc) {
          const a = await syncPc(r.pc, ui);
          const sum = pcSummary(a);
          lines.push(`<b>PC 자료</b>: ${sum ? esc(sum) : "새로 더할 것이 없었어요"}${a.skipped.length ? ` <span class="sub">(이미 있던 프린트 ${a.skipped.length}개는 건너뜀)</span>` : ""}`);
          a.errors.forEach((e) => lines.push(`<span style="color:#b91c1c">${esc(e)}</span>`));
          const top = r.pc.base.split("/")[0];
          const hs = (await Promise.all(handles)).filter((h) => h && h.kind === "directory");
          const h = hs.find((x) => x.name === top) || (hs.length === 1 ? hs[0] : null);
          if (h && (await rememberPc(h, r.pc.base, a))) lines.push(`<span class="sub">이 폴더를 기억해 두었어요 — 이 컴퓨터에서 강사도구를 열 때마다 PC에서 새로 등록한 것을 알아서 더해요.</span>`);
        }
        if (r.claude && r.claude.groups.length) {
          const c = await importClaudePdfs(r.claude, ui);
          lines.push(`<b>Claude 프린트 PDF</b>: 보관함에 ${c.done}개${c.skipped ? ` · 이미 있던 ${c.skipped}개는 건너뜀` : ""} — 학생 이름은 지운 판으로 넣었어요`);
          c.errors.forEach((e) => lines.push(`<span style="color:#b91c1c">${esc(e)}</span>`));
        }
        if (r.packages.length) {
          const b = await importPackages(r.packages, ui);
          lines.push(`<b>Claude 프린트</b>: 보관함에 ${b.done}개${b.skipped ? ` · 이미 있던 ${b.skipped}개는 건너뜀` : ""}`);
          b.errors.forEach((e) => lines.push(`<span style="color:#b91c1c">${esc(e)}</span>`));
        }
        out.innerHTML = `<div class="card" style="background:#f0fdf4;border-color:#bbf7d0"><h2>옮겼어요</h2>${lines.map((l) => `<div class="small">${l}</div>`).join("")}
          <div class="row" style="margin-top:10px"><a class="btn ghost" href="#/tt/prints">프린트함</a><a class="btn ghost" href="#/tt/register">보관함(프린트 등록)</a><a class="btn ghost" href="#/tt/students">학생</a></div></div>`;
        toast("옮기기를 마쳤어요");
        drawRem();
      } catch (e) {
        out.insertAdjacentHTML("beforeend", `<div class="card" style="border-color:#fca5a5"><b>옮기다 멈췄어요</b><div class="sub">${esc(e.message)}</div><div class="sub small">다시 하면 이미 옮긴 것은 건너뛰고 이어서 해요.</div></div>`);
        $("#imGo").disabled = false;
      } finally { pcBusy = false; }
    };
  };
  dz.onclick = async () => {
    if (fsAccessOk()) {
      let h = null;
      try { h = await window.showDirectoryPicker({ id: "tt-import", mode: "read" }); } catch { return; }   // 고르지 않고 닫음
      out.innerHTML = `<div class="card"><span class="busy"></span>폴더를 읽는 중…</div>`;
      try { run(await walkHandle(h), [Promise.resolve(h)]); } catch (e) { out.innerHTML = `<div class="card" style="border-color:#fca5a5"><b>읽지 못했어요</b><div class="sub">${esc(e.message)}</div></div>`; }
      return;
    }
    pick.click();
  };
  $("#imZipBtn").onclick = () => $("#imZip").click();
  $("#imZip").onchange = (e) => { run([...e.target.files].map((f) => ({ path: f.name, file: f }))); e.target.value = ""; };
  pick.onchange = () => { run([...pick.files].map((f) => ({ path: f.webkitRelativePath || f.name, file: f }))); pick.value = ""; };
  ["dragenter", "dragover"].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.classList.add("over"); }));
  dz.addEventListener("dragleave", (e) => { e.preventDefault(); dz.classList.remove("over"); });
  dz.addEventListener("drop", (e) => {
    e.preventDefault();
    dz.classList.remove("over");
    // 놓는 순간에만 꺼낼 수 있다 — 항목과 핸들을 먼저 모두 꺼내 둔다
    const items = [...(e.dataTransfer ? e.dataTransfer.items : [])].filter((it) => it.kind === "file");
    const entries = items.map((it) => (it.webkitGetAsEntry ? it.webkitGetAsEntry() : null));
    const handles = items.map((it) => (it.getAsFileSystemHandle ? it.getAsFileSystemHandle().catch(() => null) : Promise.resolve(null)));
    walkEntries(entries).then((files) => run(files, handles)).catch((err) => { out.innerHTML = `<div class="card" style="border-color:#fca5a5"><b>읽지 못했어요</b><div class="sub">${esc(err.message)}</div></div>`; });
  });
}
