// 학생앱 › 시청각 학습 › 문제 풀이 해설 — 목록에서 꾹 눌러 「📄 프린트」에서 뗐을 때 아래에서 올라오는 프린트 받기 판
// 그 콘텐츠(유형별 문제 세트 · 유형 · 주차별 회차)의 ☐ 문제지 · ☐ 해설지 · ☐ 빠른 정답 · ☐ OMR → [확인] →
//   PDF 가 올라가 있으면(유형별 문제 세트) [개별 다운] | [압축 다운] · 없으면(유형 · 회차 — 미리 찍어 두지 않음) [인쇄 창으로 열기]
//   (인쇄 창에서 「PDF로 저장」). 받기 흐름은 액자 오른쪽 위 📄 문서와 같다(frames/docsmenu.jsx 의 useDocsFlow) — 코드 · 문항 · 그림도 같다.
// pages/Study.jsx 가 늦게 들여온다(React.lazy) — 인쇄 문서 · 그림 모듈이 목록 화면을 무겁게 하지 않게.
import { useEffect, useState } from "react";
import { avSource } from "../lib/avsrc";
import { unitLabel } from "../lib/units";
import { AV_DOCS, useDocsFlow, fmtBytes, fmtCode } from "../features/display/frames/docsmenu.jsx";

const KIND = { unit: "유형별 문제 세트", type: "유형", week: "주차별 회차" };

export default function AvPrintSheet({ itemKey, onClose }) {
  const src = avSource(itemKey);
  const [, bump] = useState(0);
  const [err, setErr] = useState(null);
  useEffect(() => {
    if (!src || src.ready()) return undefined;
    let live = true;
    src.load().then(() => { if (live) bump((x) => x + 1); }).catch((e) => { if (live) setErr(e?.message || "불러오지 못했어요"); });
    return () => { live = false; };
  }, [itemKey]);   // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    const esc = (e) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);
  const meta = src?.meta() || null, set = src?.set() || null;
  const F = useDocsFlow({ meta, set, open: !!meta, loadSet: () => src.load().then(() => src.set()) });
  const { order, step, setStep, msg } = F;
  const labels = order.map((id) => AV_DOCS.find((d) => d.id === id).label).join(" · ");
  const n = set?.items?.length || meta?.n || 0;
  return (
    <div className="aps" onClick={onClose}>
      <style>{APS_CSS}</style>
      <div className="aps-in" role="dialog" aria-modal="true" aria-label="프린트 받기" onClick={(e) => e.stopPropagation()}>
        <div className="aps-grip" aria-hidden="true" />
        <div className="aps-h">
          <span className="i" aria-hidden="true">{meta?.icon || "📄"}</span>
          <span className="t">
            <small>{KIND[src?.kind] || "프린트"} · 프린트 받기</small>
            <b>{meta ? meta.title : err ? "불러오지 못했어요" : "불러오는 중…"}</b>
            {meta && <small>{[meta.span, unitLabel(meta.unit), n ? `${n}문항` : "", meta.code ? `코드 ${fmtCode(meta.code)}` : ""].filter(Boolean).join(" · ")}</small>}
          </span>
          <button type="button" className="x" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        {!meta ? <p className="aps-p">{err ? `프린트 정보를 불러오지 못했어요 — ${err}` : "프린트 정보를 불러오는 중…"}</p> : (<>
          {step === "pick" && (<>
            <div className="aps-list" role="group" aria-label="받을 문서 고르기">
              {AV_DOCS.map((d) => {
                const on = F.picks.includes(d.id), f = F.info(d.id);
                return (
                  <button key={d.id} type="button" className={"aps-row" + (on ? " on" : "")} role="checkbox" aria-checked={on} onClick={() => F.tog(d.id)}>
                    <span className="ck" aria-hidden="true">{on ? "✓" : ""}</span>
                    <span className="nm">{d.label}</span>
                    <small>{f ? `${f.pages}쪽 · ${fmtBytes(f.bytes)}` : ""}</small>
                  </button>
                );
              })}
            </div>
            <button type="button" className="aps-ok" disabled={!order.length} onClick={F.confirm}>확인</button>
          </>)}
          {step === "how" && (<>
            <p className="aps-p">{labels} — 어떻게 받을까요?</p>
            <div className="aps-two">
              <button type="button" className="aps-ok" onClick={() => F.down("each")}>개별 다운</button>
              <button type="button" className="aps-ok alt" onClick={() => F.down("zip")}>압축 다운</button>
            </div>
            <button type="button" className="aps-back" onClick={() => setStep("pick")}>← 다시 고르기</button>
          </>)}
          {step === "busy" && <p className="aps-p">{msg || "받는 중…"}</p>}
          {step === "done" && (<>
            <p className="aps-p">{msg}</p>
            <div className="aps-two">
              <button type="button" className="aps-ok alt" onClick={() => setStep("pick")}>다른 문서 받기</button>
              <button type="button" className="aps-ok" onClick={onClose}>닫기</button>
            </div>
          </>)}
          {(step === "nofile" || step === "print") && (<>
            <p className="aps-p">{step === "print"
              ? `${labels} — 이 자리에서 만들어 인쇄 창으로 열어요. 인쇄 창에서 「PDF로 저장」을 고르면 파일로 받을 수 있어요.`
              : "PDF 파일이 아직 올라가지 않았어요. 같은 문서를 인쇄 창으로 열 수 있어요 — 인쇄 창에서 「PDF로 저장」을 고르면 파일로 받을 수 있어요."}</p>
            <button type="button" className="aps-ok" onClick={F.printNow}>인쇄 창으로 열기</button>
            {msg && <p className="aps-p warn">{msg}</p>}
            <button type="button" className="aps-back" onClick={() => setStep("pick")}>← 다시 고르기</button>
          </>)}
        </>)}
      </div>
    </div>
  );
}

const APS_CSS = `
.aps { position: fixed; inset: 0; z-index: 3100; background: rgba(6, 10, 16, .5); display: flex; align-items: flex-end; justify-content: center;
  animation: aps-fade .18s ease-out; }
@keyframes aps-fade { from { opacity: 0; } to { opacity: 1; } }
.aps-in { width: 100%; max-width: 460px; max-height: 88vh; overflow-y: auto; background: var(--surface, #fff); color: var(--text, inherit);
  border-radius: 20px 20px 0 0; padding: 8px 16px max(18px, calc(env(safe-area-inset-bottom) + 12px)); box-shadow: 0 -10px 34px rgba(0,0,0,.3);
  display: flex; flex-direction: column; gap: 10px; animation: aps-up .26s cubic-bezier(.2, 1.1, .4, 1) both; }
@media (min-width: 640px) { .aps { align-items: center; } .aps-in { border-radius: 20px; padding-bottom: 18px; } }
@keyframes aps-up { from { transform: translateY(40px); opacity: 0; } to { transform: none; opacity: 1; } }
.aps-grip { width: 38px; height: 4px; border-radius: 4px; background: var(--border, #ccc); margin: 0 auto 2px; }
.aps-h { display: grid; grid-template-columns: 42px 1fr 32px; gap: 10px; align-items: start; }
.aps-h .i { width: 42px; height: 42px; border-radius: 12px; background: var(--surface2, #f3f4f6); display: grid; place-items: center; font-size: 22px; }
.aps-h .t { min-width: 0; display: flex; flex-direction: column; gap: 2px; }
.aps-h .t b { font-size: 15px; font-weight: 800; line-height: 1.35; }
.aps-h .t small { font-size: 11.5px; color: var(--muted, #888); font-weight: 600; line-height: 1.4; }
.aps-h .t small:first-child { color: var(--accent, #0d9488); font-weight: 800; }
.aps-h .x { width: 32px; height: 32px; border: 0; border-radius: 999px; background: var(--surface2, #f3f4f6); color: inherit; font: inherit; font-size: 14px; cursor: pointer; }
.aps-list { display: flex; flex-direction: column; gap: 6px; }
.aps-row { display: grid; grid-template-columns: 26px 1fr auto; align-items: center; gap: 10px; text-align: left; border: 1px solid var(--border, #ddd);
  background: transparent; color: inherit; border-radius: 12px; padding: 11px 12px; font: inherit; font-size: 15px; font-weight: 700; cursor: pointer;
  -webkit-tap-highlight-color: transparent; }
.aps-row .ck { width: 24px; height: 24px; border-radius: 7px; border: 2px solid var(--muted, #999); display: grid; place-items: center; font-size: 15px; color: #fff; }
.aps-row.on { border-color: var(--accent, #0d9488); }
.aps-row.on .ck { background: var(--accent, #0d9488); border-color: var(--accent, #0d9488); }
.aps-row small { font-size: 11.5px; color: var(--muted, #888); font-weight: 600; }
.aps-ok { border: 0; border-radius: 999px; background: var(--accent, #0d9488); color: #fff; font: inherit; font-size: 15px; font-weight: 800; padding: 12px 14px;
  cursor: pointer; -webkit-tap-highlight-color: transparent; }
.st-dark .aps-ok { color: #0b0c0f; }
.aps-ok:disabled { opacity: .4; cursor: default; }
.aps-ok.alt { background: transparent; color: var(--accent, #0d9488); box-shadow: inset 0 0 0 2px var(--accent, #0d9488); }
.aps-two { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.aps-back { border: 0; background: none; color: var(--muted, #888); font: inherit; font-size: 13px; font-weight: 700; cursor: pointer; align-self: flex-start; padding: 2px 0; }
.aps-p { margin: 0; font-size: 13.5px; line-height: 1.6; }
.aps-p.warn { color: var(--bad, #dc2626); }
@media (prefers-reduced-motion: reduce) { .aps, .aps-in { animation: none !important; } }
`;
