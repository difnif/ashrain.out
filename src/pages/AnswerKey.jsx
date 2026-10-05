// ashrain.out — 기말 대비 빠른 정답지 (경로 /answers · 로그인 없이 열람)
// 교재 2권 × 파트 5개(교과서 기출·빈출 유형·서술형·고난도·실전 모의고사). 정답 가리기, 서술형은 문항별 해설 이미지.
// 데이터: src/data/answerKey.js · 해설 이미지: public/answer-key/sol/
import { useEffect, useMemo, useState } from "react";
import { BOOKS } from "../data/answerKey";

const CSS = `
.ak-root { min-height: 100vh; background: var(--bg); color: var(--ink);
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif;
  font-size: 15px; line-height: 1.45; -webkit-tap-highlight-color: transparent; }
.ak-root * { box-sizing: border-box; }
.ak-light { --bg:#F3F2EE; --card:#fff; --ink:#1D1F24; --mut:#6B6E76; --bd:#E2E0DA; --soft:#ECEBE6; --cover:#D9D7D0;
  --p0:#C75A2F; --p1:#A3134D; --p2:#2F8A5F; --p3:#2F5FAE; --p4:#5A3B9C; }
.ak-dark { --bg:#15161A; --card:#1E2026; --ink:#ECEBE7; --mut:#9A9CA4; --bd:#2E3038; --soft:#262830; --cover:#3A3C45;
  --p0:#E98A5F; --p1:#E2648F; --p2:#5CC28F; --p3:#78A3EE; --p4:#A98AE6; color-scheme: dark; }
.ak-wrap { max-width: 720px; margin: 0 auto; padding: 14px 16px 48px; }
.ak-top { display: flex; align-items: center; gap: 10px; padding-top: 4px; }
.ak-back { border: 0; background: var(--soft); color: var(--ink); width: 34px; height: 34px; border-radius: 50%;
  font-size: 17px; cursor: pointer; flex: 0 0 auto; }
.ak-top h1 { font-size: 19px; font-weight: 800; margin: 0; letter-spacing: -.01em; }
.ak-top p { color: var(--mut); font-size: 12.5px; margin: 1px 0 0; }
.ak-bar { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--bg);
  margin: 10px -16px 0; padding: 10px 16px; border-bottom: 1px solid var(--bd); display: grid; gap: 10px; }
.ak-seg { display: grid; grid-template-columns: 1fr 1fr; background: var(--soft); border-radius: 12px; padding: 3px; gap: 3px; }
.ak-seg button { border: 0; background: transparent; color: var(--mut); font: inherit; font-weight: 700; font-size: 13.5px;
  line-height: 1.25; padding: 9px 6px; border-radius: 9px; cursor: pointer; min-width: 0; }
.ak-seg button small { display: block; font-weight: 400; font-size: 11px; opacity: .85; }
.ak-seg button[aria-pressed="true"] { background: var(--card); color: var(--ink); box-shadow: 0 1px 2px rgba(0,0,0,.12); }
.ak-chips { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; margin: 0 -16px; padding: 0 16px; }
.ak-chips::-webkit-scrollbar { display: none; }
.ak-chip { flex: 0 0 auto; border: 1.5px solid var(--bd); background: var(--card); color: var(--ink); font: inherit;
  font-weight: 700; font-size: 13px; padding: 7px 13px; border-radius: 999px; cursor: pointer; display: flex; align-items: center; gap: 6px; }
.ak-chip i { width: 8px; height: 8px; border-radius: 50%; background: var(--c); }
.ak-chip[aria-pressed="true"] { background: var(--c); border-color: var(--c); color: #fff; }
.ak-chip[aria-pressed="true"] i { background: #fff; }
.ak-tools { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.ak-jump { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; min-width: 0; flex: 1; }
.ak-jump::-webkit-scrollbar { display: none; }
.ak-jump button { flex: 0 0 auto; font: inherit; font-size: 12px; color: var(--mut); background: transparent;
  border: 1px solid var(--bd); border-radius: 7px; padding: 3px 8px; cursor: pointer; }
.ak-toggle { display: flex; align-items: center; gap: 7px; font-size: 12.5px; color: var(--mut); cursor: pointer; user-select: none; flex: 0 0 auto; }
.ak-toggle input { appearance: none; -webkit-appearance: none; width: 34px; height: 20px; border-radius: 999px; background: var(--bd);
  position: relative; margin: 0; cursor: pointer; transition: background .15s; }
.ak-toggle input::after { content: ""; position: absolute; top: 2px; left: 2px; width: 16px; height: 16px; border-radius: 50%;
  background: var(--card); box-shadow: 0 1px 2px rgba(0,0,0,.25); transition: transform .15s; }
.ak-toggle input:checked { background: var(--cur); }
.ak-toggle input:checked::after { transform: translateX(14px); }
.ak-root button:focus-visible, .ak-toggle input:focus-visible { outline: 2px solid var(--cur); outline-offset: 2px; }
.ak-list { display: grid; gap: 14px; margin-top: 14px; }
.ak-unit { background: var(--card); border-radius: 14px; overflow: hidden; border: 1px solid var(--bd); scroll-margin-top: 170px; }
.ak-uh { display: flex; justify-content: space-between; align-items: baseline; gap: 10px; padding: 11px 14px 9px; border-bottom: 2px solid var(--cur); }
.ak-uh h2 { font-size: 15px; font-weight: 800; margin: 0; min-width: 0; }
.ak-uh span { flex: 0 0 auto; font-size: 11.5px; color: var(--mut); font-variant-numeric: tabular-nums; }
.ak-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(104px, 1fr)); }
@media (min-width: 560px) { .ak-grid { grid-template-columns: repeat(4, 1fr); } }
.ak-cell { display: flex; align-items: center; gap: 8px; padding: 9px 12px; min-height: 46px; position: relative;
  border: 0; border-bottom: 1px solid var(--bd); border-right: 1px solid var(--bd); background: transparent;
  font: inherit; color: inherit; text-align: left; min-width: 0; }
.ak-no { flex: 0 0 auto; width: 20px; font-weight: 700; font-size: 12.5px; color: var(--cur); font-variant-numeric: tabular-nums; }
.ak-ans { font-family: 'Noto Serif KR', 'Times New Roman', 'Pretendard Variable', Pretendard, serif; font-size: 16.5px; font-weight: 500;
  min-width: 0; overflow-wrap: anywhere; display: inline-flex; align-items: center; flex-wrap: wrap; gap: 1px; }
.ak-frac { display: inline-flex; flex-direction: column; align-items: center; font-size: 13.5px; line-height: 1.08; margin: 0 2px; }
.ak-frac b { font-weight: 500; padding: 0 2px; }
.ak-frac b:first-child { border-bottom: 1.3px solid currentColor; padding-bottom: 1px; }
.ak-ans sup { font-size: .62em; line-height: 0; }
.ak-sol .ak-cell { cursor: pointer; padding-right: 22px; }
.ak-sol .ak-cell::after { content: "›"; position: absolute; right: 9px; top: 50%; transform: translateY(-52%);
  font-size: 18px; color: var(--cur); opacity: .7; }
.ak-hide .ak-cell { cursor: pointer; }
.ak-hide .ak-cell .ak-ans { visibility: hidden; position: relative; }
.ak-hide .ak-cell .ak-ans::before { content: ""; visibility: visible; position: absolute; inset: 3px -2px; border-radius: 5px; background: var(--cover); }
.ak-hide .ak-cell.open .ak-ans { visibility: visible; }
.ak-hide .ak-cell.open .ak-ans::before { display: none; }
.ak-foot { color: var(--mut); font-size: 12px; text-align: center; margin-top: 22px; }
.ak-sheet { position: fixed; inset: 0; z-index: 50; background: var(--bg); display: flex; flex-direction: column; }
.ak-sh-top { display: flex; align-items: center; gap: 10px; padding: calc(env(safe-area-inset-top, 0px) + 10px) 16px 10px;
  border-bottom: 2px solid var(--cur); background: var(--card); }
.ak-sh-top > div { flex: 1; min-width: 0; }
.ak-sh-top b { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; font-size: 15px; }
.ak-sh-top b .ak-ans { color: var(--cur); font-weight: 600; font-size: 17px; }
.ak-sh-top small { color: var(--mut); font-size: 12px; }
.ak-sh-body { flex: 1; overflow: auto; padding: 14px 16px; -webkit-overflow-scrolling: touch; }
.ak-paper { background: #fff; border-radius: 10px; padding: 10px; max-width: 720px; margin: 0 auto; }
.ak-paper img { display: block; width: 100%; height: auto; }
.ak-sh-nav { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; padding: 10px 16px calc(env(safe-area-inset-bottom, 0px) + 10px);
  border-top: 1px solid var(--bd); background: var(--card); }
.ak-sh-nav button { border: 1.5px solid var(--bd); background: var(--card); color: var(--ink); font: inherit; font-weight: 700;
  font-size: 14px; padding: 11px; border-radius: 10px; cursor: pointer; }
.ak-sh-nav button:disabled { opacity: .35; cursor: default; }
@media (prefers-reduced-motion: reduce) { .ak-root * { transition: none !important; } }
`;

const PC = ["--p0", "--p1", "--p2", "--p3", "--p4"];
const store = {
  get(k) { try { return localStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, String(v)); } catch { /* 저장 불가 환경 */ } },
};
const pad2 = (n) => String(n).padStart(2, "0");

// "{2/3}", "-{11/2}", "64 cm^2", "-3" → React 노드
function Ans({ a }) {
  const out = [];
  const re = /\{(\d+)\/(\d+)\}|\^(\d)/g;
  let s = a.replace(/(^|[\s(])-(?=[\d{])/g, "$1−");
  let last = 0, m, k = 0;
  while ((m = re.exec(s))) {
    if (m.index > last) out.push(s.slice(last, m.index));
    if (m[1]) out.push(<span key={k++} className="ak-frac"><b>{m[1]}</b><b>{m[2]}</b></span>);
    else out.push(<sup key={k++}>{m[3]}</sup>);
    last = re.lastIndex;
  }
  if (last < s.length) out.push(s.slice(last));
  return <span className="ak-ans">{out}</span>;
}
const spoken = (a) => a.replace(/\{(\d+)\/(\d+)\}/g, "$2분의 $1").replace(/\^2/, " 제곱").replace(/\^3/, " 세제곱");

function goHome() {
  if (history.length > 1) { history.back(); return; }
  history.replaceState(null, "", "/");
  window.dispatchEvent(new Event("pathchange"));
}

export default function AnswerKey({ theme = "light" }) {
  const [bi, setBi] = useState(() => { const v = +(store.get("ak_book") || 0); return BOOKS[v] ? v : 0; });
  const [pi, setPi] = useState(() => { const v = +(store.get("ak_part") || 0); return v >= 0 && v < 5 ? v : 0; });
  const [hide, setHide] = useState(false);
  const [open, setOpen] = useState(() => new Set());
  const [sheet, setSheet] = useState(null); // 서술형 해설: 평탄화 목록의 인덱스

  const book = BOOKS[bi];
  const part = book.parts[pi] || book.parts[0];
  const flat = useMemo(() => part.sections.flatMap((s, si) =>
    s[2].split("|").map((a, q) => ({ si, q, a, t: s[0] }))), [part]);
  const total = flat.length;

  useEffect(() => { document.title = "빠른 정답지 · ashrain.out"; }, []);
  useEffect(() => { setOpen(new Set()); setSheet(null); }, [bi, pi, hide]);
  useEffect(() => {
    if (sheet == null) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const onKey = (e) => {
      if (e.key === "Escape") setSheet(null);
      if (e.key === "ArrowRight") setSheet((i) => Math.min(i + 1, total - 1));
      if (e.key === "ArrowLeft") setSheet((i) => Math.max(i - 1, 0));
    };
    window.addEventListener("keydown", onKey);
    return () => { document.body.style.overflow = prev; window.removeEventListener("keydown", onKey); };
  }, [sheet, total]);

  const pickBook = (i) => { setBi(i); store.set("ak_book", i); window.scrollTo({ top: 0 }); };
  const pickPart = (i) => { setPi(i); store.set("ak_part", i); window.scrollTo({ top: 0 }); };
  const tapCell = (si, q) => {
    const key = `${si}-${q}`;
    if (hide && !open.has(key)) { setOpen((o) => new Set(o).add(key)); return; }
    if (part.sol) { setSheet(flat.findIndex((x) => x.si === si && x.q === q)); return; }
    if (hide) setOpen((o) => { const n = new Set(o); n.delete(key); return n; });
  };

  const cur = { "--cur": `var(${PC[pi]})` };
  const it = sheet != null ? flat[sheet] : null;

  return (
    <div className={`ak-root ak-${theme === "dark" ? "dark" : "light"}`} style={cur}>
      <style>{CSS}</style>
      <div className="ak-wrap">
        <header className="ak-top">
          <button type="button" className="ak-back" onClick={goHome} aria-label="뒤로">←</button>
          <div>
            <h1>빠른 정답지</h1>
            <p>정답만 빠르게 · 서술형은 문항을 누르면 해설이 열려요</p>
          </div>
        </header>

        <div className="ak-bar">
          <div className="ak-seg" role="group" aria-label="교재 선택">
            {BOOKS.map((b, i) => (
              <button key={b.id} type="button" aria-pressed={i === bi} onClick={() => pickBook(i)}>
                {b.name}<small>{b.short}</small>
              </button>
            ))}
          </div>
          <div className="ak-chips" role="group" aria-label="파트 선택">
            {book.parts.map((p, i) => (
              <button key={p.name} type="button" className="ak-chip" style={{ "--c": `var(${PC[i]})` }}
                aria-pressed={i === pi} onClick={() => pickPart(i)}><i />{p.name}</button>
            ))}
          </div>
          <div className="ak-tools">
            <nav className="ak-jump" aria-label="단원 바로가기">
              {part.sections.map((s, i) => (
                <button key={i} type="button"
                  onClick={() => document.getElementById(`ak-u${i}`)?.scrollIntoView({ behavior: "smooth", block: "start" })}>
                  {s[0].split(".")[0].replace("실전 모의고사 ", "")}
                </button>
              ))}
            </nav>
            <label className="ak-toggle" htmlFor="ak-hide">
              <input type="checkbox" id="ak-hide" checked={hide} onChange={(e) => setHide(e.target.checked)} />정답 가리기
            </label>
          </div>
        </div>

        <main className={`ak-list${hide ? " ak-hide" : ""}`}>
          {part.sections.map((s, si) => {
            const ans = s[2].split("|");
            return (
              <section key={`${bi}-${pi}-${si}`} id={`ak-u${si}`} className={`ak-unit${part.sol ? " ak-sol" : ""}`}>
                <div className="ak-uh"><h2>{s[0]}</h2><span>본문 {s[1]}쪽 · {ans.length}문항</span></div>
                <div className="ak-grid">
                  {ans.map((a, q) => (
                    <button key={q} type="button" className={`ak-cell${open.has(`${si}-${q}`) ? " open" : ""}`}
                      aria-label={`${q + 1}번 정답 ${spoken(a)}`} onClick={() => tapCell(si, q)}>
                      <span className="ak-no">{pad2(q + 1)}</span><Ans a={a} />
                    </button>
                  ))}
                </div>
              </section>
            );
          })}
        </main>
        <p className="ak-foot">{book.name} · {part.name} · 총 {total}문항</p>
      </div>

      {it && (
        <div className="ak-sheet" role="dialog" aria-modal="true" aria-label={`${it.t} ${it.q + 1}번 해설`}>
          <div className="ak-sh-top">
            <div>
              <b>{pad2(it.q + 1)}번 · 정답 <Ans a={it.a} /></b>
              <small>{part.name} · {it.t}</small>
            </div>
            <button type="button" className="ak-back" onClick={() => setSheet(null)} aria-label="해설 닫기">✕</button>
          </div>
          <div className="ak-sh-body" key={sheet}>
            <div className="ak-paper">
              <img src={`/answer-key/sol/${part.sol}${it.si}-${pad2(it.q + 1)}.png`} alt={`${it.t} ${it.q + 1}번 해설`} />
            </div>
          </div>
          <div className="ak-sh-nav">
            <button type="button" disabled={sheet === 0} onClick={() => setSheet(sheet - 1)}>← 이전 문항</button>
            <button type="button" disabled={sheet === total - 1} onClick={() => setSheet(sheet + 1)}>다음 문항 →</button>
          </div>
        </div>
      )}
    </div>
  );
}
