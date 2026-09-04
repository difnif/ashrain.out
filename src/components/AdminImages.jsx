// ashrain.out — 이미지 관리 v3.0 (슬롯 시스템, 관리자 전용)
// - 원장: public/slots.json (번호·이름·프롬프트·사용처)
// - 저장: figures 버킷 slots/{번호}/{후보k}.webp + figure_slots.meta(채택·필터·통계)
// - 드롭 파이프라인: 파일/zip 드래그 → 번호 매칭 → 배경 제거(브라우저) → WebP 변환 → 업로드
// - 슬롯 모달: 종이 미리보기(다크/라이트) · 후보 탭 채택 · 필터 슬라이더 · 후보 추가/삭제 · 프롬프트 복사
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import { UNIT_NAME } from "../lib/qcode";
import { slotUrl, adoptedCand, filterCss, bustSlotMeta } from "./StageFigure";

const SLOT_ROOT = "slots";
const ORT_CDN = "https://cdn.jsdelivr.net/npm/onnxruntime-web@1.19.2/dist/";
const MODEL_PATH = "models/silueta.onnx"; // figures 버킷에 업로드해 둘 것
const PARAMS = "--style raw --ar {ar} --no text, letters, numbers, watermark, frame, border";

const CSS = `
.ai3 { min-height: 100vh; padding: 18px 12px 70px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.ai3.light { background:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0DA95F; --in:#F4F6F8; --inbd:#D3D9DF; }
.ai3.dark { background:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#FFE03C; --in:#1B1E24; --inbd:#2A2E36; }
.ai3 .wrap { max-width: 760px; margin: 0 auto; }
.ai3 h2 { color: var(--ink); font-size: 18px; font-weight: 800; margin: 0; flex: 1; }
.ai3 .top { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.ai3 .back { color: var(--mut); font-size: 13px; cursor: pointer; text-decoration: underline; background: none; border: none; }
.ai3 .drop { border: 2px dashed var(--inbd); border-radius: 14px; padding: 18px 14px; text-align: center;
  color: var(--mut); font-size: 13px; line-height: 1.7; margin-bottom: 10px; background: var(--card); }
.ai3 .drop.over { border-color: var(--ac); color: var(--ac); }
.ai3 .row { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-bottom: 10px; }
.ai3 select { background: var(--card); border: 1px solid var(--bd); border-radius: 10px; color: var(--ink); font-size: 13px; padding: 8px 10px; }
.ai3 .tgl { background: transparent; border: 1px solid var(--bd); border-radius: 999px; color: var(--mut);
  font-size: 12.5px; font-weight: 700; padding: 7px 12px; cursor: pointer; }
.ai3 .tgl.on { border-color: var(--ac); color: var(--ac); }
.ai3 .stat { color: var(--mut); font-size: 12.5px; }
.ai3 table { width: 100%; border-collapse: collapse; background: var(--card); border: 1px solid var(--bd); border-radius: 12px; overflow: hidden; }
.ai3 th { text-align: left; font-size: 11.5px; color: var(--mut); padding: 8px 10px; border-bottom: 1px solid var(--bd); }
.ai3 td { font-size: 13px; color: var(--ink); padding: 8px 10px; border-bottom: 1px solid var(--bd); }
.ai3 tr:last-child td { border-bottom: none; }
.ai3 .num { font-weight: 800; color: var(--ac); white-space: nowrap; cursor: pointer; }
.ai3 .nm { cursor: pointer; }
.ai3 .sub { color: var(--mut); font-size: 11.5px; }
.ai3 .pill { display: inline-block; border: 1px solid var(--inbd); border-radius: 6px; font-size: 11px;
  padding: 1px 6px; color: var(--mut); margin-right: 4px; }
.ai3 .pill.ok { color: var(--ac); border-color: var(--ac); font-weight: 800; }
.ai3 .cp { background: var(--in); border: 1px solid var(--inbd); border-radius: 7px; font-size: 11.5px;
  padding: 4px 7px; cursor: pointer; color: var(--ink); margin-right: 4px; }
.ai3 .prog { background: var(--card); border: 1px solid var(--bd); border-radius: 12px; padding: 10px 12px;
  margin-bottom: 10px; font-size: 12.5px; color: var(--ink); }
.ai3 .bar { height: 6px; background: var(--in); border-radius: 999px; overflow: hidden; margin-top: 6px; }
.ai3 .bar i { display: block; height: 100%; background: var(--ac); transition: width .2s; }
.ai3 .warn { color: #DC2626; font-size: 12px; white-space: pre-wrap; margin-top: 6px; }
/* 모달 */
.ai3-dim { position: fixed; inset: 0; background: rgba(0,0,0,.5); z-index: 90; }
.ai3-md { position: fixed; left: 50%; top: 50%; transform: translate(-50%,-50%); z-index: 91;
  width: min(560px, 94vw); max-height: 90vh; overflow-y: auto; background: var(--card); border: 1px solid var(--bd);
  border-radius: 16px; padding: 14px; box-sizing: border-box; }
.ai3-md h3 { margin: 0 0 8px; font-size: 15px; color: var(--ink); }
.ai3 .paper { position: relative; width: 100%; aspect-ratio: 3/2; border-radius: 12px; overflow: hidden; border: 1px solid var(--bd); }
.ai3 .paper.dark { background: radial-gradient(130% 100% at 50% 12%, #26325a 0%, #1b2544 52%, #121a33 100%); }
.ai3 .paper.light { background: radial-gradient(120% 130% at 50% 0%, #faf4e6 0%, #f3ead6 60%, #eadfc4 100%); }
.ai3 .paper img { position: absolute; inset: 10%; width: 80%; height: 80%; object-fit: contain; }
.ai3 .cands { display: flex; gap: 8px; flex-wrap: wrap; margin: 10px 0; }
.ai3 .cand { position: relative; width: 76px; height: 76px; border: 2px solid var(--inbd); border-radius: 10px;
  background: var(--in); cursor: pointer; overflow: hidden; }
.ai3 .cand img { width: 100%; height: 100%; object-fit: contain; }
.ai3 .cand.on { border-color: var(--ac); }
.ai3 .cand .k { position: absolute; left: 3px; top: 2px; font-size: 10px; font-weight: 800; color: var(--mut); }
.ai3 .cand .del { position: absolute; right: -6px; top: -6px; width: 18px; height: 18px; border-radius: 999px;
  background: #DC2626; color: #fff; border: none; font-size: 10px; cursor: pointer; line-height: 1; }
.ai3 .sl { display: grid; grid-template-columns: 64px 1fr 44px; gap: 6px; align-items: center; font-size: 12px; color: var(--mut); }
.ai3 .btn { border: 1px solid var(--inbd); border-radius: 9px; font-size: 12.5px; font-weight: 800;
  padding: 8px 12px; cursor: pointer; background: var(--in); color: var(--ink); }
.ai3 .btn.pri { background: var(--ac); color: #fff; border-color: transparent; }
`;

/* ══════════ 배경 제거 (onnxruntime-web + silueta) ══════════ */
let sessP = null;
async function getSession() {
  if (!sessP) sessP = (async () => {
    const ort = await import(/* @vite-ignore */ ORT_CDN + "ort.min.mjs");
    ort.env.wasm.wasmPaths = ORT_CDN;
    const url = supabase.storage.from("figures").getPublicUrl(MODEL_PATH).data.publicUrl;
    let sess;
    try { sess = await ort.InferenceSession.create(url, { executionProviders: ["webgpu", "wasm"] }); }
    catch { sess = await ort.InferenceSession.create(url, { executionProviders: ["wasm"] }); }
    return { ort, sess };
  })();
  return sessP;
}
function canvas(w, h) {
  if (typeof OffscreenCanvas !== "undefined") return new OffscreenCanvas(w, h);
  const c = document.createElement("canvas"); c.width = w; c.height = h; return c;
}
async function removeBg(bitmap) {
  const { ort, sess } = await getSession();
  const S = 320, c = canvas(S, S), g = c.getContext("2d", { willReadFrequently: true });
  g.drawImage(bitmap, 0, 0, S, S);
  const d = g.getImageData(0, 0, S, S).data;
  const arr = new Float32Array(3 * S * S);
  const M = [0.485, 0.456, 0.406], SD = [0.229, 0.224, 0.225];
  for (let i = 0; i < S * S; i++)
    for (let ch = 0; ch < 3; ch++) arr[ch * S * S + i] = (d[i * 4 + ch] / 255 - M[ch]) / SD[ch];
  const out = await sess.run({ [sess.inputNames[0]]: new ort.Tensor("float32", arr, [1, 3, S, S]) });
  const m = out[sess.outputNames[0]].data;
  let mi = Infinity, ma = -Infinity;
  for (let i = 0; i < m.length; i++) { if (m[i] < mi) mi = m[i]; if (m[i] > ma) ma = m[i]; }
  const mc = canvas(S, S), mg = mc.getContext("2d");
  const md = mg.createImageData(S, S);
  for (let i = 0; i < S * S; i++) {
    let a = (m[i] - mi) / (ma - mi + 1e-6);
    a = a < 0.15 ? 0 : a > 0.85 ? 1 : (a - 0.15) / 0.7;   // 부드러운 임계
    md.data[i * 4 + 3] = Math.round(a * 255);
  }
  mg.putImageData(md, 0, 0);
  const W = bitmap.width, H = bitmap.height;
  const oc = canvas(W, H), og = oc.getContext("2d");
  og.drawImage(bitmap, 0, 0);
  og.globalCompositeOperation = "destination-in";
  og.imageSmoothingEnabled = true; og.imageSmoothingQuality = "high";
  og.drawImage(mc, 0, 0, W, H);
  return oc;
}
function trimAlpha(cv) {
  const g = cv.getContext("2d", { willReadFrequently: true });
  const W = cv.width, H = cv.height, step = Math.max(1, Math.floor(Math.min(W, H) / 400));
  const d = g.getImageData(0, 0, W, H).data;
  let x0 = W, y0 = H, x1 = 0, y1 = 0, lum = 0, cnt = 0;
  for (let y = 0; y < H; y += step) for (let x = 0; x < W; x += step) {
    const i = (y * W + x) * 4;
    if (d[i + 3] > 20) {
      if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
      lum += (0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2]) / 255; cnt++;
    }
  }
  if (!cnt || x1 <= x0 || y1 <= y0) return { cv, lum: 0.5 };
  const pad = Math.round(Math.min(W, H) * 0.02);
  x0 = Math.max(0, x0 - pad); y0 = Math.max(0, y0 - pad);
  x1 = Math.min(W, x1 + pad); y1 = Math.min(H, y1 + pad);
  const oc = canvas(x1 - x0, y1 - y0);
  oc.getContext("2d").drawImage(cv, x0, y0, x1 - x0, y1 - y0, 0, 0, x1 - x0, y1 - y0);
  return { cv: oc, lum: lum / cnt };
}
async function toWebp(cv, long = 1600, q = 0.9) {
  const r = Math.min(1, long / Math.max(cv.width, cv.height));
  let out = cv;
  if (r < 1) {
    out = canvas(Math.round(cv.width * r), Math.round(cv.height * r));
    const g = out.getContext("2d"); g.imageSmoothingQuality = "high";
    g.drawImage(cv, 0, 0, out.width, out.height);
  }
  if (out.convertToBlob) return out.convertToBlob({ type: "image/webp", quality: q });
  return new Promise((res) => out.toBlob(res, "image/webp", q));
}

/* ══════════ 페이지 ══════════ */
export default function AdminImages({ theme = "light" }) {
  const [ledger, setLedger] = useState(null);   // slots.json
  const [rows, setRows] = useState({});         // slot -> meta
  const [unit, setUnit] = useState("all");
  const [onlyMissing, setOnlyMissing] = useState(false);
  const [doRemove, setDoRemove] = useState(true);
  const [over, setOver] = useState(false);
  const [prog, setProg] = useState(null);       // {done,total,cur}
  const [warn, setWarn] = useState("");
  const [openSlot, setOpenSlot] = useState(null);
  const [review, setReview] = useState(null); // 자동 매칭 확인 목록
  const fileRef = useRef(null);

  useEffect(() => {
    fetch("/slots.json").then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(setLedger)
      .catch(() => setWarn("public/slots.json 을 읽지 못했습니다 — 원장 파일을 리포 public/ 폴더에 커밋해 주세요."));
    refreshMeta();
  }, []);
  async function refreshMeta() {
    const { data } = await supabase.from("figure_slots").select("slot, meta");
    const m = {}; for (const r of data || []) m[r.slot] = r.meta || {};
    setRows(m);
  }

  // 원장 인덱스: slot -> {name, ar, A,B,C, cid, sid} / usage
  const idx = useMemo(() => {
    if (!ledger) return null;
    const def = {}, usage = {};
    for (const sc of ledger.scenes || []) {
      for (const L of sc.layers || []) {
        const n = L.slot;
        (usage[n] = usage[n] || []).push(`${sc.cid}·${sc.sid}`);
        if (!L.reuse && !def[n]) def[n] = { name: L.name, ar: L.ar, A: L.A, B: L.B, C: L.C, cid: sc.cid, sid: sc.sid };
      }
    }
    return { def, usage, order: Object.keys(def).map(Number).sort((a, b) => a - b) };
  }, [ledger]);

  const units = useMemo(() => {
    if (!idx) return [];
    return [...new Set(idx.order.map((n) => idx.def[n].cid.slice(0, idx.def[n].cid.lastIndexOf("-"))))];
  }, [idx]);

  const list = useMemo(() => {
    if (!idx) return [];
    return idx.order.filter((n) => {
      const u = idx.def[n].cid.slice(0, idx.def[n].cid.lastIndexOf("-"));
      if (unit !== "all" && u !== unit) return false;
      if (onlyMissing && rows[n]) return false;
      return true;
    });
  }, [idx, unit, onlyMissing, rows]);

  const prompt = (n, k) => {
    const d = idx.def[n];
    return `${d[k]}, ${ledger.style} ${PARAMS.replace("{ar}", d.ar)}`;
  };
  const copy = (t) => navigator.clipboard?.writeText(t);

  /* 드롭 파이프라인 */
  async function collectFiles(dt) {
    const out = [], items = [...dt.files];
    for (const f of items) {
      if (/\.zip$/i.test(f.name)) {
        try {
          const mod = await import(/* @vite-ignore */ "https://cdn.jsdelivr.net/npm/jszip@3.10.1/+esm");
          const zip = await mod.default.loadAsync(f);
          for (const name of Object.keys(zip.files)) {
            const e = zip.files[name];
            if (e.dir || !/\.(png|jpe?g|webp)$/i.test(name) || name.includes("__MACOSX")) continue;
            out.push(new File([await e.async("blob")], name.split("/").pop()));
          }
        } catch { setWarn((w) => w + "\nzip 해제 실패: " + f.name); }
      } else if (/\.(png|jpe?g|webp)$/i.test(f.name)) out.push(f);
    }
    return out;
  }

  // 미드저니 파일명(프롬프트 앞 단어들)로 슬롯 추측
  const STOP = new Set(("a an the of on in to with and its seen from view straight directly above side front no " +
    "gouache painting manner korean gold ink landscape paintings dark indigo dyed paper opaque matte brush strokes " +
    "visible texture fine accents muted lapis verdigris warm ochre palette simple friendly educational illustration " +
    "single clear subject isolated plain flat background full object margins cast shadow ground text style raw one small large").split(" "));
  const tok = (t) => t.toLowerCase().split(/[^a-z]+/).filter((w) => w.length > 2 && !STOP.has(w));
  const slotTokens = useMemo(() => {
    if (!idx) return {};
    const m = {};
    for (const n of idx.order) m[n] = new Set(tok(`${idx.def[n].A} ${idx.def[n].B} ${idx.def[n].C}`));
    return m;
  }, [idx]);
  function guessSlot(fname) {
    const ft = new Set(tok(fname.replace(/\.[^.]+$/, "")).slice(1)); // 첫 토큰(계정명) 제외
    let best = null, bs = 0, second = 0;
    for (const n of idx.order) {
      let sc = 0;
      for (const w of ft) if (slotTokens[n].has(w)) sc++;
      if (sc > bs) { second = bs; bs = sc; best = n; }
      else if (sc > second) second = sc;
    }
    return bs >= 2 && bs - second >= 1 ? { slot: best, score: bs } : { slot: null, score: bs };
  }

  // 등록 직전 저장소 기준으로 다음 후보 번호 산출 (여러 탭 병렬 사용 대비)
  async function baseK(slot, meta) {
    try {
      const { data } = await supabase.storage.from("figures").list(`${SLOT_ROOT}/${slot}`, { limit: 100 });
      const ks = (data || []).map((f) => +f.name.replace(/\.webp$/i, "")).filter(Number.isFinite);
      return Math.max(meta.n || 0, ...(ks.length ? ks : [0]));
    } catch { return meta.n || 0; }
  }

  // 공통 등록 루프: jobs = [{f, slot, k|null}]
  async function runJobs(jobs) {
    if (!jobs.length) return;
    if (prog) { setWarn("이전 배치 처리 중 — 진행 막대가 끝난 뒤 다시 드래그해 주세요."); return; }
    jobs.sort((a, b) => a.slot - b.slot || (a.k || 99) - (b.k || 99));
    setProg({ done: 0, total: jobs.length, cur: "" });
    const touched = {}, nextK = {};
    for (const j of jobs) {
      setProg((p) => ({ ...p, cur: `#${j.slot} ${idx.def[j.slot]?.name || ""}` }));
      try {
        const bmp = await createImageBitmap(j.f);
        let cv;
        if (doRemove) cv = await removeBg(bmp);
        else { cv = canvas(bmp.width, bmp.height); cv.getContext("2d").drawImage(bmp, 0, 0); }
        const { cv: cut, lum } = trimAlpha(cv);
        const blob = await toWebp(cut);
        const meta = touched[j.slot] || rows[j.slot] || {};
        const k = j.k || ((nextK[j.slot] = (nextK[j.slot] ?? await baseK(j.slot, meta)) + 1));
        const { error } = await supabase.storage.from("figures")
          .upload(`${SLOT_ROOT}/${j.slot}/${k}.webp`, blob, { upsert: true, contentType: "image/webp" });
        if (error) throw error;
        touched[j.slot] = {
          ...meta, n: Math.max(meta.n || 0, k),
          adopted: meta.adopted || { dark: k },
          stats: { lum: +lum.toFixed(3) }, updated: Date.now(),
        };
      } catch (e) { setWarn((w) => (w ? w + "\n" : "") + `#${j.slot} 실패: ${e?.message || e}`); }
      setProg((p) => ({ ...p, done: p.done + 1 }));
      // 이 슬롯의 마지막 파일이면 메타 즉시 저장 — 중간에 끊겨도 완료분은 등록 상태 유지
      const last = !jobs.some((x, xi) => x.slot === j.slot && xi > jobs.indexOf(j));
      if (last && touched[j.slot]) {
        const { error } = await supabase.from("figure_slots")
          .upsert({ slot: j.slot, meta: touched[j.slot], updated_at: new Date().toISOString() });
        if (error) setWarn((w) => w + "\n메타 저장 실패 #" + j.slot + ": " + error.message + " (figure_slots SQL 실행 여부 확인)");
        bustSlotMeta(j.slot);
      }
    }
    setProg(null); refreshMeta();
  }

  // 전체 드롭: 번호 이름은 바로, 그 외는 자동 매칭 → 확인 목록
  async function processFiles(files) {
    if (!idx) return;
    const jobs = [], toGuess = [];
    for (const f of files) {
      const m = f.name.match(/^(\d+)(?:-(\d+))?\.(png|jpe?g|webp)$/i);
      if (m && idx.def[+m[1]]) jobs.push({ f, slot: +m[1], k: m[2] ? +m[2] : null });
      else toGuess.push(f);
    }
    setWarn("");
    if (jobs.length) await runJobs(jobs);
    if (toGuess.length)
      setReview(toGuess.map((f) => ({ f, url: URL.createObjectURL(f), ...guessSlot(f.name) })));
  }
  const onDrop = async (e) => { e.preventDefault(); setOver(false); processFiles(await collectFiles(e.dataTransfer)); };

  const cls = "ai3 " + (theme === "dark" ? "dark" : "light");
  const registered = idx ? idx.order.filter((n) => rows[n]).length : 0;
  return (
    <div className={cls}>
      <style>{CSS}</style>
      <div className="wrap">
        <div className="top">
          <h2>🖼 이미지 관리 <span className="stat">v3 · 슬롯</span></h2>
          <button className="back" onClick={() => (location.hash = "#/admin")}>← 관리자</button>
        </div>

        <div className="drop" onDragOver={(e) => { e.preventDefault(); setOver(true); }}
          onDragLeave={() => setOver(false)} onDrop={onDrop}
          onClick={() => fileRef.current?.click()} style={over ? { borderColor: "var(--ac)" } : null}>
          이미지·zip을 여기로 드래그 — 번호 이름(<b>7.png</b>)은 바로, 미드저니 원본 이름은 <b>자동 매칭 후 확인</b><br />
          <span className="stat">개별 슬롯 <b>행 위에</b> 떨어뜨리면 이름과 무관하게 그 슬롯에 등록됩니다 · 배경 제거 → WebP 자동</span>
          <input ref={fileRef} type="file" multiple accept=".png,.jpg,.jpeg,.webp,.zip" style={{ display: "none" }}
            onChange={(e) => { processFiles([...e.target.files].filter((f) => /\.(png|jpe?g|webp|zip)$/i.test(f.name))); e.target.value = ""; }} />
        </div>

        <div className="row">
          <select value={unit} onChange={(e) => setUnit(e.target.value)}>
            <option value="all">전체 단원</option>
            {units.map((u) => <option key={u} value={u}>{u} {UNIT_NAME?.[u] || ""}</option>)}
          </select>
          <button className={"tgl" + (onlyMissing ? " on" : "")} onClick={() => setOnlyMissing((v) => !v)}>미등록만</button>
          <button className={"tgl" + (doRemove ? " on" : "")} onClick={() => setDoRemove((v) => !v)}
            title="끄면 이미 오려낸 이미지를 그대로 등록">배경 제거 {doRemove ? "ON" : "OFF"}</button>
          <span style={{ flex: 1 }} />
          <span className="stat">{registered} / {idx ? idx.order.length : "…"} 등록</span>
        </div>

        {prog && (
          <div className="prog">
            처리 중 {prog.done}/{prog.total} — {prog.cur}
            <div className="bar"><i style={{ width: `${(100 * prog.done) / prog.total}%` }} /></div>
          </div>
        )}
        {warn && <div className="warn">{warn}</div>}

        {review && (
          <div className="prog">
            <b>자동 매칭 확인</b> — 파일명 단어로 추측했어요. 번호를 고치거나 비우면 건너뜁니다.
            <div className="cands" style={{ marginTop: 8 }}>
              {review.map((r, i) => (
                <div key={i} style={{ width: 96, textAlign: "center" }}>
                  <div className="cand" style={{ width: 96, height: 96, cursor: "default" }}>
                    <img src={r.url} alt="" />
                  </div>
                  <input type="number" value={r.slot ?? ""} placeholder="?"
                    onChange={(e) => setReview((v) => v.map((x, j) => j === i ? { ...x, slot: e.target.value === "" ? null : +e.target.value } : x))}
                    style={{ width: 64, marginTop: 4, textAlign: "center", background: "var(--in)", border: "1px solid var(--inbd)", borderRadius: 7, padding: "3px 4px", color: "var(--ink)" }} />
                  <div className="sub">{r.slot && idx.def[r.slot] ? idx.def[r.slot].name : "직접 입력"}</div>
                </div>
              ))}
            </div>
            <div className="row" style={{ marginTop: 8, justifyContent: "flex-end" }}>
              <button className="btn" onClick={() => { review.forEach((r) => URL.revokeObjectURL(r.url)); setReview(null); }}>취소</button>
              <button className="btn pri" onClick={() => {
                const jobs = review.filter((r) => r.slot && idx.def[r.slot]).map((r) => ({ f: r.f, slot: r.slot, k: null }));
                review.forEach((r) => URL.revokeObjectURL(r.url)); setReview(null); runJobs(jobs);
              }}>{review.filter((r) => r.slot && idx.def[r.slot]).length}건 등록</button>
            </div>
          </div>
        )}

        <table>
          <thead><tr><th>#</th><th>이름</th><th>쓰임</th><th>후보</th><th>프롬프트</th></tr></thead>
          <tbody>
            {list.map((n) => {
              const d = idx.def[n], m = rows[n];
              return (
                <tr key={n}
                  onDragOver={(e) => { e.preventDefault(); e.currentTarget.style.outline = "2px dashed var(--ac)"; }}
                  onDragLeave={(e) => { e.currentTarget.style.outline = ""; }}
                  onDrop={async (e) => { e.preventDefault(); e.stopPropagation(); e.currentTarget.style.outline = "";
                    runJobs((await collectFiles(e.dataTransfer)).map((f) => ({ f, slot: n, k: null }))); }}>
                  <td className="num" onClick={() => setOpenSlot(n)}>{n}</td>
                  <td className="nm" onClick={() => setOpenSlot(n)}>
                    {d.name}<br /><span className="sub">{d.cid} · --ar {d.ar}</span>
                  </td>
                  <td><span className="pill">{idx.usage[n]?.length || 0}곳</span></td>
                  <td>{m ? <span className="pill ok">{m.n || 0}장</span> : <span className="pill">—</span>}</td>
                  <td>
                    <button className="cp" onClick={() => copy(prompt(n, "A"))}>📋A</button>
                    <button className="cp" onClick={() => copy(prompt(n, "B"))}>B</button>
                    <button className="cp" onClick={() => copy(prompt(n, "C"))}>C</button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      {openSlot != null && idx && (
        <SlotModal slot={openSlot} def={idx.def[openSlot]} usage={idx.usage[openSlot] || []}
          meta={rows[openSlot] || null} themeInit={theme === "dark" ? "dark" : "light"}
          onClose={(changed) => { setOpenSlot(null); if (changed) { bustSlotMeta(openSlot); refreshMeta(); } }} />
      )}
    </div>
  );
}

/* ══════════ 슬롯 모달 ══════════ */
function SlotModal({ slot, def, usage, meta: meta0, themeInit, onClose }) {
  const [meta, setMeta] = useState(meta0 || {});
  const [cands, setCands] = useState(null);   // [k...]
  const [pv, setPv] = useState(themeInit);    // 미리보기 테마
  const [changed, setChanged] = useState(false);
  const [rmBg, setRmBg] = useState(false); // 모달 추가는 기본 "이미 오려낸 파일"
  const [warn, setWarn] = useState("");
  const addRef = useRef(null);

  const load = async () => {
    const { data } = await supabase.storage.from("figures").list(`${SLOT_ROOT}/${slot}`, { limit: 100 });
    setCands((data || []).map((f) => +f.name.replace(/\.webp$/i, "")).filter(Number.isFinite).sort((a, b) => a - b));
  };
  useEffect(() => { load(); }, [slot]);

  const adopted = adoptedCand(meta, pv);
  const saveMeta = async (next) => {
    setMeta(next); setChanged(true);
    const { error } = await supabase.from("figure_slots")
      .upsert({ slot, meta: { ...next, updated: Date.now() }, updated_at: new Date().toISOString() });
    if (error) setWarn("저장 실패: " + error.message);
  };
  const adopt = (k) => saveMeta({ ...meta, n: Math.max(meta.n || 0, ...(cands || [k])), adopted: { ...(meta.adopted || {}), [pv]: k } });
  const setF = (key, v) => {
    const f = { ...(meta.filters || {}) };
    f[pv] = { ...(f[pv] || {}), [key]: +v };
    saveMeta({ ...meta, filters: f });
  };
  const fcur = { b: 1, c: 1, s: 1, e: pv === "light" ? 0.12 : 0, ...((meta.filters || {})[pv] || {}) };
  const del = async (k) => {
    if (!confirm(`후보 ${k}번을 삭제할까?`)) return;
    await supabase.storage.from("figures").remove([`${SLOT_ROOT}/${slot}/${k}.webp`]);
    const left = (cands || []).filter((x) => x !== k);
    setCands(left);
    const ad = { ...(meta.adopted || {}) };
    for (const t of Object.keys(ad)) if (ad[t] === k) ad[t] = left[0] || 1;
    saveMeta({ ...meta, n: left.length ? Math.max(...left) : 0, adopted: ad });
  };
  const addFiles = async (files) => {
    const { data } = await supabase.storage.from("figures").list(`${SLOT_ROOT}/${slot}`, { limit: 100 });
    const ks = (data || []).map((f) => +f.name.replace(/\.webp$/i, "")).filter(Number.isFinite);
    let k = Math.max(0, ...(ks.length ? ks : [0]), ...(cands || [0]));
    for (const f of files) {
      try {
        const bmp = await createImageBitmap(f);
        let cv;
        if (rmBg) cv = await removeBg(bmp);
        else { cv = canvas(bmp.width, bmp.height); cv.getContext("2d").drawImage(bmp, 0, 0); }
        const { cv: cut } = trimAlpha(cv);
        const blob = await toWebp(cut);
        k += 1;
        await supabase.storage.from("figures").upload(`${SLOT_ROOT}/${slot}/${k}.webp`, blob, { upsert: true, contentType: "image/webp" });
      } catch (e) { setWarn("추가 실패: " + (e?.message || e)); }
    }
    await load(); saveMeta({ ...meta, n: k, adopted: meta.adopted || { dark: k } });
  };

  return (
    <>
      <div className="ai3-dim" onClick={() => onClose(changed)} />
      <div className="ai3-md">
        <h3>#{slot} {def.name} <span className="sub" style={{ fontWeight: 400 }}>· {usage.join(", ")}</span></h3>
        <div className={"paper " + pv}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => { e.preventDefault(); addFiles([...e.dataTransfer.files].filter((f) => /\.(png|jpe?g|webp)$/i.test(f.name))); }}>
          {cands && cands.includes(adopted) &&
            <img src={slotUrl(slot, adopted, meta.updated || "")} alt="" style={{ filter: filterCss(meta, pv) }} />}
        </div>
        <div className="row" style={{ margin: "8px 0" }}>
          <button className={"tgl" + (pv === "dark" ? " on" : "")} onClick={() => setPv("dark")}>감지(다크)</button>
          <button className={"tgl" + (pv === "light" ? " on" : "")} onClick={() => setPv("light")}>한지(라이트)</button>
          <span style={{ flex: 1 }} />
          <button className={"tgl" + (rmBg ? " on" : "")} onClick={() => setRmBg((v) => !v)}>배경 제거</button>
          <button className="btn" onClick={() => addRef.current?.click()}>후보 추가</button>
          <input ref={addRef} type="file" multiple accept=".png,.jpg,.jpeg,.webp" style={{ display: "none" }}
            onChange={(e) => { addFiles([...e.target.files]); e.target.value = ""; }} />
        </div>
        <div className="cands">
          {(cands || []).map((k) => (
            <div key={k} className={"cand" + (k === adopted ? " on" : "")} onClick={() => adopt(k)}>
              <span className="k">{k}</span>
              <img src={slotUrl(slot, k, meta.updated || "")} alt="" />
              <button className="del" onClick={(e) => { e.stopPropagation(); del(k); }}>✕</button>
            </div>
          ))}
          {cands && !cands.length && <span className="sub">후보 없음 — 드롭 화면에서 {slot}.png로 등록</span>}
        </div>
        {[["b", "밝기", 0.6, 1.4], ["c", "대비", 0.6, 1.4], ["s", "채도", 0.4, 1.6], ["e", "세피아", 0, 0.5]].map(([key, label, lo, hi]) => (
          <div className="sl" key={key}>
            <span>{label}</span>
            <input type="range" min={lo} max={hi} step="0.01" value={fcur[key]} onChange={(e) => setF(key, e.target.value)} />
            <span>{Number(fcur[key]).toFixed(2)}</span>
          </div>
        ))}
        {warn && <div className="warn">{warn}</div>}
        <div className="row" style={{ marginTop: 10, justifyContent: "flex-end" }}>
          <button className="btn pri" onClick={() => onClose(changed)}>닫기</button>
        </div>
      </div>
    </>
  );
}
