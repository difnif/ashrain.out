import { useState, useRef } from "react";
import { applyRibbedGlass, PRESETS } from "./ribbedGlass";

// 리브드 글라스 초상화 — 3단계 통합 (업로드 → 점검 → 배경 합성 → 필터)
// props: theme, onDone(blob)  ← 아바타 저장 훅

const CSS = `
.pt-root { max-width: 460px; margin: 0 auto; padding: 20px 14px;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.pt-root * { box-sizing: border-box; }
.pt-drop { border: 2px dashed #C3C9D0; border-radius: 14px; padding: 34px 16px; text-align: center;
  color: #8A929C; font-size: 14px; cursor: pointer; background: rgba(255,255,255,.6); }
.pt-drop:hover { border-color: #0DA95F; color: #0DA95F; }
.pt-cv { border-radius: 14px; overflow: hidden; box-shadow: 0 6px 24px rgba(31,41,55,.15); }
.pt-cv canvas { width: 100%; display: block; }
.pt-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
.pt-chip { border: 1.5px solid #C3C9D0; background: #fff; color: #4B5563; font-size: 13px; font-weight: 600;
  border-radius: 9999px; padding: 7px 14px; cursor: pointer; }
.pt-chip.on { border-color: #0DA95F; background: #0DA95F; color: #fff; }
.pt-status { margin: 10px 2px; font-size: 13px; color: #55708C; }
.pt-err { color: #DC2626; }
.pt-actions { display: flex; gap: 8px; margin-top: 12px; }
.pt-btn { flex: 1; border: none; border-radius: 10px; padding: 12px 0; font-size: 14px; font-weight: 800; cursor: pointer; }
.pt-btn.pri { background: #0DA95F; color: #fff; } .pt-btn.sec { background: #fff; color: #4B5563; border: 1px solid #C3C9D0; }
`;

export default function PortraitStudio({ onDone }) {
  const [preset, setPreset] = useState("pink");
  const [status, setStatus] = useState("");
  const [err, setErr] = useState("");
  const [ready, setReady] = useState(false);
  const canvasRef = useRef(null);
  const fileRef = useRef(null);
  const baseRef = useRef(null); // 세그멘테이션까지 끝난 캔버스(필터 재적용용)

  const runFilter = (base, key) => {
    const out = applyRibbedGlass(base, { ribWidth: 14, strength: 10, preBlur: 2, preset: key });
    const cv = canvasRef.current;
    cv.width = out.width; cv.height = out.height;
    cv.getContext("2d").drawImage(out, 0, 0);
  };

  const pick = (e) => {
    const f = e.target.files?.[0];
    if (!f) return;
    setErr(""); setReady(false);
    const url = URL.createObjectURL(f);
    const img = new Image();
    img.onload = async () => {
      URL.revokeObjectURL(url);
      try {
        setStatus("도구를 준비하는 중…");
        const { checkFace, cropPortrait, segmentCompose } = await import("./facePipeline");
        setStatus("얼굴을 확인하는 중…");
        const chk = await checkFace(img);
        if (!chk.ok) { setErr(chk.reason); setStatus(""); return; }
        setStatus("배경을 정리하는 중…");
        const cropped = cropPortrait(img, chk.face);
        const base = await segmentCompose(cropped, PRESETS[preset].bg);
        baseRef.current = base;
        setStatus("유리 너머로 옮기는 중…");
        runFilter(base, preset);
        setStatus(""); setReady(true);
      } catch (ex) {
        console.error(ex);
        setErr("변환 중 문제가 생겼어요. 다른 사진으로 다시 시도해 줄래?");
        setStatus("");
      }
    };
    img.src = url;
    e.target.value = "";
  };

  const changePreset = (key) => {
    setPreset(key);
    if (baseRef.current) runFilter(baseRef.current, key); // 재분석 없이 필터만 교체
  };

  const save = () => canvasRef.current?.toBlob((blob) => blob && onDone?.(blob), "image/png");

  return (
    <div className="pt-root">
      <style>{CSS}</style>
      {!ready && !status && (
        <div className="pt-drop" onClick={() => fileRef.current?.click()}>
          여기를 눌러 얼굴 사진을 올려주세요<br />
          <span style={{ fontSize: 12 }}>🔒 사진은 이 기기 안에서만 처리돼요</span>
        </div>
      )}
      <input ref={fileRef} type="file" accept="image/*" style={{ display: "none" }} onChange={pick} />
      {status && <p className="pt-status">{status}</p>}
      {err && <p className="pt-status pt-err">{err}</p>}
      <div className="pt-cv" style={{ display: ready ? "block" : "none" }}><canvas ref={canvasRef} /></div>
      {ready && (<>
        <div className="pt-row">
          {Object.entries(PRESETS).map(([key, p]) => (
            <button key={key} className={"pt-chip" + (preset === key ? " on" : "")} onClick={() => changePreset(key)}>{p.name}</button>
          ))}
        </div>
        <div className="pt-actions">
          <button className="pt-btn sec" onClick={() => fileRef.current?.click()}>다른 사진</button>
          <button className="pt-btn pri" onClick={save}>이 모습으로 저장</button>
        </div>
      </>)}
    </div>
  );
}
