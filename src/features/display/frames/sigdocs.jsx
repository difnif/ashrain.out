// ashrain.out — 시그니처 프린트 원본 받기: 해설 액자 오른쪽 위 📄 (frames/sigdocs.jsx)
// 누르면 아래로 펼쳐진다: ☐ 문제지 · ☐ 정답 · 해설 → [확인] → [개별 다운] | [압축 다운] — 기본기 해설의 📄(frames/docsmenu.jsx)과 같은 모양.
//   PDF 는 강사도구 보관함의 원본 그대로(lib/sigprint.js — 공개 버킷 concept-sets 의 av/sig/<코드>/…, 워크플로 push-sig-files 가 올림).
//   아직 보관함에 없는(올라가지 않은) 프린트는 받을 때 「아직 올라가지 않았어요」 — 앱에서 새로 만들지 않는다(원본만).
//   받은 파일 이름은 앱이 붙인다: 「중등-삼각형조건100-문제지.pdf」 · ZIP 「중등-삼각형조건100.zip」.
// 받기 흐름(useSigDocsFlow)은 학생앱 목록의 「📄 프린트」 받기 판(components/AvPrintSheet.jsx)도 같이 쓴다.
// 쓰는 곳: 해설 액자 여섯(그래프 그리기 · 10단계 계산 · 그래프와 넓이 · 두 점 → 식 · 교점 · 만날 조건 · 경우의 수와 확률 100제)의
//   spec.topExtra(sigTop) · 듀얼 「문제 풀이 해설 전부」(frames/allspec.jsx).
import { useEffect, useState } from "react";
import { zipStore } from "../../../lib/zipstore.js";
import { SIG_DOCS, sigOf, sigPdfUrl, sigDownloadName, sigFileBase, codeKey } from "../../../lib/sigprint.js";
import { fetchPdf, saveBlob, clickLink, wait, fmtCode, DOC_CSS } from "./docsmenu.jsx";

const PICK_KEY = "ash.av.sigdocs";
function readPick() {
  try { const v = JSON.parse(localStorage.getItem(PICK_KEY) || "null"); if (Array.isArray(v)) return v.filter((x) => SIG_DOCS.some((d) => d.id === x)); } catch { /* 무시 */ }
  return SIG_DOCS.map((d) => d.id);
}
export const sigCode = (sig) => fmtCode(codeKey(sig?.code));
export const sigNoFile = (sig) =>
  `원본 PDF가 아직 올라가지 않았어요 — 강사도구 보관함에 이 프린트(코드 ${sigCode(sig)})가 등록되면 하루 안에 올라와요.`;

/**
 * 원본 받기 흐름 — { picks, tog, order, step, setStep, msg, confirm, down }
 *   step: pick → how → busy → done | nofile(아직 안 올라감)
 */
export function useSigDocsFlow({ sig, open }) {
  const [picks, setPicks] = useState(readPick);
  const [step, setStep] = useState("pick");
  const [msg, setMsg] = useState("");
  useEffect(() => { if (open) { setStep("pick"); setMsg(""); } }, [open, sig?.key]);
  const tog = (id) => setPicks((p) => {
    const n = p.includes(id) ? p.filter((x) => x !== id) : SIG_DOCS.map((d) => d.id).filter((x) => x === id || p.includes(x));
    try { localStorage.setItem(PICK_KEY, JSON.stringify(n)); } catch { /* 무시 */ }
    return n;
  });
  const order = SIG_DOCS.map((d) => d.id).filter((id) => picks.includes(id));
  const confirm = () => setStep("how");
  const down = async (how) => {
    setStep("busy"); setMsg("");
    try {
      const out = [];
      for (let i = 0; i < order.length; i++) {
        setMsg(`받는 중… ${i + 1}/${order.length}`);
        out.push({ name: sigDownloadName(sig, order[i]), data: await fetchPdf(sigPdfUrl(sig.code, order[i])) });
      }
      if (how === "zip") {
        saveBlob(new Blob([zipStore(out)], { type: "application/zip" }), `${sigFileBase(sig)}.zip`);
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
          clickLink(`${sigPdfUrl(sig.code, order[i])}?download=${encodeURIComponent(sigDownloadName(sig, order[i]))}`);
          await wait(900);
        }
        setMsg(`${order.length}개 파일을 하나씩 받아요`);
        setStep("done");
      } else { setStep("nofile"); }
    }
  };
  return { picks, tog, order, step, setStep, msg, confirm, down };
}

export function SigDocsMenu({ sig, open, onOpen, poke }) {
  const F = useSigDocsFlow({ sig, open });
  const { order, step, setStep, msg } = F;
  const stop = (e) => e.stopPropagation();
  return (
    <div className="gdoc" onPointerDown={stop}>
      <style>{DOC_CSS}</style>
      <button type="button" className={"dsp-fbtn gdoc-btn" + (open ? " on" : "")} title="원본 프린트 — 문제지 · 정답" aria-label="문서"
        aria-expanded={open} onClick={() => { onOpen(!open); poke?.(); }}>
        <svg viewBox="0 0 24 24" width="52%" height="52%" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z" /><path d="M14 3v5h5M9 13h6M9 17h6" />
        </svg>
      </button>
      {open && (
        <div className="gdoc-pop" role="dialog" aria-label="원본 프린트 받기">
          <div className="gdoc-h"><b>원본 프린트</b><small>{sig.title} · {sig.n}제 · 코드 {sigCode(sig)}</small></div>
          {step === "pick" && (<>
            <div className="gdoc-list" role="group" aria-label="받을 문서 고르기">
              {SIG_DOCS.map((d) => {
                const on = F.picks.includes(d.id);
                return (
                  <button key={d.id} type="button" className={"gdoc-row" + (on ? " on" : "")} role="checkbox" aria-checked={on} onClick={() => F.tog(d.id)}>
                    <span className="ck" aria-hidden="true">{on ? "✓" : ""}</span>
                    <span className="nm">{d.label}</span>
                    <small>원본</small>
                  </button>
                );
              })}
            </div>
            <button type="button" className="gdoc-ok" disabled={!order.length} onClick={F.confirm}>확인</button>
          </>)}
          {step === "how" && (<>
            <p className="gdoc-p">{order.map((id) => SIG_DOCS.find((d) => d.id === id).label).join(" · ")} — 어떻게 받을까요?</p>
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
          {step === "nofile" && (<>
            <p className="gdoc-p">{sigNoFile(sig)}</p>
            <button type="button" className="gdoc-back" onClick={() => setStep("pick")}>← 다시 고르기</button>
          </>)}
        </div>
      )}
    </div>
  );
}

/** 해설 액자 spec.topExtra — 그 세트가 시그니처 프린트면 📄(원본 받기) */
export const sigTop = (fk) => ({ set, open, onOpen, poke }) => {
  const sig = sigOf(`${fk}:${set}`);
  return sig ? <SigDocsMenu sig={sig} open={open} onOpen={onOpen} poke={poke} /> : null;
};
