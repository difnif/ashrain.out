// src/lib/contest.js — 경시 대비: 가져오기 검증 · 정오 판정 · 기계 지표 · 분석용 md 내보내기
// 전부 결정적 계산(AI 없음). 규격은 프로젝트 문서 claude/SPEC-경시대비-v1.md.

export const FORMAT = "contest-set/v1";

// ── 답 정규화 · 판정 ─────────────────────────────────────────────────────
const CIRCLED = { "①": "1", "②": "2", "③": "3", "④": "4", "⑤": "5", "⑥": "6", "⑦": "7", "⑧": "8", "⑨": "9", "⑩": "10" };
export function normAnswer(s) {
  if (s == null) return "";
  let t = String(s).trim();
  t = t.replace(/[①-⑩]/g, (c) => CIRCLED[c] || c);
  t = t.replace(/[０-９]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xfee0));
  t = t.replace(/[－−–]/g, "-").replace(/\s+/g, "").replace(/번$/, "").toLowerCase();
  if (/^-?\d+(\.\d+)?$/.test(t)) t = String(Number(t));            // 007 → 7
  return t;
}
export function judge(item, response) {
  const r = normAnswer(response);
  if (!r) return null;                                                // 무응답
  return (item.accept || []).some((a) => normAnswer(a) === r);
}

// ── 원문에서 세는 지표 (A) ───────────────────────────────────────────────
export function computeMetrics(text, item = {}) {
  const t = String(text || "");
  const body = t.replace(/\$[^$]*\$/g, " 수식 ");
  const chars = t.replace(/\s/g, "").length;
  const sentences = (body.match(/[^.?!。]+[.?!。]/g) || []).length || (t.trim() ? 1 : 0);
  const dollar = t.match(/\$[^$]+\$/g) || [];
  const plainMath = dollar.length ? [] : (t.match(/[0-9a-zA-Z()]+(?:\s*[=<>≤≥+\-×÷*/^]\s*[0-9a-zA-Z()]+)+/g) || []);
  const formulas = dollar.length || plainMath.length;
  const longestFormula = Math.max(0, ...[...dollar, ...plainMath].map((f) => f.replace(/[$\s]/g, "").length));
  const conditions = (t.match(/\((?:가|나|다|라|마|바|사)\)|(?:^|\s)[ㄱㄴㄷㄹㅁㅂ]\s*[.)]/g) || []).length;
  const numbers = (body.match(/\d+(?:\.\d+)?/g) || []).length;
  return {
    chars,
    sentences,
    formulas,
    longest_formula: longestFormula,
    conditions,
    numbers,
    ref_figure: /그림|도형|그래프/.test(t),
    ref_table: /표\s|표에|표를|표의|다음 표/.test(t),
    n_choices: item.n_choices || null,
  };
}

// ── 가져오기 JSON 검증 ───────────────────────────────────────────────────
export function validatePackage(j) {
  if (!j || typeof j !== "object") return "JSON 객체가 아님";
  if (j.format && j.format !== FORMAT) return `format 이 ${FORMAT} 가 아님`;
  const s = j.set;
  if (!s || !s.code || !s.title) return "set.code · set.title 필요";
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
    const accept = (Array.isArray(it.answer) ? it.answer : [it.answer]).map(String);
    return {
      no: it.no,
      points: Number(it.points ?? 1),
      answer_type: it.answer_type || "int",
      n_choices: it.n_choices ?? (it.answer_type === "choice" ? 5 : null),
      accept,
      text: it.text || "",
      features: it.features || {},
      solution: it.solution || null,
    };
  }).sort((a, b) => a.no - b.no);
  for (const r of items) r.metrics = computeMetrics(r.text, r);
  const s = j.set;
  return {
    set: {
      code: s.code, title: s.title, contest: s.contest || null, year: s.year || null,
      round: s.round || null, grade_label: s.grade_label || null, test_date: s.test_date || null,
      n_items: items.length, max_score: items.reduce((a, r) => a + r.points, 0), spec: j,
    },
    items,
  };
}

export const takerCode = (t) => "S" + String(t.seq).padStart(4, "0");

// ── 집계 ─────────────────────────────────────────────────────────────────
export function aggregate(items, takers, responses) {
  const rmap = new Map();                                             // takerId → (no → row)
  for (const r of responses) {
    if (!rmap.has(r.taker_id)) rmap.set(r.taker_id, new Map());
    rmap.get(r.taker_id).set(r.item_no, r);
  }
  const active = takers.filter((t) => rmap.has(t.id));
  const st = active.map((t) => {
    const m = rmap.get(t.id);
    let score = 0, right = 0, wrong = 0, blank = 0;
    for (const it of items) {
      const r = m.get(it.no);
      const c = r ? judge(it, r.response) : null;
      if (c === true) { score += it.points; right++; } else if (c === false) wrong++; else blank++;
    }
    return { taker: t, code: takerCode(t), score, right, wrong, blank, cells: m };
  }).sort((a, b) => b.score - a.score || a.code.localeCompare(b.code));
  st.forEach((s, i) => { s.rank = i && st[i - 1].score === s.score ? st[i - 1].rank : i + 1; });

  const n = st.length;
  const k = n >= 4 ? Math.max(1, Math.round(n * 0.27)) : 0;
  const upper = st.slice(0, k), lower = k ? st.slice(n - k) : [];
  const rate = (group, no, it) => group.length
    ? group.filter((s) => judge(it, s.cells.get(no)?.response) === true).length / group.length : null;

  const it = items.map((x) => {
    const p = rate(st, x.no, x);
    const blanks = st.filter((s) => judge(x, s.cells.get(x.no)?.response) === null).length;
    const dist = {};
    if (x.answer_type === "choice") {
      for (let c = 1; c <= (x.n_choices || 5); c++) dist[c] = 0;
      for (const s of st) {
        const v = normAnswer(s.cells.get(x.no)?.response);
        if (v) dist[v] = (dist[v] || 0) + 1;
      }
    }
    return {
      no: x.no, p, blank_rate: n ? blanks / n : null,
      d: k ? rate(upper, x.no, x) - rate(lower, x.no, x) : null, dist,
    };
  });
  return { students: st, items: it, n, k };
}

// ── 분석용 md ────────────────────────────────────────────────────────────
const pct = (v) => (v == null ? "—" : Math.round(v * 100) + "%");
const yn = (v) => (v === true ? "있음" : v === false ? "없음" : "—");
const cell = (v) => (v == null || v === "" ? "—" : String(v).replace(/\|/g, "／").replace(/\n/g, " "));

export function buildExportMd(set, items, takers, responses) {
  const ag = aggregate(items, takers, responses);
  const domains = [...new Set(items.map((x) => x.features?.domain).filter(Boolean))];
  const L = [];
  L.push(`# 경시 분석용 데이터 — ${set.title}`, "");
  L.push(`- 세트 코드: ${set.code}`);
  L.push(`- 대회: ${set.contest || "—"} · ${set.year || "—"} · ${set.round || "—"}`);
  L.push(`- 대상: ${set.grade_label || "—"} · 응시일: ${set.test_date || "—"}`);
  L.push(`- 문항 수: ${items.length} · 만점: ${set.max_score} · 응시 인원: ${ag.n}`);
  L.push(`- 내보낸 시각: ${new Date().toLocaleString("ko-KR")}`);
  L.push(`- 학생 표기: 익명 코드(S0000). 실명은 앱 안에서만 연결됨.`);
  L.push(`- 변별도: 상위·하위 ${ag.k ? ag.k + "명(27%)" : "— (응시 4명 미만이라 계산 안 함)"} 정답률 차`, "");

  L.push("## 1. 문항 특성표", "");
  L.push("### 1-1. 판단 지표 (채팅방) · 실측 지표 (앱)", "");
  L.push("| 번호 | 배점 | 형식 | 정답 | 단원(주) | 부 단원 | 영역 | 세부 유형 | 전략 | 단계 | 개념 수 | 계산량 | 발상/정형 | 예상 난이도 | 실측 정답률 | 변별도 | 무응답률 |");
  L.push("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|");
  items.forEach((x, i) => {
    const f = x.features || {}, a = ag.items[i];
    L.push(`| ${x.no} | ${x.points} | ${x.answer_type}${x.n_choices ? "/" + x.n_choices : ""} | ${cell(x.accept.join(", "))} | ${cell(f.concept_main || f.unit)} | ${cell((f.concept_sub || []).join(", "))} | ${cell(f.domain)} | ${cell(f.type_code ? f.type_code + " " + (f.type_name || "") : f.type_name)} | ${cell((f.strategies || []).join(", "))} | ${cell(f.steps)} | ${cell(f.concepts_needed)} | ${cell(f.calc_load)} | ${cell(f.insight)} | ${cell(f.difficulty)} | ${pct(a.p)} | ${a.d == null ? "—" : a.d.toFixed(2)} | ${pct(a.blank_rate)} |`);
  });
  L.push("", "### 1-2. 문장·도형 지표 (앱이 원문에서 셈 / 도형은 채팅방 판단)", "");
  L.push("| 번호 | 글자 수 | 문장 수 | 수식 수 | 최장 수식 | 조건 항목 | 수치 개수 | 그림 참조 | 표 참조 | 도형 | 도형 종류 | 보조선 |");
  L.push("|---|---|---|---|---|---|---|---|---|---|---|---|");
  for (const x of items) {
    const m = x.metrics || {}, g = x.features?.figure || {};
    L.push(`| ${x.no} | ${cell(m.chars)} | ${cell(m.sentences)} | ${cell(m.formulas)} | ${cell(m.longest_formula)} | ${cell(m.conditions)} | ${cell(m.numbers)} | ${yn(m.ref_figure)} | ${yn(m.ref_table)} | ${yn(g.has)} | ${cell(g.kind)} | ${yn(g.aux_line)} |`);
  }
  L.push("", "### 1-3. 문항별 메모 (함정 · 오답 예측)", "");
  for (const x of items) {
    const f = x.features || {};
    const dis = f.distractors ? Object.entries(f.distractors).map(([k, v]) => `${k}번←${v}`).join(" / ") : "";
    if (!f.trap && !dis) continue;
    L.push(`- ${x.no}번${f.trap ? ` — 함정: ${cell(f.trap)}` : ""}${dis ? ` — 오답 예측: ${cell(dis)}` : ""}`);
  }

  L.push("", "## 2. 응답 행렬", "", "○ 정답 · ×값 오답(쓴 답) · · 무응답", "");
  L.push(`| 코드 | 학년 | 점수 | 순위 | ${items.map((x) => x.no).join(" | ")} |`);
  L.push(`|---|---|---|---|${items.map(() => "---").join("|")}|`);
  for (const s of ag.students) {
    const cs = items.map((x) => {
      const r = s.cells.get(x.no)?.response;
      const c = judge(x, r);
      return c === true ? "○" : c === false ? "×" + cell(normAnswer(r)) : "·";
    });
    L.push(`| ${s.code} | ${cell(s.taker.grade)} | ${s.score} | ${s.rank} | ${cs.join(" | ")} |`);
  }

  L.push("", "## 3. 집계 (앱 계산)", "", "### 3-1. 학생별", "");
  L.push(`| 코드 | 점수 | 순위 | 정답 | 오답 | 무응답 |${domains.map((d) => ` ${d} |`).join("")}`);
  L.push(`|---|---|---|---|---|---|${domains.map(() => "---|").join("")}`);
  for (const s of ag.students) {
    const dr = domains.map((d) => {
      const its = items.filter((x) => x.features?.domain === d);
      const ok = its.filter((x) => judge(x, s.cells.get(x.no)?.response) === true).length;
      return ` ${ok}/${its.length} |`;
    });
    L.push(`| ${s.code} | ${s.score} | ${s.rank} | ${s.right} | ${s.wrong} | ${s.blank} |${dr.join("")}`);
  }
  const choiceItems = items.filter((x) => x.answer_type === "choice");
  if (choiceItems.length) {
    const maxC = Math.max(...choiceItems.map((x) => x.n_choices || 5));
    L.push("", "### 3-2. 객관식 선택 분포 (명)", "");
    L.push(`| 번호 | 정답 |${Array.from({ length: maxC }, (_, i) => ` ${i + 1} |`).join("")} 무응답 |`);
    L.push(`|---|---|${Array.from({ length: maxC }, () => "---|").join("")}---|`);
    for (const x of choiceItems) {
      const a = ag.items[items.indexOf(x)];
      const blanks = Math.round((a.blank_rate || 0) * ag.n);
      L.push(`| ${x.no} | ${cell(x.accept.join(","))} |${Array.from({ length: maxC }, (_, i) => ` ${a.dist[i + 1] ?? "—"} |`).join("")} ${blanks} |`);
    }
  }

  const raw = {
    format: "contest-export/v1",
    set: { code: set.code, title: set.title, contest: set.contest, year: set.year, round: set.round, grade_label: set.grade_label, test_date: set.test_date, max_score: Number(set.max_score) },
    items: items.map((x, i) => ({ no: x.no, points: x.points, answer_type: x.answer_type, n_choices: x.n_choices, accept: x.accept, features: x.features, metrics: x.metrics, stats: ag.items[i] })),
    students: ag.students.map((s) => ({
      code: s.code, grade: s.taker.grade || null, score: s.score, rank: s.rank,
      responses: Object.fromEntries(items.map((x) => [x.no, s.cells.get(x.no)?.response ?? null])),
    })),
  };
  L.push("", "## 4. 원자료 (JSON)", "", "```json", JSON.stringify(raw, null, 1), "```", "");
  return L.join("\n");
}
