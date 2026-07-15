import { useEffect, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import AdminCalc from "./AdminCalc";

// ashrain.out — 연산 (v0.3.1)
// src/components/Calc.jsx — Home.jsx가 연산 탭에서 import 합니다. (v0.2.2를 완전히 대체)
//
// [v0.3.0 변경]
// - 이미지 문제 지원: 선생님 자료(image_path)가 있으면 문제 사진을 띄우고 그대로 풀이·채점
// - 객관식(choices 없음) = 자료 문제의 ①~⑤: 큰 동그라미 버튼으로 답 선택
// - 📝 답안지 채점(OMR): 종이로 푼 자료를 골라 답만 입력 → 일괄 채점 → 기록 저장
//   · 🖨 인쇄용 답안지 양식 / 📷 손글씨 답안지 사진 → AI가 자동 입력(확인 후 제출)
// - 결과 화면: 틀린 "자료" 문제를 원터치로 오답노트에 담기 (사진 촬영 없이 자동 등록)
// - 사전 조건: schema_v030.sql 실행 + api/ai.js 업로드
// [v0.3.1] 답안지 채점 선택 목록을 선생님 자료(mat-*)로 한정 — 은행 유닛은 랜덤 출제라 종이 순서와 무관

const GRADE_ORDER = ["초등", "중1", "중2", "중3", "고1", "고2", "고3"];
const N_OPTIONS = [10, 20, 30];
const D_OPTIONS = [["all", "전체"], ["1", "쉬움"], ["2", "보통"], ["3", "도전"]];
const CIRCLED = ["①", "②", "③", "④", "⑤"];

// ── 답안 정규화: 표기 차이를 흡수해 공정하게 채점 ──
function norm(s) {
  return String(s ?? "")
    .trim()
    .replace(/\s+/g, "")
    .replace(/−/g, "-")          // 유니코드 마이너스
    .replace(/×/g, "*")
    .replace(/°/g, "")           // 각도 단위 유무 허용 (60° = 60)
    .replace(/≥/g, ">=").replace(/≤/g, "<=")
    .replace(/^x=/i, "")          // 방정식 답의 x= 접두 허용
    .toLowerCase();
}
function asRational(s) {          // "3", "-1.4", "-7/4" → [분자, 분모] (아니면 null)
  if (/^[+-]?\d+$/.test(s)) return [parseInt(s, 10), 1];
  if (/^[+-]?\d*\.\d+$/.test(s)) {
    const neg = s.startsWith("-") ? -1 : 1;
    const t = s.replace(/^[+-]/, "");
    const [i, f] = t.split(".");
    const den = Math.pow(10, f.length);
    return [neg * (parseInt(i || "0", 10) * den + parseInt(f, 10)), den];
  }
  const m = s.match(/^([+-]?\d+)\/(\d+)$/);
  if (m) return [parseInt(m[1], 10), parseInt(m[2], 10)];
  return null;
}
function isCorrect(user, answer) {
  const u = norm(user), a = norm(answer);
  if (!u) return false;
  if (u === a) return true;
  const ru = asRational(u), ra = asRational(a);
  if (ru && ra) return ru[0] * ra[1] === ra[0] * ru[1];   // 값 동치 (0.5 = 1/2)
  return false;
}
const fmtSec = (s) => `${Math.floor(s / 60)}분 ${String(s % 60).padStart(2, "0")}초`;

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
.cl-top { display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:12px; flex-wrap:wrap; }
.cl-title { font-size:15px; font-weight:800; color:var(--ink); }
.cl-mini { font-size:12px; color:var(--mut); }
.cl-btn { background:var(--card); border:1px solid var(--bd); color:var(--ink); font-size:12.5px; border-radius:8px; padding:7px 12px; cursor:pointer; }
.cl-sec { font-size:13px; font-weight:800; color:var(--mut); letter-spacing:1px; margin:16px 0 8px; }
.cl-card { display:block; width:100%; text-align:left; background:var(--card); border:1px solid var(--bd);
  border-radius:12px; padding:12px 14px; margin-bottom:8px; color:var(--ink); cursor:pointer; box-sizing:border-box; }
.cl-card b { font-size:14.5px; }
.cl-card span { display:block; color:var(--mut); font-size:12.5px; margin-top:2px; }
.cl-empty { color:var(--mut); font-size:13.5px; text-align:center; padding:32px 0; }
.cl-chips { display:flex; flex-wrap:wrap; gap:6px; margin:4px 0 14px; }
.cl-chip { border:1px solid var(--bd); background:var(--card); color:var(--mut); border-radius:999px; padding:8px 14px; font-size:13px; cursor:pointer; }
.cl-chip.on { color:var(--ac); border-color:var(--ac); font-weight:800; }
.cl-go { width:100%; padding:13px; border-radius:12px; border:1px solid var(--ac); background:transparent;
  color:var(--ac); font-weight:800; font-size:14.5px; cursor:pointer; }
.cl-go:disabled { opacity:.45; }
.cl-lab { font-size:12.5px; color:var(--mut); margin:12px 0 6px; font-weight:700; }
.cl-banner { border:1px dashed var(--ac); color:var(--ac); border-radius:11px; padding:10px 12px;
  font-size:13px; font-weight:700; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center; gap:8px; }
.cl-banner button { background:none; border:none; color:var(--mut); font-size:12px; cursor:pointer; }

/* 풀이 화면 */
.cl-stage { background:var(--card); border:1px solid var(--bd); border-radius:14px; padding:16px 14px; }
.cl-head { display:flex; justify-content:space-between; align-items:center; font-size:12.5px; color:var(--mut); margin-bottom:8px; }
.cl-tbar { height:6px; border-radius:999px; background:var(--bd); overflow:hidden; margin-bottom:16px; }
.cl-tfill { height:100%; background:var(--ac); transition:width .2s linear; }
.cl-q { font-size:17px; line-height:1.75; color:var(--ink); white-space:pre-line; min-height:56px; margin-bottom:16px; word-break:keep-all; }
.cl-img { width:100%; border-radius:10px; border:1px solid var(--bd); display:block; margin-bottom:8px; background:#fff; }
.cl-cap { font-size:13px; color:var(--mut); margin:0 0 14px; }
.cl-in { width:100%; box-sizing:border-box; background:transparent; border:1.5px solid var(--bd); border-radius:12px;
  padding:13px 14px; color:var(--ink); font-size:16px; }
.cl-in:focus { outline:none; border-color:var(--ac); }
.cl-submit { width:100%; margin-top:10px; padding:12px; border-radius:12px; border:1px solid var(--ac);
  background:transparent; color:var(--ac); font-weight:800; font-size:14.5px; cursor:pointer; }
.cl-ox { display:flex; gap:10px; }
.cl-ox button { flex:1; padding:20px 0; border-radius:14px; border:1.5px solid var(--bd); background:transparent;
  color:var(--ink); font-size:26px; font-weight:800; cursor:pointer; }
.cl-circ { display:flex; gap:8px; }
.cl-circ button { flex:1; padding:16px 0; border-radius:14px; border:1.5px solid var(--bd); background:transparent;
  color:var(--ink); font-size:22px; font-weight:800; cursor:pointer; }
.cl-opt { display:block; width:100%; text-align:left; margin-bottom:8px; padding:12px 14px; border-radius:12px;
  border:1.5px solid var(--bd); background:transparent; color:var(--ink); font-size:14.5px; cursor:pointer; line-height:1.5; }
.cl-opt small { color:var(--mut); margin-right:8px; }
.cl-flash-o { border-color:#0DA95F !important; box-shadow:0 0 0 1px #0DA95F inset; }
.cl-flash-x { border-color:#E5484D !important; box-shadow:0 0 0 1px #E5484D inset; }
.cl-skip { margin-top:12px; width:100%; background:none; border:none; color:var(--mut); font-size:12px; cursor:pointer; }

/* 답안지(OMR) */
.cl-om-row { display:flex; align-items:center; gap:8px; border:1px solid var(--bd); border-radius:11px;
  padding:8px 10px; margin-bottom:6px; background:var(--card); }
.cl-om-num { width:34px; text-align:center; font-weight:800; color:var(--mut); font-size:13.5px; flex:none; }
.cl-om-in { flex:1; box-sizing:border-box; background:transparent; border:1px solid var(--bd); border-radius:9px;
  padding:9px 11px; color:var(--ink); font-size:14.5px; min-width:0; }
.cl-om-mini { display:flex; gap:5px; flex:1; }
.cl-om-mini button { flex:1; padding:9px 0; border-radius:9px; border:1px solid var(--bd); background:transparent;
  color:var(--ink); font-size:15px; cursor:pointer; }
.cl-om-mini button.on { color:var(--ac); border-color:var(--ac); font-weight:800; box-shadow:0 0 0 1px var(--ac) inset; }

/* 결과 */
.cl-score { text-align:center; padding:14px 0 4px; }
.cl-score b { font-size:34px; color:var(--ac); }
.cl-score p { color:var(--mut); font-size:13px; margin:6px 0 0; }
.cl-wrow { border:1px solid var(--bd); border-radius:12px; padding:11px 13px; margin-bottom:8px; }
.cl-wrow p { margin:0; font-size:13.5px; color:var(--ink); white-space:pre-line; word-break:keep-all; }
.cl-wrow span { display:block; font-size:12.5px; margin-top:5px; }
.cl-wimg { width:100%; border-radius:9px; border:1px solid var(--bd); display:block; margin-bottom:8px; background:#fff; }
.cl-wrong { color:#E5484D; }
.cl-right { color:#0DA95F; }
.cl-acts { display:flex; gap:8px; margin-top:14px; flex-wrap:wrap; }
.cl-acts button { flex:1; min-width:130px; padding:11px 8px; border-radius:11px; border:1px solid var(--bd);
  background:transparent; color:var(--ink); font-size:13.5px; cursor:pointer; }
.cl-acts .pri { border-color:var(--ac); color:var(--ac); font-weight:800; }
`;

export default function Calc({ uid, isAdmin, unitNames, say }) {
  const [adminView, setAdminView] = useState(false);
  const [view, setView] = useState("units");      // units | setup | play | result | omr
  const [units, setUnits] = useState(null);
  const [recent, setRecent] = useState([]);
  const [unit, setUnit] = useState(null);         // 선택한 단원 row
  const [pickMode, setPickMode] = useState(null); // null | 'omr' — 단원 카드 탭의 의미
  const [nOpt, setNOpt] = useState(20);
  const [dOpt, setDOpt] = useState("all");
  const [probs, setProbs] = useState([]);         // 이번 라운드(또는 채점 대상) 문제
  const [idx, setIdx] = useState(0);
  const [left, setLeft] = useState(0);            // 남은 초 (현재 문제)
  const [input, setInput] = useState("");
  const [flash, setFlash] = useState(null);       // 'o' | 'x'
  const [wrongs, setWrongs] = useState([]);       // {p, my}
  const [startAt, setStartAt] = useState(0);
  const [elapsed, setElapsed] = useState(0);
  const [imgs, setImgs] = useState({});           // image_path → 서명 URL (라운드 간 유지)
  const [omrProbs, setOmrProbs] = useState([]);
  const [omrAns, setOmrAns] = useState({});       // problem.id → 입력값
  const [omrBusy, setOmrBusy] = useState(false);
  const [savedWrong, setSavedWrong] = useState(false);
  const timerRef = useRef(null);
  const lockRef = useRef(false);
  const inRef = useRef(null);
  const omrFileRef = useRef(null);

  useEffect(() => {
    supabase.from("calc_units").select("*").order("sort")
      .then(({ data }) => setUnits(data || []));
    if (uid) {
      supabase.from("calc_records").select("calc_unit, correct, total, seconds, created_at")
        .eq("user_id", uid).order("created_at", { ascending: false }).limit(3)
        .then(({ data }) => setRecent(data || []));
    }
  }, [uid]);

  useEffect(() => () => clearInterval(timerRef.current), []);

  const unitName = (id) => units?.find((u) => u.id === id)?.name || id;
  // 답안지 채점은 종이 순서 = DB 순서인 "선생님 자료"에서만 의미가 있어요 (은행 유닛 제외)
  const visUnits = pickMode === "omr" ? (units || []).filter((u) => u.id.startsWith("mat-")) : (units || []);
  const grades = units ? [...new Set(visUnits.map((u) => u.grade || "기타"))]
    .sort((a, b) => (GRADE_ORDER.indexOf(a) + 99 * (GRADE_ORDER.indexOf(a) < 0)) - (GRADE_ORDER.indexOf(b) + 99 * (GRADE_ORDER.indexOf(b) < 0))) : [];

  async function signImages(list) {
    const paths = [...new Set(list.map((p) => p.image_path).filter((p) => p && !imgs[p]))];
    if (!paths.length) return;
    const { data } = await supabase.storage.from("notes").createSignedUrls(paths, 3600);
    if (data) {
      const add = {};
      data.forEach((d) => { if (d.signedUrl && d.path) add[d.path] = d.signedUrl; });
      setImgs((m) => ({ ...m, ...add }));
    }
  }

  // ── 라운드 시작 ──
  async function startRound() {
    let q = supabase.from("calc_problems").select("*").eq("calc_unit", unit.id);
    if (dOpt !== "all") q = q.eq("difficulty", +dOpt);
    const { data, error } = await q;
    if (error || !data?.length) { say(error ? "문제 로드 실패: " + error.message : "이 조건의 문제가 아직 없어요"); return; }
    const picked = [...data].sort(() => Math.random() - 0.5).slice(0, nOpt);
    if (picked.length < nOpt) say(`이 조건에는 ${picked.length}문제만 있어요 — 전부 출제할게요`);
    await signImages(picked);
    beginPlay(picked);
  }
  function beginPlay(list) {
    setProbs(list); setIdx(0); setWrongs([]); setElapsed(0); setSavedWrong(false);
    setStartAt(Date.now()); setView("play");
    armProblem(list, 0);
  }
  function armProblem(list, i) {
    clearInterval(timerRef.current);
    lockRef.current = false;
    setInput(""); setFlash(null);
    setLeft(list[i].time_limit);
    timerRef.current = setInterval(() => {
      setLeft((s) => {
        if (s <= 1) { onTimeout(list, i); return 0; }
        return s - 1;
      });
    }, 1000);
    setTimeout(() => inRef.current?.focus(), 50);
  }
  function onTimeout(list, i) {
    if (lockRef.current) return;
    grade(list, i, null);                          // 시간 초과 = 오답
  }
  function submit(my) {
    grade(probs, idx, my);
  }
  function grade(list, i, my) {
    if (lockRef.current) return;
    lockRef.current = true;
    clearInterval(timerRef.current);
    const p = list[i];
    const ok = my !== null && isCorrect(my, p.answer);
    if (!ok) setWrongs((w) => [...w, { p, my: my === null ? "(시간 초과)" : my }]);
    setFlash(ok ? "o" : "x");
    setTimeout(() => {
      if (i + 1 < list.length) { setIdx(i + 1); armProblem(list, i + 1); }
      else finish(list, ok);
    }, 650);
  }
  async function finish(list, lastOk) {
    clearInterval(timerRef.current);
    const secs = Math.round((Date.now() - startAt) / 1000);
    setElapsed(secs);
    setView("result");
    if (uid) {
      // wrongs 상태는 비동기라 마지막 문제 반영이 늦을 수 있음 → setWrongs 콜백으로 계산
      setWrongs((w) => {
        const correct = list.length - w.length;
        supabase.from("calc_records").insert({
          user_id: uid, calc_unit: unit.id,
          correct, total: list.length, seconds: secs,
          wrong_ids: w.map((x) => x.p.id),
        }).then(({ error }) => { if (error) say("기록 저장 실패: " + error.message); });
        return w;
      });
    }
  }
  function retryWrong() {
    const list = wrongs.map((w) => w.p);
    if (!list.length) return;
    beginPlay([...list].sort(() => Math.random() - 0.5));
  }

  // ── 답안지(OMR) ──
  async function startOmr(u) {
    const { data, error } = await supabase.from("calc_problems").select("*")
      .eq("calc_unit", u.id).order("id");
    if (error || !data?.length) { say(error ? "문제 로드 실패: " + error.message : "이 단원에는 문제가 없어요"); return; }
    setUnit(u); setPickMode(null);
    setOmrProbs(data); setOmrAns({});
    await signImages(data);
    setView("omr");
  }
  const omrType = (p) => (p.type === "choice" ? "choice" : p.type === "ox" ? "ox" : "calc");
  const circVal = (p, i) => (p.choices ? p.choices[i] : CIRCLED[i]);   // 은행 5지선다는 보기 텍스트로 채점

  function submitOmr() {
    const w = [];
    omrProbs.forEach((p) => {
      const my = omrAns[p.id];
      const has = my != null && String(my).trim() !== "";
      if (!(has && isCorrect(my, p.answer))) w.push({ p, my: has ? my : "(빈칸)" });
    });
    setProbs(omrProbs); setWrongs(w); setElapsed(0); setSavedWrong(false);
    setView("result");
    if (uid) {
      supabase.from("calc_records").insert({
        user_id: uid, calc_unit: unit.id,
        correct: omrProbs.length - w.length, total: omrProbs.length, seconds: 0,
        wrong_ids: w.map((x) => x.p.id),
      }).then(({ error }) => { if (error) say("기록 저장 실패: " + error.message); });
    }
  }

  // 인쇄용 답안지 양식 (종이로 풀 때)
  function printSheet() {
    const rows = omrProbs.map((p, i) => {
      const t = omrType(p);
      const cell = t === "choice" ? "① &nbsp; ② &nbsp; ③ &nbsp; ④ &nbsp; ⑤"
        : t === "ox" ? "O &nbsp;&nbsp; / &nbsp;&nbsp; X"
        : "답: ______________________";
      return `<tr><td class="n">${i + 1}</td><td class="a">${cell}</td></tr>`;
    }).join("");
    const html = `<!doctype html><html><head><meta charset="utf-8"><title>답안지</title><style>
      body { font-family:'Malgun Gothic',sans-serif; padding:28px; color:#111; }
      h2 { margin:0 0 4px; font-size:18px; } .sub { color:#666; font-size:12px; margin:0 0 16px; }
      table { width:100%; border-collapse:collapse; }
      td { border:1px solid #bbb; padding:9px 10px; font-size:14px; }
      td.n { width:44px; text-align:center; font-weight:700; }
      td.a { letter-spacing:1px; }
      @media print { body { padding:10mm; } }
    </style></head><body>
      <h2>${unit?.name || "답안지"}</h2>
      <p class="sub">이름: ______________ &nbsp;&nbsp; 날짜: ______________ &nbsp;&nbsp; 객관식은 번호에 ○, 단답은 또박또박!</p>
      <table>${rows}</table>
      <script>window.onload = function(){ window.print(); };</scr` + `ipt>
    </body></html>`;
    const win = window.open("", "_blank");
    if (!win) { say("팝업이 차단됐어요 — 브라우저에서 팝업을 허용해 주세요"); return; }
    win.document.write(html);
    win.document.close();
  }

  // 손글씨 답안지 사진 → AI 자동 입력
  function pickOmrPhoto(e) {
    const f = e.target.files?.[0];
    e.target.value = "";
    if (!f) return;
    const im = new Image();
    im.onload = async () => {
      const cap = 1200, sc = Math.min(1, cap / Math.max(im.width, im.height));
      const cv = document.createElement("canvas");
      cv.width = Math.round(im.width * sc); cv.height = Math.round(im.height * sc);
      cv.getContext("2d").drawImage(im, 0, 0, cv.width, cv.height);
      URL.revokeObjectURL(im.src);
      setOmrBusy(true);
      try {
        const base64 = cv.toDataURL("image/jpeg", 0.8).split(",")[1];
        const { answers } = await aiCall({
          task: "omr", image: base64,
          items: omrProbs.map((p, i) => ({ no: i + 1, type: omrType(p) })),
        });
        let filled = 0;
        const add = {};
        (answers || []).forEach(({ no, answer }) => {
          const p = omrProbs[no - 1];
          if (!p || !answer) return;
          const t = omrType(p);
          let val = null;
          if (t === "choice") {
            const ci = CIRCLED.indexOf(answer);
            if (ci >= 0) val = circVal(p, ci);
          } else if (t === "ox") {
            if (/^[OX]$/i.test(answer)) val = answer.toUpperCase();
          } else {
            val = answer;
          }
          if (val != null) { add[p.id] = val; filled++; }
        });
        setOmrAns((m) => ({ ...m, ...add }));
        say(filled ? `${filled}개를 자동으로 채웠어요 — 꼭 확인한 뒤 제출하세요!` : "답을 읽지 못했어요 — 더 밝고 반듯하게 다시 찍어 보세요");
      } catch (err) {
        say("사진 인식 실패: " + (err?.message || String(err)));
      }
      setOmrBusy(false);
    };
    im.onerror = () => say("사진을 열 수 없어요");
    im.src = URL.createObjectURL(f);
  }

  // 틀린 자료 문제 → 오답노트 원터치 담기
  async function saveWrongNotes() {
    const targets = wrongs.filter((w) => w.p.image_path);
    if (!uid || !targets.length) return;
    const rows = targets.map((w) => ({
      user_id: uid,
      image_path: w.p.image_path,
      unit_id: unit?.unit_id || null,
      reason: "etc",
      source: unit?.name || "연산",
      tags: ["자료"],
      status: "new",
      memo: `${w.p.question} · 내 답: ${w.my}`,
    }));
    const { error } = await supabase.from("wrong_notes").insert(rows);
    if (error) { say("오답노트 저장 실패: " + error.message); return; }
    setSavedWrong(true);
    say(`📕 ${rows.length}문제를 오답노트에 담았어요 — 오답 탭에서 확인!`);
  }

  // ── 관리자 ──
  if (adminView) {
    return (
      <>
        <style>{CSS}</style>
        <div className="cl-top">
          <span className="cl-title">🛠 연산 관리 (관리자)</span>
          <button className="cl-btn" onClick={() => { setAdminView(false); setView("units"); setUnits(null); supabase.from("calc_units").select("*").order("sort").then(({ data }) => setUnits(data || [])); }}>← 연산으로</button>
        </div>
        <AdminCalc say={say} />
      </>
    );
  }

  const cur = probs[idx];

  return (
    <div>
      <style>{CSS}</style>
      <input ref={omrFileRef} type="file" accept="image/*" capture="environment" hidden onChange={pickOmrPhoto} />

      {/* ── 단원 목록 ── */}
      {view === "units" && (
        <>
          <div className="cl-top">
            <span className="cl-title">🧮 연산 스피드</span>
            <span style={{ display: "flex", gap: 6 }}>
              <button className="cl-btn" onClick={() => setPickMode(pickMode === "omr" ? null : "omr")}>📝 답안지 채점</button>
              {isAdmin && <button className="cl-btn" onClick={() => setAdminView(true)}>🛠 관리자</button>}
            </span>
          </div>
          {pickMode === "omr" && (
            <div className="cl-banner">
              <span>채점할 자료(단원)를 아래에서 선택하세요 — 종이로 푼 답을 옮겨 적으면 한 번에 채점돼요.</span>
              <button onClick={() => setPickMode(null)}>취소 ✕</button>
            </div>
          )}
          {pickMode === "omr" && units !== null && visUnits.length === 0 && (
            <p className="cl-empty">아직 등록된 선생님 자료가 없어요 — 자료가 등록되면 여기서 답안지로 채점할 수 있어요.</p>
          )}
          {!pickMode && uid && recent.length > 0 && (
            <>
              <p className="cl-sec" style={{ marginTop: 4 }}>🏁 내 최근 기록</p>
              {recent.map((r, i) => (
                <div key={i} className="cl-card" style={{ cursor: "default" }}>
                  <b>{unitName(r.calc_unit)}</b>
                  <span>{r.correct} / {r.total} 정답 · {r.seconds ? fmtSec(r.seconds) : "답안지 채점"} · {new Date(r.created_at).toLocaleDateString()}</span>
                </div>
              ))}
            </>
          )}
          {units === null && <p className="cl-empty">불러오는 중…</p>}
          {units !== null && units.length === 0 && (
            <p className="cl-empty">아직 등록된 연산 단원이 없어요.{isAdmin ? " 관리자 메뉴에서 문제 파일을 등록해 주세요." : ""}</p>
          )}
          {grades.map((g) => (
            <div key={g}>
              <p className="cl-sec">{g}</p>
              {visUnits.filter((u) => (u.grade || "기타") === g).map((u) => (
                <button key={u.id} className="cl-card"
                  onClick={() => { if (pickMode === "omr") startOmr(u); else { setUnit(u); setView("setup"); } }}>
                  <b>{u.name}</b>
                  <span>{pickMode === "omr" ? "탭해서 이 자료 답안지 작성" : unitNames?.[u.unit_id] ? `개념 트리: ${unitNames[u.unit_id]}` : "탭해서 시작 옵션 고르기"}</span>
                </button>
              ))}
            </div>
          ))}
        </>
      )}

      {/* ── 시작 옵션 ── */}
      {view === "setup" && unit && (
        <>
          <div className="cl-top">
            <span className="cl-title">{unit.name}</span>
            <button className="cl-btn" onClick={() => setView("units")}>← 단원</button>
          </div>
          <p className="cl-lab">몇 문제 풀까요?</p>
          <div className="cl-chips">
            {N_OPTIONS.map((n) => (
              <button key={n} className={"cl-chip" + (nOpt === n ? " on" : "")} onClick={() => setNOpt(n)}>{n}문제</button>
            ))}
          </div>
          <p className="cl-lab">난이도</p>
          <div className="cl-chips">
            {D_OPTIONS.map(([k, l]) => (
              <button key={k} className={"cl-chip" + (dOpt === k ? " on" : "")} onClick={() => setDOpt(k)}>{l}</button>
            ))}
          </div>
          <button className="cl-go" onClick={startRound}>🚀 시작하기</button>
          <p className="cl-mini" style={{ marginTop: 10, lineHeight: 1.6 }}>
            문제마다 제한시간이 있어요. 시간이 다 되면 자동으로 다음 문제로 넘어가요.
            매번 은행에서 새로 뽑으니 반복할수록 새 조합을 만나요!
          </p>
        </>
      )}

      {/* ── 풀이 ── */}
      {view === "play" && cur && (
        <div className={"cl-stage" + (flash === "o" ? " cl-flash-o" : flash === "x" ? " cl-flash-x" : "")}>
          <div className="cl-head">
            <span>{idx + 1} / {probs.length}</span>
            <span>⏱ {left}초</span>
          </div>
          <div className="cl-tbar"><div className="cl-tfill" style={{ width: `${(left / cur.time_limit) * 100}%` }} /></div>

          {cur.image_path ? (
            <>
              {imgs[cur.image_path] && <img className="cl-img" src={imgs[cur.image_path]} alt="" />}
              <p className="cl-cap">{cur.question}</p>
            </>
          ) : (
            <p className="cl-q">{cur.question}</p>
          )}

          {cur.type === "calc" && (
            <>
              <input
                ref={inRef}
                className="cl-in"
                value={input}
                placeholder="답 입력 (예: -6, 3/4, 2x+1)"
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === "Enter" && input.trim()) submit(input); }}
                inputMode="text"
                autoComplete="off"
              />
              <button className="cl-submit" onClick={() => input.trim() && submit(input)}>제출</button>
            </>
          )}
          {cur.type === "ox" && (
            <div className="cl-ox">
              <button onClick={() => submit("O")}>O</button>
              <button onClick={() => submit("X")}>X</button>
            </div>
          )}
          {cur.type === "choice" && !cur.choices && (
            <div className="cl-circ">
              {CIRCLED.map((c) => (
                <button key={c} onClick={() => submit(c)}>{c}</button>
              ))}
            </div>
          )}
          {cur.type === "choice" && cur.choices && cur.choices.map((c, i) => (
            <button key={i} className="cl-opt" onClick={() => submit(c)}>
              <small>{CIRCLED[i]}</small>{c}
            </button>
          ))}
          <button className="cl-skip" onClick={() => submit(null)}>모르겠어요 — 건너뛰기</button>
        </div>
      )}

      {/* ── 답안지(OMR) 작성 ── */}
      {view === "omr" && unit && (
        <>
          <div className="cl-top">
            <span className="cl-title">📝 {unit.name}</span>
            <button className="cl-btn" onClick={() => setView("units")}>← 단원</button>
          </div>
          <p className="cl-mini" style={{ marginBottom: 10, lineHeight: 1.6 }}>
            종이로 푼 답을 옮겨 적고 제출하면 한 번에 채점돼요. 사진으로 불러온 답은 <b>반드시 확인한 뒤</b> 제출!
          </p>
          <div className="cl-acts" style={{ marginTop: 0, marginBottom: 12 }}>
            <button onClick={printSheet}>🖨 인쇄용 답안지</button>
            <button onClick={() => omrFileRef.current.click()} disabled={omrBusy}>
              {omrBusy ? "⏳ 사진 읽는 중…" : "📷 사진으로 불러오기"}
            </button>
          </div>
          {omrProbs.map((p, i) => {
            const t = omrType(p);
            return (
              <div key={p.id} className="cl-om-row">
                <span className="cl-om-num">{i + 1}</span>
                {t === "choice" && (
                  <div className="cl-om-mini">
                    {CIRCLED.map((c, ci) => (
                      <button key={c} className={omrAns[p.id] === circVal(p, ci) ? "on" : ""}
                        onClick={() => setOmrAns((m) => ({ ...m, [p.id]: m[p.id] === circVal(p, ci) ? "" : circVal(p, ci) }))}>
                        {c}
                      </button>
                    ))}
                  </div>
                )}
                {t === "ox" && (
                  <div className="cl-om-mini">
                    {["O", "X"].map((c) => (
                      <button key={c} className={omrAns[p.id] === c ? "on" : ""}
                        onClick={() => setOmrAns((m) => ({ ...m, [p.id]: m[p.id] === c ? "" : c }))}>
                        {c}
                      </button>
                    ))}
                  </div>
                )}
                {t === "calc" && (
                  <input className="cl-om-in" placeholder="답" value={omrAns[p.id] || ""}
                    onChange={(e) => setOmrAns((m) => ({ ...m, [p.id]: e.target.value }))} />
                )}
              </div>
            );
          })}
          <button className="cl-go" style={{ marginTop: 8 }} onClick={submitOmr}>✅ 제출하고 채점</button>
        </>
      )}

      {/* ── 결과 ── */}
      {view === "result" && (
        <>
          <div className="cl-stage">
            <div className="cl-score">
              <b>{probs.length - wrongs.length} / {probs.length}</b>
              <p>{unit?.name} · {elapsed ? `${fmtSec(elapsed)} 걸렸어요` : "답안지 채점"}{wrongs.length === 0 ? " · 완벽해요! 🎉" : ""}</p>
            </div>
            <div className="cl-acts">
              {wrongs.length > 0 && <button className="pri" onClick={retryWrong}>🔁 틀린 것만 다시 ({wrongs.length})</button>}
              {elapsed > 0
                ? <button onClick={startRound}>🎲 같은 설정으로 다시</button>
                : <button onClick={() => setView("omr")}>📝 답안지 다시</button>}
              <button onClick={() => setView("units")}>단원 목록</button>
            </div>
            {uid && wrongs.some((w) => w.p.image_path) && (
              <button className="cl-go" style={{ marginTop: 12 }} disabled={savedWrong} onClick={saveWrongNotes}>
                {savedWrong
                  ? "📕 오답노트에 담았어요 ✓"
                  : `📕 틀린 자료 문제 오답노트에 담기 (${wrongs.filter((w) => w.p.image_path).length})`}
              </button>
            )}
          </div>
          {wrongs.length > 0 && (
            <>
              <p className="cl-sec">✍️ 틀린 문제 복기</p>
              {wrongs.map((w, i) => (
                <div key={i} className="cl-wrow">
                  {w.p.image_path && imgs[w.p.image_path] && <img className="cl-wimg" src={imgs[w.p.image_path]} alt="" />}
                  <p>{w.p.question}</p>
                  <span className="cl-wrong">내 답: {w.my || "(빈칸)"}</span>
                  <span className="cl-right">정답: {w.p.answer}</span>
                </div>
              ))}
            </>
          )}
        </>
      )}
    </div>
  );
}
