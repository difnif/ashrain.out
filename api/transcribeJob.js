// ashrain.out — 전사 작업 러너 v2.0 (api/transcribeJob.js / MathIR·도형DSL 스펙 v1.1 구현)
// 개편 핵심: 심판이 모델(이중 전사·중재)에서 기계(mathir 파서·대입 검산)로.
//   페이지당 하이쿠 1회 → V-01~05·09 검증 → 실패 문항만 오류 피드백 재시도 1회
//   → 답 있는 문항은 대입 검산(V-03) → 답 없는 문항 15% 표본 이중(소넷, IR 정규화 diff)
//   → 페이지 소진 후 같은 체인에서 텍스트 배치 분류(개념 지도, 이미지 없음)
//   → 최종 실패·표본 불일치는 arb_mode 따라 오푸스 1회(api) 또는 상위 대기(queue).
// 화면·수동 큐·내보내기·반영은 v3.2 그대로 호환 (escalated + drafts).

import { createClient } from "@supabase/supabase-js";
import { parseText, parseAnswer, checkEquationAnswer, checkFigure } from "../src/lib/mathir.js";

export const config = { maxDuration: 60 };

const MODELS = {
  haiku: "claude-haiku-4-5-20251001",
  sonnet: "claude-sonnet-4-6",
  opus: "claude-opus-4-8",
  fable: "claude-fable-5",
};
const PRIMARY = process.env.TRANSCRIBE_PRIMARY || "haiku";
const SAMPLER = process.env.TRANSCRIBE_SAMPLER || "sonnet";
const ARBITER = process.env.TRANSCRIBE_ARBITER || "opus";
const SAMPLE_RATE = Number(process.env.TRANSCRIBE_SAMPLE || 15);   // 답 없는 문항 표본 %
const OPUS_GATE = Number(process.env.TRANSCRIBE_OPUS_GATE || 45);  // 정답률 이 값 이하(어려움)만 오푸스 중재
const BUDGET_MS = 38000;
const CLS_BATCH = 20;

// ---------------------------------------------------------------- 프롬프트
const SYS_T = `너는 수학 문제지 전사기다. 이미지 속 문항을 JSON 배열로만 출력한다. 배열 밖 텍스트 금지.
각 문항: {"seq":문항번호, "qtype":"choice|short|proof|essay", "question":"...", "choices":[...]|null,
"answer":"...(지면에 없으면 null)", "difficulty_est":1~5, "has_figure":true|false, "figure":[도형함수]|null}

■ 수식 표기 — MathIR 닫힌 문법 (이 목록 밖 토큰 금지)
- 문장 속 수식은 [[ ... ]]로 감싸고 그 안은 MathIR만. 단순 숫자·단위(3 cm, 40개)는 평문.
- 기본: 숫자, 변수(x,a,...), + - * / = != < > <= >=, 괄호, 병치곱(2x, 3(x+1)). 유니코드 수식문자·LaTeX 금지.
- 함수: frac(a,b) mixed(w,a,b) pow(b,e) sqrt(x) root(n,x) abs(x) recdec(pre,rep) floor(x) fact(n)
  max min ratio(a,b[,c]) pct(x) deg(x) dms(d,m[,s]) pm | seg line ray arc angle tri quad par perp cong sim
  point(x,y) point3 vec vcomp dot | set setb in notin subset nsubset union inter comp card imp iff neg itv(a,b,cc|co|oc|oo) conj
  | log([b,]x) ln sin cos tan csc sec cot | sub(a,n) sum(k,a,b,f) lim(x,a,f[,+|-]) prime(f[,2]) dydx integ dinteg(a,b,f,x) inv
  | perm comb pperm hcomb prob cprob ev var sd binomd normald | 상수 pi e i inf empty
- answer는 마커 없이 IR 하나("x = 8", "frac(3,4)") 또는 한국어 낱말("소수").
예: "일차방정식 [[frac(x,2) - 3 = frac(x,4) - 1]] 을 푸시오."  /  answer: "x = 8"

■ figure — 도형은 자유 서술 금지, 함수 호출 배열만:
numline{min,max,points} coordplane{x,y,points,lines} table{head,rows} hist{bins,counts} stemleaf{stems}
crossing{angles} parallel{angles} tri{v,sides,angles,marks} rect{w,h} polygon{n} circle{r} sector{r,angle}
solid{kind} net{kind} boxplot{values} scatter{points} venn{sets} tree{levels} funcgraph{expr} unitcircle
conic{kind} vecfig{vectors} space normcurve{m,v} — 표현 불가하면 {"fn":"unsupported","args":{"raw":"짧은 서술"}}
인자 속 수치·식도 MathIR 문자열.
원문 그대로 옮기되(오탈자 포함) 머리말·페이지번호·배점 표기([3점], 4점 등)는 무시.
자주 틀리는 치환 — 반드시 이렇게: √x→sqrt(x), ³√x→root(3,x), Σ→sum(...), π→pi, ×→*, ÷→/, ≤→<=, ≥→>=, ≠!=, x²→pow(x,2), 순환마디 표기→recdec. 유니코드 수학기호가 하나라도 남으면 실패다.
행렬은 mat(행,열, 성분을 행 우선 나열): [[A = mat(2,2, 1,2, 3,4)]]. (i,j) 성분 기호는 sub(a,i,j). 세미콜론·괄호 나열식 행렬 표기 금지. ±는 pm(a,b) 또는 pm(a). JSON 문자열 안 백슬래시는 \\\\ 이스케이프.

■ 페이지 종류
- 문항이 실린 문제지 페이지 → 위 규격의 문항 배열.
- 답만 표·나열로 모인 "답지" 페이지 → 배열 대신 {"answer_sheet":{"1":"x = 3","2":"frac(1,2)"}} 단일 객체 (번호→답, 답은 MathIR).
- 풀이 과정 서술 중심의 "해설" 페이지 → 빈 배열 [].`;

const sysClassify = (cmap) => `너는 수학 문항 분류기다. 입력된 문항들을 아래 개념 목록으로 분류해 JSON 배열로만 출력한다.
각 항목: {"id":"입력의 id 그대로", "unit_id":"단원(예 m1-1)", "concept_main":"주개념 cid 1개",
"concept_subs":["부개념 cid 0~2개"], "pattern_tags":["풀이 유형 태그 1~3개"], "confidence":0~1}
규칙: 주개념 = 문항이 궁극적으로 평가하는 개념 하나. 부개념 = 풀이에 실제 동원되는 개념(그 개념을 몰라도 풀리면 제외).
cid는 반드시 목록에 있는 것만. 애매하면 confidence를 낮춰라.
[개념 목록]
${cmap}`;

// ---------------------------------------------------------------- 공용
async function callModel(modelKey, sys, content, maxTokens = 4000) {
  const _t0 = Date.now();
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "content-type": "application/json", "x-api-key": process.env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01" },
    body: JSON.stringify({ model: MODELS[modelKey] || modelKey, max_tokens: maxTokens,
      system: [{ type: "text", text: sys, cache_control: { type: "ephemeral" } }],
      messages: [{ role: "user", content }] }),
  });
  const j = await r.json();
  if (!r.ok) { const e = new Error(j?.error?.message || "anthropic " + r.status); e.status = r.status; throw e; }
  return { text: (j.content || []).map((b) => b.text || "").join(""), usage: j.usage || {}, ms: Date.now() - _t0, model: modelKey };
}
const CHAIN = Math.random().toString(36).slice(2, 8);      // 이 인보케이션(체인) 식별자
function mkTracer() {
  const rows = [];
  return {
    add(step, x = {}) { rows.push({ step, ...x }); },
    ai(step, r, ok = true, note = null) { rows.push({ step, model: r.model, ms: r.ms, ok, note,
      in_tok: r.usage?.input_tokens ?? null, out_tok: r.usage?.output_tokens ?? null,
      cache_r: r.usage?.cache_read_input_tokens ?? null, cache_w: r.usage?.cache_creation_input_tokens ?? null }); },
    async flush(sb, jobId, page) {
      if (!rows.length) return;
      const payload = rows.map((r, i) => ({ job_id: jobId, page, chain: CHAIN, seq_no: i, step: r.step,
        model: r.model || null, ms: r.ms ?? null, in_tok: r.in_tok ?? null, out_tok: r.out_tok ?? null,
        cache_r: r.cache_r ?? null, cache_w: r.cache_w ?? null, ok: r.ok ?? null, note: r.note || null }));
      rows.length = 0;
      try { await sb.from("transcribe_traces").insert(payload); } catch { /* 계측 실패는 작업을 막지 않음 */ }
    },
  };
}
const RETRYABLE = (e) => [429, 500, 529].includes(e?.status) || /credit balance|overloaded|rate.?limit/i.test(String(e?.message || ""));
const parseArr = (t) => { const m = t.match(/\[[\s\S]*\]/); if (!m) return null; try { const a = JSON.parse(m[0]); return Array.isArray(a) ? a : null; } catch { return null; } };
const parseObj = (t) => { const m = t.match(/\{[\s\S]*\}/); if (!m) return null; try { return JSON.parse(m[0]); } catch { return null; } };
const norm = (s) => (s || "").toString().replace(/\s+/g, " ").trim();
const normUnit = (u) => { const m = String(u || "").match(/^[mh]\d-\d/); return m ? m[0] : ""; };

function hashStr(s) { let h = 0; for (let i = 0; i < s.length; i++) { h = (h * 31 + s.charCodeAt(i)) | 0; } return Math.abs(h); }

// ---------------------------------------------------------------- 기계 심판 (V-01~05·09)
export function verifyItem(it, gradeHint) {
  const errs = [];
  const q = parseText(String(it.question || ""), gradeHint || null);
  errs.push(...q.errs.map((e) => ({ ...e, at: "question" })));
  for (const [i, c] of (it.choices || []).entries()) {
    const r = parseText(String(c));
    errs.push(...r.errs.map((e) => ({ ...e, at: `choice${i + 1}` })));
  }
  if (it.answer != null && String(it.answer).trim()) {
    try { parseAnswer(String(it.answer)); }
    catch (e) { errs.push({ code: e.code || "V-01", at: "answer", src: String(it.answer), msg: String(e.message || e) }); }
  }
  errs.push(...checkFigure(it.figure || []).map((e) => ({ ...e, at: "figure" })));
  let solved = null;                                    // V-03 대입 검산
  if (!errs.length && it.answer != null && String(it.answer).trim()) {
    solved = checkEquationAnswer(String(it.question || ""), String(it.answer));
    if (solved === false) errs.push({ code: "V-03", at: "answer", msg: "답 대입 불일치" });
  }
  return { errs, solved };
}

function irKey(it) {                                    // 표기 변이를 제거한 비교 키
  const seg = (s) => parseText(String(s || "")).segs.map((x) => (x.kind === "ir" ? "⟨" + x.ir + "⟩" : norm(x.raw))).join("");
  return [seg(it.question), (it.choices || []).map(seg).join("|"), norm(it.answer), it.qtype || ""].join("‖");
}

// ---------------------------------------------------------------- 페이지 전사
async function transcribeOne(sb, job, pg, tr = mkTracer()) {
  const _td = Date.now();
  const { data: blob, error: dl } = await sb.storage.from("corpus").download(pg.storage_path);
  if (dl) throw new Error("이미지 다운로드 실패: " + dl.message);
  tr.add("download", { ms: Date.now() - _td });
  const b64 = Buffer.from(await blob.arrayBuffer()).toString("base64");
  const img = { type: "image", source: { type: "base64", media_type: "image/jpeg", data: b64 } };
  const ask = [img, { type: "text", text: pg.meta?.kind === "answers"
    ? "이 페이지는 답지다. answer_sheet 형식으로만 출력해라."
    : "이 페이지의 문항을 전사해라." }];

  const r1 = await callModel(PRIMARY, SYS_T, ask);
  tr.ai(pg.meta?.kind === "answers" ? "answer_sheet" : "primary", r1);
  const t1 = r1.text;
  const sheet = parseObj(t1);
  if (sheet && sheet.answer_sheet && !Array.isArray(sheet)) {           // ── 답지 페이지
    const clean = {};
    for (const [k, v] of Object.entries(sheet.answer_sheet)) {
      try { parseAnswer(String(v)); clean[String(k)] = String(v); } catch { /* 문법 위반 답은 버림 */ }
    }
    if (Object.keys(clean).length) {
      const { data: d0 } = await sb.from("corpus_docs").select("answers").eq("id", job.doc_id).single();
      await sb.from("corpus_docs").update({ answers: { ...(d0?.answers || {}), ...clean } }).eq("id", job.doc_id);
    }
    await sb.from("transcribe_runs").insert([{ doc_id: job.doc_id, page: pg.page, seq: 0, role: "answer_sheet", model: PRIMARY, agree: true, diff_fields: [], adopted: true }]);
    return { saved: 0, arbitrated: 0 };
  }
  const p1 = parseArr(t1);
  if (!p1) throw new Error("1차 전사 JSON 파싱 실패");

  const items = [], runs = [];
  let arb = 0;
  for (const raw of p1) {
    let it = raw, model = PRIMARY, escal = false, escErrs = null;
    let v = verifyItem(it, job.unit_hint);

    if (v.errs.length) {                                // ── 오류 피드백 재시도 1회 (같은 모델)
      const fb = v.errs.slice(0, 6).map((e) => `${e.code}@${e.at}${e.src ? ` [[${e.src}]]` : ""}: ${e.msg || ""}`).join("\n");
      try {
        const rr = await callModel(PRIMARY, SYS_T, [img, { type: "text",
          text: `문항 ${it.seq}번만 다시 전사해 "단일 객체"로 출력해라. 이전 시도의 문법 오류:\n${fb}\n이전 시도: ${JSON.stringify(it)}` }], 1800);
        tr.ai("retry", rr, true, `errs:${v.errs.length}`);
        const fixed = parseObj(rr.text);
        if (fixed) { it = fixed; model = PRIMARY + "+retry"; v = verifyItem(it, job.unit_hint); }
      } catch (e) { if (RETRYABLE(e)) throw e; }
      runs.push({ doc_id: job.doc_id, page: pg.page, seq: raw.seq, role: "retry", model: PRIMARY, agree: !v.errs.length, diff_fields: v.errs.map((x) => x.code), adopted: !v.errs.length });
    }

    let needArb = v.errs.length > 0;
    if (!needArb && !pg.meta                                                  // ── 표본 감시 (답 없는 문항; 파서 입고분은 답 백필+검산이 전수 검증하므로 생략)
        && (it.answer == null || !String(it.answer).trim())
        && hashStr(`${job.doc_id}|${pg.page}|${it.seq}`) % 100 < SAMPLE_RATE) {
      try {
        const rs = await callModel(SAMPLER, SYS_T, ask);
        tr.ai("sample", rs);
        const p2 = parseArr(rs.text);
        const mate = (p2 || []).find((x) => x.seq === it.seq);
        const same = mate && irKey(mate) === irKey(it);
        runs.push({ doc_id: job.doc_id, page: pg.page, seq: it.seq, role: "sample", model: SAMPLER, agree: !!same, diff_fields: same ? [] : ["ir"], adopted: false });
        if (mate && !same) needArb = true;
      } catch (e) { if (RETRYABLE(e)) throw e; }
    }

    if (needArb) {                                      // ── 최종 실패·표본 불일치
      arb++;
      if ((job.arb_mode || "api") === "queue") { escal = true; escErrs = v.errs.map((x) => x.code); }
      else {
        // ── 중재 사다리: 소넷(저비용 구조대) → 오푸스(어려운 문항만, 정답률 게이트)
        const arbAsk = (why) => [img, { type: "text",
          text: `문항 ${it.seq}번만 본다. 아래 시도가 검증에 실패했다(${why}). 이미지를 근거로 올바른 전사를 같은 규격의 "단일 객체"로 출력해라.\n시도: ${JSON.stringify(it)}` }];
        const why0 = v.errs.map((x) => x.code).join(",") || "표본 불일치";
        let rescued = false;
        try {
          const rs2 = await callModel(SAMPLER, SYS_T, arbAsk(why0), 1800);
          tr.ai("arbiter", rs2);
          const fx = parseObj(rs2.text);
          if (fx) {
            const v2 = verifyItem(fx, job.unit_hint);
            if (!v2.errs.length) { it = fx; model = SAMPLER; v = v2; rescued = true; escErrs = null; }
            else escErrs = v2.errs.map((x) => x.code);
          } else escErrs = ["parse"];
        } catch (e) { if (RETRYABLE(e)) throw e; escErrs = ["api"]; }
        runs.push({ doc_id: job.doc_id, page: pg.page, seq: it.seq, role: "arbiter", model: SAMPLER, agree: rescued, diff_fields: rescued ? [] : (escErrs || []), adopted: rescued });
        const pc = pg.meta?.p_correct;
        const hard = pc == null ? true : Number(pc) <= OPUS_GATE;
        if (!rescued && hard) {
          try {
            const ra = await callModel(ARBITER, SYS_T, arbAsk((escErrs || []).join(",") || why0), 1800);
            tr.ai("arbiter2", ra);
            const fixed = parseObj(ra.text);
            if (fixed) {
              const v3 = verifyItem(fixed, job.unit_hint);
              if (!v3.errs.length) { it = fixed; model = ARBITER; v = v3; rescued = true; escErrs = null; }
              else escErrs = v3.errs.map((x) => x.code);
            } else escErrs = ["parse"];
          } catch (e) { if (RETRYABLE(e)) throw e; escErrs = ["api"]; }
          runs.push({ doc_id: job.doc_id, page: pg.page, seq: it.seq, role: "arbiter", model: ARBITER, agree: rescued, diff_fields: rescued ? [] : (escErrs || []), adopted: rescued });
        }
        if (!rescued) escal = true;
      }
    }
    runs.push({ doc_id: job.doc_id, page: pg.page, seq: raw.seq, role: "primary", model: PRIMARY, agree: !v.errs.length && !escal, diff_fields: v.errs.map((x) => x.code), adopted: !escal });

    const hasMath = /\[\[/.test(String(it.question || "")) || (it.choices || []).some((c) => /\[\[/.test(String(c)));
    items.push({
      doc_id: job.doc_id, page: pg.page,
      seq: pg.meta ? pg.page : (it.seq ?? raw.seq),
      p_correct: pg.meta?.p_correct ?? null,
      src_tags: pg.meta?.src_tag ? [pg.meta.src_tag] : [],
      unit_id: normUnit(job.unit_hint) || null,
      qtype: it.qtype || "short", question: String(it.question || ""),
      choices: it.choices || null, answer: it.answer ?? null,
      difficulty_est: it.difficulty_est ?? null,
      has_math: hasMath, has_figure: !!(it.figure && it.figure.length),
      figure: it.figure || null, cluster_key: null,
      model_final: escal ? "queue" : model, agree: !escal && !v.errs.length,
      status: escal ? "escalated" : "active",
      drafts: escal ? { a: it, b: null, diff: escErrs || [] } : null,
      concept_main: null, concept_subs: [], concept_ids: [], pattern_tags: [],
      confidence: escal ? 0 : null,
    });
  }

  const saved = items.filter((x) => norm(x.question).length >= 5);
  if (saved.some((x) => x.status === "escalated"))
    await sb.storage.from("corpus").copy(pg.storage_path, `esc/${job.doc_id}/p${pg.page}.jpg`).catch(() => {});
  const _ts = Date.now();
  if (saved.length) await sb.from("corpus_items").upsert(saved, { onConflict: "content_key", ignoreDuplicates: true });
  if (runs.length) await sb.from("transcribe_runs").insert(runs);
  tr.add("save", { ms: Date.now() - _ts, note: `items:${saved.length} arb:${arb}` });
  return { saved: saved.length, arbitrated: arb };
}

// ---------------------------------------------------------------- 배치 분류 (텍스트만)
async function classifyBatch(sb, job, known, cmapSys) {
  const { data: rows } = await sb.from("corpus_items")
    .select("id,question,choices,answer")
    .eq("doc_id", job.doc_id).eq("status", "active").is("concept_main", null)
    .is("cluster_key", null)                       // 시도 흔적 없는 문항만 — 재시도 루프 원천 차단
    .order("page").limit(CLS_BATCH);
  if (!rows?.length) return 0;
  const payload = rows.map((r) => ({
    id: r.id,
    text: (r.question || "") + ((r.choices || []).length ? "\n보기: " + r.choices.join(" / ") : "") + (r.answer ? "\n답: " + r.answer : ""),
  }));
  const rc = await callModel(PRIMARY, cmapSys,
    [{ type: "text", text: "다음 문항들을 분류해라.\n" + JSON.stringify(payload) }], 2500);
  try { await sb.from("transcribe_traces").insert([{ job_id: job.id, page: 0, chain: CHAIN, seq_no: 0, step: "classify",
    model: rc.model, ms: rc.ms, in_tok: rc.usage?.input_tokens ?? null, out_tok: rc.usage?.output_tokens ?? null,
    cache_r: rc.usage?.cache_read_input_tokens ?? null, cache_w: rc.usage?.cache_creation_input_tokens ?? null, ok: true }]); } catch {}
  const out = parseArr(rc.text);
  const byId = new Map((out || []).map((x) => [x.id, x]));
  for (const r of rows) {
    const c = byId.get(r.id) || {};
    const cm = known.has(c.concept_main) ? c.concept_main : null;
    const subs = (c.concept_subs || []).filter((x) => known.has(x) && x !== cm).slice(0, 2);
    await sb.from("corpus_items").update({
      unit_id: normUnit(c.unit_id) || (cm ? normUnit(cm) : normUnit(job.unit_hint)) || null,
      concept_main: cm, concept_subs: subs, concept_ids: [cm, ...subs].filter(Boolean),
      pattern_tags: (c.pattern_tags || []).slice(0, 3),
      confidence: cm ? (c.confidence ?? null) : 0,
      cluster_key: `${normUnit(c.unit_id) || normUnit(cm) || "?"}|cls`,
    }).eq("id", r.id);
  }
  return rows.length;
}

// ---------------------------------------------------------------- 핸들러 (클레임 루프 + 이어달리기)
export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });
  const start = Date.now();
  try {
    const url = process.env.SUPABASE_URL || process.env.VITE_SUPABASE_URL;
    const svc = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY;
    const sb = createClient(url, svc);
    const { job_id, secret } = req.body || {};
    if (!job_id) return res.status(400).json({ error: "job_id 필요" });

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
    if (job.status !== "running") {
      const { data: list } = await sb.storage.from("corpus").list(`jobs/${job_id}`, { limit: 200 });
      if (list?.length) await sb.storage.from("corpus").remove(list.map((f) => `jobs/${job_id}/${f.name}`));
      return res.status(200).json({ ok: true, done: true, status: job.status });
    }

    // ── 로컬 작업 가드: 페이지가 남아 있으면 로컬 워커 몫 — 클라우드는 손대지 않음
    if (job.runner === "local") {
      const { count: lp } = await sb.from("transcribe_job_pages")
        .select("id", { count: "exact", head: true }).eq("job_id", job_id).eq("status", "pending");
      const { count: ld } = await sb.from("transcribe_job_pages")
        .select("id", { count: "exact", head: true }).eq("job_id", job_id).eq("status", "doing");
      if (lp || ld) return res.status(200).json({ ok: true, local: true, left: lp });
      // 페이지 소진 → 아래 분류·마감 단계로 진행
    }

    // ── 고아 회수: 3분 넘게 doing인 페이지는 죽은 체인의 잔재 — pending으로 되살림 (재배포·타임아웃 내성)
    await sb.from("transcribe_job_pages")
      .update({ status: "pending", updated_at: new Date().toISOString() })
      .eq("job_id", job_id).eq("status", "doing")
      .lt("updated_at", new Date(Date.now() - 180000).toISOString());

    // ── 1단계: 페이지 전사
    let did = 0;
    while (Date.now() - start < BUDGET_MS) {
      const { data: claimed } = await sb.rpc("claim_job_page", { p_job: job_id });
      const pg = claimed?.[0];
      if (!pg) break;
      const tr = mkTracer();
      try {
        const r = await transcribeOne(sb, job, pg, tr);
        await sb.from("transcribe_job_pages").update({ status: "done", saved: r.saved, arbitrated: r.arbitrated, updated_at: new Date().toISOString() }).eq("id", pg.id);
      } catch (e) {
        tr.add("page_error", { ok: false, note: String(e.message || e).slice(0, 80) });
        if (RETRYABLE(e)) {
          await sb.from("transcribe_job_pages").update({ status: "pending", updated_at: new Date().toISOString() }).eq("id", pg.id);
          await tr.flush(sb, job_id, pg.page);
          return res.status(200).json({ ok: true, paused: true, reason: String(e.message || e).slice(0, 120) });
        }
        await sb.from("transcribe_job_pages").update({ status: "error", error: String(e.message || e).slice(0, 300), updated_at: new Date().toISOString() }).eq("id", pg.id);
      }
      await tr.flush(sb, job_id, pg.page);
      did++;
      await sb.from("transcribe_jobs").update({ updated_at: new Date().toISOString() }).eq("id", job_id);
      const { data: j2 } = await sb.from("transcribe_jobs").select("status").eq("id", job_id).single();
      if (j2?.status !== "running") return res.status(200).json({ ok: true, done: true, status: j2?.status });
    }

    const { count: left } = await sb.from("transcribe_job_pages")
      .select("id", { count: "exact", head: true }).eq("job_id", job_id).eq("status", "pending");
    const { count: doing } = await sb.from("transcribe_job_pages")
      .select("id", { count: "exact", head: true }).eq("job_id", job_id).eq("status", "doing");

    // ── 2단계: 페이지 소진 후 배치 분류
    let classified = 0;
    if (!left && !doing) {
      const { data: dr } = await sb.from("corpus_docs").select("answers").eq("id", job.doc_id).single();
      const amap = dr?.answers || {};
      if (Object.keys(amap).length) {
        const { data: nulls } = await sb.from("corpus_items").select("id,seq,question")
          .eq("doc_id", job.doc_id).eq("status", "active").is("answer", null).limit(500);
        for (const r of nulls || []) {
          const a = amap[String(r.seq)];
          if (!a) continue;
          if (checkEquationAnswer(String(r.question || ""), a) === false) continue;   // 검산 불일치면 미기입
          await sb.from("corpus_items").update({ answer: a }).eq("id", r.id);
        }
      }
      let cq = sb.from("concepts").select("id,unit_id,title").order("unit_id").order("sort_order");
      if (job.unit_hint) cq = cq.like("id", job.unit_hint.slice(0, 2) + "%");
      const { data: cons } = await cq;
      const known = new Set((cons || []).map((c) => c.id));
      const cmapSys = sysClassify((cons || []).map((c) => `${c.id} ${c.title}`).join("\n"));
      while (Date.now() - start < BUDGET_MS) {
        let n = 0;
        try { n = await classifyBatch(sb, job, known, cmapSys); }
        catch (e) {
          if (RETRYABLE(e)) return res.status(200).json({ ok: true, paused: true, reason: String(e.message || e).slice(0, 120) });
          await sb.from("transcribe_jobs").update({ status: "done", updated_at: new Date().toISOString() }).eq("id", job_id).eq("status", "running");
          return res.status(200).json({ ok: true, done: true, processed: did, classified, note: "classify 오류 — 잔여는 분류불확실로 마감" });
        }
        classified += n;
        await sb.from("transcribe_jobs").update({ updated_at: new Date().toISOString() }).eq("id", job_id);
        if (n < CLS_BATCH) {
          await sb.from("transcribe_jobs").update({ status: "done", updated_at: new Date().toISOString() }).eq("id", job_id).eq("status", "running");
          const { data: list } = await sb.storage.from("corpus").list(`jobs/${job_id}`, { limit: 200 });
          if (list?.length) await sb.storage.from("corpus").remove(list.map((f) => `jobs/${job_id}/${f.name}`));
          return res.status(200).json({ ok: true, done: true, processed: did, classified });
        }
      }
    }

    // ── 이어달리기
    const self = `https://${req.headers.host}/api/transcribeJob`;
    fetch(self, { method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ job_id, secret: svc.slice(-24) }) }).catch(() => {});
    await new Promise((r) => setTimeout(r, 400));
    return res.status(200).json({ ok: true, done: false, processed: did, classified, left });
  } catch (e) {
    return res.status(500).json({ error: String(e.message || e) });
  }
}
