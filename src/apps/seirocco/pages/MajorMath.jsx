// 서고 › 전공 수학 — 대학 전공에서 쓰는 수학의 서가(분야별: 대학수학 · 공학 · 자연과학 · 정보 · 경제경영 · 예술)
// 책은 public/majors/<책 id>.json(생성기 majorgen/ — python3 majorgen/build.py). DB 를 쓰지 않는다.
// 주소: #/seogo/jeon(서가) · #/seogo/jeon/<책>(차례) · #/seogo/jeon/<책>/<장>(본문)
// 본문 블록(v2): 이론 · 💡 왜 그럴까 · 📘 정의 · 📐 정리(증명 접기) · 🎬 움직이는 그림(majors/anims — 보일 때 받는다) · 예제(한 줄씩 펼치기)
//   · ⚠ 흔한 실수 · 🏭 현장에서 · 표 · 코드 · 연습(힌트 · 답 · 풀이) — 장 머리에 「이 장의 목표」, 끝에 「용어」 · 「한 장 요약」.
// 수식은 MathIR 표식(components/MathText — 분수는 상하로). 읽은 장은 이 기기에만(localStorage — 막히면 표시 없이).
// 서가 · 차례 · 장 조각(Shelf · Toc · Chapter)은 검산(tests/majors.test.mjs)이 따로 그린다.
import { useEffect, useMemo, useState } from "react";
import { useAppHash, go } from "../../../shared/demo";
import { mathHtml, ensureMathCss } from "../../../components/MathText";
import { loadKind } from "./majors/anims/index.js";

const BASE = "/majors";
const TONE = {
  teal: "#1f9e8f", amber: "#c98a1b", coral: "#d4644a", violet: "#7b5fc9", sky: "#3a8fd0",
  rose: "#c9567c", lime: "#6c9a2a", indigo: "#4e5fc0", slate: "#64748b",
};
const cache = {};
function getJSON(p) {
  if (!cache[p]) cache[p] = fetch(p, { cache: "no-cache" }).then((r) => (r.ok ? r.json() : Promise.reject(new Error(`${p} ${r.status}`))));
  return cache[p];
}
/** 테스트 · 미리 받기용 — 받아 둔 책을 넣어 두면 화면이 바로 그린다 */
export function primeMajor(path, data) { cache[path] = Promise.resolve(data); }

const READ_KEY = "srk.majors.read.v2";   // v2 에서 책 · 장이 새로 짜여 읽음 표시를 새로 센다
function loadRead() { try { return JSON.parse(localStorage.getItem(READ_KEY) || "{}") || {}; } catch { return {}; } }
function saveRead(r) { try { localStorage.setItem(READ_KEY, JSON.stringify(r)); } catch { /* 저장이 막힌 기기 */ } }

/** 평문 + **굵게** + 수식 표식 → HTML (mathHtml 이 이스케이프한다) */
export function richHtml(t) {
  return String(t ?? "").split(/(\*\*(?:(?!\*\*)[\s\S])+\*\*)/g)
    .map((seg) => (/^\*\*[\s\S]+\*\*$/.test(seg) ? `<b>${mathHtml(seg.slice(2, -2))}</b>` : mathHtml(seg))).join("");
}
function R({ t, as: Tag = "span", className, style }) {
  const html = useMemo(() => richHtml(t), [t]);
  return <Tag className={className} style={style} dangerouslySetInnerHTML={{ __html: html }} />;
}

const CSS = `
.mm-wrap{display:flex;flex-direction:column;gap:12px;min-width:0;overflow-wrap:break-word}
.mm-lead{font-size:13px;color:var(--mut);line-height:1.75;margin:0}
.mm-find{width:100%;box-sizing:border-box;border:1px solid var(--bd);background:var(--card);color:var(--ink);border-radius:12px;padding:11px 14px;font:inherit;font-size:14px}
.mm-field{display:flex;flex-direction:column;gap:8px}
.mm-fh{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;margin:6px 0 0}
.mm-fh b{font-size:15px}
.mm-fh span{font-size:12px;color:var(--mut)}
.mm-shelf{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(230px,100%),1fr));gap:10px}
.mm-book{position:relative;text-align:left;background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:14px 14px 12px 20px;cursor:pointer;font-family:inherit;color:var(--ink);display:flex;flex-direction:column;gap:6px;min-height:140px;min-width:0}
.mm-book:hover{border-color:var(--sp)}
.mm-book::before{content:"";position:absolute;left:0;top:0;bottom:0;width:7px;border-radius:14px 0 0 14px;background:var(--sp)}
.mm-bt{font-size:16px;font-weight:800;letter-spacing:.01em}
.mm-bs{font-size:12px;color:var(--mut);line-height:1.55}
.mm-bm{margin-top:auto;display:flex;gap:6px;flex-wrap:wrap;align-items:center;font-size:11px;color:var(--mut)}
.mm-bar{height:5px;background:var(--in);border-radius:99px;overflow:hidden;flex:1;min-width:50px}
.mm-bar>i{display:block;height:100%;background:var(--sp)}
.mm-path{display:flex;gap:6px;flex-wrap:wrap;align-items:center;font-size:12.5px}
.mm-path button{border:1px solid var(--bd);background:var(--card);border-radius:99px;padding:5px 11px;font:inherit;font-size:12.5px;font-weight:700;color:var(--ink);cursor:pointer}
.mm-path i{color:var(--mut);font-style:normal}
.mm-hit{display:flex;flex-direction:column;gap:2px;text-align:left;border:0;border-bottom:1px solid var(--bd);background:none;padding:9px 2px;cursor:pointer;font:inherit;color:var(--ink)}
.mm-hit small{color:var(--mut);font-size:11.5px}
.mm-back{background:none;border:0;color:var(--ac);font-weight:800;font-size:12.5px;cursor:pointer;padding:2px 0;font-family:inherit;align-self:flex-start}
.mm-hd{border-left:6px solid var(--sp);padding:2px 0 2px 12px}
.mm-hd h3{margin:0;font-size:18px;line-height:1.4}
.mm-hd p{margin:4px 0 0;font-size:12.5px;color:var(--mut);line-height:1.6}
.mm-intro{font-size:13.5px;line-height:1.9;margin:0}
.mm-toc{display:flex;flex-direction:column}
.mm-ch{display:flex;gap:12px;align-items:flex-start;padding:11px 2px;border-bottom:1px solid var(--bd);cursor:pointer;background:none;border-left:0;border-right:0;border-top:0;text-align:left;font-family:inherit;color:var(--ink);min-width:0}
.mm-ch:last-child{border-bottom:0}
.mm-ch>span:last-child{min-width:0}
.mm-no{flex:0 0 auto;width:28px;height:28px;border-radius:99px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12.5px;border:1.5px solid var(--sp);color:var(--sp)}
.mm-no.on{background:var(--sp);color:var(--bg)}
.mm-ct{font-size:14px;font-weight:800}
.mm-cs{font-size:12px;color:var(--mut);margin-top:3px;line-height:1.55}
.mm-badges{display:flex;gap:6px;flex-wrap:wrap;margin-top:5px}
.mm-badges span{font-size:10.5px;font-weight:800;color:var(--sp);border:1px solid var(--sp);border-radius:99px;padding:1px 7px;opacity:.85}
.mm-goals{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:6px}
.mm-goals li{font-size:13.5px;line-height:1.7;padding-left:22px;position:relative}
.mm-goals li::before{content:"✓";position:absolute;left:2px;top:0;color:var(--sp);font-weight:900}
.mm-sec h4{margin:4px 0 8px;font-size:15px;display:flex;align-items:center;gap:8px}
.mm-sec h4::before{content:"";width:4px;height:15px;border-radius:2px;background:var(--sp);flex:none}
.mm-p{font-size:14px;line-height:1.95;margin:0 0 10px}
.mm-p:last-child{margin-bottom:0}
.mm-eq{background:var(--in);border:1px solid var(--bd);border-radius:10px;padding:10px 14px;margin:4px 0 12px;display:flex;flex-direction:column;gap:8px;overflow-x:auto;-webkit-overflow-scrolling:touch}
.mm-eq:last-child{margin-bottom:0}
.mm-eq>div{font-size:14.5px;line-height:1.9;white-space:nowrap;text-align:center}
.mm-box{border-radius:12px;padding:12px 14px;border:1px solid var(--bd);background:var(--card)}
.mm-box>.mm-tag{margin:0 0 6px}
.mm-why{background:color-mix(in srgb,var(--sp) 9%,var(--card));border-color:color-mix(in srgb,var(--sp) 35%,var(--bd))}
.mm-def{border-left:5px solid var(--sp)}
.mm-def .mm-term{font-size:15px;font-weight:800}
.mm-def .mm-term small{font-weight:600;color:var(--mut);font-size:12px;margin-left:6px;font-style:italic}
.mm-thm{border:1.5px solid var(--sp)}
.mm-thm .mm-stmt{font-size:14px;line-height:1.9;margin:0 0 8px;font-weight:600}
.mm-warn{background:color-mix(in srgb,#b4442e 7%,var(--card));border-color:color-mix(in srgb,#b4442e 30%,var(--bd))}
.mm-warn ul{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px}
.mm-warn li{font-size:13.5px;line-height:1.8}
.mm-use{background:color-mix(in srgb,#3f7d3a 7%,var(--card));border-color:color-mix(in srgb,#3f7d3a 30%,var(--bd))}
.mm-anim .mm-cap{font-size:12.5px;line-height:1.7;color:var(--mut);margin:8px 0 0}
.mm-wait{padding:26px 12px;text-align:center;font-size:12.5px;color:var(--mut);border:1px dashed var(--bd);border-radius:12px;background:var(--in)}
.mm-tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
.mm-tbl{border-collapse:collapse;width:100%;font-size:13px}
.mm-tbl th,.mm-tbl td{border:1px solid var(--bd);padding:6px 9px;text-align:left;line-height:1.6;vertical-align:top}
.mm-tbl th{background:var(--in);font-weight:800;word-break:keep-all}
.mm-code{margin:0;background:#1f1c17;color:#efe7d6;border-radius:10px;padding:12px 14px;font:12.5px/1.65 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;overflow-x:auto;white-space:pre}
.mm-ex,.mm-pr{border:1px solid var(--bd);border-radius:12px;padding:12px 14px;background:var(--card)}
.mm-ex{border-color:var(--sp)}
.mm-tag{font-size:11px;font-weight:800;letter-spacing:.05em;color:var(--sp);margin:0 0 6px}
.mm-pr .mm-tag{color:var(--mut)}
.mm-q{font-size:14px;line-height:1.85;margin:0 0 8px;font-weight:600}
.mm-steps{margin:0 0 8px;padding:0;list-style:none;display:flex;flex-direction:column;gap:6px}
.mm-steps li{font-size:13.5px;line-height:1.85;padding:6px 10px;border-radius:8px;background:var(--in);animation:mmIn .35s ease both}
.mm-steps li b.mm-sn{color:var(--sp);margin-right:6px}
.mm-ans{display:inline-flex;gap:8px;align-items:baseline;font-size:13.5px;border:1.5px solid var(--sp);border-radius:10px;padding:6px 12px;animation:mmIn .35s ease both;max-width:100%;box-sizing:border-box;flex-wrap:wrap}
.mm-ans>b{color:var(--sp);font-size:12px}
.mm-note{font-size:12.5px;line-height:1.75;color:var(--mut);margin:8px 0 0;padding-left:10px;border-left:3px solid var(--sp)}
.mm-btns{display:flex;gap:6px;flex-wrap:wrap}
.mm-terms td:first-child{font-weight:800;white-space:nowrap}
.mm-terms td:nth-child(2){font-style:italic;color:var(--mut);white-space:nowrap}
.mm-recap{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px}
.mm-recap li{font-size:13.5px;line-height:1.8}
.mm-nav{display:flex;gap:8px;justify-content:space-between;margin-top:4px;flex-wrap:wrap}
.mm-pre{display:flex;gap:6px;flex-wrap:wrap;align-items:center;font-size:12px;color:var(--mut)}
.mm-pre button{border:1px solid var(--bd);background:var(--in);border-radius:99px;padding:3px 10px;font:inherit;font-size:12px;font-weight:700;color:var(--ink);cursor:pointer}
@keyframes mmIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion: reduce){.mm-steps li,.mm-ans{animation:none}}
@supports not (background:color-mix(in srgb,red 10%,white)){.mm-why,.mm-warn,.mm-use{background:var(--in)}}
`;

/** 🎬 움직이는 그림 — 화면에 보일 때 그림 묶음을 받아 그린다 */
function Anim({ x, sp }) {
  const [Comp, setComp] = useState(null);
  const [err, setErr] = useState("");
  useEffect(() => {
    let live = true;
    loadKind(x.kind).then((C) => { if (live) setComp(() => C); }, (e) => { if (live) setErr(String(e?.message || e)); });
    return () => { live = false; };
  }, [x.kind]);
  return (
    <div className="mm-box mm-anim" style={{ "--sp": sp }}>
      <p className="mm-tag">🎬 움직이는 그림 · <R t={x.h} /></p>
      {Comp ? <Comp p={x.p || {}} /> : <div className="mm-wait">{err ? "그림을 불러오지 못했어요 — " + err : "움직이는 그림을 불러오는 중…"}</div>}
      <R as="p" className="mm-cap" t={"이렇게 보세요 — " + x.cap} />
    </div>
  );
}

function Example({ x, no, sp }) {
  const [k, setK] = useState(0);
  const all = k >= x.steps.length;
  return (
    <div className="mm-ex" style={{ "--sp": sp }}>
      <p className="mm-tag">예제 {no}</p>
      <R as="p" className="mm-q" t={x.q} />
      {k > 0 && <ol className="mm-steps">{x.steps.slice(0, k).map((s, i) => <li key={i}><b className="mm-sn">{i + 1}</b><R t={s} /></li>)}</ol>}
      {all ? (
        <>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
            <span className="mm-ans"><b>답</b><R t={x.ans} /></span>
            <button className="d-btn" onClick={() => setK(0)}>접기</button>
          </div>
          {x.note && <R as="p" className="mm-note" t={"풀이 포인트 — " + x.note} />}
        </>
      ) : (
        <div className="mm-btns">
          <button className="d-btn pri" onClick={() => setK(k + 1)}>{k ? "다음 줄" : "풀이 한 줄씩 보기"}</button>
          <button className="d-btn" onClick={() => setK(x.steps.length)}>풀이 모두 보기</button>
        </div>
      )}
    </div>
  );
}
function Practice({ x, no }) {
  const [hint, setHint] = useState(false);
  const [ans, setAns] = useState(false);
  const [sol, setSol] = useState(false);
  return (
    <div className="mm-pr">
      <p className="mm-tag">연습 {no}</p>
      <R as="p" className="mm-q" t={x.q} />
      {hint && x.hint && <p className="mm-p" style={{ fontSize: 12.5, color: "var(--mut)", margin: "0 0 8px" }}>힌트 · <R t={x.hint} /></p>}
      {sol && x.sol?.length > 0 && <ol className="mm-steps">{x.sol.map((s, i) => <li key={i}><b className="mm-sn">{i + 1}</b><R t={s} /></li>)}</ol>}
      {ans && <span className="mm-ans" style={{ "--sp": "var(--ac)" }}><b>답</b><R t={x.ans} /></span>}
      <div className="mm-btns" style={{ marginTop: ans ? 8 : 0 }}>
        {x.hint && !hint && <button className="d-btn" onClick={() => setHint(true)}>힌트</button>}
        {!ans && <button className="d-btn" onClick={() => setAns(true)}>답 보기</button>}
        {x.sol?.length > 0 && !sol && <button className="d-btn" onClick={() => { setSol(true); setAns(true); }}>풀이 보기</button>}
      </div>
    </div>
  );
}
function Theorem({ x }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="mm-box mm-thm">
      <p className="mm-tag">📐 정리 · <R t={x.name} /></p>
      <R as="p" className="mm-stmt" t={x.stmt} />
      {x.eq?.length > 0 && <div className="mm-eq">{x.eq.map((e, j) => <R key={j} as="div" t={e} />)}</div>}
      {x.proof?.length > 0 && (open
        ? <><ol className="mm-steps">{x.proof.map((s, i) => <li key={i}><b className="mm-sn">{i + 1}</b><R t={s} /></li>)}</ol>
          <button className="d-btn" onClick={() => setOpen(false)}>증명 접기</button></>
        : <button className="d-btn" onClick={() => setOpen(true)}>왜 성립할까 — 증명 보기</button>)}
    </div>
  );
}

function Block({ x, sp, no }) {
  switch (x.k) {
    case "s": return (
      <div className="d-card mm-sec">
        <h4><R t={x.h} /></h4>
        {x.p.map((p, j) => <R key={j} as="p" className="mm-p" t={p} />)}
        {x.eq?.length > 0 && <div className="mm-eq">{x.eq.map((e, j) => <R key={j} as="div" t={e} />)}</div>}
      </div>
    );
    case "why": return (
      <div className="mm-box mm-why">
        <p className="mm-tag">💡 왜 그럴까 · <R t={x.h} /></p>
        {x.p.map((p, j) => <R key={j} as="p" className="mm-p" t={p} />)}
      </div>
    );
    case "def": return (
      <div className="mm-box mm-def">
        <p className="mm-tag">📘 정의</p>
        <p className="mm-term" style={{ margin: "0 0 6px" }}><R t={x.term} />{x.en && <small>{x.en}</small>}</p>
        {x.p.map((p, j) => <R key={j} as="p" className="mm-p" t={p} />)}
        {x.eq?.length > 0 && <div className="mm-eq">{x.eq.map((e, j) => <R key={j} as="div" t={e} />)}</div>}
      </div>
    );
    case "thm": return <Theorem x={x} />;
    case "anim": return <Anim x={x} sp={sp} />;
    case "ex": return <Example x={x} no={no.ex} sp={sp} />;
    case "pr": return <Practice x={x} no={no.pr} />;
    case "warn": return (
      <div className="mm-box mm-warn">
        <p className="mm-tag" style={{ color: "#b4442e" }}>⚠ 흔한 실수</p>
        <ul>{x.items.map((t, j) => <R key={j} as="li" t={t} />)}</ul>
      </div>
    );
    case "use": return (
      <div className="mm-box mm-use">
        <p className="mm-tag" style={{ color: "#3f7d3a" }}>🏭 현장에서 · <R t={x.h} /></p>
        {x.p.map((p, j) => <R key={j} as="p" className="mm-p" t={p} />)}
      </div>
    );
    case "tbl": return (
      <div className="d-card">
        <p className="d-ct"><R t={x.h} /></p>
        <div className="mm-tw"><table className="mm-tbl"><thead><tr>{x.head.map((h, j) => <th key={j}><R t={h} /></th>)}</tr></thead>
          <tbody>{x.rows.map((r, i) => <tr key={i}>{r.map((c, j) => <td key={j}><R t={c} /></td>)}</tr>)}</tbody></table></div>
      </div>
    );
    case "code": return (
      <div className="d-card">
        <p className="d-ct"><R t={x.h} /> · {x.lang}</p>
        <pre className="mm-code">{x.code}</pre>
        {x.note && <R as="p" className="mm-note" t={x.note} />}
      </div>
    );
    default: return null;
  }
}

/** 찾기 — 책 · 장 제목 · 용어(우리말 · 영어) */
export function searchBooks(idx, q) {
  const s = q.trim().toLowerCase();
  if (!s) return null;
  const out = [];
  for (const b of idx.books) {
    if (b.title.toLowerCase().includes(s) || (b.sub || "").toLowerCase().includes(s)) out.push({ b, n: 0, label: b.sub });
    b.chapters.forEach((t, i) => { if (t.toLowerCase().includes(s)) out.push({ b, n: i + 1, label: `${i + 1}장 · ${t}` }); });
    const hit = (b.terms || []).filter((t) => t.toLowerCase().includes(s)).slice(0, 3);
    if (hit.length && !out.some((o) => o.b === b)) out.push({ b, n: 0, label: "용어 · " + hit.join(", ") });
  }
  return out.slice(0, 40);
}
const PATH = [["calc", "미적분학"], ["linalg", "선형대수"], ["mvc", "다변수 미적분"], ["ode", "미분방정식"], ["prob", "확률론"], ["stat", "통계학"]];

export function Shelf({ idx, read }) {
  const [q, setQ] = useState("");
  if (!idx) return <div className="d-card">서가를 불러오는 중…</div>;
  const found = searchBooks(idx, q);
  const fields = idx.fields || [{ id: "base", title: "전공 수학", sub: "" }];
  const have = new Set(idx.books.map((b) => b.id));
  const card = (b) => {
    const sp = TONE[b.tone] || TONE.slate, done = (read[b.id] || []).length;
    return (
      <button key={b.id} className="mm-book" style={{ "--sp": sp }} onClick={() => go(`#/seogo/jeon/${b.id}`)}>
        <span className="mm-bt">{b.title}</span>
        <span className="mm-bs">{b.sub}</span>
        <span className="mm-bm">
          <span>{b.chapters.length}장 · 예제 {b.ex} · 연습 {b.pr}{b.anim ? ` · 🎬 ${b.anim}` : ""}</span>
          <span className="mm-bar" title={`읽은 장 ${done}/${b.chapters.length}`}><i style={{ width: `${(100 * done) / b.chapters.length}%` }} /></span>
        </span>
      </button>
    );
  };
  return (
    <div className="mm-wrap">
      <p className="mm-lead">대학 전공에서 쓰는 수학을 <b>아주 기초에서부터 깊은 이론까지</b> — 장마다 이 장의 목표 · 직관(왜 그럴까) · 정의와 정리 · 🎬 움직이는 그림 · 한 줄씩 펼쳐 보는 예제 · 흔한 실수 · 현장 이야기 · 풀이가 있는 연습 · 용어 · 한 장 요약.</p>
      <input className="mm-find" type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="찾기 — 책 · 장 · 용어 (예: 고윳값, eigenvalue, 공명)" aria-label="전공 수학 찾기" />
      {found ? (
        <div className="d-card">
          {found.length === 0 ? <p className="d-note" style={{ margin: 0 }}>「{q.trim()}」에 맞는 책 · 장 · 용어가 없어요.</p>
            : found.map((f, i) => (
              <button key={i} className="mm-hit" onClick={() => go(`#/seogo/jeon/${f.b.id}${f.n ? "/" + f.n : ""}`)}>
                <b>{f.b.title}</b><small>{f.label}</small>
              </button>
            ))}
        </div>
      ) : (
        <>
          {PATH.every(([id]) => have.has(id)) && (
            <div className="d-card">
              <p className="d-ct">처음이라면 — 이 차례로</p>
              <div className="mm-path">
                {PATH.map(([id, t], i) => <span key={id} style={{ display: "contents" }}>{i > 0 && <i>→</i>}<button onClick={() => go(`#/seogo/jeon/${id}`)}>{t}</button></span>)}
              </div>
              <p className="d-note" style={{ margin: "8px 0 0" }}>전공 책(공학 · 경제 · 데이터 …)은 이 여섯 권의 언어로 쓰여 있어요. 책마다 「먼저 보면 좋은 책」이 적혀 있어요.</p>
            </div>
          )}
          {fields.map((f) => {
            const bs = idx.books.filter((b) => (b.field || "base") === f.id);
            if (!bs.length) return null;
            return (
              <div key={f.id} className="mm-field">
                <p className="mm-fh"><b>{f.title}</b><span>{f.sub}</span></p>
                <div className="mm-shelf">{bs.map(card)}</div>
              </div>
            );
          })}
        </>
      )}
    </div>
  );
}

export function Toc({ book, read, idx }) {
  const sp = TONE[book.tone] || TONE.slate, mine = new Set(read[book.id] || []);
  const title = (id) => idx?.books?.find((b) => b.id === id)?.title || id;
  const cnt = (c, k) => c.blocks.filter((x) => x.k === k).length;
  return (
    <div className="mm-wrap" style={{ "--sp": sp }}>
      <button className="mm-back" onClick={() => go("#/seogo/jeon")}>← 서가</button>
      <div className="mm-hd"><h3>{book.title}</h3><p>{book.sub}</p></div>
      <div className="d-card">
        <R as="p" className="mm-intro" t={book.intro} />
        <p className="d-note" style={{ margin: "8px 0 0" }}>이런 분께 — {book.who}</p>
        {book.pre?.length > 0 && (
          <div className="mm-pre" style={{ marginTop: 8 }}>먼저 보면 좋은 책 {book.pre.map((id) => <button key={id} onClick={() => go(`#/seogo/jeon/${id}`)}>{title(id)}</button>)}</div>
        )}
      </div>
      <div className="d-card"><p className="d-ct">차례 · 읽은 장 {mine.size}/{book.chapters.length}</p>
        <div className="mm-toc">
          {book.chapters.map((c) => (
            <button key={c.n} className="mm-ch" onClick={() => go(`#/seogo/jeon/${book.id}/${c.n}`)}>
              <span className={"mm-no" + (mine.has(c.n) ? " on" : "")}>{c.n}</span>
              <span>
                <span className="mm-ct">{c.title}</span><R as="div" className="mm-cs" t={c.sum} />
                <span className="mm-badges">
                  {cnt(c, "anim") > 0 && <span>🎬 {cnt(c, "anim")}</span>}
                  <span>예제 {cnt(c, "ex")}</span>
                  {cnt(c, "pr") > 0 && <span>연습 {cnt(c, "pr")}</span>}
                  {cnt(c, "thm") > 0 && <span>정리 {cnt(c, "thm")}</span>}
                </span>
              </span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export function Chapter({ book, n, onRead }) {
  const sp = TONE[book.tone] || TONE.slate;
  const c = book.chapters.find((x) => x.n === n);
  useEffect(() => { if (c) onRead(book.id, n); }, [book.id, n]);   // eslint-disable-line react-hooks/exhaustive-deps
  if (!c) return <div className="d-card">없는 장이에요. <button className="mm-back" onClick={() => go(`#/seogo/jeon/${book.id}`)}>차례로</button></div>;
  const no = { ex: 0, pr: 0 };
  const last = book.chapters.length;
  const goPre = (ref) => { const [b, k] = String(ref).split(":"); go(`#/seogo/jeon/${b}${k ? "/" + k : ""}`); };
  return (
    <div className="mm-wrap" style={{ "--sp": sp }}>
      <button className="mm-back" onClick={() => go(`#/seogo/jeon/${book.id}`)}>← {book.title} 차례</button>
      <div className="mm-hd"><h3>{n}. {c.title}</h3><R as="p" t={c.sum} /></div>
      {(c.goals?.length > 0 || c.pre?.length > 0) && (
        <div className="d-card">
          {c.goals?.length > 0 && <><p className="d-ct">이 장의 목표</p><ul className="mm-goals">{c.goals.map((g, i) => <R key={i} as="li" t={g} />)}</ul></>}
          {c.pre?.length > 0 && <div className="mm-pre" style={{ marginTop: c.goals?.length ? 10 : 0 }}>먼저 보면 좋은 곳 {c.pre.map((r) => <button key={r} onClick={() => goPre(r)}>{r.replace(":", " · ") + (r.includes(":") ? "장" : "")}</button>)}</div>}
        </div>
      )}
      {c.blocks.map((x, i) => {
        if (x.k === "ex") no.ex++;
        if (x.k === "pr") no.pr++;
        return <Block key={i} x={x} sp={sp} no={{ ...no }} />;
      })}
      {c.terms?.length > 0 && (
        <div className="d-card">
          <p className="d-ct">용어</p>
          <div className="mm-tw"><table className="mm-tbl mm-terms"><tbody>
            {c.terms.map(([ko, en, mean], i) => <tr key={i}><td>{ko}</td><td>{en}</td><td><R t={mean} /></td></tr>)}
          </tbody></table></div>
        </div>
      )}
      {c.recap?.length > 0 && (
        <div className="d-card" style={{ borderColor: sp }}>
          <p className="d-ct" style={{ color: sp }}>한 장 요약</p>
          <ul className="mm-recap">{c.recap.map((t, i) => <R key={i} as="li" t={t} />)}</ul>
        </div>
      )}
      <div className="mm-nav">
        {n > 1 ? <button className="d-btn" onClick={() => go(`#/seogo/jeon/${book.id}/${n - 1}`)}>← {n - 1}장</button> : <span />}
        {n < last ? <button className="d-btn pri" onClick={() => go(`#/seogo/jeon/${book.id}/${n + 1}`)}>{n + 1}장 →</button>
          : <button className="d-btn" onClick={() => go("#/seogo/jeon")}>서가로</button>}
      </div>
    </div>
  );
}

export default function MajorMath() {
  const [, , h] = useAppHash();
  const seg = h.split("/");                 // seogo / jeon / <책> / <장>
  const bookId = seg[2] || "", n = Number(seg[3] || 0) || 0;
  const [idx, setIdx] = useState(null);
  const [book, setBook] = useState(null);
  const [err, setErr] = useState("");
  const [read, setRead] = useState(loadRead);
  useEffect(ensureMathCss, []);
  useEffect(() => { getJSON(`${BASE}/index.json`).then(setIdx, (e) => setErr(String(e.message || e))); }, []);
  useEffect(() => {
    let alive = true;
    setBook(null);
    if (bookId) getJSON(`${BASE}/${bookId}.json`).then((b) => alive && setBook(b), (e) => alive && setErr(String(e.message || e)));
    return () => { alive = false; };
  }, [bookId]);
  useEffect(() => { if (typeof window !== "undefined" && window.scrollTo) window.scrollTo(0, 0); }, [bookId, n]);
  const onRead = (id, k) => setRead((r) => {
    if ((r[id] || []).includes(k)) return r;
    const nx = { ...r, [id]: [...(r[id] || []), k].sort((a, b) => a - b) };
    saveRead(nx);
    return nx;
  });

  let body;
  if (err) body = <div className="d-card">전공 수학 서가를 불러오지 못했어요 — {err}</div>;
  else if (!bookId) body = <Shelf idx={idx} read={read} />;
  else if (!book) body = <div className="d-card">책을 펴는 중…</div>;
  else if (!n) body = <Toc book={book} read={read} idx={idx} />;
  else body = <Chapter book={book} n={n} onRead={onRead} />;
  return <><style>{CSS}</style>{body}</>;
}
