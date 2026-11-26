// ashrain.out — 관리자 가입 로그 (v1.0, #/admin/signups)
// 2026-11-26 원장님: 가입을 다 마치면 승인 없이 바로 이용 — 대신 누가 언제(분까지) 가입했는지 관리자 화면에서 본다.
// 데이터: DB 함수 admin_signup_log() (관리자만 행이 나온다, supabase/2026-11_signup_open.sql). 표시 규칙: src/lib/signupLog.js
import { useEffect, useMemo, useState } from "react";
import { supabase } from "../supabaseClient";
import { buildSignupLog } from "../lib/signupLog";

const FILTERS = [["all", "전체"], ["notready", "가입 마무리 전"], ["minor", "14세 미만"]];

export default function AdminSignups() {
  const [isAdmin, setIsAdmin] = useState(null);
  const [rows, setRows] = useState(null);
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  const [only, setOnly] = useState("all");

  const load = async () => {
    setErr(""); setBusy(true);
    const { data, error } = await supabase.rpc("admin_signup_log", { p_limit: 500 });
    if (error) {
      setErr(/admin_signup_log/.test(error.message || "")
        ? "가입 로그 함수가 아직 DB에 없어요 — supabase/2026-11_signup_open.sql 을 실행해 주세요."
        : "불러오기 실패: " + error.message);
      setRows([]);
    } else setRows(data || []);
    setBusy(false);
  };

  useEffect(() => {
    supabase.auth.getUser().then(({ data }) => {
      if (!data?.user) return setIsAdmin(false);
      supabase.from("profiles").select("role").eq("id", data.user.id).single()
        .then(({ data: p }) => {
          const ok = p?.role === "admin";
          setIsAdmin(ok);
          if (ok) load();
        });
    });
  }, []);

  const log = useMemo(() => buildSignupLog(rows || []), [rows]);
  const groups = useMemo(() => log.groups
    .map((g) => ({ ...g, items: g.items.filter((it) =>
      only === "notready" ? !it.state.ok : only === "minor" ? it.minor : true) }))
    .filter((g) => g.items.length), [log, only]);

  if (isAdmin === null) return null;
  if (!isAdmin) return (
    <div className="sg-wrap"><style>{CSS}</style>
      <p className="sg-empty" style={{ paddingTop: 40, textAlign: "center" }}>관리자 전용 화면입니다.</p></div>
  );

  return (
    <div className="sg-wrap">
      <style>{CSS}</style>
      <div className="sg-head">
        <span className="sg-back" onClick={() => (location.hash = "")}>← 홈</span>
        <h1 className="sg-h1">📋 가입 로그</h1>
        <span className="sg-sp" />
        <button className="sg-btn" disabled={busy} onClick={load}>{busy ? "불러오는 중…" : "새로고침"}</button>
      </div>
      <p className="sg-desc">
        누가 언제 가입했는지 한국 시간으로 분까지 보여 줘요. 가입을 끝까지 마친 계정(만 14세 미만은 보호자 문자 인증·동의까지)은
        승인 없이 바로 <b>이용 중</b>이 돼요. 보호자 동의를 막아야 하면 「🛡 보호자」에서 연결 해제하세요.
      </p>
      {rows && (
        <p className="sg-sum">
          전체 <b>{log.counts.total}</b>명 · 오늘 <b>{log.counts.today}</b> · 최근 7일 <b>{log.counts.week}</b>
          {log.counts.notReady > 0 && <> · 가입 마무리 전 <b className="sg-warnc">{log.counts.notReady}</b></>}
        </p>
      )}
      <div className="sg-tabs">
        {FILTERS.map(([v, l]) => (
          <button key={v} className={"sg-tab" + (only === v ? " on" : "")} onClick={() => setOnly(v)}>{l}</button>
        ))}
      </div>
      {err && <p className="sg-msg sg-err">{err}</p>}
      {rows === null && <p className="sg-empty">불러오는 중…</p>}
      {rows && groups.length === 0 && !err && <p className="sg-empty">해당하는 가입 기록이 없습니다.</p>}

      {groups.map((g) => (
        <section key={g.day} className="sg-day">
          <h2 className="sg-dayh">{g.label} <i>{g.items.length}명</i></h2>
          {g.items.map((it) => (
            <div key={it.id} className="sg-item">
              <div className="sg-line">
                <span className="sg-time">{it.time}</span>
                <span className="sg-name">{it.name}</span>
                {it.nickname && <span className="sg-nick">· {it.nickname}</span>}
                <span className="sg-sp" />
                <span className={"sg-st sg-" + it.state.key}>{it.state.label}</span>
              </div>
              <div className="sg-line sg-sub">
                <span>{it.age}</span>
                <span>· {it.provider}{it.username ? ` (${it.username})` : ""}</span>
                {it.minor && <span>· 14세 미만 가입{it.guardianAt ? ` · 보호자 동의 ${it.guardianAt}` : ""}</span>}
                {it.guardianWarn && <span className="sg-warn">⚠ 나이 간극</span>}
              </div>
            </div>
          ))}
        </section>
      ))}
    </div>
  );
}

const CSS = `
.sg-wrap { max-width: 720px; margin: 0 auto; padding: 24px 16px 64px; }
.sg-head { display: flex; align-items: baseline; gap: 12px; margin-bottom: 10px; }
.sg-h1 { font-size: 1.3rem; margin: 0; }
.sg-back { cursor: pointer; opacity: .65; font-size: .9rem; }
.sg-back:hover { opacity: 1; }
.sg-sp { flex: 1; }
.sg-desc { font-size: .84rem; opacity: .75; line-height: 1.6; margin: 0 0 10px; }
.sg-sum { font-size: .86rem; margin: 0 0 10px; }
.sg-warnc { color: #d97706; }
.sg-tabs { display: flex; gap: 6px; margin-bottom: 12px; flex-wrap: wrap; }
.sg-tab { border: 1px solid rgba(127,127,127,.3); background: transparent; color: inherit;
  border-radius: 999px; padding: 6px 12px; font-size: .82rem; cursor: pointer; opacity: .7; }
.sg-tab.on { border-color: rgba(20,164,148,.7); color: #16a08f; opacity: 1; font-weight: 700; }
.sg-msg { font-size: .84rem; margin: 6px 0; color: #16a08f; }
.sg-err { color: #e05252; }
.sg-empty { font-size: .85rem; opacity: .6; }
.sg-day { margin-bottom: 14px; }
.sg-dayh { font-size: .9rem; margin: 14px 0 8px; opacity: .85; }
.sg-dayh i { font-style: normal; font-weight: 400; opacity: .6; font-size: .8rem; margin-left: 4px; }
.sg-item { border: 1px solid rgba(127,127,127,.22); background: rgba(127,127,127,.05);
  border-radius: 12px; padding: 10px 12px; margin-bottom: 8px; }
.sg-line { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; font-size: .9rem; }
.sg-sub { margin-top: 5px; font-size: .78rem; opacity: .8; gap: 6px; }
.sg-time { font-variant-numeric: tabular-nums; font-weight: 700; min-width: 3.2em; }
.sg-name { font-weight: 700; }
.sg-nick { opacity: .7; }
.sg-st { border-radius: 999px; padding: 2px 9px; font-size: .74rem; font-weight: 700;
  border: 1px solid rgba(127,127,127,.3); white-space: nowrap; }
.sg-ok { color: #16a08f; border-color: rgba(20,164,148,.5); background: rgba(20,164,148,.1); }
.sg-guardian, .sg-verify { color: #d97706; border-color: rgba(217,119,6,.45); background: rgba(217,119,6,.08); }
.sg-trial, .sg-merged { opacity: .65; }
.sg-warn { color: #d97706; font-weight: 700; }
.sg-btn { border-radius: 9px; padding: 5px 12px; font-size: .8rem; cursor: pointer;
  border: 1px solid rgba(127,127,127,.3); background: rgba(127,127,127,.08); color: inherit; }
.sg-btn:disabled { opacity: .45; cursor: default; }
`;
