// node tests/sig-files.test.mjs — 시그니처 프린트 원본 받기(lib/sigprint.js · scripts/sig-files.mjs) 시험. 실패 시 exit 1.
// ① 프린트 코드: 해설 액자 시그니처 프린트 22장 모두 코드(6글자 · 프린트 코드 글자) · 겹침 없음 · 액자 세트에 적힌 코드와 같음.
// ② 앱: sigOf(key) — 시그니처 프린트만 · 공개 주소 av/sig/<코드>/{problems,answers}.pdf · 받은 파일 이름.
// ③ 워크플로 스크립트: 정답 문서 고르기(빠른정답 > 정답해설 > 해설 > 정답 PDF) · 보관함 자리(<선생님>/tt/<경로>) ·
//    가짜 서버로 collect — 표에서 코드 찾기(가장 최근) · PDF 받기 · 20 MB · PDF 아님 · 없는 코드 건너뛰기 · build-sig.json.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const imp = (p) => import(pathToFileURL(path.join(ROOT, p)).href);
let pass = 0, fail = 0;
async function test(name, fn) {
  try { await fn(); pass++; console.log(`✓ ${name}`); } catch (e) { fail++; console.log(`✗ ${name}\n   ${e.message}`); }
}

const { FRAMES } = await imp("src/features/display/frames/index.js");
const S = await imp("scripts/sig-files.mjs");
const { AREA_SETS } = await imp("src/features/display/area.js");
const { PRINT_FRAMES } = await imp("src/features/display/prints/index.js");
const SP = await imp("src/lib/sigprint.js");

await test("프린트 코드: 시그니처 프린트 22장 모두 · 6글자 · 겹침 없음 · 세트에 적힌 코드와 같음", () => {
  const L = S.sigCodes(FRAMES);
  const prints = FRAMES.filter((f) => f.lesson && !f.basics).flatMap((f) => f.prints.map((p) => `${f.key}:${p.set}`));
  assert.equal(prints.length, 22);
  assert.deepEqual(L.map((x) => x.key), prints, "모든 시그니처 프린트에 코드");
  assert.equal(new Set(L.map((x) => x.code)).size, 22, "코드 겹침");
  for (const x of L) assert.match(x.code, /^[23456789ABCDEFGHJKMNPQRSTUVWXYZ]{6}$/, x.key);
  const byKey = Object.fromEntries(L.map((x) => [x.key, x.code]));
  for (const [k, s] of Object.entries(AREA_SETS)) assert.equal(byKey[`area:${k}`], S.codeKey(s.code), `area:${k}`);
  for (const fk of ["lin2", "meet"]) for (const k of PRINT_FRAMES[fk].keys) assert.equal(byKey[`${fk}:${k}`], S.codeKey(PRINT_FRAMES[fk].sets[k].code), `${fk}:${k}`);
  assert.equal(byKey["meet:tri"], "WF7QYN"); assert.equal(byKey["meet:ntri"], "N76K3X"); assert.equal(byKey["cnt100:sel"], "SQ9HWR");
  assert.equal(byKey["graph:basic"], "TKKEXN"); assert.equal(byKey["lin10:2"], "5YDFAW");
});

await test("앱: sigOf — 시그니처 프린트만 · 공개 주소 · 받은 파일 이름", () => {
  const sig = SP.sigOf("meet:tri");
  assert.ok(sig && sig.sig && sig.code === "WF7-QYN" && sig.title.includes("삼각형"), "meet:tri");
  assert.ok(SP.sigOf("lin2:3")?.code === "4QJ-4QH", "숫자 세트");
  for (const k of ["m-lin", "e-ten", "e-ten.3", "w-e3-07a", "hanoi", "meet", "nope:1"]) assert.equal(SP.sigOf(k), null, k);
  assert.equal(SP.sigPdfUrl("WF7-QYN", "problems"), "https://ueohwmjtfmvqunjgfrhx.supabase.co/storage/v1/object/public/concept-sets/av/sig/WF7QYN/problems.pdf");
  assert.equal(SP.sigPdfUrl("n76k3x", "answers").endsWith("/av/sig/N76K3X/answers.pdf"), true);
  assert.deepEqual(SP.SIG_DOCS.map((d) => d.id), ["problems", "answers"]);
  assert.equal(SP.sigDownloadName(sig, "problems"), "중등-삼각형조건100-문제지.pdf");
  assert.equal(SP.sigDownloadName(SP.sigOf("graph:hard"), "answers"), "중등-그래프그리기심화64-정답.pdf");
  for (const x of S.sigCodes(FRAMES)) assert.equal(SP.codeKey(SP.sigOf(x.key).code), x.code, x.key);
});

await test("스크립트: 정답 문서 고르기 · 보관함 자리", () => {
  assert.equal(S.pickAnswer({ answer: "A/answer.pdf", extras: [{ path: "A/extras/x2.pdf", role: "해설" }, { path: "A/extras/x1.pdf", role: "정답해설" }] }), "A/extras/x1.pdf");
  assert.equal(S.pickAnswer({ answer: "A/answer.pdf", extras: [{ path: "A/extras/x1.pdf", role: "빠른정답" }, { path: "A/extras/x2.pdf", role: "정답해설" }] }), "A/extras/x1.pdf");
  assert.equal(S.pickAnswer({ answer: "A/answer.pdf", extras: [{ path: "A/extras/x1.png", role: "정답해설" }, { path: "A/extras/x3.pdf", role: "학생용" }] }), "A/answer.pdf");
  assert.equal(S.pickAnswer({ answer: null, extras: [] }), null);
  assert.equal(S.pickAnswer(null), null);
  assert.equal(S.objectPath("u-1", "WF7QYN/sheet.pdf"), "u-1/tt/WF7QYN/sheet.pdf");
  assert.equal(S.objectPath("u-1", "/WF7QYN/extras/x1.pdf"), "u-1/tt/WF7QYN/extras/x1.pdf");
});

await test("스크립트: 가짜 서버로 collect — 가장 최근 것 · 원본 받기 · 건너뛰기 · build-sig.json", async () => {
  const out = fs.mkdtempSync(path.join(os.tmpdir(), "sig-files-"));
  const pdf = (n, pad = 0) => Buffer.concat([Buffer.from("%PDF-1.4\n"), Buffer.from(Array.from({ length: n }, (_, i) => `${i + 1} 0 obj << /Type /Page >> endobj\n`).join("")), Buffer.alloc(pad, 32)]);
  const files = {
    "u-1/tt/WF7QYN/sheet.pdf": pdf(10), "u-1/tt/WF7QYN/answer.pdf": pdf(9),
    "u-1/tt/TKKEXN/sheet.pdf": pdf(12), "u-1/tt/TKKEXN/extras/x1.pdf": pdf(3), "u-1/tt/TKKEXN/answer.pdf": pdf(30),
    "u-0/tt/MACKR8/sheet.pdf": pdf(1), "u-1/tt/MACKR8/sheet.pdf": pdf(25), "u-1/tt/MACKR8/answer.pdf": Buffer.from("not a pdf"),
    "u-1/tt/SQ9HWR/sheet.pdf": pdf(2, S.MAX_BYTES), "u-1/tt/SQ9HWR/answer.pdf": pdf(17),
  };
  const rows = [
    { owner: "u-1", code: "WF7QYN", title: "삼각형 조건", updated_at: "2026-11-25T10:00:00Z", files: { sheet: "WF7QYN/sheet.pdf", answer: "WF7QYN/answer.pdf", extras: [] } },
    { owner: "u-1", code: "TKKEXN", title: "그래프 96", updated_at: "2026-11-25T10:00:00Z",
      files: { sheet: "TKKEXN/sheet.pdf", answer: "TKKEXN/answer.pdf", extras: [{ name: "(정답 쪽).pdf", path: "TKKEXN/extras/x1.pdf", role: "정답해설" }] } },
    { owner: "u-0", code: "MACKR8", title: "옛 것", updated_at: "2026-11-01T00:00:00Z", files: { sheet: "MACKR8/sheet.pdf", answer: null, extras: [] } },
    { owner: "u-1", code: "MACKR8", title: "교점 활용", updated_at: "2026-11-25T13:26:45Z", files: { sheet: "MACKR8/sheet.pdf", answer: "MACKR8/answer.pdf", extras: [] } },
    { owner: "u-1", code: "SQ9HWR", title: "선발", updated_at: "2026-11-25T10:00:00Z", files: { sheet: "SQ9HWR/sheet.pdf", answer: "SQ9HWR/answer.pdf", extras: [] } },
  ];
  const seen = [];
  const fake = async (url, opt) => {
    seen.push(url);
    assert.equal(opt?.headers?.authorization, "Bearer KEY", "service 키로");
    const u = new URL(url);
    if (u.pathname === "/rest/v1/tt_prints") {
      const codes = u.searchParams.get("code").replace(/^in\.\(|\)$/g, "").split(",");
      assert.ok(codes.includes("N76K3X") && codes.length === 22, "시그니처 코드 전부를 한 번에");
      return new Response(JSON.stringify(rows), { status: 200, headers: { "content-type": "application/json" } });
    }
    const m = u.pathname.match(/^\/storage\/v1\/object\/teacher-tool\/(.+)$/);
    const b = m && files[decodeURIComponent(m[1])];
    return b ? new Response(b, { status: 200 }) : new Response("not found", { status: 404 });
  };
  const logs = [];
  const r = await S.collect({ base: "https://x.supabase.co", key: "KEY", out, frames: FRAMES, fetchImpl: fake, log: (s) => logs.push(s) });
  assert.deepEqual(r.found.sort(), ["MACKR8", "SQ9HWR", "TKKEXN", "WF7QYN"]);
  assert.equal(r.missing.length, 18, "보관함에 없는 코드는 건너뜀");
  assert.ok(r.missing.includes("N76K3X") && r.missing.includes("BZ8R58"));
  const B = JSON.parse(fs.readFileSync(path.join(out, "build-sig.json"), "utf8"));
  assert.equal(B.cat, "sig"); assert.equal(B.bucket, "concept-sets");
  assert.deepEqual(Object.keys(B.sets.WF7QYN), ["problems", "answers"]);
  assert.equal(B.sets.WF7QYN.problems.path, "av/sig/WF7QYN/problems.pdf");
  assert.equal(B.sets.WF7QYN.problems.pages, 10); assert.equal(B.sets.WF7QYN.answers.pages, 9);
  assert.equal(B.sets.TKKEXN.answers.pages, 3, "정답은 보관함의 정답해설(원본 정답 쪽)");
  assert.equal(B.sets.MACKR8.problems.pages, 25, "같은 코드는 가장 최근 것");
  assert.equal(B.sets.MACKR8.answers, undefined, "PDF 가 아닌 정답은 빼고");
  assert.equal(B.sets.SQ9HWR.problems, undefined, "20 MB 넘는 문서는 빼고");
  assert.equal(B.sets.SQ9HWR.answers.pages, 17);
  for (const [code, e] of Object.entries(B.sets)) for (const x of Object.values(e)) {
    const buf = fs.readFileSync(path.join(out, x.path));
    assert.equal(buf.length, x.bytes, `${code} 크기`);
  }
  assert.ok(r.skipped.some((s) => s.startsWith("MACKR8 answers")) && r.skipped.some((s) => s.startsWith("SQ9HWR problems")), r.skipped.join(" / "));
  assert.ok(seen.some((u) => u.includes("/storage/v1/object/teacher-tool/u-1/tt/TKKEXN/extras/x1.pdf")));
  assert.ok(!seen.some((u) => u.includes("TKKEXN/answer.pdf")), "정답해설이 있으면 정답 PDF 는 받지 않는다");
  const only = await S.collect({ base: "https://x.supabase.co", key: "KEY", out, frames: FRAMES, only: ["WF7QYN"], fetchImpl: async (url, o) => {
    if (url.includes("/rest/v1/")) { assert.ok(url.includes("code=in.(WF7QYN)")); return new Response(JSON.stringify(rows.slice(0, 1)), { status: 200 }); }
    return fake(url, o);
  }, log: () => {} });
  assert.deepEqual(only.found, ["WF7QYN"]);
  fs.rmSync(out, { recursive: true, force: true });
});

await test("워크플로: main 머지 · 매일 · 수동 — 보관함 원본 받기 → 공개 버킷에 올리기", () => {
  const y = fs.readFileSync(path.join(ROOT, ".github/workflows/push-sig-files.yml"), "utf8");
  for (const w of ["schedule:", "workflow_dispatch:", "src/features/display/frames/index.js", "node scripts/sig-files.mjs --out .cf",
    "node scripts/push-concept-files.mjs .cf .cf/build-sig.json", "secrets.SUPABASE_SERVICE_KEY"]) assert.ok(y.includes(w), w);
  const app = ["src/lib/sigprint.js", "src/features/display/frames/sigdocs.jsx", "src/components/AvPrintSheet.jsx"].map((p) => fs.readFileSync(path.join(ROOT, p), "utf8")).join("\n");
  assert.ok(!/SERVICE_KEY|service_role/.test(app.replace(/\/\/.*$/gm, "")), "앱 코드에 service 키 없음");
});

console.log(`\n${pass}/${pass + fail} 통과`);
if (fail) process.exit(1);
