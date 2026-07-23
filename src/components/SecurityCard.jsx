// src/components/SecurityCard.jsx — 마이페이지 「보안·계정 연결」 카드
// MyPage의 mp-* 클래스와 CSS 변수를 그대로 사용 (MyPage 내부에서만 렌더)
import { useEffect, useState } from "react";
import { supabase } from "../supabaseClient";

const P_LABEL = { google: "Google", kakao: "카카오", email: "아이디/이메일" };

export default function SecurityCard({ profile }) {
  const [ids, setIds] = useState(null);       // 연결된 로그인 수단
  const [msg, setMsg] = useState("");
  const [busy, setBusy] = useState(false);

  // TOTP 간편인증
  const [factor, setFactor] = useState(null); // 등록 완료된 factor
  const [enroll, setEnroll] = useState(null); // 등록 진행 중 { id, qr, secret }
  const [code, setCode] = useState("");

  const refresh = async () => {
    const { data: idData } = await supabase.auth.getUserIdentities();
    setIds(idData?.identities || []);
    const { data: f } = await supabase.auth.mfa.listFactors();
    setFactor((f?.totp || []).find((x) => x.status === "verified") || null);
  };
  useEffect(() => { refresh(); }, []);

  const run = async (fn) => {
    setMsg(""); setBusy(true);
    try { await fn(); } catch (e) { setMsg("⚠ " + (e.message || String(e))); }
    setBusy(false);
  };

  const link = (provider) => run(async () => {
    const { error } = await supabase.auth.linkIdentity({
      provider, options: { redirectTo: window.location.origin },
    });
    if (error) throw new Error(error.message.includes("enabled")
      ? "계정 연결 기능이 꺼져 있어요. (Supabase: Allow manual linking)" : error.message);
  });

  const unlink = (identity) => run(async () => {
    if ((ids || []).length <= 1) throw new Error("마지막 로그인 수단은 해제할 수 없어요.");
    if (!window.confirm(`${P_LABEL[identity.provider] || identity.provider} 연결을 해제할까요?`)) return;
    const { error } = await supabase.auth.unlinkIdentity(identity);
    if (error) throw new Error(error.message);
    await refresh();
    setMsg("✓ 연결을 해제했어요.");
  });

  const startEnroll = () => run(async () => {
    const { data, error } = await supabase.auth.mfa.enroll({ factorType: "totp" });
    if (error) throw new Error(error.message.includes("disabled") || error.message.includes("enabled")
      ? "간편인증(TOTP)이 서버에서 꺼져 있어요. (Supabase: Auth → Multi-Factor 에서 TOTP 켜기)" : error.message);
    setEnroll({ id: data.id, qr: data.totp?.qr_code, secret: data.totp?.secret });
  });

  const confirmEnroll = () => run(async () => {
    const { data: ch, error: e1 } = await supabase.auth.mfa.challenge({ factorId: enroll.id });
    if (e1) throw new Error(e1.message);
    const { error: e2 } = await supabase.auth.mfa.verify({
      factorId: enroll.id, challengeId: ch.id, code: code.trim(),
    });
    if (e2) throw new Error("번호가 맞지 않아요. 앱의 최신 6자리로 다시 시도해주세요.");
    setEnroll(null); setCode("");
    await refresh();
    setMsg("✓ 간편인증을 켰어요. 다음 로그인부터 6자리 인증이 추가돼요.");
  });

  const removeFactor = () => run(async () => {
    if (!window.confirm("간편인증을 끌까요? 로그인 시 6자리 인증이 사라져요.")) return;
    const { error } = await supabase.auth.mfa.unenroll({ factorId: factor.id });
    if (error) throw new Error(error.message);
    await refresh();
    setMsg("✓ 간편인증을 껐어요.");
  });

  const linked = (provider) => (ids || []).find((i) => i.provider === provider);

  return (
    <div className="mp-card">
      <p className="mp-sec">보안 · 계정 연결</p>

      {/* 소셜 연결 */}
      {ids === null ? null : (
        <>
          {["google", "kakao"].map((pv) => {
            const it = linked(pv);
            return (
              <div className="mp-tgl" key={pv}>
                <span>{P_LABEL[pv]} 로그인<small>{it ? "연결됨 — 이 계정으로도 로그인할 수 있어요" : "연결하면 같은 계정으로 소셜 로그인이 가능해요"}</small></span>
                {it
                  ? <button className="mp-mini" disabled={busy} onClick={() => unlink(it)}>해제</button>
                  : <button className="mp-mini" disabled={busy} onClick={() => link(pv)}>연결</button>}
              </div>
            );
          })}
        </>
      )}

      {/* TOTP */}
      <div className="mp-tgl">
        <span>간편인증 (OTP 6자리)<small>{factor ? "사용 중 — 로그인 시 인증 앱 번호 필요" : "인증 앱으로 2단계 보호 (관리자 권장)"}</small></span>
        {factor
          ? <button className="mp-mini" disabled={busy} onClick={removeFactor}>끄기</button>
          : (!enroll && <button className="mp-mini" disabled={busy} onClick={startEnroll}>켜기</button>)}
      </div>

      {enroll && (
        <div style={{ textAlign: "center", padding: "6px 0 2px" }}>
          {enroll.qr && (
            <img src={enroll.qr} alt="OTP 등록 QR"
              style={{ width: 168, height: 168, background: "#fff", borderRadius: 12, padding: 8 }} />
          )}
          <p style={{ fontSize: 12, color: "var(--mut)", margin: "8px 0" }}>
            Google Authenticator 등 인증 앱으로 QR을 스캔한 뒤, 표시된 6자리를 입력해주세요.
            {enroll.secret ? <><br />수동 입력 키: <b style={{ userSelect: "all" }}>{enroll.secret}</b></> : null}
          </p>
          <div className="mp-row">
            <input className="mp-in" inputMode="numeric" maxLength={6} placeholder="123456"
              value={code} onChange={(e) => setCode(e.target.value)} />
            <button className="mp-mini" disabled={busy || code.length !== 6} onClick={confirmEnroll}>등록 완료</button>
          </div>
          <button className="mp-mini" style={{ width: "100%" }} disabled={busy}
            onClick={() => { setEnroll(null); setCode(""); }}>취소</button>
        </div>
      )}

      {profile?.role === "admin" && !factor && (
        <p className="mp-msg" style={{ color: "var(--mut)" }}>관리자 계정은 간편인증을 켜두는 걸 권장해요.</p>
      )}
      {msg && <p className={"mp-msg" + (msg.startsWith("✓") ? "" : " mp-err")}>{msg}</p>}
    </div>
  );
}
