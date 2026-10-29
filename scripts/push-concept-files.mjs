// 컨셉 문제 PDF → Supabase Storage 공개 버킷 (워크플로 push-concept-files 가 부른다)
//
//   SUPABASE_URL=… SUPABASE_SERVICE_KEY=… node scripts/push-concept-files.mjs <PDF 폴더> <build-<범주>.json>…
//
// PDF 는 scripts/concept-files.mjs 가 만든다(같은 워크플로 안에서). build-<범주>.json 에 경로 · 크기 · sha256 이 있다.
// 1) 목록의 파일이 폴더에 다 있고 sha256 · 크기가 맞는지 먼저 본다 — 하나라도 어긋나면 아무것도 올리지 않는다.
// 2) 버킷이 없으면 공개 버킷으로 만든다(PDF 만, 한 파일 20 MB 까지). 있는데 비공개면 공개로 바꾼다.
// 3) 파일마다 덮어쓰기(upsert)로 올린다 — 여러 번 돌려도 같다. 실패하면 세 번까지 다시.
// 4) 공개 주소로 다시 받아 sha256 을 비교한다. CORS 헤더와 ?download= 의 Content-Disposition 도 한 파일로 살펴 요약에 남긴다.
// service_role 키는 이 스크립트(서버 쪽)에서만 쓴다 — 앱(클라이언트)에는 절대 넣지 않는다.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const BASE = (process.env.SUPABASE_URL || "").replace(/\/+$/, "");
const KEY = process.env.SUPABASE_SERVICE_KEY || "";
const [stage, ...manifests] = process.argv.slice(2);
if (!BASE || !KEY) { console.error("SUPABASE_URL · SUPABASE_SERVICE_KEY 가 필요하다"); process.exit(2); }
if (!stage || !manifests.length) { console.error("사용: node scripts/push-concept-files.mjs <PDF 폴더> <build-<범주>.json>…"); process.exit(2); }

const H = { authorization: `Bearer ${KEY}`, apikey: KEY };
const sha256 = (b) => crypto.createHash("sha256").update(b).digest("hex");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const summary = [];
const log = (s) => { console.log(s); summary.push(s); };

async function req(method, url, { body, headers = {}, ok = [200] } = {}) {
  const r = await fetch(url, { method, body, headers: { ...H, ...headers } });
  const text = await r.text();
  return { status: r.status, ok: ok.includes(r.status), text };
}

async function ensureBucket(id) {
  const g = await req("GET", `${BASE}/storage/v1/bucket/${id}`, { ok: [200] });
  if (g.ok) {
    let b = {}; try { b = JSON.parse(g.text); } catch { /* 무시 */ }
    if (b.public === true) { log(`버킷 ${id}: 있음(공개)`); return; }
    const u = await req("PUT", `${BASE}/storage/v1/bucket/${id}`, { body: JSON.stringify({ public: true }), headers: { "content-type": "application/json" } });
    if (!u.ok) throw new Error(`버킷 공개 전환 실패 ${u.status} ${u.text}`);
    log(`버킷 ${id}: 비공개 → 공개로 바꿈`);
    return;
  }
  const c = await req("POST", `${BASE}/storage/v1/bucket`, {
    body: JSON.stringify({ id, name: id, public: true, file_size_limit: 20 * 1024 * 1024, allowed_mime_types: ["application/pdf"] }),
    headers: { "content-type": "application/json" },
  });
  if (!c.ok && !/already exists|Duplicate/i.test(c.text || "")) throw new Error(`버킷 만들기 실패 ${c.status} ${c.text}`);
  log(`버킷 ${id}: 새로 만듦(공개 · PDF 전용 · 20 MB)`);
}

async function upload(bucket, rel, buf) {
  for (let t = 1; t <= 3; t++) {
    try {
      const r = await req("POST", `${BASE}/storage/v1/object/${bucket}/${rel}`, {
        body: buf, headers: { "content-type": "application/pdf", "x-upsert": "true", "cache-control": "max-age=3600" },
      });
      if (r.ok) return;
      if (r.status < 500 && r.status !== 429) throw new Error(`${r.status} ${r.text}`);
      console.warn(`  다시(${t}) ${rel}: ${r.status}`);
    } catch (e) {
      if (t === 3 || /^4\d\d /.test(e.message)) throw new Error(`올리기 실패 ${rel}: ${e.message}`);
      console.warn(`  다시(${t}) ${rel}: ${e.message}`);
    }
    await sleep(1500 * t);
  }
}

async function verify(bucket, rel, want) {
  const r = await fetch(`${BASE}/storage/v1/object/public/${bucket}/${rel}`, { cache: "no-store" });
  if (r.status !== 200) throw new Error(`공개 주소 확인 실패 ${rel}: ${r.status}`);
  const got = sha256(Buffer.from(await r.arrayBuffer()));
  if (got !== want) throw new Error(`공개 주소의 파일이 다르다 ${rel}`);
}

async function pool(list, n, fn) {
  let i = 0;
  await Promise.all(Array.from({ length: Math.min(n, list.length) }, async () => { while (i < list.length) { const x = list[i++]; await fn(x); } }));
}

let failed = false;
for (const mf of manifests) {
  const m = JSON.parse(fs.readFileSync(mf, "utf8"));
  const bucket = m.bucket || "concept-sets";
  const jobs = [];
  for (const [nn, docs] of Object.entries(m.sets || {})) {
    for (const [doc, info] of Object.entries(docs)) {
      const p = path.join(stage, info.path);
      if (!fs.existsSync(p)) throw new Error(`폴더에 없다: ${info.path}`);
      const buf = fs.readFileSync(p);
      if (buf.length !== info.bytes || sha256(buf) !== info.sha256) throw new Error(`목록과 다르다(sha256/크기): ${info.path}`);
      jobs.push({ nn, doc, rel: info.path, buf, sha: info.sha256 });
    }
  }
  log(`목록 ${path.basename(mf)}: ${m.cat} · ${Object.keys(m.sets).length}세트 · 파일 ${jobs.length}개 · ${(jobs.reduce((n, j) => n + j.buf.length, 0) / 1e6).toFixed(1)} MB`);
  await ensureBucket(bucket);
  let done = 0;
  await pool(jobs, 4, async (j) => {
    await upload(bucket, j.rel, j.buf);
    if (++done % 20 === 0 || done === jobs.length) console.log(`  올림 ${done}/${jobs.length}`);
  });
  let checked = 0;
  try {
    await pool(jobs, 6, async (j) => { await verify(bucket, j.rel, j.sha); checked++; });
  } catch (e) { failed = true; log(`✗ ${e.message}`); }
  // 앱이 쓰는 두 길을 한 파일로 확인(알림만 — 실패로 치지 않는다):
  //   ① 다른 출처(앱)에서 fetch → CORS 허용 헤더 (앱이 받아서 한글 이름을 붙인다)
  //   ② ?download= → Content-Disposition: attachment (①이 막힐 때 앱이 쓰는 길)
  const j0 = jobs[0];
  if (j0) {
    const u = `${BASE}/storage/v1/object/public/${bucket}/${j0.rel}`;
    const r1 = await fetch(u, { cache: "no-store", headers: { origin: "https://ashrain.example" } });
    try { await r1.arrayBuffer(); } catch { /* 무시 */ }
    log(`CORS(Access-Control-Allow-Origin) → ${r1.headers.get("access-control-allow-origin") || "없음 — 앱은 ?download= 링크로 받는다"}`);
    const r2 = await fetch(`${u}?download=${encodeURIComponent("확인용-문제.pdf")}`, { cache: "no-store" });
    try { await r2.arrayBuffer(); } catch { /* 무시 */ }
    log(`?download= → ${r2.status} ${r2.headers.get("content-disposition") || "Content-Disposition 없음"}`);
  }
  log(`${failed ? "✗" : "✓"} ${m.cat}: 올림 ${done}/${jobs.length} · 공개 주소 확인 ${checked}/${jobs.length}`);
}
if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, summary.map((s) => `- ${s}`).join("\n") + "\n");
if (failed) process.exit(1);
