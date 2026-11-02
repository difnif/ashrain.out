// ashrain.out — 컨셉 문제 「해설지 바로 보기」(#/sets/<범주>/<NN>/sol[?no=N])
// 인쇄용 해설지 HTML(public/concept-sets/<범주>/print/NN-solutions.html — PDF 를 찍은 바로 그 문서)을 shadow DOM 에 넣어
// 화면 폭에 맞춰 펼친다. 휴대폰에서도 첫 쪽의 빠른 정답 50칸이 한눈에 들어온다.
//   · 확대: 폭 맞춤 × 1 · 1.25 · 1.5 · 2 (종이처럼 풀기와 같은 단계)
//   · 번호로 가기 · 빠른 정답의 번호 칸을 누르면 그 문항의 해설로 간다. ?no=N 이면 열자마자 그 문항으로.
//   · 인쇄 · 다운로드는 세트 화면의 「자료」와 같다(여기서는 해설지만 바로 인쇄).
import { useCallback, useEffect, useRef, useState } from "react";
import { pad2, printUrl } from "../../lib/conceptsets";
import { splitDoc, scopeCss, openPrintWindow, failPrintWindow } from "./printdoc";
import { ensureLinks, PAGE_W_PX } from "./paper";
import { ensureSerif, printDocs } from "./common";

const ZOOMS = [1, 1.25, 1.5, 2];
const ZK = "ash.cs.sol.zoom";
const lsGet = (k, d) => { try { return localStorage.getItem(k) ?? d; } catch { return d; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, String(v)); } catch { /* 무시 */ } };

export const SOL_VIEW_CSS = `
:host { display: block; }
.csx-s { min-width: max-content; }
.keyt td.n { cursor: pointer; -webkit-tap-highlight-color: transparent; }
.keyt td.n:active { background: #cfeee7; }
.sol { scroll-margin-top: 72px; }
.sol.cs-hit { animation: csHit 1.8s ease-out; }
@keyframes csHit { 0% { background: rgba(255, 214, 102, .55); } 100% { background: transparent; } }
@media (hover: hover) { .keyt td.n:hover { background: #dff3ee; } }
`;

export default function SolView({ catId, set, at, say }) {
  const hostRef = useRef(null), boxRef = useRef(null), wrapRef = useRef(null), rootRef = useRef(null);
  const [ready, setReady] = useState(false);
  const [err, setErr] = useState(null);
  const [jump, setJump] = useState(false);
  const [busy, setBusy] = useState(false);
  const [zi, setZi] = useState(() => { const v = Number(lsGet(ZK, 0)); return v >= 0 && v < ZOOMS.length ? v : 0; });

  const go = useCallback((no) => {
    const it = set.items.find((x) => x.no === no);
    const el = it && rootRef.current?.getElementById?.(`s-${it.id}`);
    if (!el) return;
    el.scrollIntoView({ behavior: "smooth", block: "start" });
    el.classList.remove("cs-hit");
    void el.offsetWidth;                           // 같은 문항을 다시 눌러도 깜빡이게
    el.classList.add("cs-hit");
  }, [set]);
  const goRef = useRef(go);
  goRef.current = go;

  // 해설지 HTML 불러와 shadow 에 펼치기
  useEffect(() => {
    let alive = true;
    ensureSerif();
    fetch(printUrl(catId, set.no, "solutions"), { cache: "no-cache" })
      .then((r) => { if (!r.ok) throw new Error(`해설지를 불러오지 못했어요 (${r.status})`); return r.text(); })
      .then((html) => {
        if (!alive || !hostRef.current) return;
        const doc = splitDoc(html);
        ensureLinks(doc.links);
        const root = hostRef.current.shadowRoot || hostRef.current.attachShadow({ mode: "open" });
        const css = doc.css.map((c) => scopeCss(c, ".csx-s")).join("\n");
        root.innerHTML = `<style>${css}</style><style>${SOL_VIEW_CSS}</style><div class="csx-s">${doc.body}</div>`;
        rootRef.current = root;
        wrapRef.current = root.querySelector(".csx-s");
        // 빠른 정답의 번호 칸 → 그 해설로
        root.addEventListener("click", (e) => {
          const td = e.target.closest?.(".keyt td.n");
          if (td) goRef.current(Number(td.textContent));
        });
        setReady(true);
      })
      .catch((e) => { if (alive) setErr(e?.message || String(e)); });
    return () => { alive = false; };
  }, [catId, set]);

  // 확대: 폭 맞춤 × 배수
  const fit = useCallback(() => {
    const box = boxRef.current, w = wrapRef.current;
    if (!box || !w) return;
    const z = Math.max(0.3, (box.clientWidth - 8) / PAGE_W_PX) * ZOOMS[zi];
    w.style.zoom = z.toFixed(4);
  }, [zi]);
  useEffect(() => { if (ready) fit(); }, [ready, fit]);
  useEffect(() => {
    const on = () => fit();
    window.addEventListener("resize", on);
    return () => window.removeEventListener("resize", on);
  }, [fit]);
  useEffect(() => { lsSet(ZK, zi); }, [zi]);
  useEffect(() => { if (ready && at) setTimeout(() => go(at), 120); }, [ready, at, go]);

  const onPrint = () => {
    const win = openPrintWindow();
    if (!win) { say?.("새 창이 막혔어요 — 브라우저에서 이 사이트의 팝업을 허용해 주세요"); return; }
    setBusy(true);
    printDocs(catId, set, ["solutions"], win)
      .catch((e) => failPrintWindow(win, e?.message || "인쇄를 준비하지 못했어요"))
      .finally(() => setBusy(false));
  };

  return (
    <div className="cs-paperpage">
      {err && <div className="cs-wrap"><div className="sv-empty">{err}</div></div>}
      {!ready && !err && <div className="cs-wrap sv-muted">해설지를 펼치는 중…</div>}
      {ready && <div className="cs-gsum"><span className="cs-gx">빠른 정답의 번호를 누르면 그 문항의 해설로 가요</span></div>}
      <div ref={boxRef} className="cs-paperbox">
        <div ref={hostRef} className="cs-paperhost" />
      </div>

      <div className="cs-pbar2" role="toolbar" aria-label="해설지 도구">
        <div className="cs-zoom">
          <button type="button" className="cs-tb" disabled={zi === 0} onClick={() => setZi((v) => Math.max(0, v - 1))} aria-label="작게">−</button>
          <button type="button" className="cs-tb cs-zv" onClick={() => setZi(0)} title="폭 맞춤">{zi === 0 ? "맞춤" : `${Math.round(ZOOMS[zi] * 100)}%`}</button>
          <button type="button" className="cs-tb" disabled={zi === ZOOMS.length - 1} onClick={() => setZi((v) => Math.min(ZOOMS.length - 1, v + 1))} aria-label="크게">＋</button>
        </div>
        <button type="button" className="cs-tb" disabled={!ready} onClick={() => setJump(true)}>번호로 가기</button>
        <button type="button" className="cs-tb" disabled={!ready} onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}>빠른 정답</button>
        <span className="cs-fill" />
        <button type="button" className="sv-btn sm" disabled={busy} onClick={onPrint}>{busy ? "준비 중…" : "🖨 인쇄"}</button>
      </div>

      {jump && (
        <div className="cs-sheetbg" onClick={() => setJump(false)}>
          <div className="cs-sheet" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="번호로 가기">
            <div className="cs-shh"><div className="cs-sht"><b>번호로 가기</b><small>{pad2(set.no)} {set.short} 해설지</small></div><span className="cs-fill" />
              <button type="button" className="cs-x" onClick={() => setJump(false)} aria-label="닫기">✕</button></div>
            <div className="cs-jump">
              {set.items.map((it) => (
                <button key={it.no} type="button" className="cs-jn" onClick={() => { setJump(false); setTimeout(() => go(it.no), 30); }}>{it.no}</button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
