// ashrain.out — 기본기 해설의 오른쪽 위 📄 문서 (frames/docsmenu.jsx)
// 누르면 아래로 펼쳐진다: ☐ 문제지 · ☐ 해설지 · ☐ 빠른 정답 · ☐ OMR → [확인] → [개별 다운] | [압축 다운]
//   PDF 는 Storage 공개 버킷 concept-sets 의 av/<단원>/<문서>.pdf (main 머지 때 워크플로 push-av-files 가
//   scripts/av-files.mjs 로 찍어 올린다 — 저장소에는 PDF 를 넣지 않는다). 쪽 수 · 크기는 public/av-sets/files.json.
//   받은 파일 이름은 앱이 붙인다(blob + a.download): 「초1-10만들기-문제지.pdf」 · ZIP 「초1-10만들기.zip」(압축 없는 ZIP, 한글 이름 UTF-8).
//   PDF 가 아직 없으면(머지 전 · 미리보기) 같은 문서를 그 자리에서 만들어 인쇄 창으로 연다 — 문제지 · 해설지 · 빠른 정답은
//   frames/avprint.js(그림은 frames/avfig.jsx 가 흑백 SVG 로), OMR 카드는 grid.js(손글씨 한 줄 칸). 인쇄 창에서 「PDF로 저장」하면 된다.
//   유형(e-ten.3) · 주차별 회차는 PDF 를 미리 찍어 두지 않는다(워크플로는 유형별 문제 세트만) — [확인] 다음이 바로 「인쇄 창으로 열기」.
// 받기 흐름(고르기 → 확인 → 받기 | 인쇄 창)은 useDocsFlow 하나 — 액자 오른쪽 위 📄(DocsMenu)와
//   학생앱 목록에서 꾹 눌러 「📄 프린트」(components/AvPrintSheet.jsx)가 같이 쓴다.
import { useEffect, useState } from "react";
import { FILES_BASE } from "../../../lib/conceptsets.js";
import { zipStore } from "../../../lib/zipstore.js";
import { cardHtml } from "../../../lib/omr/grid.js";
import { composePrint, openPrintWindow, fillPrintWindow, failPrintWindow } from "../../../pages/sets/printdoc.js";
import { avDocHtml, avCard, fmtCode } from "./avprint.js";
import { figSvg } from "./avfig.jsx";

export const AV_DOCS = [
  { id: "problems", label: "문제지", suf: "문제지" },
  { id: "solutions", label: "해설지", suf: "해설지" },
  { id: "answers", label: "빠른 정답", suf: "빠른정답" },
  { id: "omr", label: "OMR", suf: "OMR" },
];
const PICK_KEY = "ash.av.docs";
export const avPdfUrl = (id, doc) => `${FILES_BASE}/av/${id}/${doc}.pdf`;
export const avFileBase = (meta) => `${meta.level}-${String(meta.short).replace(/[\s·/\\:*?"<>|()]+/g, "")}`;
export const avDownloadName = (meta, doc) => `${avFileBase(meta)}-${(AV_DOCS.find((d) => d.id === doc) || AV_DOCS[0]).suf}.pdf`;

export { avCard, fmtCode };

let filesP = null;
export function loadFiles() {
  if (!filesP) filesP = fetch("/av-sets/files.json", { cache: "no-cache" }).then((r) => (r.ok ? r.json() : null)).catch(() => null);
  return filesP;
}
export function readPick() {
  try { const v = JSON.parse(localStorage.getItem(PICK_KEY) || "null"); if (Array.isArray(v)) return v.filter((x) => AV_DOCS.some((d) => d.id === x)); } catch { /* 무시 */ }
  return ["problems", "solutions"];
}
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
/** PDF 를 미리 찍어 두는 세트인가 — 유형별 문제 세트(유형은 base, 회차는 week 가 있다) */
export const prerendered = (meta) => !!meta && !meta.base && meta.week == null;
function saveBlob(blob, name) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = name; a.rel = "noopener";
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 30000);
}
function clickLink(url) {
  const a = document.createElement("a");
  a.href = url; a.rel = "noopener";
  document.body.appendChild(a); a.click(); a.remove();
}
async function fetchPdf(url) {
  let r;
  try { r = await fetch(url, { cache: "no-cache" }); } catch { throw new Error("NET"); }
  if (!r.ok) throw new Error("NOFILE");
  const b = new Uint8Array(await r.arrayBuffer());
  if (b.length < 5 || String.fromCharCode(...b.slice(0, 5)) !== "%PDF-") throw new Error("NOFILE");
  return b;
}
export const fmtBytes = (n) => (!n ? "" : n >= 1e6 ? `${(n / 1e6).toFixed(1)}MB` : `${Math.max(1, Math.round(n / 1e3))}KB`);

/** 고른 문서를 한 인쇄 창으로 (PDF 가 아직 없을 때) — set: 세트 자료({ items, pp, note, tips }) */
export async function avPrint(meta, set, picks, win) {
  const parts = [];
  for (const d of AV_DOCS) {
    if (!picks.includes(d.id)) continue;
    if (d.id === "omr") { parts.push({ kind: "omr", html: cardHtml(avCard(meta, set.items)) }); continue; }
    await wait(0);                                       // 그림 100장 — 화면이 멈춘 듯 보이지 않게 한 문서씩 숨 돌리기
    parts.push({ kind: "doc", cls: "cs-p", html: avDocHtml(meta, set, d.id, figSvg) });
  }
  fillPrintWindow(win, composePrint(parts, `${avFileBase(meta)} ${AV_DOCS.filter((d) => picks.includes(d.id)).map((d) => d.label).join(" · ")}`));
}

/**
 * 문서 받기 흐름 — { picks, tog, order, step, setStep, msg, files, info, hasPdf, confirm, down, printNow }
 *   meta: 머리 정보(id · level · short · title · span · code) · set: 문항(없으면 loadSet() 으로 들여온다) · open: 펼쳤나
 *   step: pick → (PDF 가 있으면) how → busy → done | nofile · (PDF 가 없으면) print
 */
export function useDocsFlow({ meta, set, open, loadSet = null }) {
  const [picks, setPicks] = useState(readPick);
  const [step, setStep] = useState("pick");
  const [msg, setMsg] = useState("");
  const [files, setFiles] = useState(null);
  useEffect(() => { if (open) { setStep("pick"); setMsg(""); loadFiles().then(setFiles); } }, [open, meta?.id]);
  const tog = (id) => setPicks((p) => {
    const n = p.includes(id) ? p.filter((x) => x !== id) : AV_DOCS.map((d) => d.id).filter((x) => x === id || p.includes(x));
    try { localStorage.setItem(PICK_KEY, JSON.stringify(n)); } catch { /* 무시 */ }
    return n;
  });
  const info = (id) => files?.sets?.[meta?.id]?.[id] || null;
  const order = AV_DOCS.map((d) => d.id).filter((id) => picks.includes(id));
  // PDF 를 미리 찍어 올려 두는 것은 유형별 문제 세트뿐(워크플로 push-av-files) — 유형 · 회차는 [확인] 다음이 바로 인쇄 창.
  //   단원도 아직 안 올라갔으면(머지 전 · 미리보기) 받아 보다가 404 일 때 인쇄 창으로(nofile)
  const hasPdf = prerendered(meta) || !!files?.sets?.[meta?.id];
  const confirm = () => setStep(hasPdf ? "how" : "print");

  const down = async (how) => {
    setStep("busy"); setMsg("");
    try {
      const out = [];
      for (let i = 0; i < order.length; i++) {
        setMsg(`받는 중… ${i + 1}/${order.length}`);
        out.push({ name: avDownloadName(meta, order[i]), data: await fetchPdf(avPdfUrl(meta.id, order[i])) });
      }
      if (how === "zip") {
        saveBlob(new Blob([zipStore(out)], { type: "application/zip" }), `${avFileBase(meta)}.zip`);
        setMsg(`${out.length}개 문서를 압축 파일 하나로 받았어요`);
      } else {
        for (let i = 0; i < out.length; i++) {
          saveBlob(new Blob([out[i].data], { type: "application/pdf" }), out[i].name);
          if (i < out.length - 1) await wait(800);
        }
        setMsg(out.length > 1 ? `${out.length}개 파일을 하나씩 받았어요 — 브라우저가 물으면 「여러 파일 받기」를 허용해 주세요` : "파일을 받았어요");
      }
      setStep("done");
    } catch (e) {
      if (e.message === "NET") {
        for (let i = 0; i < order.length; i++) {          // 받아 오기가 막히면 서버가 이름을 붙이는 링크로 하나씩
          clickLink(`${avPdfUrl(meta.id, order[i])}?download=${encodeURIComponent(avDownloadName(meta, order[i]))}`);
          await wait(900);
        }
        setMsg(`${order.length}개 파일을 하나씩 받아요`);
        setStep("done");
      } else { setStep("nofile"); }
    }
  };
  const printNow = () => {
    const win = openPrintWindow();                       // 누르는 순간 창부터(팝업 차단 회피)
    if (!win) { setMsg("새 창이 막혔어요 — 이 사이트의 팝업을 허용해 주세요"); return; }
    setMsg("");
    Promise.resolve(set || (loadSet ? loadSet() : null))
      .then((S) => { if (!S) throw new Error("문항을 불러오지 못했어요"); return avPrint(meta, S, order, win); })
      .catch((e) => failPrintWindow(win, e?.message || "인쇄를 준비하지 못했어요"));
  };
  return { picks, tog, order, step, setStep, msg, files, info, hasPdf, confirm, down, printNow };
}

export function DocsMenu({ meta, set, open, onOpen, poke }) {
  const items = set.items;
  const F = useDocsFlow({ meta, set, open });
  const { order, step, setStep, msg } = F;
  const stop = (e) => e.stopPropagation();
  return (
    <div className="gdoc" onPointerDown={stop}>
      <style>{DOC_CSS}</style>
      <button type="button" className={"dsp-fbtn gdoc-btn" + (open ? " on" : "")} title="문서 — 문제지 · 해설지 · 빠른 정답 · OMR" aria-label="문서"
        aria-expanded={open} onClick={() => { onOpen(!open); poke?.(); }}>
        <svg viewBox="0 0 24 24" width="52%" height="52%" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z" /><path d="M14 3v5h5M9 13h6M9 17h6" />
        </svg>
      </button>
      {open && (
        <div className="gdoc-pop" role="dialog" aria-label="문서 받기">
          <div className="gdoc-h"><b>문서</b><small>{meta.span} · {meta.title} · {items.length}제{meta.code ? ` · 코드 ${fmtCode(meta.code)}` : ""}</small></div>
          {step === "pick" && (<>
            <div className="gdoc-list" role="group" aria-label="받을 문서 고르기">
              {AV_DOCS.map((d) => {
                const on = F.picks.includes(d.id), f = F.info(d.id);
                return (
                  <button key={d.id} type="button" className={"gdoc-row" + (on ? " on" : "")} role="checkbox" aria-checked={on} onClick={() => F.tog(d.id)}>
                    <span className="ck" aria-hidden="true">{on ? "✓" : ""}</span>
                    <span className="nm">{d.label}</span>
                    <small>{f ? `${f.pages}쪽 · ${fmtBytes(f.bytes)}` : ""}</small>
                  </button>
                );
              })}
            </div>
            <button type="button" className="gdoc-ok" disabled={!order.length} onClick={F.confirm}>확인</button>
          </>)}
          {step === "how" && (<>
            <p className="gdoc-p">{order.map((id) => AV_DOCS.find((d) => d.id === id).label).join(" · ")} — 어떻게 받을까요?</p>
            <div className="gdoc-two">
              <button type="button" className="gdoc-ok" onClick={() => F.down("each")}>개별 다운</button>
              <button type="button" className="gdoc-ok alt" onClick={() => F.down("zip")}>압축 다운</button>
            </div>
            <button type="button" className="gdoc-back" onClick={() => setStep("pick")}>← 다시 고르기</button>
          </>)}
          {step === "busy" && <p className="gdoc-p">{msg || "받는 중…"}</p>}
          {step === "done" && (<>
            <p className="gdoc-p">{msg}</p>
            <button type="button" className="gdoc-back" onClick={() => setStep("pick")}>← 다른 문서 받기</button>
          </>)}
          {(step === "nofile" || step === "print") && (<>
            <p className="gdoc-p">{step === "print"
              ? `${order.map((id) => AV_DOCS.find((d) => d.id === id).label).join(" · ")} — 이 자리에서 만들어 인쇄 창으로 열어요. 인쇄 창에서 「PDF로 저장」을 고르면 파일로 받을 수 있어요.`
              : "PDF 파일이 아직 올라가지 않았어요. 같은 문서를 인쇄 창으로 열 수 있어요 — 인쇄 창에서 「PDF로 저장」을 고르면 파일로 받을 수 있어요."}</p>
            <button type="button" className="gdoc-ok" onClick={F.printNow}>인쇄 창으로 열기</button>
            {msg && <p className="gdoc-p warn">{msg}</p>}
            <button type="button" className="gdoc-back" onClick={() => setStep("pick")}>← 다시 고르기</button>
          </>)}
        </div>
      )}
    </div>
  );
}

const DOC_CSS = `
.gdoc { position: relative; }
.gdoc-btn.on { color: var(--gold); border-color: var(--gold); }
.gdoc-pop { position: absolute; right: 0; top: calc(100% + .8cqw); width: 25cqw; z-index: 9; background: var(--card); color: var(--ink);
  border: 1px solid var(--chipbd); border-radius: 1.3cqw; padding: 1.1cqw 1.2cqw 1.2cqw; box-shadow: 0 1.6cqw 4cqw rgba(0,0,0,.35);
  display: flex; flex-direction: column; gap: .7cqw; }
.gdoc-h { display: flex; flex-direction: column; gap: .15cqw; }
.gdoc-h b { font-size: 1.45cqw; }
.gdoc-h small { font-size: .95cqw; color: var(--soft); font-weight: 600; line-height: 1.35; }
.gdoc-list { display: flex; flex-direction: column; gap: .45cqw; }
.gdoc-row { display: grid; grid-template-columns: 2.1cqw 1fr auto; align-items: center; gap: .7cqw; text-align: left; border: 1px solid var(--chipbd);
  background: transparent; color: var(--ink); border-radius: .9cqw; padding: .6cqw .8cqw; font: inherit; font-size: 1.3cqw; font-weight: 700; cursor: pointer;
  -webkit-tap-highlight-color: transparent; }
.gdoc-row .ck { width: 2.1cqw; height: 2.1cqw; border-radius: .5cqw; border: 2px solid var(--soft); display: grid; place-items: center; font-size: 1.3cqw; color: #1c2647; }
.gdoc-row.on { border-color: var(--gold); }
.gdoc-row.on .ck { background: var(--gold); border-color: var(--gold); }
.dsp-light .gdoc-row.on .ck { color: #fffdf6; }
.gdoc-row small { font-size: .9cqw; color: var(--soft); font-weight: 600; }
.gdoc-ok { border: 0; border-radius: 999px; background: var(--gold); color: #1c2647; font: inherit; font-size: 1.3cqw; font-weight: 800; padding: .75cqw 1cqw;
  cursor: pointer; -webkit-tap-highlight-color: transparent; }
.dsp-light .gdoc-ok { color: #fffdf6; }
.gdoc-ok:disabled { opacity: .4; cursor: default; }
.gdoc-ok.alt { background: transparent; color: var(--gold); box-shadow: inset 0 0 0 2px var(--gold); }
.dsp-light .gdoc-ok.alt { color: var(--gold); }
.gdoc-two { display: grid; grid-template-columns: 1fr 1fr; gap: .6cqw; }
.gdoc-back { border: 0; background: none; color: var(--soft); font: inherit; font-size: 1.05cqw; font-weight: 700; cursor: pointer; align-self: flex-start; padding: .2cqw 0; }
.gdoc-p { margin: 0; font-size: 1.1cqw; line-height: 1.5; color: var(--ink); }
.gdoc-p.warn { color: var(--e); }
`;
