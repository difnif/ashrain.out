// ashrain.out — 학교별 모의고사 자료 보기(#/mock/<id>/doc/<자료>) · 정답과 채점 기준(#/mock/<id>/key)
//   자료 보기: 문제지 · 빠른 정답지 · 해설지 … 를 쪽 그림으로 화면 폭에 맞춰 펼친다(확대 · 쪽 이동 · 받기 · 인쇄).
//   정답과 채점 기준: 선택형 정답표(번호 · 정답 · 배점 · 단원 — 시험지를 채점했으면 내 답 · ○ ✗도) + 서답형 답 · 채점 요소.
import { useEffect, useMemo, useRef, useState } from "react";
import { fileUrl, fmtBytes, downloadName, readMockPaper, gradeMock, choiceText, CIRCLED } from "../../lib/mockexams";
import { Rich, avKnown } from "./parts";
import { avItem } from "../../lib/av";
import { zipStore } from "../../lib/zipstore";
import { openPrintWindow, fillPrintWindow, failPrintWindow, PRINT_SCRIPT } from "../sets/printdoc";

const ZOOMS = [1, 1.25, 1.5, 2];

// ── 자료 고르기 · 바로 인쇄 · 다운로드 (컨셉 문제 「📂 자료」와 같은 틀) ─────────────────
export const DOC_IC = { problems: "📄", answersheet: "📝", omr: "🔘", key: "✅", solutions: "📘", english: "🔤", vocab: "📒", subjects: "🔗" };
const PICK_KEY = "ash.mock.docs";
const MODE_KEY = "ash.mock.dlmode";           // 여럿 받을 때: "zip"(ZIP 하나) | "each"(파일 각각)
const lsGet = (k) => { try { return localStorage.getItem(k); } catch { return null; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, v); } catch { /* 사생활 모드 등 */ } };
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
function saveBlob(blob, name) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = name; a.rel = "noopener";
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 30000);
}
async function fetchPdf(url) {
  let r;
  try { r = await fetch(url); } catch { throw new Error("NET"); }
  if (!r.ok) throw new Error("NOFILE");
  return new Uint8Array(await r.arrayBuffer());
}

/** 고른 자료의 쪽 그림을 A4 한 장씩 이어 붙인 인쇄 문서 */
export function printHtml(exam, docs, title) {
  const pages = docs.flatMap((d) => d.pages.map((pg, k) => `<div class="pg"><img src="${esc(fileUrl(exam, pg.img))}" alt="${esc(d.label)} ${k + 1}쪽"></div>`));
  return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=840"><title>${esc(title)}</title><style>
@page{size:A4;margin:0}html,body{margin:0;padding:0;background:#fff}
.pg{width:210mm;height:296.5mm;display:flex;align-items:center;justify-content:center;overflow:hidden;break-after:page;page-break-after:always}
.pg:last-of-type{break-after:auto;page-break-after:auto}.pg img{width:100%;height:100%;object-fit:contain;display:block}
@media screen{html{background:#e9e9e9}body{padding:6mm 0 18mm}.pg{margin:0 auto 6mm;background:#fff;box-shadow:0 1px 6px rgba(0,0,0,.18)}}
#cs-print-btn{position:fixed;right:14px;bottom:14px;z-index:9;font:700 15px/1 system-ui,sans-serif;padding:12px 18px;border-radius:999px;border:0;background:#0D9488;color:#fff;box-shadow:0 6px 18px rgba(0,0,0,.25);cursor:pointer}
@media print{#cs-print-btn{display:none}}</style></head><body>${pages.join("")}<button id="cs-print-btn" type="button">🖨 인쇄하기</button>${PRINT_SCRIPT}</body></html>`;
}

function readPicks(exam) {
  try {
    const v = JSON.parse(lsGet(PICK_KEY) || "null");
    if (Array.isArray(v)) { const ok = v.filter((x) => exam.docs.some((d) => d.id === x)); if (ok.length) return ok; }
  } catch { /* 무시 */ }
  return ["problems"];
}

export function MockDocsPanel({ exam, school, say }) {
  const [picks, setPicks] = useState(() => readPicks(exam));
  const [mode, setModeS] = useState(() => (lsGet(MODE_KEY) === "each" ? "each" : "zip"));
  const setMode = (m) => { setModeS(m); lsSet(MODE_KEY, m); };
  const [busy, setBusy] = useState(null);            // "print" | "down" | null
  const [prog, setProg] = useState("");
  const tog = (id) => setPicks((p) => {
    const n = p.includes(id) ? p.filter((x) => x !== id) : [...p, id];
    lsSet(PICK_KEY, JSON.stringify(n));
    return n;
  });
  const chosen = exam.docs.filter((d) => picks.includes(d.id));     // 자료 차례대로
  const name = (d) => downloadName(exam, d, school?.short);

  const onPrint = () => {
    if (!chosen.length) { say("인쇄할 자료를 하나 이상 골라 주세요"); return; }
    const win = openPrintWindow();          // 클릭 순간에 창부터 (팝업 차단 회피)
    if (!win) { say("새 창이 막혔어요 — 브라우저에서 이 사이트의 팝업을 허용해 주세요"); return; }
    setBusy("print");
    try { fillPrintWindow(win, printHtml(exam, chosen, `${school?.short || ""} ${exam.title} ${exam.ed} — ${chosen.map((d) => d.label).join(" · ")}`.trim())); }
    catch (e) { failPrintWindow(win, e?.message || "인쇄를 준비하지 못했어요"); }
    finally { setBusy(null); }
  };

  const onDown = async () => {
    if (!chosen.length) { say("받을 자료를 하나 이상 골라 주세요"); return; }
    if (chosen.length === 1) { setBusy("down"); try { await downloadDoc(exam, chosen[0], school?.short, say); } finally { setBusy(null); } return; }
    setBusy("down"); setProg("");
    try {
      const out = [];
      try {
        for (let i = 0; i < chosen.length; i++) {
          setProg(`${i + 1}/${chosen.length}`);
          out.push({ name: name(chosen[i]), data: await fetchPdf(fileUrl(exam, chosen[i].pdf)) });
        }
      } catch (e) {
        if (e.message !== "NET") throw e;
        for (let i = 0; i < chosen.length; i++) {        // 받아 오기가 막히면 하나씩 서버 링크로
          setProg(`${i + 1}/${chosen.length}`);
          await downloadDoc(exam, chosen[i], school?.short);
          await wait(900);
        }
        say(`${chosen.length}개 파일을 하나씩 받아요`);
        return;
      }
      if (mode === "each") {
        for (let i = 0; i < out.length; i++) {
          setProg(`${i + 1}/${out.length}`);
          saveBlob(new Blob([out[i].data], { type: "application/pdf" }), out[i].name);
          if (i < out.length - 1) await wait(800);
        }
        say(`${out.length}개 파일을 하나씩 받았어요 — 브라우저가 묻으면 「여러 파일 받기」를 허용해 주세요`);
        return;
      }
      saveBlob(new Blob([zipStore(out)], { type: "application/zip" }), name({ label: "자료" }).replace(/\.pdf$/, ".zip"));
      say(`${out.length}개 파일을 ZIP 하나로 받았어요`);
    } catch {
      say("받지 못했어요 — 연결을 확인하고 다시 시도해 주세요");
    } finally { setBusy(null); setProg(""); }
  };

  const view = chosen[0] || exam.docs[0];
  return (
    <div className="cs-card cs-docs mx-dpanel">
      <div className="cs-ch"><b>📂 자료</b><span>고른 것만 인쇄하거나 받아요</span></div>
      <div className="cs-dchips" role="group" aria-label="자료 고르기">
        {exam.docs.map((d) => {
          const on = picks.includes(d.id);
          return (
            <button key={d.id} type="button" className={"cs-dchip" + (on ? " on" : "")} aria-pressed={on} onClick={() => tog(d.id)}>
              <span className="ck" aria-hidden="true">{on ? "✓" : ""}</span>
              <span className="ic" aria-hidden="true">{DOC_IC[d.id] || "📄"}</span>
              <span className="nm">{d.label}<small>{d.pages.length}쪽{d.bytes ? ` · ${fmtBytes(d.bytes)}` : ""}</small></span>
            </button>
          );
        })}
      </div>
      {chosen.length > 1 && (
        <div className="cs-dlmode" role="radiogroup" aria-label="여럿을 받는 방식">
          <span>받는 방식</span>
          <div className="cs-modes">
            <button type="button" role="radio" aria-checked={mode === "zip"} className={mode === "zip" ? "on" : ""} onClick={() => setMode("zip")}>🗜 ZIP 하나로</button>
            <button type="button" role="radio" aria-checked={mode === "each"} className={mode === "each" ? "on" : ""} onClick={() => setMode("each")}>📄 파일 각각</button>
          </div>
        </div>
      )}
      <div className="cs-dbtns">
        <button type="button" className="sv-btn pri" disabled={!!busy} onClick={onPrint}>{busy === "print" ? "준비 중…" : "🖨 바로 인쇄"}</button>
        <button type="button" className="sv-btn" disabled={!!busy} onClick={onDown}>{busy === "down" ? `받는 중… ${prog}` : "⬇ 다운로드"}</button>
        <button type="button" className="sv-btn" onClick={() => (location.hash = `#/mock/${exam.id}/doc/${view.id}`)}>👀 화면으로 보기</button>
      </div>
      <p className="cs-dnote">여러 개를 고르면 인쇄는 한 번에 이어서, 다운로드는 ZIP 하나 또는 파일 각각으로 받아요. OMR 답안지는 선택형 {exam.n.mc}문항을 칠하는 카드(A4 한 장)이고, 서답형은 서답형 답안지에 풀이와 답을 함께 써요.</p>
    </div>
  );
}

/** PDF 받기 — 앱이 받아 한글 이름을 붙인다(막히면 서버가 이름을 붙이는 ?download= 주소로) */
export async function downloadDoc(exam, doc, schoolShort, say) {
  const name = downloadName(exam, doc, schoolShort);
  const url = fileUrl(exam, doc.pdf);
  try {
    const r = await fetch(url);
    if (!r.ok) throw new Error(String(r.status));
    const blob = await r.blob();
    const u = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = u; a.download = name; a.rel = "noopener";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(u), 30000);
    say?.(`${doc.label}를 받았어요`);
  } catch {
    const a = document.createElement("a");
    a.href = `${url}?download=${encodeURIComponent(name)}`; a.rel = "noopener";
    document.body.appendChild(a); a.click(); a.remove();
    say?.(`${doc.label}를 받는 중이에요`);
  }
}
/** 인쇄 — PDF 를 새 창에서(브라우저 PDF 보기의 인쇄) */
export function printDoc(exam, doc, say) {
  const w = window.open(fileUrl(exam, doc.pdf), "_blank", "noopener");
  if (!w) say?.("새 창이 막혔어요 — 브라우저에서 이 사이트의 팝업을 허용해 주세요");
}

export function MockDoc({ exam, school, docId, say }) {
  const doc = exam.docs.find((d) => d.id === docId) || exam.docs[0];
  const [zi, setZi] = useState(0);
  const [cur, setCur] = useState(0);
  const boxRef = useRef(null);
  const [w, setW] = useState(0);
  useEffect(() => {
    const el = boxRef.current;
    if (!el) return undefined;
    const fit = () => setW(el.clientWidth);
    fit();
    const ro = typeof ResizeObserver !== "undefined" ? new ResizeObserver(fit) : null;
    ro?.observe(el);
    return () => ro?.disconnect();
  }, []);
  useEffect(() => {
    const on = () => {
      const pgs = [...(boxRef.current?.querySelectorAll(".mx-dpg") || [])];
      const mid = window.innerHeight / 2;
      const k = pgs.findIndex((p) => { const r = p.getBoundingClientRect(); return r.top <= mid && r.bottom >= mid; });
      if (k >= 0) setCur(k);
    };
    window.addEventListener("scroll", on, { passive: true });
    return () => window.removeEventListener("scroll", on);
  }, []);
  const goPage = (k) => {
    const el = boxRef.current?.querySelectorAll(".mx-dpg")[k];
    if (el) window.scrollBy({ top: el.getBoundingClientRect().top - 64, behavior: "smooth" });
  };
  const pw = Math.max(280, (w - 4) * ZOOMS[zi]);
  return (
    <div className="cs-paperpage">
      <div className="mx-dtabs">
        {exam.docs.map((d) => (
          <a key={d.id} href={`#/mock/${exam.id}/doc/${d.id}`} className={"cs-chip" + (d.id === doc.id ? " on" : "")}>{d.label}<small> {d.pages.length}쪽</small></a>
        ))}
      </div>
      <div ref={boxRef} className="cs-paperbox mx-dbox">
        <div style={{ width: pw, margin: zi === 0 ? "0 auto" : 0 }}>
          {doc.pages.map((pg, k) => (
            <div key={pg.img} className="mx-dpg" style={{ aspectRatio: `${pg.w} / ${pg.h}` }}>
              <img src={fileUrl(exam, pg.img)} alt={`${doc.label} ${k + 1}쪽`} loading={k < 2 ? "eager" : "lazy"} draggable={false} />
            </div>
          ))}
        </div>
      </div>
      <div className="cs-pbar2" role="toolbar" aria-label="자료 도구">
        <div className="cs-zoom">
          <button type="button" className="cs-tb" disabled={zi === 0} onClick={() => setZi((v) => Math.max(0, v - 1))} aria-label="작게">−</button>
          <button type="button" className="cs-tb cs-zv" onClick={() => setZi(0)} title="폭 맞춤">{zi === 0 ? "맞춤" : `${Math.round(ZOOMS[zi] * 100)}%`}</button>
          <button type="button" className="cs-tb" disabled={zi === ZOOMS.length - 1} onClick={() => setZi((v) => Math.min(ZOOMS.length - 1, v + 1))} aria-label="크게">＋</button>
        </div>
        <div className="cs-zoom">
          <button type="button" className="cs-tb" disabled={cur <= 0} onClick={() => goPage(cur - 1)} aria-label="앞 쪽">‹</button>
          <span className="cs-tb mx-pgn">{cur + 1}/{doc.pages.length}</span>
          <button type="button" className="cs-tb" disabled={cur >= doc.pages.length - 1} onClick={() => goPage(cur + 1)} aria-label="다음 쪽">›</button>
        </div>
        <span className="cs-fill" />
        <button type="button" className="sv-btn sm mx-nw" onClick={() => printDoc(exam, doc, say)} title="인쇄">🖨<span className="lg"> 인쇄</span></button>
        <button type="button" className="sv-btn sm mx-nw" onClick={() => downloadDoc(exam, doc, school?.short, say)} title="받기">⬇<span className="lg"> 받기{doc.bytes ? ` ${fmtBytes(doc.bytes)}` : ""}</span></button>
      </div>
    </div>
  );
}

export function MockKey({ exam, uid }) {
  const paper = useMemo(() => (uid === undefined ? null : readMockPaper(exam.id)), [exam.id, uid]);
  const g = useMemo(() => (paper?.submitted ? gradeMock(exam, paper.answers, paper.sa) : null), [exam, paper]);
  const rowOf = g ? Object.fromEntries(g.rows.map((r) => [r.i, r])) : {};
  const mcs = exam.items.filter((it) => it.kind === "mc"), sas = exam.items.filter((it) => it.kind === "sa");
  const go = (i) => { location.hash = `#/mock/${exam.id}/q/${i}`; };
  return (
    <div className="cs-wrap mx-keypage">
      {g && <div className="mx-keysum">시험지 채점 <b>{g.score}</b>/{g.max} · 선택형 {g.mc.ok}/{g.mc.n} 맞힘 — 표의 ○ ✗는 그 채점이에요</div>}
      <div className="cs-sec">선택형 <small>{mcs.length}문항 · {exam.pts.mc}점</small></div>
      <div className="mx-ktab" role="table" aria-label="선택형 정답">
        <div className="mx-kr head" role="row"><span>번호</span><span>정답</span><span>배점</span><span>단원 · 유형</span>{g && <span>내 답</span>}</div>
        {mcs.map((it) => {
          const r = rowOf[it.i], mine = paper?.answers?.[it.i]?.sel || [];
          const avs = (it.av || []).filter(avKnown);
          return (
            <button key={it.i} type="button" className={"mx-kr" + (r ? " " + r.status : "")} role="row" onClick={() => go(it.i)}>
              <span className="n">{it.label}</span>
              <span className="a">{choiceText(it.ans)}</span>
              <span className="p">{it.pts}</span>
              <span className="u"><Rich text={it.unit} />{avs.length > 0 && <i title={avs.map((k) => avItem(k)?.title).join(" · ")}> 🎬</i>}</span>
              {g && <span className="m">{mine.length ? mine.map((c) => CIRCLED[c]).join("") : "—"} {r?.status === "ok" ? "○" : "✗"}</span>}
            </button>
          );
        })}
      </div>
      <div className="cs-sec">서답형 <small>{sas.length}문항 · {exam.pts.sa}점</small></div>
      {sas.map((it) => {
        const r = rowOf[it.i];
        return (
          <div key={it.i} className="cs-card mx-ksa">
            <div className="mx-ksah"><b>[{it.label}]</b> <span>{it.title}</span><span className="cs-fill" /><b>{it.pts}점</b>{r && r.status !== "pending" && <em className={r.status}>{r.got}점</em>}</div>
            <div className="mx-ans"><span className="iv-lab">답</span><Rich text={it.answer} /></div>
            {it.rubric?.length > 0 && (
              <ul className="mx-krub">{it.rubric.map(([t, p], k) => <li key={k}><Rich text={t} /> <b>({p}점)</b></li>)}</ul>
            )}
            <div className="mx-ksaf"><button type="button" className="sv-btn sm" onClick={() => go(it.i)}>한 문제씩 풀기 ›</button></div>
          </div>
        );
      })}
      {exam.notes?.length > 0 && <p className="cs-dnote">※ {exam.notes.join(" ")}</p>}
    </div>
  );
}
