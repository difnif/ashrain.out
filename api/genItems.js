// ashrain.out — 테스트 문항 · 풀이 AI 생성 서버리스 (v1.0)
// 위치: 리포 "최상단" api/genItems.js  (genCalc.js 옆)
// 환경변수: ANTHROPIC_API_KEY (genCalc와 공유 — 이미 설정돼 있으면 추가 작업 없음)
import { createClient } from "@supabase/supabase-js";

const MODELS = {
  haiku: "claude-haiku-4-5-20251001",
  sonnet: "claude-sonnet-4-6",
  opus: "claude-opus-4-8",
  fable: "claude-fable-5",
};
const MAX_COUNT = 10;
const QTYPES = new Set(["choice", "short", "ox", "proof", "essay"]);

const TEST_DESC = {
  concept_set: "개념 묶음 테스트 — 지정한 개념들의 이해·적용을 확인하는 소형 테스트",
  unit: "단원 테스트 — 단원 전체를 아우르는 종합 평가",
  calc: "연산 테스트 — 신속·정확한 계산력 확인 (짧고 명확한 계산 문항)",
  sangwa: "산과(算科) 시험 — 과거 시험 모티브의 증명·서술형 평가 (proof/essay 중심, 논리 전개를 평가)",
  mock: "실전 모의고사 — 내신 대비 실전형 (학교 시험 스타일, 배점 다양)",
  ash: "Ash TEST — 애쉬레인 대표 최고난도 테스트 (경시 수준, 여러 개념 융합, 발상 필요)",
  rain: "Rain TEST — 난이도 하 대량 문항을 빠듯한 시간에 푸는 신속정확 테스트 (한 문항 8~30초)",
  out: "Out TEST — 학력 평가용 일제고사 (표준적 문항, 변별도 고른 분포)",
};

const MATH_UNI = `수식 표기(기본 규격 — 유니코드 전용):
- 곱셈 ×, 나눗셈 ÷, 음수·빼기 −(U+2212), 거듭제곱은 위첨자(x², 2³, aⁿ), 근호 √( ), 분수는 a/b, 파이 π, 각도 °, ≤ ≥ ≠ 사용.
- 백슬래시(\\)와 LaTeX 명령( \\frac 등 ) 절대 금지. 달러 기호($) 금지.`;
const MATH_TEX = `수식 표기(고급 규격 — 제한 LaTeX 허용):
- 간단한 식은 유니코드(×, ÷, −, x², √, π)로. 복잡한 식(중첩 분수, 시그마, 극한, 적분, 케이스)만 $...$ 안에 LaTeX로.
- 허용 명령: \\dfrac \\frac \\sqrt \\sum \\int \\lim \\to \\infty \\le \\ge \\ne \\pm \\times \\div \\cdot \\pi \\theta \\alpha \\beta \\overline \\vec \\begin{cases}…\\end{cases} \\left \\right, 첨자 ^ _.
- $는 반드시 짝으로. JSON 문자열 안이므로 백슬래시는 \\\\ 로 이스케이프(예: "$\\\\dfrac{1}{2}$").`;

const SCHEMA = `각 문항 JSON 스키마(필드 순서 무관, 전 필드 포함):
{
 "qtype": "choice|short|ox|proof|essay",
 "question": "문제 본문(문제체, 짧고 명확)",
 "choices": ["보기 5개(choice일 때만, 아니면 null)"],
 "answer": "정답 — choice는 보기와 '정확히 같은 문자열', ox는 O 또는 X, proof/essay는 모범 결론 요약",
 "answer_alt": ["동치 표기 답들(없으면 [])"],
 "points": 배점(정수),
 "difficulty": 1~5,
 "time_limit": 문항당 권장 초(없으면 null, rain·calc는 필수 8~30),
 "tags": ["유형 태그 1~3개"],
 "solution": {"outline":"핵심 아이디어 한 줄","steps":["단계별 풀이 3~7줄"],"check":"검산 한 줄"} 또는 null
}`;

function stripFence(t) {
  return String(t || "").trim().replace(/^```(?:json)?\s*/i, "").replace(/```\s*$/, "").trim();
}
function dollarBalanced(s) {
  return (String(s).match(/\$/g) || []).length % 2 === 0;
}

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "POST만 지원해요" });
  try {
    // ── 1) 로그인 + 관리자 확인 (genCalc 패턴) ──
    const auth = req.headers.authorization || "";
    const token = auth.startsWith("Bearer ") ? auth.slice(7) : null;
    if (!token) return res.status(401).json({ error: "로그인이 필요해요" });
    const url = process.env.VITE_SUPABASE_URL || process.env.SUPABASE_URL;
    const anon = process.env.VITE_SUPABASE_ANON_KEY || process.env.SUPABASE_ANON_KEY;
    if (!url || !anon) return res.status(500).json({ error: "Supabase 환경변수가 없어요" });
    const sb = createClient(url, anon, { global: { headers: { Authorization: `Bearer ${token}` } } });
    const { data: userData, error: uErr } = await sb.auth.getUser(token);
    if (uErr || !userData?.user) return res.status(401).json({ error: "인증 실패" });
    const { data: prof } = await sb.from("profiles").select("role").eq("id", userData.user.id).single();
    if (prof?.role !== "admin") return res.status(403).json({ error: "관리자만 사용할 수 있어요" });
    if (!process.env.ANTHROPIC_API_KEY)
      return res.status(500).json({ error: "ANTHROPIC_API_KEY가 Vercel에 설정되지 않았어요" });

    // ── 2) 입력 ──
    const b = req.body || {};
    const model = MODELS[b.model];
    if (!model) return res.status(400).json({ error: "model은 haiku/sonnet/opus/fable 중 하나" });
    const mode = b.mode === "solutions" ? "solutions" : "items";
    const latex = !!b.latex;
    const mathRule = latex ? MATH_TEX : MATH_UNI;

    let prompt, maxTokens, temperature;
    if (mode === "items") {
      const testType = TEST_DESC[b.testType] ? b.testType : "concept_set";
      const count = Math.min(Math.max(parseInt(b.count, 10) || 5, 1), MAX_COUNT);
      const withSolution = !!b.withSolution;
      const scope = [b.unitName && `단원: ${b.unitName}(${b.unitId || ""})`,
        b.conceptTitles?.length && `개념: ${b.conceptTitles.join(", ")}`].filter(Boolean).join(" / ");
      prompt = `너는 한국 중·고등 수학 학원 "애쉬레인"의 시험 출제자다.

[테스트 성격] ${TEST_DESC[testType]}
[출제 범위] ${scope || "요청문 참고"}
[요청] ${count}문항 · 난이도 ${b.difficulty || "2~3"}(1~5) · 문항형 ${b.qtypes || "choice, short"}
${b.refText ? `[참고 자료 발췌 — 유형·범위·답 형식만 참고하고, 문항은 전부 새로 출제(복제·숫자 바꾸기 금지)]\n${String(b.refText).slice(0, 6000)}\n` : ""}${b.extra ? `[추가 지시] ${b.extra}\n` : ""}
절대 규칙:
1. ${mathRule}
2. ${SCHEMA}
3. choice는 보기 5개, 오답 4개는 전형적 오개념(부호 실수, 공식 혼동 등)에서 설계. answer는 보기 중 하나와 정확히 같은 문자열로 단 한 번만 일치.
4. 대상은 혼자 공부하는 학생 — 문장은 짧고 명확한 문제체. 불필요한 상황 설정 금지(단, mock·out은 학교 시험풍 허용).
5. 모든 계산 문항은 스스로 풀어 검산한 뒤 answer를 확정하라. 확신 없는 문항은 만들지 마라.
6. solution은 ${withSolution ? "모든 문항에 채워라(steps 3~7줄, check 검산 필수)" : "null로 두어라(풀이는 별도 생성)"} .
7. 실존 시험·교재 문항의 복제 금지. 저작권 문구·출처 표기 금지.

출력은 문항 ${count}개의 JSON 배열 "만" — 설명·마크다운·코드펜스 금지.`;
      maxTokens = Math.min(count * (withSolution ? 950 : 400) + 700, 14000);
      temperature = 0.7;
    } else {
      const items = Array.isArray(b.items) ? b.items.slice(0, MAX_COUNT) : [];
      if (!items.length) return res.status(400).json({ error: "풀이를 붙일 items가 없어요" });
      prompt = `너는 한국 중·고등 수학 학원 "애쉬레인"의 풀이 저자다.
아래 문항 배열의 각 항목에 solution을 채워, "같은 순서·같은 개수"의 JSON 배열로 반환하라.

절대 규칙:
1. question·choices·answer 등 기존 필드는 한 글자도 바꾸지 마라. solution만 채운다.
2. solution = {"outline":"핵심 아이디어 한 줄","steps":["3~7줄 — 혼자 공부하는 학생 눈높이, 한 줄에 한 동작"],"check":"답을 다른 방법이나 대입으로 확인하는 검산 한 줄"}.
3. ${mathRule}
4. 각 문항을 실제로 풀어 answer와 일치함을 확인하라. 만약 answer가 틀렸다고 판단되면 solution.check 끝에 "⚠검토필요: (이유)"를 덧붙여라(answer 자체는 수정 금지).

[문항 배열]
${JSON.stringify(items).slice(0, 20000)}

출력은 JSON 배열 "만" — 설명·마크다운·코드펜스 금지.`;
      maxTokens = Math.min(items.length * 750 + 500, 14000);
      temperature = 0.35;
    }

    // ── 3) Anthropic 호출 ──
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": process.env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({ model, max_tokens: maxTokens, temperature,
        messages: [{ role: "user", content: prompt }] }),
    });
    const j = await r.json();
    if (!r.ok) return res.status(502).json({ error: j?.error?.message || "AI 호출 실패" });
    const text = (j.content || []).filter((c) => c.type === "text").map((c) => c.text).join("\n");

    // ── 4) 파싱 + 구조 검증 (구조 파손만 drop, 나머지는 경고 플래그) ──
    let arr;
    try { arr = JSON.parse(stripFence(text)); } catch {
      return res.status(422).json({ error: "AI 출력이 JSON이 아니에요 — 다시 시도해 주세요", raw: text.slice(0, 800) });
    }
    if (!Array.isArray(arr)) arr = [arr];
    const out = []; let dropped = 0;
    for (const it of arr) {
      if (!it || typeof it.question !== "string" || !it.question.trim()) { dropped++; continue; }
      const warns = [];
      if (!QTYPES.has(it.qtype)) { it.qtype = "short"; warns.push("qtype 보정"); }
      if (it.qtype === "choice") {
        if (!Array.isArray(it.choices) || it.choices.length !== 5) warns.push("보기 5개 아님");
        else if (it.choices.filter((c) => String(c) === String(it.answer)).length !== 1) warns.push("answer≠보기 일치");
      } else it.choices = null;
      if (it.answer === undefined || it.answer === null || String(it.answer).trim() === "") warns.push("answer 비어 있음");
      const blob = JSON.stringify(it);
      if (!dollarBalanced(blob)) warns.push("$ 짝 안 맞음");
      if (!latex && /\\\\|\\frac|\\sqrt|\$/.test(blob)) warns.push("기본 규격인데 LaTeX/$ 포함");
      it.difficulty = Math.min(Math.max(parseInt(it.difficulty, 10) || 2, 1), 5);
      it.points = Math.max(parseInt(it.points, 10) || 4, 1);
      it.answer_alt = Array.isArray(it.answer_alt) ? it.answer_alt : [];
      it.tags = Array.isArray(it.tags) ? it.tags.slice(0, 3) : [];
      it.time_limit = it.time_limit == null ? null : Math.max(parseInt(it.time_limit, 10) || 0, 0) || null;
      if (it.solution && (!it.solution.steps || !Array.isArray(it.solution.steps))) { it.solution = null; warns.push("solution 구조 이상"); }
      out.push({ ...it, _warns: warns });
    }
    return res.status(200).json({ items: out, dropped, model: b.model, mode, usage: j.usage || null });
  } catch (e) {
    return res.status(500).json({ error: e?.message || String(e) });
  }
}
