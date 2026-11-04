// src/lib/contest.js — 경시 대비: 가져오기 검증 · 채점 · 기계 지표 · 오답 프린트 · 분석용 md
// 전부 결정적 계산(AI 없음). 규격: docs/SPEC-contest-v1.md

export const FORMAT = "contest-set/v1";
export const HALVES = ["상반기", "하반기"];

// ── 답 정규화 · 판정 ─────────────────────────────────────────────────────
const CIRCLED = { "①": "1", "②": "2", "③": "3", "④": "4", "⑤": "5", "⑥": "6", "⑦": "7", "⑧": "8", "⑨": "9", "⑩": "10" };
export function normAnswer(s) {
  if (s == null) return "";
  let t = String(s).trim();
  t = t.replace(/[①-⑩]/g, (c) => CIRCLED[c] || c);
  t = t.replace(/[０-９]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xfee0));
  t = t.replace(/[－−–]/g, "-").replace(/\s+/g, "").replace(/번$/, "").toLowerCase();
  if (/^-?\d+(\.\d+)?$/.test(t)) t = String(Number(t));
  return t;
}
export function judge(item, response) {
  const r = normAnswer(response);
  if (!r) return null;
  return (item.accept || []).some((a) => normAnswer(a) === r);
}
export function gradeAll(items, answers) {
  let score = 0, right = 0, wrong = 0, blank = 0, max = 0;
  const rows = items.map((x) => {
    const v = (answers[x.no] ?? "").toString().trim();
    const c = judge(x, v);
    max += Number(x.points);
    // 무응답은 따로 세되 오답에 포함한다 (wrong = 틀린 답 + 무응답, blank = 그중 무응답)
    if (c === true) { score += Number(x.points); right++; } else { wrong++; if (c === null) blank++; }
    return { item_no: x.no, response: v || null, is_correct: c === true };
  });
  return { rows, score, max, right, wrong, blank };
}

// ── 원문에서 세는 지표 ───────────────────────────────────────────────────
export function computeMetrics(text, item = {}) {
  const t = String(text || "");
  const body = t.replace(/\$[^$]*\$/g, " 수식 ");
  const dollar = t.match(/\$[^$]+\$/g) || [];
  const plainMath = dollar.length ? [] : (t.match(/[0-9a-zA-Z()²³]+(?:\s*[=<>≤≥+\-×÷*/^]\s*[0-9a-zA-Z()²³]+)+/g) || []);
  return {
    chars: t.replace(/\s/g, "").length,
    sentences: (body.match(/[^.?!。]+[.?!。]/g) || []).length || (t.trim() ? 1 : 0),
    formulas: dollar.length || plainMath.length,
    longest_formula: Math.max(0, ...[...dollar, ...plainMath].map((f) => f.replace(/[$\s]/g, "").length)),
    conditions: (t.match(/\((?:가|나|다|라|마|바|사)\)|(?:^|\s)[ㄱㄴㄷㄹㅁㅂ]\s*[.)]/g) || []).length,
    numbers: (body.match(/\d+(?:\.\d+)?/g) || []).length,
    ref_figure: /그림|도형|그래프/.test(t) || !!item.figure,
    ref_table: /표\s|표에|표를|표의|다음 표/.test(t),
    n_choices: item.n_choices || null,
  };
}

// ── 가져오기 JSON ────────────────────────────────────────────────────────
export function validatePackage(j) {
  if (!j || typeof j !== "object") return "JSON 객체가 아님";
  if (j.format && j.format !== FORMAT) return `format 이 ${FORMAT} 가 아님`;
  const s = j.set;
  if (!s || !s.code || !s.title) return "set.code · set.title 필요";
  if (s.half && !HALVES.includes(s.half)) return "set.half 는 상반기|하반기";
  if (!Array.isArray(j.items) || !j.items.length) return "items 배열이 비어 있음";
  const seen = new Set();
  for (const it of j.items) {
    if (!Number.isInteger(it.no)) return "문항 no(정수) 없음";
    if (seen.has(it.no)) return `${it.no}번 중복`;
    seen.add(it.no);
    if (!["choice", "int", "text"].includes(it.answer_type || "int")) return `${it.no}번 answer_type 오류`;
    const acc = Array.isArray(it.answer) ? it.answer : [it.answer];
    if (!acc.length || acc.some((a) => a == null || String(a).trim() === "")) return `${it.no}번 answer 없음`;
  }
  return null;
}
export function packageToRows(j) {
  const items = j.items.map((it) => {
    const r = {
      no: it.no,
      points: Number(it.points ?? 1),
      answer_type: it.answer_type || "int",
      n_choices: it.n_choices ?? (it.answer_type === "choice" ? (it.choices?.length || 5) : null),
      choices: Array.isArray(it.choices) ? it.choices.map(String) : null,
      accept: (Array.isArray(it.answer) ? it.answer : [it.answer]).map(String),
      text: it.text || "",
      figure: it.figure || null,
      features: it.features || {},
      solution: it.solution || null,
    };
    r.metrics = computeMetrics(r.text, r);
    return r;
  }).sort((a, b) => a.no - b.no);
  const s = j.set;
  return {
    set: {
      code: s.code, kind: "original", title: s.title, contest: s.contest || null, year: s.year || null,
      half: s.half || null, grade_label: s.grade_label || null, test_date: s.test_date || null,
      n_items: items.length, max_score: items.reduce((a, r) => a + r.points, 0), spec: j,
    },
    items,
  };
}

export const takerCode = (t) => "S" + String(t.seq).padStart(4, "0");
export const setLabel = (s) => s.kind === "wrong"
  ? s.title
  : [s.year, s.half, s.grade_label].filter(Boolean).join(" ") + (s.title ? ` · ${s.title}` : "");

// ── 오답 프린트 ──────────────────────────────────────────────────────────
// sources: [{ set, items, responses(이 학생) }] → 오답 문항(원본 기준 중복 제거)
export function collectWrong(sources) {
  const out = [];
  const seen = new Set();
  for (const { set, items, responses } of sources) {
    const rmap = new Map(responses.map((r) => [r.item_no, r]));
    for (const x of items) {
      const r = rmap.get(x.no);
      if (r?.is_correct === true) continue;               // 오답 + 무응답 모두 담는다
      const rootSet = x.src_set_id || set.id, rootNo = x.src_no ?? x.no;
      const key = rootSet + "#" + rootNo;
      if (seen.has(key)) continue;
      seen.add(key);
      out.push({ item: x, from: set, rootSet, rootNo, response: r?.response ?? null });
    }
  }
  return out;
}
export function wrongPrintRows(wrongs) {
  return wrongs.map((w, i) => ({
    no: i + 1,
    points: w.item.points,
    answer_type: w.item.answer_type,
    n_choices: w.item.n_choices,
    choices: w.item.choices,
    accept: w.item.accept,
    text: w.item.text,
    figure: w.item.figure,
    crop: w.item.crop,
    features: w.item.features,
    metrics: w.item.metrics,
    solution: w.item.solution,
    src_set_id: w.rootSet,
    src_no: w.rootNo,
  }));
}

// 인쇄용 HTML (새 창에서 인쇄)
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const CIRC = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩"];
export function printHtml({ set, items, taker, perPage = 2, srcLabel = () => "" }) {
  const blocks = items.map((x) => x.cropUrl ? `
    <section class="q">
      <div class="qh"><b>${x.no}.</b> <span class="src">${esc(srcLabel(x))} (그림 속 번호는 원본 번호)</span><span class="pt">${x.points}점</span></div>
      <img class="crop" src="${esc(x.cropUrl)}">
      <div class="ans">답: ______________</div>
    </section>` : `
    <section class="q">
      <div class="qh"><b>${x.no}.</b> <span class="src">${esc(srcLabel(x))}</span><span class="pt">${x.points}점</span></div>
      <div class="qt">${esc(String(x.text || "").replace(/\$/g, "")).replace(/\n/g, "<br>")}</div>
      ${x.figure ? `<img class="fig" src="${esc(x.figure)}">` : ""}
      ${x.choices?.length ? `<ol class="ch">${x.choices.map((c, i) => `<li><span>${CIRC[i] || i + 1}</span> ${esc(c)}</li>`).join("")}</ol>` : ""}
      <div class="ans">답: ______________</div>
    </section>`);
  const pages = [];
  for (let i = 0; i < blocks.length; i += perPage) pages.push(blocks.slice(i, i + perPage).join(""));
  return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>${esc(set.title)}</title>
<style>
@page{size:A4;margin:16mm 15mm}
body{font-family:"Noto Sans KR","Apple SD Gothic Neo",sans-serif;color:#111;margin:0}
.page{page-break-after:always;display:flex;flex-direction:column;gap:10mm;min-height:250mm}
.page:last-child{page-break-after:auto}
.head{display:flex;justify-content:space-between;border-bottom:2px solid #111;padding-bottom:3mm;font-size:12pt}
.q{flex:1;display:flex;flex-direction:column;gap:3mm;font-size:11.5pt;line-height:1.7}
.qh{display:flex;gap:3mm;align-items:baseline}.src{color:#777;font-size:9pt}.pt{margin-left:auto;color:#777;font-size:9pt}
.fig{max-width:70%;max-height:70mm;object-fit:contain;align-self:center}
.crop{width:100%;max-height:105mm;object-fit:contain;object-position:left top}
.ch{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:2mm 8mm}.ch span{margin-right:1mm}
.ans{margin-top:auto;text-align:right;font-size:11pt}
.noprint{position:fixed;top:8px;right:8px}@media print{.noprint{display:none}}
</style></head><body>
<button class="noprint" onclick="print()">인쇄</button>
${pages.map((p, i) => `<div class="page"><div class="head"><span>${esc(set.title)}</span><span>${esc(taker?.name || "")} · ${i + 1}/${pages.length}</span></div>${p}</div>`).join("")}
</body></html>`;
}

// ── 분석용 md (학생 1명 · 고른 프린트들) ─────────────────────────────────
// prints: [{ set, items, responses(이 학생), attempt }]
// group: Map(rootSet#rootNo → { n, right })  — 같은 원본 문항을 푼 모든 학생 기준 정답률
const pct = (v) => (v == null || Number.isNaN(v) ? "—" : Math.round(v * 100) + "%");
const yn = (v) => (v === true ? "있음" : v === false ? "없음" : "—");
const cell = (v) => (v == null || v === "" ? "—" : String(v).replace(/\|/g, "／").replace(/\n/g, " "));
const mark = (c, r) => (c === true ? "○" : normAnswer(r) ? "×" + cell(normAnswer(r)) : "×·");

export function buildStudentExport({ taker, prints, group, setById }) {
  const L = [];
  const code = takerCode(taker);
  const keyOf = (set, x) => (x.src_set_id || set.id) + "#" + (x.src_no ?? x.no);
  const srcName = (x) => {
    if (!x.src_set_id) return "";
    const s = setById.get(x.src_set_id);
    return s ? `${s.code} ${x.src_no}번` : `원본 ${x.src_no}번`;
  };

  L.push(`# 경시 분석 의뢰 — ${code}`, "");
  L.push(`- 학생: ${code} · 학년 ${taker.grade || "—"} (실명은 앱 안에서만)`);
  L.push(`- 프린트 ${prints.length}개 · 내보낸 시각 ${new Date().toLocaleString("ko-KR")}`);
  L.push(`- 집단 정답률 = 같은 원본 문항을 푼 모든 분석 대상 기준 (오답 프린트 재응시 포함하지 않음)`);
  L.push(`- 결과 표기: ○ 정답 · ×값 오답(쓴 답) · ×· 무응답(오답으로 채점)`, "");

  L.push("## 1. 프린트 요약", "");
  L.push("| 프린트 | 종류 | 연도 | 반기 | 대상 | 등록일 | 점수 | 정답 | 오답(무응답 포함) | 그중 무응답 |");
  L.push("|---|---|---|---|---|---|---|---|---|---|");
  for (const p of prints) {
    const a = p.attempt || {};
    L.push(`| ${cell(p.set.code)} | ${p.set.kind === "wrong" ? "오답 프린트" : "기출"} | ${cell(p.set.year)} | ${cell(p.set.half)} | ${cell(p.set.grade_label)} | ${cell(a.taken_on)} | ${a.score ?? "—"}/${a.max_score ?? p.set.max_score} | ${a.n_right ?? "—"} | ${a.n_wrong ?? "—"} | ${a.n_blank ?? "—"} |`);
  }

  for (const p of prints) {
    const rmap = new Map(p.responses.map((r) => [r.item_no, r]));
    L.push("", `## 2. 문항별 — ${p.set.code}${p.set.kind === "wrong" ? " (오답 프린트)" : ""}`, "");
    L.push("| 번호 | 원본 | 결과 | 정답 | 배점 | 단원(주) | 영역 | 세부 유형 | 전략 | 단계 | 개념 수 | 계산량 | 발상/정형 | 예상 난이도 | 집단 정답률 | 글자 수 | 문장 수 | 수식 | 조건 | 도형 | 보조선 |");
    L.push("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|");
    for (const x of p.items) {
      const f = x.features || {}, m = x.metrics || {}, g = f.figure || {};
      const r = rmap.get(x.no);
      const gs = group.get(keyOf(p.set, x));
      L.push(`| ${x.no} | ${cell(srcName(x))} | ${mark(r?.is_correct ?? null, r?.response)} | ${cell(x.accept.join(","))} | ${x.points} | ${cell(f.concept_main || f.unit)} | ${cell(f.domain)} | ${cell(f.type_code ? f.type_code + " " + (f.type_name || "") : f.type_name)} | ${cell((f.strategies || []).join(", "))} | ${cell(f.steps)} | ${cell(f.concepts_needed)} | ${cell(f.calc_load)} | ${cell(f.insight)} | ${cell(f.difficulty)} | ${gs ? pct(gs.right / gs.n) + ` (${gs.n}명)` : "—"} | ${cell(m.chars)} | ${cell(m.sentences)} | ${cell(m.formulas)} | ${cell(m.conditions)} | ${g.has ? cell(g.kind || "있음") : yn(m.ref_figure ? true : g.has)} | ${yn(g.aux_line)} |`);
    }
    const memo = p.items.filter((x) => x.features?.trap || x.features?.distractors);
    if (memo.length) {
      L.push("", "메모 (함정 · 오답 예측):");
      for (const x of memo) {
        const f = x.features;
        const dis = f.distractors ? Object.entries(f.distractors).map(([k, v]) => `${k}←${v}`).join(" / ") : "";
        L.push(`- ${x.no}번${f.trap ? ` 함정: ${cell(f.trap)}` : ""}${dis ? ` · 오답 예측: ${cell(dis)}` : ""}`);
      }
    }
  }

  // 재응시 추적: 원본 문항 하나의 시도 이력
  const hist = new Map();
  const order = [...prints].sort((a, b) => String(a.attempt?.graded_at || "").localeCompare(String(b.attempt?.graded_at || "")));
  for (const p of order) {
    const rmap = new Map(p.responses.map((r) => [r.item_no, r]));
    for (const x of p.items) {
      const k = keyOf(p.set, x);
      if (!hist.has(k)) hist.set(k, { label: x.src_set_id ? srcName(x) : `${p.set.code} ${x.no}번`, tries: [] });
      const r = rmap.get(x.no);
      hist.get(k).tries.push(mark(r?.is_correct ?? null, r?.response));
    }
  }
  const multi = [...hist.values()].filter((h) => h.tries.length > 1);
  if (multi.length) {
    L.push("", "## 3. 재응시 추적 (원본 문항별 시도 순서)", "");
    L.push("| 원본 문항 | 시도 |", "|---|---|");
    for (const h of multi) L.push(`| ${cell(h.label)} | ${h.tries.join(" → ")} |`);
  }

  // 영역별
  const dom = new Map();
  for (const p of prints) {
    if (p.set.kind === "wrong") continue;
    const rmap = new Map(p.responses.map((r) => [r.item_no, r]));
    for (const x of p.items) {
      const d = x.features?.domain || "미분류";
      if (!dom.has(d)) dom.set(d, { n: 0, right: 0, pts: 0, got: 0 });
      const o = dom.get(d), c = rmap.get(x.no)?.is_correct;
      o.n++; o.pts += Number(x.points);
      if (c === true) { o.right++; o.got += Number(x.points); }
    }
  }
  if (dom.size) {
    L.push("", "## 4. 영역별 (기출 프린트만)", "");
    L.push("| 영역 | 문항 | 정답 | 정답률 | 득점/배점 |", "|---|---|---|---|---|");
    for (const [d, o] of dom) L.push(`| ${d} | ${o.n} | ${o.right} | ${pct(o.right / o.n)} | ${o.got}/${o.pts} |`);
  }

  const raw = {
    format: "contest-student-export/v1",
    student: { code, grade: taker.grade || null },
    prints: prints.map((p) => ({
      code: p.set.code, kind: p.set.kind, year: p.set.year, half: p.set.half, grade_label: p.set.grade_label,
      attempt: p.attempt ? { registered_on: p.attempt.taken_on, score: Number(p.attempt.score), max: Number(p.attempt.max_score), graded_at: p.attempt.graded_at } : null,
      items: p.items.map((x) => {
        const r = p.responses.find((y) => y.item_no === x.no);
        const gs = group.get(keyOf(p.set, x));
        return {
          no: x.no, src: x.src_set_id ? srcName(x) : null, points: Number(x.points), answer_type: x.answer_type,
          accept: x.accept, response: r?.response ?? null, correct: r?.is_correct ?? null,
          group_rate: gs ? +(gs.right / gs.n).toFixed(3) : null, group_n: gs?.n ?? 0,
          features: x.features, metrics: x.metrics,
        };
      }),
    })),
  };
  L.push("", "## 5. 원자료 (JSON)", "", "```json", JSON.stringify(raw), "```", "");
  return L.join("\n");
}
