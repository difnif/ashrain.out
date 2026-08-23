// ashrain.out — 자료 전사 API (api/transcribeCorpus.js, v2.0 — 자동 분류)
// 페이지 이미지 1장: 1차·2차 모델 독립 전사(+단원·개념 자동 판정) → 필드 diff(분류 포함)
// → 불일치 문항만 상위 모델 중재 → corpus_items 자동 채택 + 로그 + 라우팅 통계.
// unit_hint는 선택 — 주면 해당 학년 개념 지도만 프롬프트에 실어 토큰 절약·정확도 향상.
// 환경변수: 기존 재사용 — ANTHROPIC_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY(또는 SUPABASE_SERVICE_KEY)

import { createClient } from "@supabase/supabase-js";

const MODELS = {
  haiku: "claude-haiku-4-5-20251001",
  sonnet: "claude-sonnet-4-6",
  opus: "claude-opus-4-8",
  fable: "claude-fable-5",
};
const PRIMARY = process.env.TRANSCRIBE_PRIMARY || "haiku";
const SECONDARY = process.env.TRANSCRIBE_SECONDARY || "sonnet";
const ARBITER = process.env.TRANSCRIBE_ARBITER || "opus";

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
    body: JSON.stringify({
      model: MODELS[modelKey] || modelKey,
      max_tokens: maxTokens,
      system: sys,
      messages: [{ role: "user", content }],
    }),
  });
  const j = await r.json();
  if (!r.ok) throw new Error(j?.error?.message || "anthropic " + r.status);
  return (j.content || []).map((b) => b.text || "").join("");
}

function parseItems(text) {
  const m = text.match(/\[[\s\S]*\]/);
  if (!m) return null;
  try { const a = JSON.parse(m[0]); return Array.isArray(a) ? a : null; } catch { return null; }
}

const norm = (s) => (s || "").toString().replace(/\s+/g, " ").trim();

function sim(a, b) {
  a = norm(a); b = norm(b);
  if (a === b) return 1;
  if (a.length < 2 || b.length < 2) return 0;
  const grams = (s) => { const g = new Map();
    for (let i = 0; i < s.length - 1; i++) { const k = s.slice(i, i + 2); g.set(k, (g.get(k) || 0) + 1); }
    return g; };
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
  const pc = (p.choices || []).map(norm).join("|"), sc = (s.choices || []).map(norm).join("|");
  if (pc !== sc) bad.push("choices");
  if ((p.qtype || "") !== (s.qtype || "")) bad.push("qtype");
  if (!!p.has_figure !== !!s.has_figure) bad.push("has_figure");
  if ((p.unit_id || "") !== (s.unit_id || "")) bad.push("unit");
  if ((p.concept_main || "") !== (s.concept_main || "")) bad.push("classify");
  return bad;
}

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });
  try {
    const url = process.env.SUPABASE_URL || process.env.VITE_SUPABASE_URL;
    const svc = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY;
    const sb = createClient(url, svc);

    // ---- 관리자 확인
    const token = (req.headers.authorization || "").replace(/^Bearer\s+/i, "");
    const { data: { user } = {} } = await sb.auth.getUser(token);
    if (!user) return res.status(401).json({ error: "로그인이 필요합니다" });
    const { data: prof } = await sb.from("profiles").select("role").eq("id", user.id).single();
    if (prof?.role !== "admin") return res.status(403).json({ error: "관리자 전용" });

    const { doc_id, page, image, unit_hint } = req.body || {};
    if (!image) return res.status(400).json({ error: "image(dataURL) 필요" });

    // ---- 개념 지도 (힌트 있으면 같은 학년만)
    let cq = sb.from("concepts").select("id,unit_id,title").order("unit_id").order("sort_order");
    if (unit_hint) cq = cq.like("id", unit_hint.slice(0, 2) + "%");
    const { data: cons } = await cq;
    const known = new Set((cons || []).map((c) => c.id));
    const sys = buildSys((cons || []).map((c) => `${c.id} ${c.title}`).join("\n"));

    const b64 = image.replace(/^data:image\/\w+;base64,/, "");
    const media = (image.match(/^data:(image\/\w+);/) || [])[1] || "image/jpeg";
    const imgBlock = { type: "image", source: { type: "base64", media_type: media, data: b64 } };
    const ask = [imgBlock, { type: "text", text: "이 페이지의 문항을 전사·분류해라." }];

    // ---- 1차·2차 독립 전사 (병렬)
    const [t1, t2] = await Promise.all([callModel(PRIMARY, sys, ask), callModel(SECONDARY, sys, ask)]);
    const p1 = parseItems(t1), p2 = parseItems(t2);
    if (!p1) return res.status(502).json({ error: "1차 전사 JSON 파싱 실패" });

    const items = [], runs = [];
    for (const it of p1) {
      const mate = (p2 || []).find((x) => x.seq === it.seq) || null;
      const bad = mate ? diffItem(it, mate) : ["no_secondary"];
      const agree = bad.length === 0;
      let finalIt = it, finalModel = PRIMARY;

      if (!agree) {
        const arbAsk = [imgBlock, { type: "text",
          text: `문항 ${it.seq}번만 본다. 두 전사가 불일치(${bad.join(",")}). 이미지를 근거로 올바른 전사·분류 하나를 같은 JSON 규격의 "단일 객체"로 출력해라.\nA안: ${JSON.stringify(it)}\nB안: ${JSON.stringify(mate)}` }];
        try {
          const ta = await callModel(ARBITER, sys, arbAsk, 1600);
          const m = ta.match(/\{[\s\S]*\}/);
          if (m) { finalIt = JSON.parse(m[0]); finalModel = ARBITER; }
        } catch { /* 중재 실패 시 1차안 유지 */ }
      }

      // 분류 검증 — 목록에 없는 cid는 환각으로 보고 제거
      const cMain = known.has(finalIt.concept_main) ? finalIt.concept_main : null;
      const cSubs = (finalIt.concept_subs || []).filter((x) => known.has(x) && x !== cMain).slice(0, 2);
      const unitJ = finalIt.unit_id || (cMain ? cMain.split("-").slice(0, 2).join("-") : unit_hint) || null;
      const ck = `${unitJ || "?"}|${finalIt.qtype || "?"}|m${finalIt.has_math ? 1 : 0}|f${finalIt.has_figure ? 1 : 0}`;

      if (!agree) runs.push({ doc_id, page, seq: it.seq, cluster_key: ck, role: "arbiter", model: ARBITER, agree: false, diff_fields: bad, adopted: true });
      runs.push({ doc_id, page, seq: it.seq, cluster_key: ck, role: "primary", model: PRIMARY, agree, diff_fields: bad, adopted: agree });
      if (mate) runs.push({ doc_id, page, seq: it.seq, cluster_key: ck, role: "secondary", model: SECONDARY, agree, diff_fields: bad, adopted: false });

      items.push({
        doc_id, page, seq: finalIt.seq ?? it.seq,
        unit_id: unitJ, concept_main: cMain, concept_subs: cSubs,
        concept_ids: [cMain, ...cSubs].filter(Boolean),
        pattern_tags: (finalIt.pattern_tags || []).slice(0, 3),
        confidence: cMain ? (finalIt.confidence ?? null) : 0,
        qtype: finalIt.qtype || "short", question: finalIt.question || "",
        choices: finalIt.choices || null, answer: finalIt.answer ?? null,
        difficulty_est: finalIt.difficulty_est ?? null,
        has_math: !!finalIt.has_math, has_figure: !!finalIt.has_figure,
        figure: finalIt.figure || null, cluster_key: ck,
        model_final: finalModel, agree,
      });
    }

    // ---- 저장(자동 채택) + 로그 + 라우팅 통계
    const saved = items.filter((x) => norm(x.question).length >= 5);
    if (saved.length) await sb.from("corpus_items").insert(saved);
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
    return res.status(200).json({
      ok: true, page, saved: saved.length,
      arbitrated: saved.filter((x) => !x.agree).length,
      unclassified: saved.filter((x) => !x.concept_main).length,
      items: saved,
    });
  } catch (e) {
    return res.status(500).json({ error: String(e.message || e) });
  }
}
