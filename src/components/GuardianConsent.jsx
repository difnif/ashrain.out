// ashrain.out — 보호자(법정대리인) 동의 화면 (v1.1, #/guardian)
// v1.1: 인증번호 입력 제한시간(5:00) 타이머 — 초과 시 확인 비활성(서버도 만료 무효 처리)
// 흐름: 보호자 정보 입력 → 보호자 휴대폰으로 인증번호 발송(/api/otp, purpose 'guardian')
//       → 인증 확인 → 고지문·동의 체크 → 제출(/api/guardian) → 강사 확인 후 활성화.
// 조회·철회는 guardian_consents RLS로 직접. 새 환경변수 불필요(기존 SMS 인프라 재사용).
import { useEffect, useState } from "react";
import { supabase } from "../supabaseClient";

const REL = ["모", "부", "조부모", "기타"];
const ST = { pending: "⏳ 강사 확인 대기", active: "✅ 활성", rejected: "❌ 반려" };

export default function GuardianConsent() {
  const [me, setMe] = useState(null);
  const [list, setList] = useState(null);
  const [f, setF] = useState({ name: "", relation: "모", birth: "", phone: "" });
  const [code, setCode] = useState("");
  const [otp, setOtp] = useState("idle"); // idle | sent | ok
  const [token, setToken] = useState(null);
  const [otpEnd, setOtpEnd] = useState(null);
  const [otpLeft, setOtpLeft] = useState(0);
  const [ag1, setAg1] = useState(false);
  const [ag2, setAg2] = useState(false);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");

  useEffect(() => {
    if (!otpEnd) return;
    const tick = () => setOtpLeft(Math.max(0, Math.ceil((otpEnd - Date.now()) / 1000)));
    tick();
    const t = setInterval(tick, 500);
    return () => clearInterval(t);
  }, [otpEnd]);
  const otpExpired = !!otpEnd && otpLeft === 0;
  const fmtLeft = (s) => Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0");

  const load = async () => {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;
    const { data: p } = await supabase.from("profiles")
      .select("id, name, birth_year").eq("id", user.id).maybeSingle();
    setMe(p || { id: user.id });
    const { data: gs } = await supabase.from("guardian_consents").select("*")
      .eq("student_id", user.id).order("created_at", { ascending: false });
    setList(gs || []);
  };
  useEffect(() => { load(); }, []);

  const api = async (path, body) => {
    const { data: s } = await supabase.auth.getSession();
    const r = await fetch(path, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        ...(s?.session?.access_token ? { authorization: `Bearer ${s.session.access_token}` } : {}),
      },
      body: JSON.stringify(body),
    });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(j?.error || `요청 실패 (${r.status})`);
    return j;
  };

  const sendOtp = async () => {
    if (busy) return;
    setErr(""); setMsg(""); setBusy(true);
    try {
      await api("/api/otp", { action: "send", phone: f.phone, purpose: "guardian" });
      setOtp("sent"); setCode("");
      setOtpEnd(Date.now() + 5 * 60e3);
      setMsg("보호자님 휴대폰으로 인증번호를 보냈어요 (5분 내 입력).");
    } catch (e) { setErr(e.message); }
    setBusy(false);
  };

  const verifyOtp = async () => {
    if (busy) return;
    setErr(""); setMsg(""); setBusy(true);
    try {
      if (otpExpired) throw new Error("입력 시간이 지났어요 — 인증번호를 다시 발송해주세요");
      const j = await api("/api/otp", { action: "verify", phone: f.phone, purpose: "guardian", code });
      setToken(j.phone_token); setOtp("ok"); setOtpEnd(null);
      setMsg("보호자 휴대폰 인증 완료 ✓ — 아래 동의 항목을 확인해주세요.");
    } catch (e) { setErr(e.message); }
    setBusy(false);
  };

  const submit = async () => {
    if (busy) return;
    setErr(""); setMsg("");
    if (otp !== "ok" || !token) { setErr("보호자 휴대폰 인증을 먼저 완료해주세요."); return; }
    if (f.name.trim().length < 2) { setErr("보호자 성명을 입력해주세요."); return; }
    if (!/^\d{4}$/.test(f.birth)) { setErr("보호자 출생연도 4자리를 입력해주세요 (예: 1980)."); return; }
    if (!ag1 || !ag2) { setErr("필수 동의 항목 2개에 모두 체크해주세요."); return; }
    setBusy(true);
    try {
      const j = await api("/api/guardian", {
        action: "submit", phone_token: token,
        guardian_name: f.name.trim(), relation: f.relation, guardian_birth_year: +f.birth,
      });
      if (j.already) setMsg("이미 활성화된 보호자예요.");
      else setMsg("제출 완료 — 강사 확인 후 활성화됩니다." + (j.age_gap_warn ? " (확인이 조금 더 걸릴 수 있어요)" : ""));
      setF({ name: "", relation: "모", birth: "", phone: "" });
      setCode(""); setToken(null); setOtp("idle"); setAg1(false); setAg2(false);
      load();
    } catch (e) { setErr(e.message); }
    setBusy(false);
  };

  const withdraw = async (g) => {
    if (!window.confirm(`「${g.guardian_name}」 보호자 등록 요청을 철회할까요?\n입력한 보호자 정보는 삭제됩니다.`)) return;
    const { error } = await supabase.from("guardian_consents").delete().eq("id", g.id);
    if (error) setErr("철회 실패: " + error.message);
    else { setMsg("철회했어요 — 보호자 정보가 삭제되었습니다."); load(); }
  };

  const young = me?.birth_year && new Date().getFullYear() - me.birth_year <= 14;

  return (
    <div className="gc-wrap">
      <style>{CSS}</style>
      <div className="gc-head">
        <span className="gc-back" onClick={() => (location.hash = "")}>← 홈</span>
        <h1 className="gc-h1">👨‍👩‍👧 보호자 동의</h1>
      </div>

      {young && (
        <p className="gc-note">
          만 14세 미만 학생은 법에 따라 <b>법정대리인(보호자)의 동의</b>가 꼭 필요해요.
          아래 절차는 보호자님과 함께 진행해주세요.
        </p>
      )}

      <div className="gc-card">
        <p className="gc-desc"><b>진행 순서</b> — ① 보호자 정보 입력 → ② 보호자님 휴대폰으로 인증번호 발송,
          보호자님이 직접 확인·입력 → ③ 동의 항목 체크 → ④ 제출. 이후 강사 확인을 거쳐 활성화됩니다.</p>

        <div className="gc-row">
          <input className="gc-inp" style={{ flex: 2, minWidth: 120 }} placeholder="보호자 성명"
            value={f.name} onChange={(e) => setF((s) => ({ ...s, name: e.target.value }))} />
          <select className="gc-inp" value={f.relation}
            onChange={(e) => setF((s) => ({ ...s, relation: e.target.value }))}>
            {REL.map((r) => <option key={r} value={r}>{r}</option>)}
          </select>
          <input className="gc-inp" style={{ width: 110 }} placeholder="출생연도 4자리"
            inputMode="numeric" maxLength={4} value={f.birth}
            onChange={(e) => setF((s) => ({ ...s, birth: e.target.value.replace(/\D/g, "") }))} />
        </div>

        <div className="gc-row">
          <input className="gc-inp" style={{ flex: 1, minWidth: 160 }} placeholder="보호자 휴대폰 번호"
            inputMode="numeric" value={f.phone} disabled={otp === "ok"}
            onChange={(e) => { setF((s) => ({ ...s, phone: e.target.value })); setOtp("idle"); setToken(null); setOtpEnd(null); }} />
          <button className="gc-btn gc-pri" disabled={busy || otp === "ok" || !f.phone.trim()} onClick={sendOtp}>
            {otp === "sent" ? "재발송" : "인증번호 발송"}
          </button>
        </div>

        {otp === "sent" && (
          <div className="gc-row">
            <input className="gc-inp" style={{ width: 130 }} placeholder="인증번호 6자리"
              inputMode="numeric" maxLength={6} value={code}
              onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))} />
            <button className="gc-btn gc-pri" disabled={busy || code.length !== 6 || otpExpired} onClick={verifyOtp}>인증 확인</button>
          </div>
        )}
        {otp === "sent" && (
          <p className="gc-timer">
            {otpExpired ? "입력 시간이 지났어요 — 인증번호를 다시 발송해주세요" : `남은 입력 시간 ${fmtLeft(otpLeft)}`}
          </p>
        )}
        {otp === "ok" && <p className="gc-ok">보호자 휴대폰 인증 완료 ✓</p>}

        <div className="gc-law">
          <b>법정대리인(보호자) 동의 안내</b>
          <div>· 수집 항목: 보호자 성명, 관계, 출생연도, 휴대전화번호</div>
          <div>· 수집 목적: 만 14세 미만 아동의 개인정보 처리에 대한 법정대리인 동의 확인 및 보호자 연결</div>
          <div>· 보유 기간: 회원 탈퇴 또는 연결 해제 시까지 (동의가 확인되지 않은 정보는 5일 이내 파기)</div>
          <div>· 동의를 거부할 수 있으며, 만 14세 미만 학생은 동의 없이는 일부 서비스 이용이 제한됩니다.</div>
        </div>
        <label className="gc-chk">
          <input type="checkbox" checked={ag1} onChange={(e) => setAg1(e.target.checked)} />
          <span>(필수) 위 안내를 확인했고, 보호자 개인정보 수집·이용에 동의합니다.</span>
        </label>
        <label className="gc-chk">
          <input type="checkbox" checked={ag2} onChange={(e) => setAg2(e.target.checked)} />
          <span>(필수) 본인은 위 학생의 법정대리인이며, 학생의 애쉬레인 이용과 개인정보 처리에 동의합니다.</span>
        </label>

        <div className="gc-row" style={{ marginTop: 10 }}>
          <button className="gc-btn gc-pri" disabled={busy} onClick={submit}>동의 제출</button>
        </div>
        {msg && <p className="gc-msg">{msg}</p>}
        {err && <p className="gc-msg gc-err">{err}</p>}
      </div>

      <div className="gc-card">
        <p className="gc-desc"><b>등록된 보호자</b></p>
        {list && list.length === 0 && <p className="gc-empty">아직 등록된 보호자가 없어요.</p>}
        {(list || []).map((g) => (
          <div key={g.id} className="gc-item">
            <span className="gc-st">{ST[g.status] || g.status}</span>
            <span className="gc-nm">{g.guardian_name} ({g.relation})</span>
            <span className="gc-ph">{String(g.guardian_phone).replace(/(\d{3})(\d{3,4})(\d{4})/, "$1-$2-$3")}</span>
            {g.status === "rejected" && g.reject_reason && <span className="gc-rr">사유: {g.reject_reason}</span>}
            {g.status === "pending" && (
              <button className="gc-btn gc-del" onClick={() => withdraw(g)}>철회</button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

const CSS = `
.gc-wrap { max-width: 640px; margin: 0 auto; padding: 24px 16px 64px; }
.gc-head { display: flex; align-items: baseline; gap: 12px; margin-bottom: 14px; }
.gc-h1 { font-size: 1.3rem; margin: 0; }
.gc-back { cursor: pointer; opacity: .65; font-size: .9rem; }
.gc-back:hover { opacity: 1; }
.gc-note { font-size: .85rem; padding: 10px 14px; border-radius: 10px; line-height: 1.55;
  background: rgba(20,164,148,.1); border: 1px solid rgba(20,164,148,.4); }
.gc-card { border: 1px solid rgba(127,127,127,.22); background: rgba(127,127,127,.05);
  border-radius: 14px; padding: 16px; margin-bottom: 16px; }
.gc-desc { font-size: .86rem; opacity: .85; margin: 0 0 10px; line-height: 1.6; }
.gc-row { display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap; align-items: center; }
.gc-inp { padding: 9px 11px; border-radius: 10px; border: 1px solid rgba(127,127,127,.32);
  background: rgba(255,255,255,.55); color: inherit; font-size: .88rem; box-sizing: border-box; }
[data-theme="dark"] .gc-inp { background: rgba(0,0,0,.25); }
.gc-btn { border-radius: 10px; padding: 9px 14px; font-size: .86rem; cursor: pointer;
  border: 1px solid rgba(127,127,127,.3); background: rgba(127,127,127,.08); color: inherit; }
.gc-btn:disabled { opacity: .45; cursor: default; }
.gc-pri { background: rgba(20,164,148,.16); border-color: rgba(20,164,148,.5); }
.gc-pri:not(:disabled):hover { background: rgba(20,164,148,.26); }
.gc-del { padding: 4px 10px; font-size: .78rem;
  background: rgba(244,99,99,.1); border-color: rgba(244,99,99,.4); }
.gc-ok { font-size: .82rem; color: #16a08f; font-weight: 700; margin: 8px 0 0; }
.gc-timer { font-size: .78rem; color: #e05252; font-weight: 700; margin: 4px 0 0; font-variant-numeric: tabular-nums; }
.gc-law { font-size: .78rem; line-height: 1.7; opacity: .85; margin-top: 12px;
  border: 1px dashed rgba(127,127,127,.4); border-radius: 10px; padding: 10px 12px; }
.gc-chk { display: flex; gap: 8px; align-items: flex-start; font-size: .8rem;
  line-height: 1.5; margin-top: 8px; cursor: pointer; }
.gc-chk input { margin-top: 2px; }
.gc-msg { font-size: .84rem; margin: 10px 0 0; white-space: pre-wrap; color: #16a08f; }
.gc-err { color: #e05252; }
.gc-empty { font-size: .84rem; opacity: .6; }
.gc-item { display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
  padding: 8px 10px; border-radius: 10px; font-size: .86rem; }
.gc-item:hover { background: rgba(127,127,127,.08); }
.gc-st { font-size: .78rem; font-weight: 700; }
.gc-nm { font-weight: 600; }
.gc-ph { opacity: .6; font-size: .8rem; }
.gc-rr { width: 100%; font-size: .76rem; color: #e05252; }
`;
