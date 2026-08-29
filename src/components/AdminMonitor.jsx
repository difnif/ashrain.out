// ashrain.out — 파이프라인 모니터 (AdminMonitor.jsx v1.0, #/admin/monitor)
// 새 창에 띄워두는 관제탑: 15초 계측 갱신 + 과다 작업 경보 + 전체 일시정지/재개
// + 체인 워치독 내장 — 이 창만 열려 있어도 작업 자동 승계·재점화가 유지된다.
// 필요: SQL v11(pipeline_stats), 러너 v2.7+ (계측), 관리자 로그인(코퍼스 화면과 세션 공유)

import { useEffect, useRef, useState } from "react";
import { supabase } from "../supabaseClient";

const CHAINS = 4;
const RETRO_USD = { primary: 0.005, retry: 0.005, sample: 0.015, arbiter: 0.025, answer_sheet: 0.005, classify: 0.002 };

function derive(d) {
  if (!d) return null;
  const P = d.pages || {}, H = d.hour || {};
  const total = (P.done || 0) + (P.pending || 0) + (P.doing || 0) + (P.error || 0);
  const tracedUsd = (d.cost || []).reduce((a, c) => a + Number(c.usd || 0), 0);
  const retroUsd = (d.retro || []).reduce((a, r) => a + (RETRO_USD[r.role] || 0.005) * r.n, 0);
  const krw = Math.round((tracedUsd + retroUsd) * 1400);
  const rate = H.pages_done || 0;
  const callsPerPage = rate ? ((H.primary || 0) + (H.retry || 0) + (H.sample || 0) + (H.arbiter || 0)) / rate : 0;
  return { P, H, total, tracedUsd, retroUsd, krw, rate, callsPerPage,
           leftH: rate ? (P.pending || 0) / rate : null };
}

export default function AdminMonitor() {
  const [mon, setMon] = useState(null);
  const [note, setNote] = useState("연결 중…");
  const [authed, setAuthed] = useState(null);
  const [budget, setBudget] = useState(() => Number(localStorage.getItem("cp_budget") || 300000));
  const alertsRef = useRef({});
  const [, force] = useState(0);

  useEffect(() => { supabase.auth.getSession().then(({ data }) => setAuthed(!!data.session)); }, []);

  async function kick(jobId, n = CHAINS) {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) return;
    for (let k = 0; k < n; k++)
      fetch("/api/transcribeJob", {
        method: "POST",
        headers: { "content-type": "application/json", Authorization: `Bearer ${session.access_token}` },
        body: JSON.stringify({ job_id: jobId }),
      }).catch(() => {});
  }

  function checkAlerts(d) {
    const m = derive(d); if (!m) return;
    const fire = (key, msg) => {
      if (!alertsRef.current[key]) window.alert("⚠ 파이프라인 경보\n\n" + msg);
      alertsRef.current[key] = msg;
    };
    const clear = (key) => { delete alertsRef.current[key]; };
    if (m.krw > budget) fire("budget", `누적 지출 추정 ${m.krw.toLocaleString()}원 > 예산 ${budget.toLocaleString()}원 — 일시정지 권장`); else clear("budget");
    if (m.rate > 5 && m.callsPerPage > 2.6) fire("burst", `페이지당 호출 ${m.callsPerPage.toFixed(1)}회 — 재시도 폭주 의심 (정상 1.3~2.2)`); else clear("burst");
    if ((d.chains || 0) === 0 && (m.P.pending || 0) > 0 && (d.jobs_running || 0) > 0) alertsRef.current.dead = "활성 체인 0 — 워치독이 재점화 중"; else clear("dead");
    force((x) => x + 1);
  }

  useEffect(() => {
    if (!authed) return;
    let on = true;
    const tick = async () => {
      const { data, error } = await supabase.rpc("pipeline_stats", { p_hours: 1 });
      if (!on) return;
      if (error) { setNote("통계 RPC 실패 — v11 SQL 실행 확인: " + error.message); return; }
      setMon(data); setNote(""); checkAlerts(data);
      // ── 내장 워치독: 가장 오래된 running 작업이 정체면 재점화 (작업 자동 승계 겸용)
      const { data: j } = await supabase.from("transcribe_jobs").select("id,updated_at")
        .eq("status", "running").order("created_at", { ascending: true }).limit(1);
      const lack = CHAINS - (data.chains || 0);                       // 체인 감쇠 보충
      const stale = j?.length && Date.now() - new Date(j[0].updated_at).getTime() > 25000;
      if (j?.length && (stale || lack > 0)) kick(j[0].id, stale ? CHAINS : Math.max(1, lack));
    };
    tick();
    const iv = setInterval(tick, 15000);
    return () => { on = false; clearInterval(iv); };
  }, [authed, budget]);  // eslint-disable-line

  const pauseAll = async () => {
    await supabase.from("transcribe_jobs").update({ status: "paused" }).eq("status", "running");
    setNote("전 작업 일시정지 — 체인이 1분 내 멈춥니다");
  };
  const resumeAll = async () => {
    await supabase.from("transcribe_jobs").update({ status: "running" }).eq("status", "paused");
    setNote("재개 — 워치독이 곧 점화합니다");
  };

  const m = derive(mon);
  const alerts = Object.values(alertsRef.current);
  return (
    <div className="am-wrap">
      <style>{CSS}</style>
      <h2>파이프라인 모니터</h2>
      {authed === false && <p className="am-note">관리자 로그인이 필요해 — 코퍼스 화면에서 로그인 후 이 창을 새로고침.</p>}
      <div className="am-row">
        <button className="am-btn" onClick={pauseAll}>⏸ 전체 일시정지</button>
        <button className="am-btn" onClick={resumeAll}>▶ 전체 재개{mon?.jobs_paused ? ` (${mon.jobs_paused})` : ""}</button>
        <span className="am-note" style={{ marginLeft: "auto" }}>예산 ₩</span>
        <input type="number" step="10000" value={budget}
          onChange={(e) => { const v = Number(e.target.value) || 0; setBudget(v); localStorage.setItem("cp_budget", String(v)); }} />
      </div>
      {alerts.length > 0 && <div className="am-alert">{alerts.map((a, i) => <div key={i}>⚠ {a}</div>)}</div>}
      {note && <p className="am-note">{note}</p>}
      {m && (
        <>
          <div className="am-cards">
            <div className="am-card"><p>진행</p><b>{(m.P.done || 0).toLocaleString()} / {m.total.toLocaleString()}p</b>
              <span>{m.leftH != null ? `잔여 ~${m.leftH.toFixed(1)}h` : "—"} · 오류 {m.P.error || 0}p</span></div>
            <div className="am-card"><p>시간당</p><b>{m.rate.toLocaleString()}p</b>
              <span>문항 {(m.H.items || 0).toLocaleString()} · 호출/p {m.callsPerPage.toFixed(2)}</span></div>
            <div className="am-card"><p>체인 · 품질</p><b style={{ color: (mon.chains || 0) ? "#4ade80" : "#f87171" }}>{mon.chains || 0}</b>
              <span>재시도 {m.H.primary ? Math.round(100 * (m.H.retry || 0) / m.H.primary) : 0}% · 소넷중재 {m.H.arbiter || 0} · 오푸스 {m.H.arbiter2 || 0} · 대기行 {m.H.esc || 0}</span></div>
            <div className="am-card"><p>누적 지출</p><b>{m.krw.toLocaleString()}원</b>
              <span>실측 ${m.tracedUsd.toFixed(2)} + 소급 ~${m.retroUsd.toFixed(0)} / 예산 {budget.toLocaleString()}</span></div>
          </div>
          <p className="am-h">단계별 평균 (1h)</p>
          {(mon.steps || []).map((st) => (
            <div key={st.step} className="am-row" style={{ gap: 8 }}>
              <span className="am-step">{st.step}</span>
              <div className="am-barbg"><div className="am-bar" style={{ width: Math.min(100, (st.avg_ms || 0) / 120) + "%" }} /></div>
              <span className="am-ms">{st.avg_ms}ms · {st.n}</span>
            </div>
          ))}
          <p className="am-h">모델별 실측 (계측 이후 누적)</p>
          {(mon.cost || []).map((c) => (
            <p key={c.model} className="am-det">{c.model} — {c.calls.toLocaleString()}회 · in {(c.itok / 1000).toFixed(0)}K
              (캐시적중 {(c.cr / 1000).toFixed(0)}K) · out {(c.otok / 1000).toFixed(0)}K · <b>${Number(c.usd).toFixed(2)}</b></p>
          ))}
          <p className="am-h">실시간</p>
          <div className="am-tick">
            {(mon.recent || []).map((r, i) => (
              <div key={i} style={{ color: r.ok === false ? "#f87171" : "#94a3b8" }}>
                p.{r.page} {r.step}{r.model ? `·${r.model}` : ""}{r.ms ? ` ${r.ms}ms` : ""}{r.note ? ` — ${r.note}` : ""}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

const CSS = `
.am-wrap{max-width:760px;margin:0 auto;padding:18px 14px 60px;color:#e2e8f0;background:#0f172a;min-height:100vh}
.am-wrap h2{font-size:18px;margin:0 0 12px}
.am-row{display:flex;align-items:center;gap:8px;margin:6px 0}
.am-btn{padding:8px 12px;border:1px solid #334155;border-radius:8px;background:#1e293b;color:#e2e8f0;font-size:13px;cursor:pointer}
.am-wrap input{width:110px;padding:7px 8px;border:1px solid #334155;border-radius:8px;background:#1e293b;color:#e2e8f0;font-size:13px}
.am-alert{background:#7f1d1d;color:#fecaca;border-radius:8px;padding:8px 10px;margin:8px 0;font-size:13px;line-height:1.6}
.am-note{font-size:12.5px;color:#94a3b8}
.am-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px;margin:10px 0}
.am-card{background:#1e293b;border-radius:10px;padding:10px}
.am-card p{margin:0;font-size:12px;color:#94a3b8}
.am-card b{font-size:19px}
.am-card span{display:block;font-size:11.5px;color:#64748b;margin-top:2px}
.am-h{font-size:13px;font-weight:700;margin:14px 0 6px}
.am-step{width:92px;font-size:12px}
.am-barbg{flex:1;background:#1e293b;border-radius:4px;height:10px}
.am-bar{background:#38bdf8;height:10px;border-radius:4px}
.am-ms{font-size:12px;min-width:88px;text-align:right}
.am-det{font-size:12.5px;color:#cbd5e1;margin:2px 0}
.am-tick{font-family:monospace;font-size:12px;line-height:1.7}
`;
