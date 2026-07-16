import { useEffect, useRef, useState } from "react";
import { supabase } from "../supabaseClient";

// ashrain.out — 선생님 자료 등록 (v0.3.2)
// [v0.3.2] 드래그앤드롭 — 문제 PDF는 상자에, 정답 PDF는 버튼에 끌어다 놓기 지원
// src/components/AdminMaterials.jsx — AdminCalc.jsx(v0.3.0)의 📄 자료 탭이 import 합니다.
// 흐름: 문제 PDF 열기 → 문제 페이지 선택(최대 6장) → AI가 문제별로 잘라줌(경계 확인·조정·제외)
//      → 정답 페이지 선택(같은 PDF or 별도 PDF or 직접 입력) → AI가 정답 읽음 → 검토 → 등록
// 등록 결과: calc_units에 "[자료] 이름" 유닛 1개 + calc_problems에 이미지 문제들(image_path)
//           → 학생은 연산 탭에서 일반 문제처럼 풀고, OMR 답안지 채점도 가능

const GRADES = ["중1", "중2", "중3", "고1", "고2", "고3"];
const GRADE_UNIT = { "중1": "m1-1", "중2": "m2-1", "중3": "m3-1", "고1": "h1-1", "고2": "h2-1", "고3": "h3-1" };
const MAX_PAGES = 6;
const pad2 = (n) => String(n).padStart(2, "0");
const pad3 = (n) => String(n).padStart(3, "0");

let pdfjsPromise = null;
function loadPdfJs() {
  if (pdfjsPromise) return pdfjsPromise;
  pdfjsPromise = new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js";
    s.onload = () => {
      window.pdfjsLib.GlobalWorkerOptions.workerSrc =
        "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
      resolve(window.pdfjsLib);
    };
    s.onerror = () => reject(new Error("pdf.js 로드 실패 — 인터넷 연결을 확인해 주세요"));
    document.head.appendChild(s);
  });
  return pdfjsPromise;
}

async function aiCall(body) {
  const { data: sess } = await supabase.auth.getSession();
  const token = sess?.session?.access_token;
  if (!token) throw new Error("세션이 만료됐어요 — 다시 로그인해 주세요");
  const r = await fetch("/api/ai", {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
    body: JSON.stringify(body),
  });
  const j = await r.json();
  if (!r.ok) throw new Error(j?.error || "요청 실패");
  return j;
}

const CSS = `
.am-drop { border:1.5px dashed var(--bd); border-radius:14px; padding:14px; margin-top:12px; text-align:center; }
.am-drop.on { border-color:var(--ac); background:rgba(127,127,127,.08); }
.am-dropTxt { margin:9px 0 0; font-size:12px; color:var(--mut); }
.am-ghost.dragon { border-color:var(--ac); color:var(--ac); border-style:dashed; }
.am-note { color:var(--mut); font-size:12px; line-height:1.65; margin:0 2px 12px; }
.am-lab { font-size:12.5px; color:var(--mut); margin:12px 0 6px; font-weight:700; }
.am-in { width:100%; box-sizing:border-box; background:transparent; border:1px solid var(--bd); border-radius:10px;
  padding:10px 12px; color:var(--ink); font-size:14px; }
.am-chips { display:flex; flex-wrap:wrap; gap:6px; margin:4px 0 8px; }
.am-chip { border:1px solid var(--bd); background:var(--card); color:var(--mut); border-radius:999px; padding:7px 13px; font-size:13px; cursor:pointer; }
.am-chip.on { color:var(--ac); border-color:var(--ac); font-weight:800; }
.am-go { width:100%; margin-top:12px; padding:12px; border-radius:11px; border:1px solid var(--ac); background:transparent;
  color:var(--ac); font-weight:800; font-size:14px; cursor:pointer; }
.am-go:disabled { opacity:.4; }
.am-ghost { width:100%; margin-top:8px; padding:10px; border-radius:11px; border:1px solid var(--bd); background:transparent;
  color:var(--mut); font-size:13px; cursor:pointer; }
.am-prog { text-align:center; color:var(--mut); font-size:13.5px; padding:26px 0; line-height:1.8; }
.am-thumbs { display:grid; grid-template-columns:repeat(auto-fill,minmax(86px,1fr)); gap:8px; }
.am-thumb { position:relative; border:2px solid var(--bd); border-radius:10px; overflow:hidden; padding:0; cursor:pointer; background:var(--card); }
.am-thumb img { width:100%; display:block; }
.am-thumb.on { border-color:var(--ac); }
.am-thumb span { position:absolute; top:4px; left:4px; background:var(--card); border:1px solid var(--bd);
  border-radius:6px; font-size:10.5px; padding:1px 6px; color:var(--ink); }
.am-item { border:1px solid var(--bd); border-radius:12px; padding:10px; margin-bottom:10px; background:var(--card); }
.am-item.off { opacity:.38; }
.am-crop { width:100%; border-radius:8px; border:1px solid var(--bd); display:block; background:#fff; }
.am-irow { display:flex; gap:6px; align-items:center; margin-top:8px; flex-wrap:wrap; }
.am-num { width:58px; text-align:center; }
.am-ans { flex:1; min-width:90px; }
.am-ans.miss { border-color:#E5484D; }
.am-mini { border:1px solid var(--bd); background:transparent; color:var(--mut); border-radius:8px; padding:6px 8px; font-size:11.5px; cursor:pointer; }
.am-mini.warn { color:#E5484D; border-color:#E5484D55; }
.am-cnt { font-size:12.5px; color:var(--mut); margin:2px 2px 10px; }
`;

export default function AdminMaterials({ say }) {
  const [step, setStep] = useState("setup");     // setup | probPages | slicing | ansPage | reading | review | saving
  const [title, setTitle] = useState("");
  const [grade, setGrade] = useState("중1");
  const [thumbs, setThumbs] = useState([]);      // [{no, url}]
  const [probSel, setProbSel] = useState(() => new Set());
  const [items, setItems] = useState([]);        // {key, no, box, srcCv, url, answer, excluded}
  const [prog, setProg] = useState("");
  const docRef = useRef(null);
  const fullCache = useRef(new Map());           // 현재 문서의 pageNo → 1400px 캔버스
  const probFileRef = useRef(null);
  const ansFileRef = useRef(null);
  const [drag, setDrag] = useState(false);

  useEffect(() => {                                 // 빗나간 드롭이 페이지를 덮지 않게
    const stop = (e) => e.preventDefault();
    window.addEventListener("dragover", stop);
    window.addEventListener("drop", stop);
    return () => { window.removeEventListener("dragover", stop); window.removeEventListener("drop", stop); };
  }, []);
  const dropProps = (forAnswers) => ({
    onDragOver: (e) => { e.preventDefault(); setDrag(true); },
    onDragLeave: () => setDrag(false),
    onDrop: (e) => {
      e.preventDefault(); setDrag(false);
      const f = e.dataTransfer.files?.[0];
      if (!f) return;
      if (!(f.type === "application/pdf" || /\.pdf$/i.test(f.name))) { say("PDF 파일만 올릴 수 있어요"); return; }
      openPdf(f, forAnswers);
    },
  });

  // ── PDF 열기 (문제용 / 정답용 공용) ──
  async function openPdf(f, forAnswers) {
    if (!f) return;
    try {
      setProg("PDF 여는 중…");
      setStep(forAnswers ? "ansPage" : "probPages");
      const pdfjs = await loadPdfJs();
      const buf = await f.arrayBuffer();
      const doc = await pdfjs.getDocument({ data: buf }).promise;
      docRef.current = doc;
      fullCache.current = new Map();             // 문서 바뀌면 캐시 초기화 (잘라둔 문제는 안전)
      const list = [];
      for (let i = 1; i <= doc.numPages; i++) {
        const page = await doc.getPage(i);
        const vp0 = page.getViewport({ scale: 1 });
        const vp = page.getViewport({ scale: 120 / vp0.width });
        const cv = document.createElement("canvas");
        cv.width = vp.width; cv.height = vp.height;
        await page.render({ canvasContext: cv.getContext("2d"), viewport: vp }).promise;
        list.push({ no: i, url: cv.toDataURL("image/jpeg", 0.6) });
        setProg(`PDF 여는 중… ${i}/${doc.numPages}`);
      }
      setThumbs(list);
      if (!forAnswers) setProbSel(new Set());
      setProg("");
    } catch (err) {
      say("PDF 열기 실패: " + (err?.message || String(err)));
      setStep(forAnswers ? "ansPage" : "setup");
      setProg("");
    }
  }

  async function renderFull(pageNo) {
    if (fullCache.current.has(pageNo)) return fullCache.current.get(pageNo);
    const page = await docRef.current.getPage(pageNo);
    const vp0 = page.getViewport({ scale: 1 });
    const vp = page.getViewport({ scale: 1400 / vp0.width });
    const cv = document.createElement("canvas");
    cv.width = vp.width; cv.height = vp.height;
    await page.render({ canvasContext: cv.getContext("2d"), viewport: vp }).promise;
    fullCache.current.set(pageNo, cv);
    return cv;
  }

  function cropBox(srcCv, box) {
    const W = srcCv.width, H = srcCv.height;
    const sx = Math.max(0, Math.round(box.x * W));
    const sy = Math.max(0, Math.round(box.y * H));
    const sw = Math.min(W - sx, Math.max(24, Math.round(box.w * W)));
    const sh = Math.min(H - sy, Math.max(24, Math.round(box.h * H)));
    const out = document.createElement("canvas");
    out.width = sw; out.height = sh;
    const ctx = out.getContext("2d");
    ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, sw, sh);
    ctx.drawImage(srcCv, sx, sy, sw, sh, 0, 0, sw, sh);
    return out;
  }
  const cvUrl = (cv) => cv.toDataURL("image/jpeg", 0.85);

  // ── 문제 페이지들 → AI 분해 ──
  async function startSlicing() {
    const pages = [...probSel].sort((a, b) => a - b);
    if (!pages.length) { say("문제 페이지를 선택해 주세요"); return; }
    setStep("slicing");
    const got = [];
    try {
      for (let k = 0; k < pages.length; k++) {
        setProg(`페이지 ${k + 1}/${pages.length} — AI가 문제를 찾는 중… (페이지당 15~30초)`);
        const full = await renderFull(pages[k]);
        const base64 = full.toDataURL("image/jpeg", 0.8).split(",")[1];
        const { problems } = await aiCall({ task: "slice", image: base64 });
        (problems || []).forEach((p, i) => {
          // 사방 1% 여백을 더해 잘림 방지
          const box = {
            x: Math.max(0, p.box.x - 0.01), y: Math.max(0, p.box.y - 0.01),
            w: Math.min(1, p.box.w + 0.02), h: Math.min(1, p.box.h + 0.02),
          };
          const cv = cropBox(full, box);
          got.push({
            key: `${pages[k]}-${i}-${p.no}`, no: p.no, box, srcCv: full,
            url: cvUrl(cv), answer: "", excluded: false,
          });
        });
      }
      if (!got.length) throw new Error("문제를 찾지 못했어요 — 페이지를 다시 선택해 보세요");
      setItems(got);
      setStep("ansPage");
      setProg("");
      say(`문제 ${got.length}개를 찾았어요 — 이제 정답 페이지를 골라 주세요`);
    } catch (err) {
      say("분석 실패: " + (err?.message || String(err)));
      setStep("probPages");
      setProg("");
    }
  }

  // ── 정답 페이지 → AI 읽기 ──
  async function readAnswers(pageNo) {
    setStep("reading");
    setProg("정답표를 읽는 중… (10~20초)");
    try {
      const full = await renderFull(pageNo);
      const base64 = full.toDataURL("image/jpeg", 0.8).split(",")[1];
      const { answers } = await aiCall({ task: "answers", image: base64 });
      const map = {};
      (answers || []).forEach((a) => { map[a.no] = a.answer; });
      let hit = 0;
      setItems((its) => its.map((it) => {
        if (map[it.no] != null) { hit++; return { ...it, answer: map[it.no] }; }
        return it;
      }));
      setStep("review");
      setProg("");
      say(`정답 ${hit}개를 채웠어요 — 검토 후 등록해 주세요`);
    } catch (err) {
      say("정답 읽기 실패: " + (err?.message || String(err)));
      setStep("ansPage");
      setProg("");
    }
  }

  // ── 검토: 경계 조정·제외 ──
  function adjust(key, mode) {
    setItems((its) => its.map((it) => {
      if (it.key !== key) return it;
      const b = { ...it.box };
      const d = 0.02;
      if (mode === "topOut") { b.y = Math.max(0, b.y - d); b.h = Math.min(1, b.h + d); }
      if (mode === "topIn") { b.y = b.y + d; b.h = Math.max(0.03, b.h - d); }
      if (mode === "botOut") { b.h = Math.min(1, b.h + d); }
      if (mode === "botIn") { b.h = Math.max(0.03, b.h - d); }
      const cv = cropBox(it.srcCv, b);
      return { ...it, box: b, url: cvUrl(cv) };
    }));
  }
  const setField = (key, patch) =>
    setItems((its) => its.map((it) => (it.key === key ? { ...it, ...patch } : it)));

  // ── 등록 ──
  async function save() {
    const inc = items.filter((it) => !it.excluded);
    if (!title.trim()) { say("자료 이름을 입력해 주세요"); return; }
    if (!inc.length) { say("등록할 문제가 없어요"); return; }
    const miss = inc.filter((it) => !String(it.answer).trim());
    if (miss.length) { say(`답이 비어 있는 문항 ${miss.length}개 — 입력하거나 [제외]해 주세요`); return; }
    const nos = inc.map((it) => Math.round(+it.no));
    if (nos.some((n) => !Number.isFinite(n) || n < 1)) { say("문항 번호가 잘못된 항목이 있어요"); return; }
    if (new Set(nos).size !== nos.length) { say("문항 번호가 중복됐어요 — 번호를 고쳐 주세요"); return; }

    setStep("saving");
    try {
      const unitId = "mat-" + Date.now().toString(36);
      const sort = (Math.floor(Date.now() / 1000) % 100000) + 1000;   // 일반 유닛 뒤, 등록 순 유지
      const { error: e0 } = await supabase.from("calc_units").upsert({
        id: unitId, name: "[자료] " + title.trim(), grade,
        unit_id: GRADE_UNIT[grade], sort,
      });
      if (e0) throw e0;

      const rows = [];
      for (let i = 0; i < inc.length; i++) {
        const it = inc[i];
        const no = Math.round(+it.no);
        setProg(`이미지 업로드 중… ${i + 1}/${inc.length}`);
        const cv = cropBox(it.srcCv, it.box);
        const blob = await new Promise((r) => cv.toBlob(r, "image/jpeg", 0.85));
        const path = `materials/${unitId}/${pad2(no)}.jpg`;
        const { error: e1 } = await supabase.storage.from("notes")
          .upload(path, blob, { contentType: "image/jpeg", upsert: true });
        if (e1) throw e1;
        const ans = String(it.answer).trim();
        rows.push({
          id: `${unitId}-${pad3(no)}`, calc_unit: unitId,
          type: /^[①②③④⑤]$/.test(ans) ? "choice" : /^[OX]$/i.test(ans) ? "ox" : "calc",
          choices: null, question: `문항 ${no}`,
          answer: /^[OX]$/i.test(ans) ? ans.toUpperCase() : ans,
          image_path: path, difficulty: 2, time_limit: 60, origin: "manual",
        });
      }
      setProg("문제 등록 중…");
      const { error: e2 } = await supabase.from("calc_problems").upsert(rows);
      if (e2) throw e2;
      say(`✅ [자료] ${title.trim()} — ${rows.length}문항 등록 완료`);
      reset();
    } catch (err) {
      say("등록 실패: " + (err?.message || String(err)));
      setStep("review");
      setProg("");
    }
  }

  function reset() {
    setStep("setup"); setTitle(""); setThumbs([]); setProbSel(new Set());
    setItems([]); setProg(""); docRef.current = null; fullCache.current = new Map();
  }

  const incCount = items.filter((it) => !it.excluded).length;

  return (
    <div>
      <style>{CSS}</style>
      <input ref={probFileRef} type="file" accept="application/pdf" hidden onChange={(e) => { openPdf(e.target.files?.[0], false); e.target.value = ""; }} />
      <input ref={ansFileRef} type="file" accept="application/pdf" hidden onChange={(e) => { openPdf(e.target.files?.[0], true); e.target.value = ""; }} />

      {step === "setup" && (
        <>
          <p className="am-note">
            문제 PDF를 열면 AI가 페이지에서 문제를 하나씩 잘라내고, 빠른정답 페이지를 읽어 정답을 채워요.
            등록된 자료는 연산 탭에 「[자료] 이름」 단원으로 올라가 학생이 바로 풀 수 있어요 (답안지 채점 포함).
          </p>
          <p className="am-lab">자료 이름</p>
          <input className="am-in" placeholder="예: 3월 대비 일차방정식 20제" value={title} onChange={(e) => setTitle(e.target.value)} />
          <p className="am-lab">학년</p>
          <div className="am-chips">
            {GRADES.map((g) => (
              <button key={g} className={"am-chip" + (grade === g ? " on" : "")} onClick={() => setGrade(g)}>{g}</button>
            ))}
          </div>
          <div className={"am-drop" + (drag ? " on" : "")} {...dropProps(false)}>
            <button className="am-go" style={{ marginTop: 0 }} onClick={() => probFileRef.current.click()}>📂 문제 PDF 열기</button>
            <p className="am-dropTxt">또는 PDF 파일을 이 상자에 끌어다 놓으세요</p>
          </div>
        </>
      )}

      {step === "probPages" && (
        <>
          {prog ? <p className="am-prog">{prog}</p> : (
            <>
              <p className="am-note">문제가 실려 있는 페이지를 탭해서 선택하세요 (최대 {MAX_PAGES}장). 정답 페이지는 다음 단계에서 골라요.</p>
              <div className="am-thumbs">
                {thumbs.map((t) => (
                  <button key={t.no} className={"am-thumb" + (probSel.has(t.no) ? " on" : "")}
                    onClick={() => setProbSel((s) => {
                      const n = new Set(s);
                      if (n.has(t.no)) n.delete(t.no);
                      else if (n.size >= MAX_PAGES) { say(`문제 페이지는 최대 ${MAX_PAGES}장까지예요`); return s; }
                      else n.add(t.no);
                      return n;
                    })}>
                    <span>{t.no}p</span><img src={t.url} alt="" />
                  </button>
                ))}
              </div>
              <button className="am-go" disabled={!probSel.size} onClick={startSlicing}>
                🤖 선택한 {probSel.size}장에서 문제 잘라내기
              </button>
              <button className="am-ghost" onClick={reset}>처음으로</button>
            </>
          )}
        </>
      )}

      {(step === "slicing" || step === "reading" || step === "saving") && (
        <p className="am-prog">{prog || "처리 중…"}</p>
      )}

      {step === "ansPage" && (
        <>
          {prog ? <p className="am-prog">{prog}</p> : (
            <>
              <p className="am-note">
                문제 {items.length}개를 잘라냈어요. 이제 <b>빠른정답이 있는 페이지 1장</b>을 탭하세요.
                정답이 다른 파일에 있으면 아래에서 그 PDF를 열고, 없으면 건너뛰고 직접 입력해도 돼요.
              </p>
              <div className="am-thumbs">
                {thumbs.map((t) => (
                  <button key={t.no} className="am-thumb" onClick={() => readAnswers(t.no)}>
                    <span>{t.no}p</span><img src={t.url} alt="" />
                  </button>
                ))}
              </div>
              <button className={"am-ghost" + (drag ? " dragon" : "")} {...dropProps(true)} onClick={() => ansFileRef.current.click()}>📂 정답 PDF 따로 열기 (끌어다 놓기 가능)</button>
              <button className="am-ghost" onClick={() => setStep("review")}>건너뛰고 정답 직접 입력 →</button>
            </>
          )}
        </>
      )}

      {step === "review" && (
        <>
          <p className="am-note">
            잘린 모양과 번호·정답을 확인하세요. 위/아래가 잘렸으면 <b>[위+] [아래+]</b>로 늘리고,
            잘못 잡힌 항목은 <b>[제외]</b>. 객관식 답은 ①~⑤, 단답은 -6 · 3/4 · 2x+1 형식이에요.
          </p>
          <p className="am-cnt">등록 대상 {incCount}개 / 전체 {items.length}개 · 「[자료] {title || "(이름 없음)"}」 · {grade}</p>
          {items.map((it) => (
            <div key={it.key} className={"am-item" + (it.excluded ? " off" : "")}>
              <img className="am-crop" src={it.url} alt="" />
              <div className="am-irow">
                <input className="am-in am-num" value={it.no}
                  onChange={(e) => setField(it.key, { no: e.target.value.replace(/[^0-9]/g, "") })} />
                <input className={"am-in am-ans" + (!it.excluded && !String(it.answer).trim() ? " miss" : "")}
                  placeholder="정답" value={it.answer}
                  onChange={(e) => setField(it.key, { answer: e.target.value })} />
                <button className="am-mini" onClick={() => adjust(it.key, "topOut")}>위+</button>
                <button className="am-mini" onClick={() => adjust(it.key, "topIn")}>위−</button>
                <button className="am-mini" onClick={() => adjust(it.key, "botOut")}>아래+</button>
                <button className="am-mini" onClick={() => adjust(it.key, "botIn")}>아래−</button>
                <button className={"am-mini" + (it.excluded ? "" : " warn")}
                  onClick={() => setField(it.key, { excluded: !it.excluded })}>
                  {it.excluded ? "복구" : "제외"}
                </button>
              </div>
            </div>
          ))}
          <button className="am-go" onClick={save}>✅ {incCount}문항 등록하기</button>
          <button className="am-ghost" onClick={() => setStep("ansPage")}>← 정답 페이지 다시</button>
          <button className="am-ghost" onClick={reset}>처음부터</button>
        </>
      )}
    </div>
  );
}
