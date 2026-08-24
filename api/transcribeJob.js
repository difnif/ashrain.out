// ashrain.out — 전사 작업 러너 (api/transcribeJob.js, v1.0)
// 호출 1회 = 작업 큐에서 페이지를 원자적으로 하나씩 집어 이중 전사(+자동 분류) 후 적재.
// 시간 예산(~38초) 안에서 여러 페이지 연속 처리 → 남은 게 있으면 자기 자신을 다시 호출(이어달리기).
// 탭이 닫혀도 체인이 계속 돌고, 화면 쪽 워치독이 혹시 끊긴 체인을 재점화한다.
// 기존 api/transcribeCorpus.js 는 삭제해도 됨 — 모든 전사가 이 러너를 통함.
// 환경변수: 기존 재사용 — ANTHROPIC_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY(또는 SUPABASE_SERVICE_KEY)

import { createClient } from "@supabase/supabase-js";

export const config = { maxDuration: 60 };

const MODELS = {
  haiku: "claude-haiku-4-5-20251001",
  sonnet: "claude-sonnet-4-6",
  opus: "claude-opus-4-8",
  fable: "claude-fable-5",
};
const PRIMARY = process.env.TRANSCRIBE_PRIMARY || "haiku";
const SECONDARY = process.env.TRANSCRIBE_SECONDARY || "sonnet";
const ARBITER = process.env.TRANSCRIBE_ARBITER || "opus";
const BUDGET_MS = 38000;

function buildSys(conceptMap) {
  return `너는 수학 문제지 전사·분류기다. 이미지 속 문항을 아래 JSON 배열로만 출력한다. 배열 밖 텍스트 금지.
각 문항: {"seq":문항번호(정수), "qtype":"choice|short|proof|essay", "question":"문제 전문",
"choices":["보기1",...] 또는 null, "answer":"답(지면에 없으면 null)", "difficulty_est":1~5 추정,
"has_math":복잡한 수식 존재, "has_figure":도형·그래프 존재,
"figure": has_figure면 {"kind":"도형 종류","labels":["점·변 라벨"],"relations":["평행·수직·길이·각 관계 짧은 문장"]} 아니면 null,
"unit_id":"단원(예 m1-1)", "concept_main":"주개념 cid 1개", "concept_subs":["부개념 cid 0~2개"],
"pattern_tags":["풀이 유형 태그 1~3개 — 예: 문장제, 역산, 반례판별, 개수세기, 최댓값"],
"confidence": 분류 확신도 0~1}

분류 규칙:
- 주개념 = 이 문항이 궁극적으로 평가하는 개념 하나. 부개념 = 풀이에 실제로 동원되는 다른 개념 — 그 개념을 몰라도 풀 수 있으면 부개념이 아니다.
- cid는 반드시 아래 개념 목록에 있는 것만 사용. 애매하면 confidence를 낮춰라.
전사 규칙: 수식은 유니코드(×,−,x²,√,¹⁄₂) 우선, 복잡한 것만 $...$ LaTeX(\\dfrac,\\sqrt 등). JSON 문자열 안 백슬래시는 \\\\ 이스케이프. 원문 그대로(오탈자 포함). 머리말·페이지번호 무시.

[개념 목록]
${conceptMap}`;
}

async function callModel(modelKey, sys, content, maxTokens = 4000) {
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": process.env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({ model: MODELS[modelKey] || modelKey, max_tokens: maxTokens, system: sys, messages: [{ role: "user", content }] }),
  });
  const j = await r.json();
  if (!r.ok) { const e = new Error(j?.error?.message || "anthropic " + r.status); e.status = r.status; throw e; }
  return (j.content || []).map((b) => b.text || "").join("");
}

const RETRYABLE = (e) => [429, 500, 529].includes(e?.status)
  || /credit balance|overloaded|rate.?limit/i.test(String(e?.message || ""));

function parseItems(t) { const m = t.match(/\[[\s\S]*\]/); if (!m) return null;
  try { const a = JSON.parse(m[0]); return Array.isArray(a) ? a : null; } catch { return null; } }
const norm = (s) => (s || "").toString().replace(/\s+/g, " ").trim();
const normUnit = (u) => { const m = String(u || "").match(/^[mh]\d-\d/); return m ? m[0] : ""; };
function sim(a, b) {
  a = norm(a); b = norm(b);
  if (a === b) return 1;
  if (a.length < 2 || b.length < 2) return 0;
  const grams = (s) => { const g = new Map();
    for (let i = 0; i < s.length - 1; i++) { const k = s.slice(i, i + 2); g.set(k, (g.get(k) || 0) + 1); } return g; };
  const ga = grams(a), gb = grams(b);
  let hit = 0, tot = 0;
  for (const [k, v] of ga) { tot += v; hit += Math.min(v, gb.get(k) || 0); }
  for (const v of gb.values()) tot += v;
  return (2 * hit) / tot;
}
function diffItem(p, s) {
  const bad = [];
  if (sim(p.question, s.question) < 0.92) bad.push("question");
  if (norm(p.answer) !== norm(s.answer)) bad.push("answer");
  if ((p.choices || []).map(norm).join("|") !== (s.choices || []).map(norm).join("|")) bad.push("choices");
  if ((p.qtype || "") !== (s.qtype || "")) bad.push("qtype");
  if (!!p.has_figure !== !!s.has_figure) bad.push("has_figure");
  if (normUnit(p.unit_id) !== normUnit(s.unit_id)) bad.push("unit");
  if ((p.concept_main || "") !== (s.concept_main || "")) bad.push("classify");
  return bad;
}

async function transcribeOne(sb, job, pg, sys, known) {
  const { data: blob, error: dl } = await sb.storage.from("corpus").download(pg.storage_path);
  if (dl) throw new Error("이미지 다운로드 실패: " + dl.message);
  const b64 = Buffer.from(await blob.arrayBuffer()).toString("base64");
  const imgBlock = { type: "image", source: { type: "base64", media_type: "image/jpeg", data: b64 } };
  const ask = [imgBlock, { type: "text", text: "이 페이지의 문항을 전사·분류해라." }];

  const [t1, t2] = await Promise.all([callModel(PRIMARY, sys, ask), callModel(SECONDARY, sys, ask)]);
  const p1 = parseItems(t1), p2 = parseItems(t2);
  if (!p1) throw new Error("1차 전사 JSON 파싱 실패");

  const items = [], runs = [];
  let arb = 0;
  for (const it of p1) {
    const mate = (p2 || []).find((x) => x.seq === it.seq) || null;
    const bad = mate ? diffItem(it, mate) : ["no_secondary"];
    const contentBad = bad.filter((b) => b !== "unit" && b !== "classify");
    const agree = contentBad.length === 0;          // 내용 합의 기준 (분류 단독 불일치는 합의로 침)
    let finalIt = it, finalModel = PRIMARY, escalate = false;
    if (agree && bad.length > 0 && mate) {
      // 분류만 갈린 경우 — 중재 없이 확신도 높은 쪽 분류 채택
      if ((mate.confidence ?? 0) > (it.confidence ?? 0))
        finalIt = { ...it, unit_id: mate.unit_id, concept_main: mate.concept_main,
                    concept_subs: mate.concept_subs, confidence: mate.confidence };
    }
    if (!agree) {
      arb++;
      if ((job.arb_mode || "api") === "queue") { escalate = true; }
      else {
      const arbAsk = [imgBlock, { type: "text",
        text: `문항 ${it.seq}번만 본다. 두 전사가 불일치(${bad.join(",")}). 이미지를 근거로 올바른 전사·분류 하나를 같은 JSON 규격의 "단일 객체"로 출력해라.\nA안: ${JSON.stringify(it)}\nB안: ${JSON.stringify(mate)}` }];
      try {
        const ta = await callModel(ARBITER, sys, arbAsk, 1600);
        const m = ta.match(/\{[\s\S]*\}/);
        if (m) { finalIt = JSON.parse(m[0]); finalModel = ARBITER; }
      } catch { /* 중재 실패 시 1차안 유지 */ }
      }
    }
    const cMain = known.has(finalIt.concept_main) ? finalIt.concept_main : null;
    const cSubs = (finalIt.concept_subs || []).filter((x) => known.has(x) && x !== cMain).slice(0, 2);
    const unitJ = normUnit(finalIt.unit_id) || (cMain ? normUnit(cMain) : normUnit(job.unit_hint)) || null;
    const ck = `${unitJ || "?"}|${finalIt.qtype || "?"}|m${finalIt.has_math ? 1 : 0}|f${finalIt.has_figure ? 1 : 0}`;

    if (!agree) runs.push({ doc_id: job.doc_id, page: pg.page, seq: it.seq, cluster_key: ck, role: "arbiter", model: ARBITER, agree: false, diff_fields: bad, adopted: true });
    runs.push({ doc_id: job.doc_id, page: pg.page, seq: it.seq, cluster_key: ck, role: "primary", model: PRIMARY, agree, diff_fields: bad, adopted: agree });
    if (mate) runs.push({ doc_id: job.doc_id, page: pg.page, seq: it.seq, cluster_key: ck, role: "secondary", model: SECONDARY, agree, diff_fields: bad, adopted: false });

    items.push({
      doc_id: job.doc_id, page: pg.page, seq: finalIt.seq ?? it.seq,
      unit_id: unitJ, concept_main: cMain, concept_subs: cSubs,
      concept_ids: [cMain, ...cSubs].filter(Boolean),
      pattern_tags: (finalIt.pattern_tags || []).slice(0, 3),
      confidence: cMain ? (finalIt.confidence ?? null) : 0,
      qtype: finalIt.qtype || "short", question: finalIt.question || "",
      choices: finalIt.choices || null, answer: finalIt.answer ?? null,
      difficulty_est: finalIt.difficulty_est ?? null,
      has_math: !!finalIt.has_math, has_figure: !!finalIt.has_figure,
      figure: finalIt.figure || null, cluster_key: ck,
      model_final: escalate ? "queue" : finalModel, agree,
      status: escalate ? "escalated" : "active",
      drafts: escalate ? { a: it, b: mate, diff: bad } : null,
    });
  }

  const saved = items.filter((x) => norm(x.question).length >= 5);
  if (saved.some((x) => x.status === "escalated"))
    await sb.storage.from("corpus").copy(pg.storage_path, `esc/${job.doc_id}/p${pg.page}.jpg`).catch(() => {});
  if (saved.length)
    await sb.from("corpus_items").upsert(saved, { onConflict: "content_key", ignoreDuplicates: true });
  if (runs.length) await sb.from("transcribe_runs").insert(runs);
  const byCk = {};
  for (const x of saved) { byCk[x.cluster_key] = byCk[x.cluster_key] || { n: 0, a: 0 }; byCk[x.cluster_key].n++; if (x.agree) byCk[x.cluster_key].a++; }
  for (const [ck, v] of Object.entries(byCk)) {
    const { data: cur } = await sb.from("transcribe_routing").select("*").eq("cluster_key", ck).maybeSingle();
    await sb.from("transcribe_routing").upsert({
      cluster_key: ck, primary_model: cur?.primary_model || PRIMARY, state: cur?.state || "dual",
      sample_n: (cur?.sample_n || 0) + v.n, agree_n: (cur?.agree_n || 0) + v.a,
      last_check: new Date().toISOString(), updated_at: new Date().toISOString(),
    });
  }
  return { saved: saved.length, arbitrated: arb };
}

async function cleanupJobFiles(sb, jobId) {
  const { data: list } = await sb.storage.from("corpus").list(`jobs/${jobId}`, { limit: 200 });
  if (list?.length) await sb.storage.from("corpus").remove(list.map((f) => `jobs/${jobId}/${f.name}`));
}

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });
  const start = Date.now();
  try {
    const url = process.env.SUPABASE_URL || process.env.VITE_SUPABASE_URL;
    const svc = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY;
    const sb = createClient(url, svc);
    const { job_id, secret } = req.body || {};
    if (!job_id) return res.status(400).json({ error: "job_id 필요" });

    // ---- 인증: 관리자 세션(화면 킥·워치독) 또는 내부 시크릿(이어달리기)
    const internal = secret && secret === svc.slice(-24);
    if (!internal) {
      const token = (req.headers.authorization || "").replace(/^Bearer\s+/i, "");
      const { data: { user } = {} } = await sb.auth.getUser(token);
      if (!user) return res.status(401).json({ error: "로그인이 필요합니다" });
      const { data: prof } = await sb.from("profiles").select("role").eq("id", user.id).single();
      if (prof?.role !== "admin") return res.status(403).json({ error: "관리자 전용" });
    }

    const { data: job } = await sb.from("transcribe_jobs").select("*").eq("id", job_id).single();
    if (!job) return res.status(404).json({ error: "작업 없음" });
    if (job.status !== "running") { await cleanupJobFiles(sb, job_id); return res.status(200).json({ ok: true, done: true, status: job.status }); }

    // ---- 개념 지도 1회 로드
    let cq = sb.from("concepts").select("id,unit_id,title").order("unit_id").order("sort_order");
    if (job.unit_hint) cq = cq.like("id", job.unit_hint.slice(0, 2) + "%");
    const { data: cons } = await cq;
    const known = new Set((cons || []).map((c) => c.id));
    const sys = buildSys((cons || []).map((c) => `${c.id} ${c.title}`).join("\n"));

    // ---- 시간 예산 안에서 페이지 연속 처리
    let did = 0;
    while (Date.now() - start < BUDGET_MS) {
      const { data: claimed } = await sb.rpc("claim_job_page", { p_job: job_id });
      const pg = claimed?.[0];
      if (!pg) break;
      try {
        const r = await transcribeOne(sb, job, pg, sys, known);
        await sb.from("transcribe_job_pages").update({ status: "done", saved: r.saved, arbitrated: r.arbitrated, updated_at: new Date().toISOString() }).eq("id", pg.id);
      } catch (e) {
        if (RETRYABLE(e)) {
          await sb.from("transcribe_job_pages").update({ status: "pending", updated_at: new Date().toISOString() }).eq("id", pg.id);
          return res.status(200).json({ ok: true, paused: true, reason: String(e.message || e).slice(0, 120) });
        }
        await sb.from("transcribe_job_pages").update({ status: "error", error: String(e.message || e).slice(0, 300), updated_at: new Date().toISOString() }).eq("id", pg.id);
      }
      did++;
      await sb.from("transcribe_jobs").update({ updated_at: new Date().toISOString() }).eq("id", job_id);
      const { data: j2 } = await sb.from("transcribe_jobs").select("status").eq("id", job_id).single();
      if (j2?.status !== "running") { await cleanupJobFiles(sb, job_id); return res.status(200).json({ ok: true, done: true, status: j2?.status }); }
    }

    // ---- 남은 페이지 확인 → 이어달리기 or 마감
    const { count: left } = await sb.from("transcribe_job_pages")
      .select("id", { count: "exact", head: true }).eq("job_id", job_id).eq("status", "pending");
    if (!left) {
      const { count: doing } = await sb.from("transcribe_job_pages")
        .select("id", { count: "exact", head: true }).eq("job_id", job_id).eq("status", "doing");
      if (!doing) {
        await sb.from("transcribe_jobs").update({ status: "done", updated_at: new Date().toISOString() }).eq("id", job_id).eq("status", "running");
        await cleanupJobFiles(sb, job_id);
      }
      return res.status(200).json({ ok: true, done: !doing, processed: did });
    }
    // 자기 자신 재점화 (응답 전 발사)
    const self = `https://${req.headers.host}/api/transcribeJob`;
    fetch(self, { method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ job_id, secret: svc.slice(-24) }) }).catch(() => {});
    await new Promise((r) => setTimeout(r, 400));
    return res.status(200).json({ ok: true, done: false, processed: did, left });
  } catch (e) {
    return res.status(500).json({ error: String(e.message || e) });
  }
}
