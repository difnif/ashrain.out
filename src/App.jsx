import { useEffect, useState } from "react";
import { supabase } from "./supabaseClient";
import { useTheme } from "./lib/theme";
import SplashAuth from "./components/SplashAuth";
import Home from "./components/Home";
import ConceptViewer from "./components/ConceptViewer";
import AdminQna from "./components/AdminQna";
import AdminConcepts from "./components/AdminConcepts";
import MyPage from "./components/MyPage";
import PortraitStudio from "./features/portrait/PortraitStudio";
// raindrop (v0.4.0)
import Signup from "./pages/Signup";
import FindAccount from "./pages/FindAccount";
import Onboarding from "./pages/Onboarding";
import TrialStart from "./pages/TrialStart";
import StaffJoin from "./pages/StaffJoin";
import QrApprove from "./pages/QrApprove";
import QrLogin from "./pages/QrLogin";
import AdminCodes from "./pages/AdminCodes";
import AdminUsers from "./pages/AdminUsers";

function useHash() {
  const [hash, setHash] = useState(location.hash);
  useEffect(() => {
    const h = () => setHash(location.hash);
    window.addEventListener("hashchange", h);
    return () => window.removeEventListener("hashchange", h);
  }, []);
  return hash;
}

// raindrop 신규 화면용 테마 변수 매핑 (페이지들은 var(--text) 등만 사용)
const RX_CSS = `
.rx-shell{min-height:100vh}
.rx-light{background:#EDEFF2;--text:#1F2937;--muted:#6B7480;--surface:#FFFFFF;--surface2:#F1F2F4;--surface3:#E4E7EB;--border:#D9DEE4;--accent:#0DA95F;--good:#16A34A;--bad:#DC2626}
.rx-dark{background:#0B0C0F;--text:#E2E8F0;--muted:#8A929C;--surface:#15171C;--surface2:#1C1F26;--surface3:#23262D;--border:#2B2E36;--accent:#5B8DEF;--good:#4ADE80;--bad:#F87171}
`;
function Rx({ theme, children }) {
  return (
    <div className={`rx-shell rx-${theme}`}>
      <style>{RX_CSS}</style>
      {children}
    </div>
  );
}

// ── 간편인증(TOTP) 게이트: 등록된 기기가 있으면 로그인 직후 6자리 요구 ──
function MfaGate({ theme, onPass }) {
  const [factor, setFactor] = useState(null);
  const [code, setCode] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    supabase.auth.mfa.listFactors().then(({ data }) => {
      const f = (data?.totp || []).find((x) => x.status === "verified");
      setFactor(f || null);
    });
  }, []);

  const verify = async () => {
    if (!factor || busy) return;
    setBusy(true); setErr("");
    try {
      const { data: ch, error: e1 } = await supabase.auth.mfa.challenge({ factorId: factor.id });
      if (e1) throw e1;
      const { error: e2 } = await supabase.auth.mfa.verify({
        factorId: factor.id, challengeId: ch.id, code: code.trim(),
      });
      if (e2) throw new Error("인증번호가 맞지 않아요. 앱의 최신 번호로 다시 시도해주세요.");
      onPass();
    } catch (e) { setErr(e.message || String(e)); }
    setBusy(false);
  };

  return (
    <Rx theme={theme}>
      <div style={{ maxWidth: 380, margin: "0 auto", padding: "56px 16px", color: "var(--text)" }}>
        <h2 style={{ fontSize: 20, margin: "0 0 8px" }}>간편인증</h2>
        <p style={{ fontSize: 14, color: "var(--muted)", margin: "0 0 14px" }}>
          인증 앱(Google Authenticator 등)에 표시된 6자리 번호를 입력해주세요.
        </p>
        <input value={code} onChange={(e) => setCode(e.target.value)} inputMode="numeric" maxLength={6}
          placeholder="123456" onKeyDown={(e) => e.key === "Enter" && verify()}
          style={{ width: "100%", boxSizing: "border-box", padding: 14, fontSize: 20, letterSpacing: 6,
            textAlign: "center", borderRadius: 12, border: "1px solid var(--border)",
            background: "var(--surface)", color: "var(--text)" }} />
        <button onClick={verify} disabled={busy || code.length !== 6}
          style={{ width: "100%", marginTop: 10, padding: 13, borderRadius: 12, border: "none",
            background: "var(--accent)", color: "#fff", fontSize: 15, fontWeight: 700,
            opacity: busy || code.length !== 6 ? 0.6 : 1 }}>확인</button>
        {err && <p style={{ color: "var(--bad)", fontSize: 13 }}>{err}</p>}
        <button onClick={async () => { await supabase.auth.signOut(); location.hash = ""; }}
          style={{ marginTop: 18, background: "none", border: "none", color: "var(--muted)",
            fontSize: 13, textDecoration: "underline", cursor: "pointer" }}>다른 계정으로 로그인</button>
      </div>
    </Rx>
  );
}

function TrialExpired({ theme }) {
  return (
    <Rx theme={theme}>
      <div style={{ maxWidth: 380, margin: "0 auto", padding: "72px 16px", textAlign: "center", color: "var(--text)" }}>
        <h2 style={{ fontSize: 20 }}>체험 시간이 끝났어요</h2>
        <p style={{ fontSize: 14, color: "var(--muted)", lineHeight: 1.7 }}>
          24시간 체험이 만료됐어요. 계속 쓰고 싶다면 학원 선생님께 정식 고유번호를 요청한 뒤
          회원가입을 진행해주세요. 체험 중 기록은 보관돼요.
        </p>
        <button onClick={async () => { await supabase.auth.signOut(); location.hash = "#/signup"; }}
          style={{ marginTop: 8, padding: "12px 20px", borderRadius: 12, border: "none",
            background: "var(--accent)", color: "#fff", fontSize: 15, fontWeight: 700 }}>회원가입 하러 가기</button>
      </div>
    </Rx>
  );
}

export default function App() {
  const { theme, toggle } = useTheme();
  const hash = useHash();
  const [session, setSession] = useState(undefined); // undefined = 로딩 중
  const [prof, setProf] = useState(undefined);       // undefined = 미조회
  const [aalOk, setAalOk] = useState(undefined);     // undefined = 확인 중

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => setSession(data.session ?? null));
    const { data: sub } = supabase.auth.onAuthStateChange((_e, s) => setSession(s));
    return () => sub.subscription.unsubscribe();
  }, []);

  // 로그인 시 프로필 + 간편인증 수준 조회
  useEffect(() => {
    if (!session) { setProf(undefined); setAalOk(undefined); return; }
    let alive = true;
    (async () => {
      const [{ data: p }, { data: aal }] = await Promise.all([
        supabase.from("profiles")
          .select("role, member_code, trial_expires_at, merged_into")
          .eq("id", session.user.id).maybeSingle(),
        supabase.auth.mfa.getAuthenticatorAssuranceLevel(),
      ]);
      if (!alive) return;
      setProf(p ?? null);
      setAalOk(!(aal && aal.nextLevel === "aal2" && aal.currentLevel !== "aal2"));
    })();
    return () => { alive = false; };
  }, [session?.user?.id]);

  if (session === undefined) return null;

  // ── 비로그인 라우트 ──
  if (!session) {
    if (hash.startsWith("#/signup")) return <Rx theme={theme}><Signup /></Rx>;
    if (hash.startsWith("#/find")) return <Rx theme={theme}><FindAccount /></Rx>;
    if (hash.startsWith("#/trial")) return <Rx theme={theme}><TrialStart /></Rx>;
    if (hash.startsWith("#/staff-join")) return <Rx theme={theme}><StaffJoin /></Rx>;
    if (hash.startsWith("#/qr-approve")) return <Rx theme={theme}><QrApprove /></Rx>;
    if (hash.startsWith("#/qr")) return <Rx theme={theme}><QrLogin /></Rx>;
    return <SplashAuth theme={theme} onToggleTheme={toggle} onSuccess={() => (location.hash = "")} />;
  }

  // ── 로그인 공통 게이트 ──
  if (prof === undefined || aalOk === undefined) return null;
  if (!aalOk) return <MfaGate theme={theme} onPass={() => setAalOk(true)} />;

  if (prof?.role === "trial" && prof.trial_expires_at && new Date(prof.trial_expires_at) < new Date()) {
    return <TrialExpired theme={theme} />;
  }

  const needsOnboarding = prof && !prof.member_code
    && prof.role !== "admin" && prof.role !== "trial" && !prof.merged_into;
  if (needsOnboarding && !hash.startsWith("#/onboarding") && !hash.startsWith("#/qr-approve")) {
    location.hash = "#/onboarding";
  }

  // ── 로그인 라우트 ──
  if (hash.startsWith("#/onboarding")) return <Rx theme={theme}><Onboarding /></Rx>;
  if (hash.startsWith("#/qr-approve")) return <Rx theme={theme}><QrApprove /></Rx>;
  if (hash.startsWith("#/find")) return <Rx theme={theme}><FindAccount /></Rx>;
  if (hash.startsWith("#/admin/codes")) return <Rx theme={theme}><AdminCodes /></Rx>;
  if (hash.startsWith("#/admin/users")) return <Rx theme={theme}><AdminUsers /></Rx>;

  const c = hash.match(/^#\/c\/(.+)$/);
  if (c) return <ConceptViewer conceptId={decodeURIComponent(c[1])} theme={theme} />;
  if (hash.startsWith("#/portrait")) {
    return (
      <PortraitStudio onDone={async (blob) => {
        const uid = session.user.id;
        const { error } = await supabase.storage.from("avatars")
          .upload(`${uid}/portrait.png`, blob, { upsert: true, contentType: "image/png" });
        if (!error) {
          const { data } = supabase.storage.from("avatars").getPublicUrl(`${uid}/portrait.png`);
          await supabase.from("profiles").update({ avatar_url: data.publicUrl }).eq("id", uid);
          alert("초상화가 프로필에 저장됐어요!");
          location.hash = "";
        } else alert("저장에 실패했어요. 잠시 후 다시 시도해 주세요.");
      }} />
    );
  }
  if (hash.startsWith("#/admin/qna")) return <AdminQna theme={theme} />;
  if (hash.startsWith("#/admin/concepts")) return <AdminConcepts theme={theme} />;
  if (hash.startsWith("#/me")) return <MyPage theme={theme} onToggleTheme={toggle} />;
  return <Home theme={theme} onToggleTheme={toggle} />;
}
