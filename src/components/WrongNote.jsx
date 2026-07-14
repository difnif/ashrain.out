import { useEffect, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import AdminWrongNotes from "./AdminWrongNotes";

// ashrain.out — 오답노트 (v0.2.1)
// 이 파일을 src/components/WrongNote.jsx 로 업로드하세요. Home.jsx(v0.2.1)가 import 합니다.
// 흐름: 사진 선택/촬영 → ① 4점 코너 조정(원근 보정) → ② 스캔 필터(필기 보존) → ③ 분류·메모 → 저장
// 저장 위치: storage 'notes' 버킷 {uid}/wrong/{uuid}.jpg + wrong_notes 테이블 (RLS로 계정 격리)

const REASONS = [
  ["calc", "계산 실수"], ["concept", "개념 부족"], ["reading", "문제 해석"],
  ["time", "시간 부족"], ["guess", "찍음"], ["etc", "기타"],
];
const REASON_LABEL = Object.fromEntries(REASONS);
const STATUS = { new: ["🆕", "새 오답"], retried: ["🔄", "다시 풂"], cleared: ["✅", "극복!"] };
const NEXT_HINT = { new: "다시 풀어봤다면 상태를 바꿔 주세요", retried: "완전히 이해했다면 극복으로!", cleared: "훌륭해요 — 극복한 오답이에요" };

// 단위 정사각형 (u,v) → 사각형 4점(TL,TR,BR,BL) 투영 계수 — 수치 검증 완료
function coef(p) {
  const [x0, y0] = p[0], [x1, y1] = p[1], [x2, y2] = p[2], [x3, y3] = p[3];
  const dx1 = x1 - x2, dx2 = x3 - x2, dy1 = y1 - y2, dy2 = y3 - y2;
  const sx = x0 - x1 + x2 - x3, sy = y0 - y1 + y2 - y3;
  const den = dx1 * dy2 - dx2 * dy1;
  const g = (sx * dy2 - sy * dx2) / den, h = (dx1 * sy - dy1 * sx) / den;
  return { a: x1 - x0 + g * x1, b: x3 - x0 + h * x3, c: x0, d: y1 - y0 + g * y1, e: y3 - y0 + h * y3, f: y0, g, h };
}
const dist = (p, q) => Math.hypot(p[0] - q[0], p[1] - q[1]);

const CSS = `
.wn-top { display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:12px; flex-wrap:wrap; }
.wn-title { font-size:15px; font-weight:800; color:var(--ink); }
.wn-mini { font-size:12px; color:var(--mut); }
.wn-btn { background:var(--card); border:1px solid var(--bd); color:var(--ink); font-size:12.5px; border-radius:8px; padding:7px 12px; cursor:pointer; }
.wn-act { width:100%; padding:13px 8px; border-radius:12px; border:1px solid var(--ac); background:transparent;
  color:var(--ac); font-weight:800; font-size:14px; cursor:pointer; margin-bottom:14px; }
.wn-chips { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:12px; }
.wn-chip { border:1px solid var(--bd); background:var(--card); color:var(--mut); border-radius:999px; padding:6px 11px; font-size:12.5px; cursor:pointer; }
.wn-chip.on { color:var(--ac); border-color:var(--ac); }
.wn-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:8px; }
.wn-shot { position:relative; border:1px solid var(--bd); border-radius:12px; overflow:hidden; background:var(--card); cursor:pointer; padding:0; text-align:left; }
.wn-shot img { width:100%; aspect-ratio:3/4; object-fit:cover; display:block; background:rgba(0,0,0,.06); }
.wn-shot p { margin:0; padding:7px 10px 8px; font-size:12px; color:var(--mut); }
.wn-badge { position:absolute; top:7px; left:7px; background:var(--card); border:1px solid var(--bd);
  border-radius:999px; font-size:11.5px; padding:3px 8px; color:var(--ink); }
.wn-empty { color:var(--mut); font-size:14px; text-align:center; padding:36px 0; }
.wn-sec { font-size:13px; font-weight:800; color:var(--mut); letter-spacing:1px; margin:18px 0 8px; }

/* 추가 플로우 */
.wn-stage { background:var(--card); border:1px solid var(--bd); border-radius:14px; padding:14px; }
.wn-step { font-size:12.5px; color:var(--mut); margin:0 0 10px; }
.wn-step b { color:var(--ac); }
.wn-cv { width:100%; display:block; border-radius:10px; touch-action:none; background:rgba(0,0,0,.05); }
.wn-row { display:flex; gap:8px; margin-top:12px; }
.wn-next { flex:1; padding:11px; border-radius:10px; border:1px solid var(--ac); background:transparent; color:var(--ac); font-weight:800; font-size:14px; cursor:pointer; }
.wn-back { padding:11px 14px; border-radius:10px; border:1px solid var(--bd); background:transparent; color:var(--mut); font-size:13px; cursor:pointer; }
.wn-preset { display:flex; gap:6px; margin:10px 0 4px; }
.wn-slider { display:flex; align-items:center; gap:10px; margin-top:8px; font-size:12.5px; color:var(--mut); }
.wn-slider input { flex:1; accent-color:var(--ac); }
.wn-lab { font-size:12.5px; color:var(--mut); margin:12px 0 6px; font-weight:700; }
.wn-in { width:100%; box-sizing:border-box; background:transparent; border:1px solid var(--bd); border-radius:10px;
  padding:10px 12px; color:var(--ink); font-size:14px; }
.wn-ta { min-height:74px; resize:vertical; font-family:inherit; }
.wn-sel { appearance:auto; }

/* 상세 모달 */
.wn-modal-bg { position:fixed; inset:0; background:rgba(0,0,0,.5); display:flex; align-items:center; justify-content:center; z-index:70; padding:18px; }
.wn-modal { background:var(--card); border:1px solid var(--bd); border-radius:16px; max-width:460px; width:100%;
  padding:16px; color:var(--ink); max-height:88vh; overflow-y:auto; }
.wn-modal h3 { margin:0 0 8px; font-size:15.5px; }
.wn-img { width:100%; border-radius:10px; border:1px solid var(--bd); }
.wn-meta { font-size:12.5px; color:var(--mut); margin:8px 0 4px; line-height:1.7; }
.wn-st3 { display:flex; gap:6px; margin:10px 0 4px; }
.wn-st3 button { flex:1; padding:9px 4px; border-radius:10px; border:1px solid var(--bd); background:transparent; color:var(--mut); font-size:12.5px; cursor:pointer; }
.wn-st3 button.on { color:var(--ac); border-color:var(--ac); font-weight:800; }
.wn-del { width:100%; margin-top:10px; padding:9px; border-radius:10px; border:1px solid #E5484D55; color:#E5484D; background:transparent; font-size:12.5px; cursor:pointer; }
`;

export default function WrongNote({ uid, isAdmin, unitNames, say }) {
  const [adminView, setAdminView] = useState(false);

  // 목록
  const [notes, setNotes] = useState(null);
  const [urls, setUrls] = useState({});
  const [flt, setFlt] = useState("all");
  const [detail, setDetail] = useState(null);
  const [memoDraft, setMemoDraft] = useState("");
  const [delArm, setDelArm] = useState(false);
  const [sharedW, setSharedW] = useState(null);
  const [viewer, setViewer] = useState(null);

  // 추가 플로우
  const [step, setStep] = useState(null);            // null | crop | filter | meta | saving
  const [srcCv, setSrcCv] = useState(null);          // 원본(축소) 캔버스
  const [corners, setCorners] = useState(null);      // 원본 좌표계 [TL,TR,BR,BL]
  const [warped, setWarped] = useState(null);        // 원근 보정 결과 캔버스
  const [fx, setFx] = useState({ bright: 18, contrast: 1.35, gray: false });
  const [meta, setMeta] = useState({ unit: "", reason: "", source: "", tags: "", memo: "" });
  const cropRef = useRef(null);
  const filtRef = useRef(null);
  const dragRef = useRef(-1);
  const fileRef = useRef(null);

  const unitIds = Object.keys(unitNames).sort((a, b) => (a[0] === b[0] ? a.localeCompare(b) : a[0] === "m" ? -1 : 1));

  useEffect(() => { loadNotes(); loadShared(); }, [uid]); // eslint-disable-line

  async function loadNotes() {
    if (!uid) { setNotes([]); return; }
    const { data } = await supabase.from("wrong_notes").select("*")
      .eq("user_id", uid).order("created_at", { ascending: false });
    setNotes(data || []);
    signAll(data);
  }
  async function loadShared() {
    const { data } = await supabase.from("shared_wrong_notes").select("*")
      .order("created_at", { ascending: false }).limit(12);
    setSharedW(data || []);
    signAll(data);
  }
  async function signAll(rows) {
    for (const r of rows || []) {
      if (!r.image_path || urls[r.image_path]) continue;
      const { data } = await supabase.storage.from("notes").createSignedUrl(r.image_path, 3600);
      if (data?.signedUrl) setUrls((m) => ({ ...m, [r.image_path]: data.signedUrl }));
    }
  }

  // ── ① 사진 선택 ──
  function pickFile(e) {
    const f = e.target.files?.[0];
    e.target.value = "";
    if (!f) return;
    const img = new Image();
    img.onload = () => {
      const cap = 1600, sc = Math.min(1, cap / Math.max(img.width, img.height));
      const cv = document.createElement("canvas");
      cv.width = Math.round(img.width * sc); cv.height = Math.round(img.height * sc);
      cv.getContext("2d").drawImage(img, 0, 0, cv.width, cv.height);
      URL.revokeObjectURL(img.src);
      const ix = cv.width * 0.08, iy = cv.height * 0.08;
      setSrcCv(cv);
      setCorners([[ix, iy], [cv.width - ix, iy], [cv.width - ix, cv.height - iy], [ix, cv.height - iy]]);
      setStep("crop");
    };
    img.onerror = () => say("사진을 열 수 없어요");
    img.src = URL.createObjectURL(f);
  }

  // ── ② 4점 크롭 캔버스 ──
  useEffect(() => { if (step === "crop") drawCrop(); }, [step, srcCv, corners]); // eslint-disable-line
  function drawCrop() {
    const cv = cropRef.current;
    if (!cv || !srcCv || !corners) return;
    const s = Math.min(1, 700 / srcCv.width);
    cv.width = Math.round(srcCv.width * s); cv.height = Math.round(srcCv.height * s);
    const ctx = cv.getContext("2d");
    ctx.drawImage(srcCv, 0, 0, cv.width, cv.height);
    ctx.fillStyle = "rgba(0,0,0,.34)";
    ctx.fillRect(0, 0, cv.width, cv.height);
    const pts = corners.map(([x, y]) => [x * s, y * s]);
    ctx.save();
    ctx.beginPath();
    pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
    ctx.closePath(); ctx.clip();
    ctx.drawImage(srcCv, 0, 0, cv.width, cv.height);
    ctx.restore();
    ctx.strokeStyle = "#0DA95F"; ctx.lineWidth = 2;
    ctx.beginPath();
    pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
    ctx.closePath(); ctx.stroke();
    pts.forEach(([x, y]) => {
      ctx.beginPath(); ctx.arc(x, y, 13, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(13,169,95,.25)"; ctx.fill();
      ctx.beginPath(); ctx.arc(x, y, 6, 0, Math.PI * 2);
      ctx.fillStyle = "#0DA95F"; ctx.fill();
    });
  }
  function cvPoint(e) {
    const cv = cropRef.current, r = cv.getBoundingClientRect();
    const s = Math.min(1, 700 / srcCv.width);
    return [((e.clientX - r.left) * cv.width) / r.width / s, ((e.clientY - r.top) * cv.height) / r.height / s];
  }
  function cropDown(e) {
    const [x, y] = cvPoint(e);
    let best = -1, bd = 1e9;
    corners.forEach(([cx, cy], i) => { const d = Math.hypot(cx - x, cy - y); if (d < bd) { bd = d; best = i; } });
    const s = Math.min(1, 700 / srcCv.width);
    if (bd * s < 34) { dragRef.current = best; e.target.setPointerCapture(e.pointerId); }
  }
  function cropMove(e) {
    if (dragRef.current < 0) return;
    const [x, y] = cvPoint(e);
    setCorners((c) => c.map((p, i) => (i === dragRef.current
      ? [Math.max(0, Math.min(srcCv.width, x)), Math.max(0, Math.min(srcCv.height, y))] : p)));
  }
  function cropUp() { dragRef.current = -1; }

  // ── ③ 원근 보정 (역매핑 + 이중선형 보간) ──
  function doWarp() {
    const p = corners;
    let W = Math.round((dist(p[0], p[1]) + dist(p[3], p[2])) / 2);
    let H = Math.round((dist(p[0], p[3]) + dist(p[1], p[2])) / 2);
    const cap = 1300, sc = Math.min(1, cap / Math.max(W, H));
    W = Math.max(60, Math.round(W * sc)); H = Math.max(60, Math.round(H * sc));
    const m = coef(p);
    const sctx = srcCv.getContext("2d");
    const sd = sctx.getImageData(0, 0, srcCv.width, srcCv.height);
    const sw = srcCv.width, sh = srcCv.height, S = sd.data;
    const out = document.createElement("canvas");
    out.width = W; out.height = H;
    const od = out.getContext("2d").createImageData(W, H);
    const O = od.data;
    for (let j = 0; j < H; j++) {
      const v = H === 1 ? 0 : j / (H - 1);
      for (let i = 0; i < W; i++) {
        const u = W === 1 ? 0 : i / (W - 1);
        const w = m.g * u + m.h * v + 1;
        let x = (m.a * u + m.b * v + m.c) / w;
        let y = (m.d * u + m.e * v + m.f) / w;
        x = Math.max(0, Math.min(sw - 1.001, x));
        y = Math.max(0, Math.min(sh - 1.001, y));
        const x0 = x | 0, y0 = y | 0, fx1 = x - x0, fy1 = y - y0;
        const i00 = (y0 * sw + x0) * 4, i10 = i00 + 4, i01 = i00 + sw * 4, i11 = i01 + 4;
        const o = (j * W + i) * 4;
        for (let k = 0; k < 3; k++) {
          const top = S[i00 + k] * (1 - fx1) + S[i10 + k] * fx1;
          const bot = S[i01 + k] * (1 - fx1) + S[i11 + k] * fx1;
          O[o + k] = top * (1 - fy1) + bot * fy1;
        }
        O[o + 3] = 255;
      }
    }
    out.getContext("2d").putImageData(od, 0, 0);
    setWarped(out);
    setStep("filter");
  }

  // ── ④ 스캔 필터 (밝기·대비·흑백 — 필기는 보존) ──
  useEffect(() => { if (step === "filter") drawFilter(); }, [step, warped, fx]); // eslint-disable-line
  function applyFx(target) {
    const W = warped.width, H = warped.height;
    target.width = W; target.height = H;
    const ctx = target.getContext("2d");
    ctx.drawImage(warped, 0, 0);
    const im = ctx.getImageData(0, 0, W, H), D = im.data;
    const { bright, contrast, gray } = fx;
    for (let i = 0; i < D.length; i += 4) {
      let r = D[i], g = D[i + 1], b = D[i + 2];
      if (gray) { const l = 0.299 * r + 0.587 * g + 0.114 * b; r = g = b = l; }
      D[i]     = Math.max(0, Math.min(255, (r - 128) * contrast + 128 + bright));
      D[i + 1] = Math.max(0, Math.min(255, (g - 128) * contrast + 128 + bright));
      D[i + 2] = Math.max(0, Math.min(255, (b - 128) * contrast + 128 + bright));
    }
    ctx.putImageData(im, 0, 0);
  }
  function drawFilter() { if (filtRef.current && warped) applyFx(filtRef.current); }

  // ── ⑤ 저장 ──
  async function save() {
    if (!uid) { say("로그인 후 이용할 수 있어요"); return; }
    setStep("saving");
    const cv = document.createElement("canvas");
    applyFx(cv);
    cv.toBlob(async (blob) => {
      try {
        const path = `${uid}/wrong/${crypto.randomUUID()}.jpg`;
        const { error: e1 } = await supabase.storage.from("notes")
          .upload(path, blob, { contentType: "image/jpeg" });
        if (e1) throw e1;
        const tags = meta.tags.split(",").map((t) => t.trim()).filter(Boolean);
        const { error: e2 } = await supabase.from("wrong_notes").insert({
          user_id: uid, image_path: path,
          unit_id: meta.unit || null, reason: meta.reason || null,
          source: meta.source.trim() || null, tags, memo: meta.memo.trim() || null,
        });
        if (e2) throw e2;
        say("오답이 저장됐어요 📕");
        resetAdd();
        loadNotes();
      } catch (err) {
        say("저장 실패: " + err.message);
        setStep("meta");
      }
    }, "image/jpeg", 0.85);
  }
  function resetAdd() { setStep(null); setSrcCv(null); setCorners(null); setWarped(null); setFx({ bright: 18, contrast: 1.35, gray: false }); setMeta({ unit: "", reason: "", source: "", tags: "", memo: "" }); }

  // ── 상세: 상태·메모·삭제 ──
  async function setStatus(note, status) {
    setDetail({ ...note, status });
    setNotes((ns) => ns.map((n) => (n.id === note.id ? { ...n, status } : n)));
    const { error } = await supabase.from("wrong_notes").update({ status }).eq("id", note.id);
    if (error) say("상태 변경 실패: " + error.message);
  }
  async function saveMemo(note) {
    const memo = memoDraft.trim() || null;
    setDetail({ ...note, memo });
    setNotes((ns) => ns.map((n) => (n.id === note.id ? { ...n, memo } : n)));
    const { error } = await supabase.from("wrong_notes").update({ memo }).eq("id", note.id);
    say(error ? "메모 저장 실패: " + error.message : "메모를 저장했어요");
  }
  async function removeNote(note) {
    if (!delArm) { setDelArm(true); return; }
    setDetail(null); setDelArm(false);
    setNotes((ns) => ns.filter((n) => n.id !== note.id));
    await supabase.storage.from("notes").remove([note.image_path]);
    const { error } = await supabase.from("wrong_notes").delete().eq("id", note.id);
    say(error ? "삭제 실패: " + error.message : "삭제했어요");
  }

  // ── 관리자 보기 ──
  if (adminView) {
    return (
      <>
        <style>{CSS}</style>
        <div className="wn-top">
          <span className="wn-title">🛠 오답 관리 (관리자)</span>
          <button className="wn-btn" onClick={() => setAdminView(false)}>← 내 오답노트로</button>
        </div>
        <AdminWrongNotes unitNames={unitNames} say={say} />
      </>
    );
  }

  const shown = (notes || []).filter((n) => (flt === "all" ? true : n.status === flt));

  return (
    <div>
      <style>{CSS}</style>

      {/* ── 추가 플로우 ── */}
      {step && (
        <div className="wn-stage">
          {step === "crop" && (
            <>
              <p className="wn-step"><b>1/3</b> 문제 영역의 네 모서리를 점으로 맞춰 주세요 — 비스듬히 찍었어도 반듯하게 펴 드려요.</p>
              <canvas ref={cropRef} className="wn-cv"
                onPointerDown={cropDown} onPointerMove={cropMove}
                onPointerUp={cropUp} onPointerCancel={cropUp} />
              <div className="wn-row">
                <button className="wn-back" onClick={resetAdd}>취소</button>
                <button className="wn-next" onClick={doWarp}>보정하기 →</button>
              </div>
            </>
          )}
          {step === "filter" && (
            <>
              <p className="wn-step"><b>2/3</b> 스캔 느낌으로 다듬어요. 필기 흔적은 그대로 남아요.</p>
              <canvas ref={filtRef} className="wn-cv" />
              <div className="wn-preset">
                <button className={"wn-chip" + (!fx.gray && fx.contrast > 1 ? " on" : "")} onClick={() => setFx({ bright: 18, contrast: 1.35, gray: false })}>✨ 스캔</button>
                <button className={"wn-chip" + (fx.gray ? " on" : "")} onClick={() => setFx({ bright: 18, contrast: 1.4, gray: true })}>⬜ 흑백 스캔</button>
                <button className={"wn-chip" + (!fx.gray && fx.contrast === 1 && fx.bright === 0 ? " on" : "")} onClick={() => setFx({ bright: 0, contrast: 1, gray: false })}>원본</button>
              </div>
              <div className="wn-slider">밝기<input type="range" min="-60" max="60" value={fx.bright}
                onChange={(e) => setFx({ ...fx, bright: +e.target.value })} /></div>
              <div className="wn-slider">대비<input type="range" min="0.6" max="2" step="0.05" value={fx.contrast}
                onChange={(e) => setFx({ ...fx, contrast: +e.target.value })} /></div>
              <div className="wn-row">
                <button className="wn-back" onClick={() => setStep("crop")}>← 다시 맞추기</button>
                <button className="wn-next" onClick={() => setStep("meta")}>다음 →</button>
              </div>
            </>
          )}
          {(step === "meta" || step === "saving") && (
            <>
              <p className="wn-step"><b>3/3</b> 분류하고 메모를 남겨요 — 전부 선택 사항, 나중에 바꿀 수 있어요.</p>
              <p className="wn-lab">단원</p>
              <select className="wn-in wn-sel" value={meta.unit} onChange={(e) => setMeta({ ...meta, unit: e.target.value })}>
                <option value="">선택 안 함</option>
                {unitIds.map((u) => <option key={u} value={u}>{unitNames[u]}</option>)}
              </select>
              <p className="wn-lab">왜 틀렸을까요?</p>
              <div className="wn-chips" style={{ marginBottom: 0 }}>
                {REASONS.map(([k, label]) => (
                  <button key={k} className={"wn-chip" + (meta.reason === k ? " on" : "")}
                    onClick={() => setMeta({ ...meta, reason: meta.reason === k ? "" : k })}>{label}</button>
                ))}
              </div>
              <p className="wn-lab">출처</p>
              <input className="wn-in" placeholder="예: 쎈 중3-1 / 2학기 중간" value={meta.source}
                onChange={(e) => setMeta({ ...meta, source: e.target.value })} />
              <p className="wn-lab">태그 (쉼표로 구분)</p>
              <input className="wn-in" placeholder="예: 근의공식, 서술형" value={meta.tags}
                onChange={(e) => setMeta({ ...meta, tags: e.target.value })} />
              <p className="wn-lab">메모</p>
              <textarea className="wn-in wn-ta" placeholder="어디서 막혔는지, 다음엔 어떻게 할지 적어 두면 복습이 빨라져요"
                value={meta.memo} onChange={(e) => setMeta({ ...meta, memo: e.target.value })} />
              <div className="wn-row">
                <button className="wn-back" onClick={() => setStep("filter")} disabled={step === "saving"}>← 필터</button>
                <button className="wn-next" onClick={save} disabled={step === "saving"}>
                  {step === "saving" ? "저장 중…" : "저장하기 ✓"}
                </button>
              </div>
            </>
          )}
        </div>
      )}

      {/* ── 목록 ── */}
      {!step && (
        <>
          <input ref={fileRef} type="file" accept="image/*" capture="environment" hidden onChange={pickFile} />
          <div className="wn-top">
            <span className="wn-title">📕 내 오답노트 <span className="wn-mini">{notes ? `${notes.length}개` : ""}</span></span>
            {isAdmin && <button className="wn-btn" onClick={() => setAdminView(true)}>🛠 관리자</button>}
          </div>
          <button className="wn-act" onClick={() => (uid ? fileRef.current.click() : say("로그인 후 이용할 수 있어요"))}>
            📷 오답 추가하기
          </button>

          <div className="wn-chips">
            {[["all", "전체"], ["new", "🆕 새 오답"], ["retried", "🔄 다시 풂"], ["cleared", "✅ 극복"]].map(([k, l]) => (
              <button key={k} className={"wn-chip" + (flt === k ? " on" : "")} onClick={() => setFlt(k)}>{l}</button>
            ))}
          </div>

          {notes === null && <p className="wn-empty">불러오는 중…</p>}
          {notes !== null && shown.length === 0 && (
            <p className="wn-empty">{flt === "all" ? "첫 오답을 추가해 보세요 — 틀린 문제가 진짜 교재예요." : "이 상태의 오답이 없어요."}</p>
          )}
          <div className="wn-grid">
            {shown.map((n) => (
              <button key={n.id} className="wn-shot" onClick={() => { setDetail(n); setMemoDraft(n.memo || ""); setDelArm(false); }}>
                <span className="wn-badge">{STATUS[n.status]?.[0]}</span>
                {urls[n.image_path] && <img src={urls[n.image_path]} alt="" />}
                <p>{n.unit_id ? unitNames[n.unit_id] || n.unit_id : "단원 미지정"}{n.reason ? ` · ${REASON_LABEL[n.reason]}` : ""}</p>
              </button>
            ))}
          </div>

          <p className="wn-sec">👥 친구의 오답에서 배우기</p>
          {sharedW !== null && sharedW.length === 0 && <p className="wn-empty">아직 공유된 친구 오답이 없어요.</p>}
          <div className="wn-grid">
            {(sharedW || []).map((w) => (
              <button key={w.id} className="wn-shot" onClick={() => setViewer(w)}>
                {urls[w.image_path] && <img src={urls[w.image_path]} alt="" />}
                <p><b style={{ color: "var(--ink)" }}>{w.title}</b>{w.unit_id ? ` · ${unitNames[w.unit_id] || w.unit_id}` : ""}</p>
              </button>
            ))}
          </div>
        </>
      )}

      {/* ── 내 오답 상세 ── */}
      {detail && (
        <div className="wn-modal-bg" onClick={() => setDetail(null)}>
          <div className="wn-modal" onClick={(e) => e.stopPropagation()}>
            {urls[detail.image_path] && <img className="wn-img" src={urls[detail.image_path]} alt="" />}
            <p className="wn-meta">
              {detail.unit_id ? unitNames[detail.unit_id] || detail.unit_id : "단원 미지정"}
              {detail.reason ? ` · ${REASON_LABEL[detail.reason]}` : ""}
              {detail.source ? ` · ${detail.source}` : ""}
              {detail.tags?.length ? <><br />🏷 {detail.tags.join(", ")}</> : null}
              <br />{new Date(detail.created_at).toLocaleDateString()} 저장 · {NEXT_HINT[detail.status]}
            </p>
            <div className="wn-st3">
              {Object.entries(STATUS).map(([k, [icon, label]]) => (
                <button key={k} className={detail.status === k ? "on" : ""} onClick={() => setStatus(detail, k)}>{icon} {label}</button>
              ))}
            </div>
            <textarea className="wn-in wn-ta" placeholder="메모" value={memoDraft} onChange={(e) => setMemoDraft(e.target.value)} />
            <div className="wn-row">
              <button className="wn-back" onClick={() => setDetail(null)}>닫기</button>
              <button className="wn-next" onClick={() => saveMemo(detail)}>메모 저장</button>
            </div>
            <button className="wn-del" onClick={() => removeNote(detail)}>
              {delArm ? "정말 삭제할까요? 한 번 더 누르면 삭제돼요" : "🗑 이 오답 삭제"}
            </button>
          </div>
        </div>
      )}

      {/* ── 친구 오답 상세 ── */}
      {viewer && (
        <div className="wn-modal-bg" onClick={() => setViewer(null)}>
          <div className="wn-modal" onClick={(e) => e.stopPropagation()}>
            <h3>{viewer.title}</h3>
            {urls[viewer.image_path] && <img className="wn-img" src={urls[viewer.image_path]} alt="" />}
            {viewer.comment && <p className="wn-meta">💬 {viewer.comment}</p>}
            <div className="wn-row">
              <button className="wn-next" onClick={() => setViewer(null)}>닫기</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
