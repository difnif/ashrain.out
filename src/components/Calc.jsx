import { useEffect, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import AdminCalc from "./AdminCalc";

// ashrain.out — 연산 (v0.2.2)
// src/components/Calc.jsx — Home.jsx(v0.2.2)가 연산 탭에서 import 합니다.
// 흐름: 단원 선택 → 문제 수·난이도 → 은행에서 랜덤 추출 → 문제별 제한시간 풀이 → 채점 → 틀린 것만 다시
// 데이터: calc_units / calc_problems / calc_records (schema_calc_v2.sql)

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
.cl-lab { font-size:12.5px; color:var(--mut); margin:12px 0 6px; font-weight:700; }

/* 풀이 화면 */
.cl-stage { background:var(--card); border:1px solid var(--bd); border-radius:14px; padding:16px 14px; }
.cl-head { display:flex; justify-content:space-between; align-items:center; font-size:12.5px; color:var(--mut); margin-bottom:8px; }
.cl-tbar { height:6px; border-radius:999px; background:var(--bd); overflow:hidden; margin-bottom:16px; }
.cl-tfill { height:100%; background:var(--ac); transition:width .2s linear; }
.cl-q { font-size:17px; line-height:1.75; color:var(--ink); white-space:pre-line; min-height:56px; margin-bottom:16px; word-break:keep-all; }
.cl-in { width:100%; box-sizing:border-box; background:transparent; border:1.5px solid var(--bd); border-radius:12px;
  padding:13px 14px; color:var(--ink); font-size:16px; }
.cl-in:focus { outline:none; border-color:var(--ac); }
.cl-submit { width:100%; margin-top:10px; padding:12px; border-radius:12px; border:1px solid var(--ac);
  background:transparent; color:var(--ac); font-weight:800; font-size:14.5px; cursor:pointer; }
.cl-ox { display:flex; gap:10px; }
.cl-ox button { flex:1; padding:20px 0; border-radius:14px; border:1.5px solid var(--bd); background:transparent;
  color:var(--ink); font-size:26px; font-weight:800; cursor:pointer; }
.cl-opt { display:block; width:100%; text-align:left; margin-bottom:8px; padding:12px 14px; border-radius:12px;
  border:1.5px solid var(--bd); background:transparent; color:var(--ink); font-size:14.5px; cursor:pointer; line-height:1.5; }
.cl-opt small { color:var(--mut); margin-right:8px; }
.cl-flash-o { border-color:#0DA95F !important; box-shadow:0 0 0 1px #0DA95F inset; }
.cl-flash-x { border-color:#E5484D !important; box-shadow:0 0 0 1px #E5484D inset; }
.cl-skip { margin-top:12px; width:100%; background:none; border:none; color:var(--mut); font-size:12px; cursor:pointer; }

/* 결과 */
.cl-score { text-align:center; padding:14px 0 4px; }
.cl-score b { font-size:34px; color:var(--ac); }
.cl-score p { color:var(--mut); font-size:13px; margin:6px 0 0; }
.cl-wrow { border:1px solid var(--bd); border-radius:12px; padding:11px 13px; margin-bottom:8px; }
.cl-wrow p { margin:0; font-size:13.5px; color:var(--ink); white-space:pre-line; word-break:keep-all; }
.cl-wrow span { display:block; font-size:12.5px; margin-top:5px; }
.cl-wrong { color:#E5484D; }
.cl-right { color:#0DA95F; }
.cl-acts { display:flex; gap:8px; margin-top:14px; flex-wrap:wrap; }
.cl-acts button { flex:1; min-width:130px; padding:11px 8px; border-radius:11px; border:1px solid var(--bd);
  background:transparent; color:var(--ink); font-size:13.5px; cursor:pointer; }
.cl-acts .pri { border-color:var(--ac); color:var(--ac); font-weight:800; }
`;

export default function Calc({ uid, isAdmin, unitNames, say }) {
  const [adminView, setAdminView] = useState(false);
  const [view, setView] = useState("units");      // units | setup | play | result
  const [units, setUnits] = useState(null);
  const [recent, setRecent] = useState([]);
  const [unit, setUnit] = useState(null);         // 선택한 단원 row
  const [nOpt, setNOpt] = useState(20);
  const [dOpt, setDOpt] = useState("all");
  const [probs, setProbs] = useState([]);         // 이번 라운드 문제
  const [idx, setIdx] = useState(0);
  const [left, setLeft] = useState(0);            // 남은 초 (현재 문제)
  const [input, setInput] = useState("");
  const [flash, setFlash] = useState(null);       // 'o' | 'x'
  const [wrongs, setWrongs] = useState([]);       // {p, my}
  const [startAt, setStartAt] = useState(0);
  const [elapsed, setElapsed] = useState(0);
  const timerRef = useRef(null);
  const lockRef = useRef(false);
  const inRef = useRef(null);

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
  const grades = units ? [...new Set(units.map((u) => u.grade || "기타"))]
    .sort((a, b) => (GRADE_ORDER.indexOf(a) + 99 * (GRADE_ORDER.indexOf(a) < 0)) - (GRADE_ORDER.indexOf(b) + 99 * (GRADE_ORDER.indexOf(b) < 0))) : [];

  // ── 라운드 시작 ──
  async function startRound() {
    let q = supabase.from("calc_problems").select("*").eq("calc_unit", unit.id);
    if (dOpt !== "all") q = q.eq("difficulty", +dOpt);
    const { data, error } = await q;
    if (error || !data?.length) { say(error ? "문제 로드 실패: " + error.message : "이 조건의 문제가 아직 없어요"); return; }
    const picked = [...data].sort(() => Math.random() - 0.5).slice(0, nOpt);
    if (picked.length < nOpt) say(`이 조건에는 ${picked.length}문제만 있어요 — 전부 출제할게요`);
    beginPlay(picked);
  }
  function beginPlay(list) {
    setProbs(list); setIdx(0); setWrongs([]); setElapsed(0);
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

      {/* ── 단원 목록 ── */}
      {view === "units" && (
        <>
          <div className="cl-top">
            <span className="cl-title">🧮 연산 스피드</span>
            {isAdmin && <button className="cl-btn" onClick={() => setAdminView(true)}>🛠 관리자</button>}
          </div>
          {uid && recent.length > 0 && (
            <>
              <p className="cl-sec" style={{ marginTop: 4 }}>🏁 내 최근 기록</p>
              {recent.map((r, i) => (
                <div key={i} className="cl-card" style={{ cursor: "default" }}>
                  <b>{unitName(r.calc_unit)}</b>
                  <span>{r.correct} / {r.total} 정답 · {fmtSec(r.seconds)} · {new Date(r.created_at).toLocaleDateString()}</span>
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
              {units.filter((u) => (u.grade || "기타") === g).map((u) => (
                <button key={u.id} className="cl-card" onClick={() => { setUnit(u); setView("setup"); }}>
                  <b>{u.name}</b>
                  <span>{unitNames?.[u.unit_id] ? `개념 트리: ${unitNames[u.unit_id]}` : "탭해서 시작 옵션 고르기"}</span>
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
          <p className="cl-q">{cur.question}</p>

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
          {cur.type === "choice" && (cur.choices || []).map((c, i) => (
            <button key={i} className="cl-opt" onClick={() => submit(c)}>
              <small>{CIRCLED[i]}</small>{c}
            </button>
          ))}
          <button className="cl-skip" onClick={() => submit(null)}>모르겠어요 — 건너뛰기</button>
        </div>
      )}

      {/* ── 결과 ── */}
      {view === "result" && (
        <>
          <div className="cl-stage">
            <div className="cl-score">
              <b>{probs.length - wrongs.length} / {probs.length}</b>
              <p>{unit?.name} · {fmtSec(elapsed)} 걸렸어요{wrongs.length === 0 ? " · 완벽해요! 🎉" : ""}</p>
            </div>
            <div className="cl-acts">
              {wrongs.length > 0 && <button className="pri" onClick={retryWrong}>🔁 틀린 것만 다시 ({wrongs.length})</button>}
              <button onClick={startRound}>🎲 같은 설정으로 다시</button>
              <button onClick={() => setView("units")}>단원 목록</button>
            </div>
          </div>
          {wrongs.length > 0 && (
            <>
              <p className="cl-sec">✍️ 틀린 문제 복기</p>
              {wrongs.map((w, i) => (
                <div key={i} className="cl-wrow">
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
