// 서고 › 전공 수학 — 대학 전공 수학 서가(대학수학 · 경제수학 · 무역학 · 기계공학 · 천문공학 · 전자공학 · 데이터 공학 · 물리학 · 통계학)
// 책은 public/majors/<책 id>.json(생성기 majorgen/ — python3 majorgen/build.py). DB 를 쓰지 않는다.
// 주소: #/seogo/jeon(서가) · #/seogo/jeon/<책>(차례) · #/seogo/jeon/<책>/<장>(본문)
// 본문: 이론 단락(문단 + 공식 상자) · 예제(풀이를 한 줄씩 펼치기 → 답) · 연습(답 보기). 수식은 MathIR 표식(components/MathText — 분수는 상하로).
// 읽은 장은 이 기기에만 표시(localStorage — 막히면 표시 없이). 서가 · 차례 · 장 조각(Shelf · Toc · Chapter)은 검산(tests/majors.test.mjs)이 따로 그린다.
import { useEffect, useMemo, useState } from "react";
import { useAppHash, go } from "../../../shared/demo";
import { mathHtml, ensureMathCss } from "../../../components/MathText";

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

const READ_KEY = "srk.majors.read";
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
.mm-wrap{display:flex;flex-direction:column;gap:12px}
.mm-lead{font-size:13px;color:var(--mut);line-height:1.7;margin:0}
.mm-shelf{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
.mm-book{position:relative;text-align:left;background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:14px 14px 12px 20px;cursor:pointer;font-family:inherit;color:var(--ink);display:flex;flex-direction:column;gap:6px;min-height:150px}
.mm-book:hover{border-color:var(--sp)}
.mm-book::before{content:"";position:absolute;left:0;top:0;bottom:0;width:7px;border-radius:14px 0 0 14px;background:var(--sp)}
.mm-bt{font-size:16px;font-weight:800;letter-spacing:.01em}
.mm-bs{font-size:12px;color:var(--mut);line-height:1.55}
.mm-bm{margin-top:auto;display:flex;gap:6px;flex-wrap:wrap;align-items:center;font-size:11px;color:var(--mut)}
.mm-bar{height:5px;background:var(--in);border-radius:99px;overflow:hidden;flex:1;min-width:50px}
.mm-bar>i{display:block;height:100%;background:var(--sp)}
.mm-back{background:none;border:0;color:var(--ac);font-weight:800;font-size:12.5px;cursor:pointer;padding:2px 0;font-family:inherit;align-self:flex-start}
.mm-hd{border-left:6px solid var(--sp);padding:2px 0 2px 12px}
.mm-hd h3{margin:0;font-size:18px}
.mm-hd p{margin:4px 0 0;font-size:12.5px;color:var(--mut);line-height:1.6}
.mm-intro{font-size:13.5px;line-height:1.85;margin:0}
.mm-toc{display:flex;flex-direction:column}
.mm-ch{display:flex;gap:12px;align-items:flex-start;padding:11px 2px;border-bottom:1px solid var(--bd);cursor:pointer;background:none;border-left:0;border-right:0;border-top:0;text-align:left;font-family:inherit;color:var(--ink)}
.mm-ch:last-child{border-bottom:0}
.mm-no{flex:0 0 auto;width:28px;height:28px;border-radius:99px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12.5px;border:1.5px solid var(--sp);color:var(--sp)}
.mm-no.on{background:var(--sp);color:var(--bg)}
.mm-ct{font-size:14px;font-weight:800}
.mm-cs{font-size:12px;color:var(--mut);margin-top:3px;line-height:1.55}
.mm-sec h4{margin:4px 0 8px;font-size:15px;display:flex;align-items:center;gap:8px}
.mm-sec h4::before{content:"";width:4px;height:15px;border-radius:2px;background:var(--sp)}
.mm-p{font-size:14px;line-height:1.95;margin:0 0 10px}
.mm-eq{background:var(--in);border:1px solid var(--bd);border-radius:10px;padding:10px 14px;margin:4px 0 12px;display:flex;flex-direction:column;gap:8px;overflow-x:auto}
.mm-eq>div{font-size:14.5px;line-height:1.9;white-space:nowrap;text-align:center}
.mm-ex,.mm-pr{border:1px solid var(--bd);border-radius:12px;padding:12px 14px;background:var(--card)}
.mm-ex{border-color:var(--sp)}
.mm-tag{font-size:11px;font-weight:800;letter-spacing:.05em;color:var(--sp);margin:0 0 6px}
.mm-pr .mm-tag{color:var(--mut)}
.mm-q{font-size:14px;line-height:1.85;margin:0 0 8px;font-weight:600}
.mm-steps{margin:0 0 8px;padding:0;list-style:none;display:flex;flex-direction:column;gap:6px}
.mm-steps li{font-size:13.5px;line-height:1.85;padding:6px 10px;border-radius:8px;background:var(--in);animation:mmIn .35s ease both}
.mm-steps li b.mm-sn{color:var(--sp);margin-right:6px}
.mm-ans{display:inline-flex;gap:8px;align-items:baseline;font-size:13.5px;border:1.5px solid var(--sp);border-radius:10px;padding:6px 12px;animation:mmIn .35s ease both}
.mm-ans>b{color:var(--sp);font-size:12px}
.mm-btns{display:flex;gap:6px;flex-wrap:wrap}
.mm-nav{display:flex;gap:8px;justify-content:space-between;margin-top:4px}
@keyframes mmIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion: reduce){.mm-steps li,.mm-ans{animation:none}}
`;

function Example({ x, no, sp }) {
  const [k, setK] = useState(0);
  const all = k >= x.steps.length;
  return (
    <div className="mm-ex" style={{ "--sp": sp }}>
      <p className="mm-tag">예제 {no}</p>
      <R as="p" className="mm-q" t={x.q} />
      {k > 0 && <ol className="mm-steps">{x.steps.slice(0, k).map((s, i) => <li key={i}><b className="mm-sn">{i + 1}</b><R t={s} /></li>)}</ol>}
      {all ? (
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
          <span className="mm-ans"><b>답</b><R t={x.ans} /></span>
          <button className="d-btn" onClick={() => setK(0)}>접기</button>
        </div>
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
  return (
    <div className="mm-pr">
      <p className="mm-tag">연습 {no}</p>
      <R as="p" className="mm-q" t={x.q} />
      {hint && x.hint && <p className="mm-p" style={{ fontSize: 12.5, color: "var(--mut)", margin: "0 0 8px" }}>힌트 · <R t={x.hint} /></p>}
      {ans ? <span className="mm-ans" style={{ "--sp": "var(--ac)" }}><b>답</b><R t={x.ans} /></span> : (
        <div className="mm-btns">
          {x.hint && !hint && <button className="d-btn" onClick={() => setHint(true)}>힌트</button>}
          <button className="d-btn" onClick={() => setAns(true)}>답 보기</button>
        </div>
      )}
    </div>
  );
}

export function Shelf({ idx, read }) {
  if (!idx) return <div className="d-card">서가를 불러오는 중…</div>;
  return (
    <div className="mm-wrap">
      <p className="mm-lead">대학 전공에서 쓰는 수학을 <b>아주 기초에서부터 다소 깊은 이론까지</b> 차례로 — 장마다 이론 · 공식 상자 · 한 줄씩 펼쳐 보는 예제 · 연습 문제. 모든 책의 바탕은 「대학수학」이에요.</p>
      <div className="mm-shelf">
        {idx.books.map((b) => {
          const sp = TONE[b.tone] || TONE.slate, done = (read[b.id] || []).length;
          return (
            <button key={b.id} className="mm-book" style={{ "--sp": sp }} onClick={() => go(`#/seogo/jeon/${b.id}`)}>
              <span className="mm-bt">{b.title}</span>
              <span className="mm-bs">{b.sub}</span>
              <span className="mm-bm">
                <span>{b.chapters.length}장 · 예제 {b.ex} · 연습 {b.pr}</span>
                <span className="mm-bar" title={`읽은 장 ${done}/${b.chapters.length}`}><i style={{ width: `${(100 * done) / b.chapters.length}%` }} /></span>
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

export function Toc({ book, read }) {
  const sp = TONE[book.tone] || TONE.slate, mine = new Set(read[book.id] || []);
  return (
    <div className="mm-wrap" style={{ "--sp": sp }}>
      <button className="mm-back" onClick={() => go("#/seogo/jeon")}>← 서가</button>
      <div className="mm-hd"><h3>{book.title}</h3><p>{book.sub}</p></div>
      <div className="d-card"><R as="p" className="mm-intro" t={book.intro} /><p className="d-note" style={{ margin: "8px 0 0" }}>이런 분께 — {book.who}</p></div>
      <div className="d-card"><p className="d-ct">차례</p>
        <div className="mm-toc">
          {book.chapters.map((c) => (
            <button key={c.n} className="mm-ch" onClick={() => go(`#/seogo/jeon/${book.id}/${c.n}`)}>
              <span className={"mm-no" + (mine.has(c.n) ? " on" : "")}>{c.n}</span>
              <span><span className="mm-ct">{c.title}</span><R as="div" className="mm-cs" t={c.sum} /></span>
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
  let ne = 0, np = 0;
  const last = book.chapters.length;
  return (
    <div className="mm-wrap" style={{ "--sp": sp }}>
      <button className="mm-back" onClick={() => go(`#/seogo/jeon/${book.id}`)}>← {book.title} 차례</button>
      <div className="mm-hd"><h3>{n}. {c.title}</h3><R as="p" t={c.sum} /></div>
      {c.blocks.map((x, i) => {
        if (x.k === "s") return (
          <div key={i} className="d-card mm-sec">
            <h4>{x.h}</h4>
            {x.p.map((p, j) => <R key={j} as="p" className="mm-p" t={p} />)}
            {x.eq?.length > 0 && <div className="mm-eq">{x.eq.map((e, j) => <R key={j} as="div" t={e} />)}</div>}
          </div>
        );
        if (x.k === "ex") return <Example key={i} x={x} no={++ne} sp={sp} />;
        if (x.k === "pr") return <Practice key={i} x={x} no={++np} />;
        return null;
      })}
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
  else if (!n) body = <Toc book={book} read={read} />;
  else body = <Chapter book={book} n={n} onRead={onRead} />;
  return <><style>{CSS}</style>{body}</>;
}
