// 시록고 강사도구 — 하위 문제 (1) · (2) · (3) 를 따로 채점하기 (순수 함수, node --test tests/ttparts.test.mjs)
// 채점 단위 = 문항 줄(tt_print_items 한 줄). 하위 문제가 있는 문제는 하위 문제마다 한 줄로 나눈다:
//   같은 문항 그림(png) · 정답 그림 · 해설 그림을 함께 쓰고, label 은 「3 (1)」 「3 (2)」, hash 는 「…#1」 「…#2」.
//   seq 는 채점 단위 차례(1, 2, 3, …)이고, 시험지에 찍힌 문제 번호는 label 의 앞부분이다.
//   나눈 프린트에서는 나누지 않은 문항도 label 에 문제 번호를 적는다(seq 와 문제 번호가 달라지므로).

const CIRC_PAREN = "⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇";
const MARK_RE = /\((\d{1,2})\)|（(\d{1,2})）|([⑴-⒇])/g;
const markNo = (m) => (m[1] || m[2] ? Number(m[1] || m[2]) : CIRC_PAREN.indexOf(m[3]) + 1);
export const partLabel = (k) => `(${k})`;

// 정답 글자에서 하위 문제: "(1) 12 (2) 5" → [{label:"(1)", answer:"12"}, {label:"(2)", answer:"5"}]
// 표시가 (1)부터 차례로 둘 이상이고 글자 맨 앞에서 시작할 때만. "f(1)=3" 같은 식은 나누지 않는다.
export function partsFromAnswer(s) {
  const str = String(s || "").trim();
  if (!str) return null;
  const found = [];
  for (const m of str.matchAll(MARK_RE)) {
    const before = str.slice(0, m.index);
    if (before && !/[\s,，;；/·]$/.test(before)) continue;        // 앞에 글자가 붙은 괄호(f(1))는 표시가 아님
    found.push({ no: markNo(m), at: m.index, end: m.index + m[0].length });
  }
  if (found.length < 2 || found[0].at !== 0) return null;
  const run = [];
  for (const f of found) { if (f.no === run.length + 1) run.push(f); }
  if (run.length < 2 || run.length !== found.filter((f) => f.no <= run.length).length) return null;
  return run.map((f, i) => ({
    label: partLabel(f.no),
    answer: str.slice(f.end, i + 1 < run.length ? run[i + 1].at : str.length).trim().replace(/^[:：.)\s]+/, "").replace(/[\s,，;；/·]+$/, ""),
  }));
}

// 문항 자리 안 글줄에서 하위 문제 수: 줄 머리의 (1) (2) (3) … (1부터 차례로 둘 이상일 때)
export function partsFromLines(lines) {
  const nos = [];
  for (const l of lines || []) {
    const t = String(l || "").trim();
    const m = /^(?:\((\d{1,2})\)|（(\d{1,2})）|([⑴-⒇]))/.exec(t);
    if (m) nos.push(markNo(m));
  }
  let n = 0;
  for (const k of nos) if (k === n + 1) n = k;
  return n >= 2 ? n : 0;
}

// label 「3 (2)」 → {base:"3", part:2} · 「3」 → {base:"3", part:0}
export function splitLabel(label) {
  const s = String(label || "").trim();
  const m = /^(.*\S)\s*(?:\((\d{1,2})\)|（(\d{1,2})）|([⑴-⒇]))$/.exec(s);
  if (!m) return { base: s, part: 0 };
  return { base: m[1], part: m[2] || m[3] ? Number(m[2] || m[3]) : CIRC_PAREN.indexOf(m[4]) + 1 };
}
export const baseHash = (h) => (h ? String(h).replace(/#\d+$/, "") : h);

// 문항 줄(seq 차례) → 문제 묶음 [{base, rows:[…]}] — 같은 문제 번호 · 같은 그림의 하위 문제 줄을 하나로
export function groupProblems(rows) {
  const out = [];
  for (const r of [...rows].sort((a, b) => a.seq - b.seq)) {
    const { base, part } = splitLabel(r.label || String(r.seq));
    const last = out[out.length - 1];
    if (part && last && last.base === base && last.parts && (last.rows[0].png || null) === (r.png || null)) { last.rows.push(r); continue; }
    out.push({ base, parts: part > 0, rows: [r] });
  }
  return out;
}

// 문제 → 채점 단위 줄로 펼치기. problems: [{ row:{…문항 줄 필드}, no:"3", parts:null | [{label, answer}] }]
// 하위 문제가 하나라도 있으면 모든 줄의 label 에 문제 번호를 적는다.
export function expandParts(problems) {
  const any = problems.some((p) => p.parts && p.parts.length >= 2);
  const rows = [];
  for (const p of problems) {
    const base = p.row;
    if (!p.parts || p.parts.length < 2) {
      rows.push({ ...base, seq: rows.length + 1, label: any ? base.label || String(p.no) : base.label });
      continue;
    }
    p.parts.forEach((pt, k) => {
      rows.push({ ...base, seq: rows.length + 1, label: `${base.label || p.no} ${pt.label || partLabel(k + 1)}`, answer: String(pt.answer || ""), choice: false,
        hash: base.hash ? `${baseHash(base.hash)}#${k + 1}` : base.hash, points: k === 0 ? base.points ?? null : null });
    });
  }
  return rows;
}

// 지금 문항 줄 + 고친 하위 문제 수 → 새 배치(tt_relayout_items 에 넘김)
// plan: Map(문제 첫 줄 seq → [{label, answer}] | null(나누지 않음)). 줄마다 from = 기록(채점 표시)을 물려받을 옛 seq.
export function relayout(rows, plan) {
  const groups = groupProblems(rows);
  const any = groups.some((g) => { const p = plan.has(g.rows[0].seq) ? plan.get(g.rows[0].seq) : g.parts ? g.rows : null; return p && p.length >= 2; });
  const out = [];
  for (const g of groups) {
    const first = g.rows[0];
    const want = plan.has(first.seq) ? plan.get(first.seq) : g.parts ? g.rows.map((r) => ({ label: partLabel(splitLabel(r.label).part), answer: r.answer })) : null;
    const h = baseHash(first.hash);
    if (!want || want.length < 2) {
      // 하나로: 첫 줄의 기록을 물려받음. 정답은 나눠 적었던 것을 「(1) a (2) b」로 다시 모음
      const ans = g.parts ? g.rows.map((r) => `${partLabel(splitLabel(r.label).part)} ${r.answer || ""}`.trim()).join(" ") : first.answer || "";
      out.push({ from: first.seq, label: any ? g.base : g.parts ? g.base : first.label || "", answer: g.parts ? ans : first.answer || "", choice: g.parts ? false : !!first.choice, hash: h || null });
      continue;
    }
    want.forEach((pt, k) => {
      const old = g.parts ? g.rows.find((r) => splitLabel(r.label).part === k + 1) : null;
      out.push({ from: (old || first).seq, label: `${g.base} ${pt.label || partLabel(k + 1)}`, answer: String(pt.answer ?? (old ? old.answer : "") ?? ""), choice: false,
        hash: h ? `${h}#${k + 1}` : null, points: k === 0 ? (old || first).points ?? null : null });
    });
  }
  return out.map((r, i) => ({ seq: i + 1, ...r }));
}
