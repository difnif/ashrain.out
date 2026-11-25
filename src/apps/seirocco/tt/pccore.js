// 시록고 강사도구 — PC 강사도구 자료(data 폴더의 mf.db)를 웹 표에 맞출 때 쓰는 순수 함수.
// 브라우저·노드 둘 다에서 돌아간다(시험: tests/ttpc.test.mjs). 표 읽기·쓰기는 importer.js 의 syncPc 가 한다.
import { stripNames } from "./logic.js";

// PC 시각은 한국 시각 「2026-11-12 16:21:05」(시간대 없음) → +09:00
export const KST = (s) => {
  if (!s) return null;
  const t = String(s).trim().replace(" ", "T");
  return /[zZ]|[+-]\d\d:?\d\d$/.test(t) ? t : t + "+09:00";
};
export const jparse = (s, d) => {
  if (s == null || s === "") return d;
  if (typeof s === "object") return s;
  try { return JSON.parse(s); } catch { return d; }
};
// 같은 순간인지 비교할 열쇠(초 단위) — PC 「…16:21:05」 와 웹 「…07:21:05+00:00」 가 같아야 함
export const tsKey = (s) => {
  if (s == null || s === "") return "";
  const t = Date.parse(KST(s));
  return Number.isFinite(t) ? String(Math.round(t / 1000)) : String(s);
};

// 옛 판 mf.db 에는 없는 표(scans · transcripts …)가 있다 — 없는 표는 빈 것으로
export function safeQuery(q) {
  return (sql) => {
    try { return q(sql); } catch (e) {
      if (/no such table|no such column/i.test(String(e && e.message))) return [];
      throw e;
    }
  };
}

// 매쓰플랫 파일 이름 「261112_11&12 3-2 5,6단원_홍길동_문제지.pdf」 에서 학생 이름 자리
const FILE_NAME_RE = /_([가-힣]{2,4})_(?:문제지|정답지|해설지|정답과\s*해설|빠른\s*정답)/;
// 이 자료에서 학생 이름으로 볼 것: 학생 명단 + 프린트마다 고른 출제 대상 + 원본 파일 이름 속 이름
export function knownFromPc(q, extra = []) {
  const out = new Set();
  const add = (n) => { const v = String(n || "").replace(/\s+/g, " ").trim(); if (v.length >= 2 && v.length <= 12) out.add(v); };
  for (const r of q("SELECT name FROM students")) add(r.name);
  for (const p of q("SELECT options, sources FROM prints")) {
    const o = jparse(p.options, {}) || {};
    (Array.isArray(o.targets) ? o.targets : []).forEach(add);
    for (const s of jparse(p.sources, []) || []) { const m = FILE_NAME_RE.exec(String(s)); if (m) add(m[1]); }
  }
  extra.forEach(add);
  return out;
}

// 프린트 한 장의 글자 정보에서 학생 이름 빼기 — 제목·부제·원본 이름·문항 출처. options 의 출제 대상(targets)은 표(tt_targets)로 가므로 뺀다.
export function cleanPrintMeta(p, names) {
  const nm = [...names];
  const st = (s) => stripNames(s, nm);
  const opts = { ...(jparse(p.options, {}) || {}) };
  delete opts.targets;
  for (const k of ["title", "sub", "upper", "footer"]) if (typeof opts[k] === "string") opts[k] = st(opts[k]);
  const sources = (jparse(p.sources, []) || []).map((s) => st(s) || "학습지.pdf");
  return { title: st(p.title) || p.code, sub: st(p.sub || ""), sources, options: opts };
}

// 활동 로그 내용에서도 이름 빼기 — 학생 추가(student_add)의 이름은 학생 기록이라 그대로 둔다
export function cleanEventDetail(kind, detail, names) {
  const d = { ...(jparse(detail, {}) || {}) };
  if (kind === "student_add") return d;
  const nm = [...names];
  for (const k of ["title", "sub"]) if (typeof d[k] === "string") d[k] = stripNames(d[k], nm);
  if (Array.isArray(d.files)) d.files = d.files.map((f) => stripNames(f, nm) || "학습지.pdf");
  if (Array.isArray(d.targets)) { d.n_targets = d.targets.length; delete d.targets; }
  if (typeof d.name === "string" && names.has(d.name)) delete d.name;
  return d;
}

// 겹침 판단 열쇠
export const markKey = (m) => `${m.session_no}|${m.seq}|${m.result}|${tsKey(m.at)}`;
export const eventKey = (e) => `${tsKey(e.at)}|${e.kind}|${e.student_id ?? ""}|${e.print_id ?? ""}`;
export const scanKey = (s) => `${s.name || ""}|${Number(s.size) || 0}`;
export function onlyNew(rows, have, keyOf) {
  const seen = new Set(have.map(keyOf));
  const out = [];
  for (const r of rows) { const k = keyOf(r); if (!seen.has(k)) { seen.add(k); out.push(r); } }
  return out;
}

// 회차: 웹에 없는 것은 넣고, 웹에서 아직 안 끝난 회차가 PC에서 끝났으면 끝난 것으로
export function sessionPlan(pcSessions, webSessions) {
  const web = new Map(webSessions.map((s) => [Number(s.no), s]));
  const add = [], close = [];
  for (const s of pcSessions) {
    const w = web.get(Number(s.no));
    if (!w) add.push(s);
    else if (!w.ended_at && s.ended_at) close.push(s);
  }
  return { add, close };
}

// 채점 상태: PC 쪽이 더 나중에 고쳐졌으면 PC 상태로
export function gradingNewer(pc, web) {
  const a = Date.parse(KST(pc.updated_at) || ""), b = Date.parse(web.updated_at || "");
  return Number.isFinite(a) && (!Number.isFinite(b) || a > b + 999) && (pc.status || "open") !== web.status;
}

// SQLite WAL 이 남아 있으면(PC 강사도구가 열려 있는 때) 커밋된 쪽을 덮어써 최신 상태로
export function applyWal(db, wal) {
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

// 드롭한 폴더 안에서 PC 강사도구 「결과」 폴더(변환 결과 PDF 사본)는 Claude 프린트로 보지 않는다
export function insidePcTool(path, pcBase) {
  if (!pcBase) return false;
  const parent = pcBase.replace(/data\/$/, "");
  return path.startsWith(pcBase) || (parent !== pcBase && path.startsWith(parent + "결과/"));
}

// PNG 크기 (IHDR) — [가로, 세로] 픽셀, PNG가 아니면 null
export function pngSize(b) {
  if (!b || b.length < 24 || b[0] !== 0x89 || b[1] !== 0x50 || b[2] !== 0x4e || b[3] !== 0x47) return null;
  const u = (i) => ((b[i] << 24) >>> 0) + (b[i + 1] << 16) + (b[i + 2] << 8) + b[i + 3];
  return [u(16), u(20)];
}

// 해설 묶음(data/웹해설/solutions.json) — 문항 지문(hash)마다 Claude가 쓴 해설 그림과 정답
//   {kind:"ashrain.tt.solutions", version:1, made:"…", by:"claude", items:{ "<hash>": {answer:"2", sol:"<파일>.png", w:<pt>, h:<pt>} }}
export function readSolutions(j) {
  if (!j || j.kind !== "ashrain.tt.solutions" || typeof j.items !== "object" || !j.items) return null;
  const items = new Map();
  for (const [hash, v] of Object.entries(j.items)) {
    if (!hash || !v || typeof v !== "object") continue;
    const sol = typeof v.sol === "string" && /^[\w.-]+\.png$/i.test(v.sol) ? v.sol : null;
    const w = Number(v.w), h = Number(v.h);
    items.set(hash, { answer: typeof v.answer === "string" ? v.answer.trim() : "", sol: sol && w > 0 && h > 0 ? sol : null, w: w > 0 ? w : null, h: h > 0 ? h : null });
  }
  return { items, stamp: `${String(j.made || "")}|${items.size}`, by: String(j.by || ""), made: String(j.made || "") };
}

// 매쓰플랫 빠른정답 한 칸 → 정답 글자 (객관식은 "2", 여러 개는 "1,3")
export const quickText = (q) => (q ? String(q.choice || q.text || "").trim() : "");

// 정답 글자 고르기: PC에 적어 둔 것(선생님이 넣은 것) > 해설 묶음(Claude가 확인한 것) > 매쓰플랫 빠른정답 읽은 것
export function pickAnswer(pcAnswer, pkgAnswer, quick) {
  const a = String(pcAnswer ?? "").trim();
  if (a) return a;
  const b = String(pkgAnswer ?? "").trim();
  if (b) return b;
  return String(quick ?? "").trim();
}
