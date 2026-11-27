// 시그니처 프린트 원본(강사도구 보관함) → 공개 버킷 concept-sets 의 av/sig/<코드>/{problems,answers}.pdf
// (학생앱 · 교실 모니터 시청각 학습의 시그니처 프린트 해설 📄 「원본 프린트」가 받는 곳 — src/lib/sigprint.js · frames/sigdocs.jsx)
//
//   SUPABASE_URL=… SUPABASE_SERVICE_KEY=… node scripts/sig-files.mjs [--out .cf] [--only WF7QYN,MACKR8]
//
// 1) 시그니처 프린트 목록 = src/features/display/frames/index.js 의 해설 액자 prints(code — 프린트 코드).
// 2) 강사도구 표 tt_prints 에서 그 코드를 찾는다(같은 코드가 여럿이면 가장 최근에 고친 것).
// 3) 문제지 = files.sheet · 정답 = files.extras 가운데 빠른정답 > 정답해설 > 해설 차례로 첫 것, 없으면 files.answer
//    (파일은 비공개 버킷 teacher-tool 의 <선생님 id>/tt/<경로> — 강사도구 tt/sb.js 와 같은 자리).
// 4) 받아서 PDF 인지 · 20 MB(공개 버킷 한도) 이하인지 보고 <out>/av/sig/<코드>/{problems,answers}.pdf 로 쓰고,
//    목록 <out>/build-sig.json(경로 · 크기 · 쪽 수 · sha256)을 만든다 — scripts/push-concept-files.mjs 가 올리고 공개 주소로 다시 받아 확인.
// 보관함에 아직 없는 코드는 건너뛴다(로그) — 앱은 받을 때 「아직 올라가지 않았어요」. 워크플로 push-sig-files 가 main 머지 때 · 매일 돌린다.
// PDF 는 저장소에 넣지 않는다(공개 저장소에는 프린트를 두지 않는다). service_role 키는 이 스크립트(서버 쪽)에서만 — 앱에는 넣지 않는다.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const BUCKET_SRC = "teacher-tool";
export const MAX_BYTES = 20 * 1024 * 1024;
export const ROLE_ORDER = ["빠른정답", "정답해설", "해설"];
const ALPHA = /^[23456789ABCDEFGHJKMNPQRSTUVWXYZ]{6}$/;

/** 「WF7-QYN」 → 「WF7QYN」 */
export const codeKey = (c) => String(c || "").replace(/-/g, "").toUpperCase();
/** 해설 액자의 시그니처 프린트 — [{ code, key, title }] (code 없는 프린트는 빼고) */
export function sigCodes(frames) {
  const out = [];
  for (const f of frames) for (const p of f.prints || []) {
    if (!p.code) continue;
    const code = codeKey(p.code);
    if (!ALPHA.test(code)) throw new Error(`프린트 코드 꼴이 아니다: ${f.key}:${p.set} ${p.code}`);
    out.push({ code, key: `${f.key}:${p.set}`, title: p.title });
  }
  return out;
}
/** 보관함 파일 — 정답 문서(빠른정답 > 정답해설 > 해설 > 정답 PDF) */
export function pickAnswer(files) {
  const ex = Array.isArray(files?.extras) ? files.extras : [];
  for (const role of ROLE_ORDER) {
    const e = ex.find((x) => x && x.role === role && /\.pdf$/i.test(x.path || ""));
    if (e) return e.path;
  }
  return files?.answer || null;
}
/** 강사도구 저장 자리 — teacher-tool/<owner>/tt/<rel> */
export const objectPath = (owner, rel) => `${owner}/tt/${String(rel).replace(/^\/+/, "")}`;
const sha256 = (b) => crypto.createHash("sha256").update(b).digest("hex");
const pdfPages = (buf) => (Buffer.from(buf).toString("latin1").match(/\/Type\s*\/Page(?![s\w])/g) || []).length;
const isPdf = (buf) => buf.length >= 5 && Buffer.from(buf.subarray(0, 5)).toString("latin1") === "%PDF-";

/**
 * 보관함에서 받아 <out> 에 쓰고 목록을 돌려준다 — { build, found: [코드], missing: [코드], skipped: [사유] }
 *   fetchImpl 은 시험에서 바꿔 끼운다(기본은 전역 fetch).
 */
export async function collect({ base, key, out, frames, only = [], fetchImpl = fetch, log = console.log }) {
  const H = { authorization: `Bearer ${key}`, apikey: key };
  let list = sigCodes(frames);
  if (only.length) list = list.filter((x) => only.includes(x.code));
  const codes = [...new Set(list.map((x) => x.code))];
  const build = { cat: "sig", bucket: "concept-sets", sets: {} };
  if (!codes.length) return { build, found: [], missing: [], skipped: [] };
  const q = `${base}/rest/v1/tt_prints?select=owner,code,title,files,updated_at&code=in.(${codes.join(",")})`;
  const r = await fetchImpl(q, { headers: H });
  if (!r.ok) throw new Error(`tt_prints 읽기 실패 ${r.status} ${await r.text()}`);
  const rows = await r.json();
  const best = {};
  for (const row of rows) {
    const c = codeKey(row.code);
    if (!best[c] || String(row.updated_at || "") > String(best[c].updated_at || "")) best[c] = row;
  }
  const found = [], missing = [], skipped = [];
  for (const code of codes) {
    const row = best[code];
    if (!row || !row.files?.sheet) { missing.push(code); continue; }
    const want = { problems: row.files.sheet, answers: pickAnswer(row.files) };
    const entry = {};
    for (const [doc, rel] of Object.entries(want)) {
      if (!rel) { skipped.push(`${code} ${doc}: 보관함에 문서 없음`); continue; }
      const g = await fetchImpl(`${base}/storage/v1/object/${BUCKET_SRC}/${objectPath(row.owner, rel).split("/").map(encodeURIComponent).join("/")}`, { headers: H });
      if (!g.ok) { skipped.push(`${code} ${doc}: 받기 실패 ${g.status}`); continue; }
      const buf = Buffer.from(await g.arrayBuffer());
      if (!isPdf(buf)) { skipped.push(`${code} ${doc}: PDF 가 아님`); continue; }
      if (buf.length > MAX_BYTES) { skipped.push(`${code} ${doc}: ${(buf.length / 1e6).toFixed(1)} MB — 공개 버킷 한도(20 MB) 넘음`); continue; }
      const p = `av/sig/${code}/${doc}.pdf`;
      fs.mkdirSync(path.join(out, path.dirname(p)), { recursive: true });
      fs.writeFileSync(path.join(out, p), buf);
      entry[doc] = { path: p, bytes: buf.length, pages: pdfPages(buf), sha256: sha256(buf) };
    }
    if (Object.keys(entry).length) { build.sets[code] = entry; found.push(code); }
    else missing.push(code);
    log(`${entry.problems ? "✓" : "·"} ${code} ${row.title || ""} — ${Object.entries(entry).map(([d, x]) => `${d} ${x.pages}쪽 ${(x.bytes / 1e3).toFixed(0)}KB`).join(" · ") || "없음"}`);
  }
  fs.mkdirSync(out, { recursive: true });
  fs.writeFileSync(path.join(out, "build-sig.json"), JSON.stringify(build, null, 1) + "\n");
  return { build, found, missing, skipped };
}

async function main() {
  const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
  const base = (process.env.SUPABASE_URL || "").replace(/\/+$/, "");
  const key = process.env.SUPABASE_SERVICE_KEY || "";
  if (!base || !key) { console.error("SUPABASE_URL · SUPABASE_SERVICE_KEY 가 필요하다"); process.exit(2); }
  const out = path.resolve(arg("--out", path.join(ROOT, ".cf")));
  const only = (arg("--only", "") || "").split(",").map(codeKey).filter(Boolean);
  const { FRAMES } = await import(pathToFileURL(path.join(ROOT, "src/features/display/frames/index.js")).href);
  const { build, found, missing, skipped } = await collect({ base, key, out, frames: FRAMES, only });
  const lines = [
    `시그니처 프린트 원본: 올릴 것 ${found.length}장 · 보관함에 아직 없음 ${missing.length}장${missing.length ? `(${missing.join(", ")})` : ""}`,
    ...skipped.map((s) => `건너뜀 — ${s}`),
    `파일 ${Object.values(build.sets).reduce((n, e) => n + Object.keys(e).length, 0)}개 → ${path.join(out, "build-sig.json")}`,
  ];
  for (const l of lines) console.log(l);
  if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, lines.map((s) => `- ${s}`).join("\n") + "\n");
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main().catch((e) => { console.error(e?.stack || String(e)); process.exit(1); });
}
