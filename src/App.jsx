import { lazy, Suspense, useEffect, useState } from "react";
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
import PracticeViewer from "./pages/PracticeViewer";
import AdminPractice from "./pages/AdminPractice";
import AdminChats from "./components/AdminChats";
import AdminImages from "./components/AdminImages";
import AdminItemGen from "./components/AdminItemGen";
import AdminItemReview from "./components/AdminItemReview";
import AdminCorpus from "./components/AdminCorpus";
import AdminMonitor from "./components/AdminMonitor";
import AdminSchemas from "./components/AdminSchemas";
import GuardianConsent from "./components/GuardianConsent";
import AdminGuardians from "./components/AdminGuardians";
import Philosophy from "./components/Philosophy";
import HomeDash from "./components/HomeDash";
import AdminCalendar from "./components/AdminCalendar";
import QnaBoard from "./components/QnaBoard";
// P0 셸 — 관문·경로층 라우터
import Gate from "./gate/Gate";
import { rolePath } from "./shared/roles";
const SeiroccoApp = lazy(() => import("./apps/seirocco/SeiroccoApp"));
const JongseongApp = lazy(() => import("./apps/jongseong/JongseongApp"));

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
.rx-shell{min-height:100vh;color:var(--text)}
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

function VerifyGate({ theme, prof }) {
  const minor = prof?.is_minor;
  const trial = prof?.role === "trial";
  const noBirth = !trial && !prof?.birth_date;
  return (
    <Rx theme={theme}>
      <div style={{ maxWidth: 400, margin: "0 auto", padding: "72px 16px", textAlign: "center", color: "var(--text)" }}>
        <h2 style={{ fontSize: 20 }}>🔒 지금은 개념 열람만 가능해요</h2>
        <p style={{ fontSize: 14, color: "var(--muted)", lineHeight: 1.7 }}>
          {trial ? "체험 계정은 개념 열람만 가능해요. 정식 가입 후 모든 기능을 쓸 수 있어요."
            : noBirth ? "나이 확인이 아직 안 됐어요. 생년월일 확인과 본인 인증을 마치면 모든 기능이 열려요."
            : minor ? "만 14세 미만 학생은 보호자(법정대리인) 동의가 확인되면 모든 기능이 열려요."
            : "본인 인증(휴대폰)이 확인되면 모든 기능이 열려요. 마이페이지에서 인증할 수 있어요."}
        </p>
        {trial ? (
          <button onClick={async () => { await supabase.auth.signOut(); location.hash = "#/signup"; }}
            style={{ marginTop: 8, padding: "12px 20px", borderRadius: 12, border: "none",
              background: "var(--accent)", color: "#fff", fontSize: 15, fontWeight: 700 }}>회원가입 하러 가기</button>
        ) : (
          <button onClick={() => (location.hash = noBirth ? "#/onboarding" : minor ? "#/guardian" : "#/me")}
            style={{ marginTop: 8, padding: "12px 20px", borderRadius: 12, border: "none",
              background: "var(--accent)", color: "#fff", fontSize: 15, fontWeight: 700 }}>
            {noBirth ? "확인 이어서 하기" : minor ? "보호자 동의 진행하기" : "마이페이지로 이동"}</button>
        )}
        <p style={{ marginTop: 14 }}>
          <a href="#/" style={{ color: "var(--muted)", fontSize: 13 }}>개념 학습 계속하기</a>
        </p>
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

function AppRoutes() {
  const { theme, toggle } = useTheme();
  const hash = useHash();
  const [session, setSession] = useState(undefined); // undefined = 로딩 중
  const [prof, setProf] = useState(undefined);       // undefined = 미조회
  const [aalOk, setAalOk] = useState(undefined);     // undefined = 확인 중
  const [gOk, setGOk] = useState(undefined);         // 미성년 보호자 동의: true 활성 | false 미완 | null 해당없음
  const [gStarted, setGStarted] = useState(false);   // 보호자 동의 신청 이력

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => setSession(data.session ?? null));
    const { data: sub } = supabase.auth.onAuthStateChange((_e, s) => setSession(s));
    return () => sub.subscription.unsubscribe();
  }, []);

  // 로그인 시 프로필 + 간편인증 수준 조회 (+ 가입 확정, 미성년 보호자 동의 상태)
  useEffect(() => {
    if (!session) { setProf(undefined); setAalOk(undefined); setGOk(undefined); return; }
    let alive = true;
    (async () => {
      // 가입 예약 확정 — 이메일 인증 후 첫 로그인 1회 (예약된 전화·고유번호를 프로필에 반영)
      const st = session.user.user_metadata?.signup_token;
      if (st) {
        try {
          await fetch("/api/account", {
            method: "POST",
            headers: { "content-type": "application/json", authorization: `Bearer ${session.access_token}` },
            body: JSON.stringify({ action: "finalize", signup_token: st }),
          });
          await supabase.auth.updateUser({ data: { signup_token: null } });
        } catch { /* 실패 시 다음 로그인에서 재시도 */ }
      }
      const [{ data: p }, { data: aal }] = await Promise.all([
        supabase.from("profiles")
          .select("role, member_code, trial_expires_at, merged_into, phone_verified, is_minor, birth_date")
          .eq("id", session.user.id).maybeSingle(),
        supabase.auth.mfa.getAuthenticatorAssuranceLevel(),
      ]);
      if (!alive) return;
      setProf(p ?? null);
      setAalOk(!(aal && aal.nextLevel === "aal2" && aal.currentLevel !== "aal2"));
      if (p?.is_minor && p?.role !== "admin") {
        const { data: gs } = await supabase.from("guardian_consents")
          .select("status").eq("student_id", session.user.id);
        if (!alive) return;
        setGStarted((gs || []).length > 0);
        setGOk((gs || []).some((g) => g.status === "active"));
      } else {
        setGOk(null); setGStarted(false);
      }
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

  // v2: 고유번호는 선택 — 온보딩 강제 없음. 대신 인증 상태에 따라 기능을 잠근다.
  //  · 만 14세 미만: 보호자 동의(활성) 전까지 개념 열람만
  //  · 만 14세 이상: 전화 인증 또는 이메일 가입 확인 전까지 개념 열람만
  //  · 체험(trial): 개념 열람만
  if (prof?.is_minor && prof?.role !== "admin" && gOk === undefined) return null;
  const provider = session.user.app_metadata?.provider || "email";

  // 소셜 첫 로그인 — 생년월일(나이 확인)이 없으면 온보딩부터
  // 소셜 미온보딩: 세션당 1회만 온보딩으로 안내 — 이후엔 자유 이동(기능 잠금은 VerifyGate 담당)
  if (prof && prof.role !== "admin" && provider !== "email" && !prof.birth_date
      && !hash.startsWith("#/onboarding") && !hash.startsWith("#/qr-approve")
      && !sessionStorage.getItem("ob_nudged")) {
    sessionStorage.setItem("ob_nudged", "1");
    location.hash = "#/onboarding";
  }
  const verified =
    prof?.role === "admin" ? true
    : prof?.role === "trial" ? false
    : prof?.is_minor ? gOk === true
    : (prof?.phone_verified || provider === "email");

  // 미성년이 보호자 동의를 아직 시작하지 않았으면 동의 화면으로 안내
  if (prof?.is_minor && prof?.role !== "admin" && !verified && !gStarted
      && !hash.startsWith("#/guardian") && !hash.startsWith("#/me")) {
    location.hash = "#/guardian";
  }

  const LOCKED = ["#/learn/calc", "#/learn/wrong", "#/learn/hint", "#/board", "#/p/"];
  if (!verified && LOCKED.some((x) => hash.startsWith(x))) {
    return <VerifyGate theme={theme} prof={prof} />;
  }

  // ── 로그인 라우트 ──
  if (hash.startsWith("#/onboarding")) return <Rx theme={theme}><Onboarding /></Rx>;
  if (hash.startsWith("#/qr-approve")) return <Rx theme={theme}><QrApprove /></Rx>;
  if (hash.startsWith("#/find")) return <Rx theme={theme}><FindAccount /></Rx>;
  const pm = hash.match(/^#\/p\/(.+)$/);
  if (pm) return <Rx theme={theme}><PracticeViewer conceptId={decodeURIComponent(pm[1])} /></Rx>;
  if (hash.startsWith("#/admin/practice")) return <Rx theme={theme}><AdminPractice /></Rx>;
  if (hash.startsWith("#/admin/codes")) return <Rx theme={theme}><AdminCodes /></Rx>;
  if (hash.startsWith("#/admin/users")) return <Rx theme={theme}><AdminUsers /></Rx>;

  const bd = hash.match(/^#\/board(?:\/(.+))?$/);
  if (bd) return <Rx theme={theme}><QnaBoard theme={theme} initialId={bd[1] ? decodeURIComponent(bd[1]) : null} /></Rx>;
  if (hash === "#/admin/chats") return <Rx theme={theme}><AdminChats theme={theme} /></Rx>;
  if (hash === "#/admin/images") return <Rx theme={theme}><AdminImages theme={theme} /></Rx>;
  if (hash === "#/admin/itemgen") return <Rx theme={theme}><AdminItemGen theme={theme} /></Rx>;
  if (hash === "#/admin/items") return <Rx theme={theme}><AdminItemReview /></Rx>;
  if (hash === "#/admin/corpus") return <Rx theme={theme}><AdminCorpus /></Rx>;
  if (hash === "#/admin/monitor") return <Rx theme={theme}><AdminMonitor /></Rx>;
  if (hash === "#/admin/schemas") return <Rx theme={theme}><AdminSchemas /></Rx>;
  if (hash === "#/admin/guardians") return <Rx theme={theme}><AdminGuardians /></Rx>;
  if (hash.startsWith("#/guardian")) return <Rx theme={theme}><GuardianConsent /></Rx>;
  if (hash === "#/admin/calendar") return <Rx theme={theme}><AdminCalendar theme={theme} /></Rx>;
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
  if (hash.startsWith("#/philosophy")) return <Philosophy theme={theme} />;
  if (hash.startsWith("#/admin/qna")) return <AdminQna theme={theme} />;
  if (hash.startsWith("#/admin/concepts")) return <AdminConcepts theme={theme} />;
  if (hash.startsWith("#/me")) return <MyPage theme={theme} onToggleTheme={toggle} />;
  if (hash.startsWith("#/learn")) {
    const sub = hash.split("/")[2];
    return <Home theme={theme} onToggleTheme={toggle} initialCat={sub || "concept"} />;
  }
  return <HomeDash theme={theme} onToggleTheme={toggle} />;
}


// ── 전역 상단 바: 모든 페이지 상단(1행 인프라 + 2행 기능 5등분) ──
function TopBar({ theme, onToggleTheme, hash }) {
  const [me, setMe] = useState(null);
  const [dday, setDday] = useState(null);
  useEffect(() => {
    supabase.auth.getUser().then(async ({ data }) => {
      const u = data?.user; if (!u) { setMe(false); return; }
      const { data: p } = await supabase.from("profiles").select("role").eq("id", u.id).maybeSingle();
      setMe({ isAdmin: p?.role === "admin" });
    });
    const today = new Date().toISOString().slice(0, 10);
    supabase.from("events").select("date, title").eq("dday", true).gte("date", today)
      .order("date").limit(1).then(({ data }) => {
        if (data?.[0]) {
          const d = Math.round((new Date(data[0].date + "T00:00:00") - new Date(today + "T00:00:00")) / 86400000);
          setDday({ days: d, title: data[0].title });
        }
      });
  }, []);
  if (!me) return null;
  const light = theme !== "dark";
  const FN = [["📚", "개념", "#/learn/concept"], ["🧮", "연산", "#/learn/calc"],
              ["📕", "오답", "#/learn/wrong"], ["🗝️", "힌트", "#/learn/hint"], ["💬", "질문", "#/board"]];
  const isOn = (to) => to === "#/board" ? hash.startsWith("#/board")
    : hash.startsWith(to) || (to === "#/learn/concept" && (hash === "#/learn" || hash === "#/learn/"));
  return (
    <div className={"tb tb-" + theme}>
      <style>{`
        .tb { padding: 10px 14px 10px; font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
        .tb * { box-sizing: border-box; }
        .tb-light { background: #EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0D9488; }
        .tb-dark  { background: #0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#5EEAD4; }
        .tb-in { max-width: 680px; margin: 0 auto; }
        .tb-r1 { display: flex; gap: 7px; flex-wrap: wrap; align-items: center; margin-bottom: 8px; }
        .tb-sp { flex: 1; }
        .tb-logo { height: 28px; }
        .tb-light .tb-logo { filter: grayscale(1) brightness(0); }
        .tb-dday { min-width: 34px; height: 32px; border-radius: 999px; background: #EF4444; color: #fff;
          display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 800; padding: 0 8px; }
        .tb-btn { background: var(--card); border: 1px solid var(--bd); border-radius: 999px; color: var(--ink);
          font-size: 11.5px; font-weight: 700; padding: 7px 11px; cursor: pointer; }
        .tb-fn { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; }
        .tb-fnbtn { background: var(--card); border: 1px solid var(--bd); border-radius: 12px; padding: 8px 0 7px;
          color: var(--ink); cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 2px; }
        .tb-fnbtn.on { border-color: var(--ac); color: var(--ac); border-width: 1.5px; }
        .tb-fnbtn span:first-child { font-size: 15px; }
        .tb-fnbtn span:last-child { font-size: 11px; font-weight: 800; }
      `}</style>
      <div className="tb-in">
        <div className="tb-r1">
          {dday ? (
            <div className="tb-dday" title={dday.title} onClick={() => (location.hash = "")} style={{ cursor: "pointer" }}>
              {dday.days === 0 ? "D-DAY" : `D-${dday.days}`}
            </div>
          ) : (
            <img className="tb-logo" src="/brand/ashrain_logo.png" alt="ashrain"
              style={{ cursor: "pointer" }} onClick={() => (location.hash = "")} />
          )}
          <span className="tb-sp" />
          <button className="tb-btn" onClick={() => (location.hash = "#/me")}>👤 마이페이지</button>
          <a className="tb-btn" style={{ textDecoration: "none", display: "flex", alignItems: "center", gap: 4 }}
            href="https://www.instagram.com/ashrain.out" target="_blank" rel="noreferrer" title="앱 문의">
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 3a6 6 0 0 0-3.7 10.7c.6.5 1 1.3 1 2.1v.2h5.4v-.2c0-.8.4-1.6 1-2.1A6 6 0 0 0 12 3z" />
              <path d="M9.5 19h5" /><path d="M10.5 21.5h3" />
            </svg> 문의
          </a>
          {onToggleTheme && <button className="tb-btn" onClick={onToggleTheme}>{theme === "dark" ? "☀️" : "🌙"}</button>}
          {me.isAdmin && <>
            <button className="tb-btn" onClick={() => (location.hash = "#/admin/concepts")}>📚 등록</button>
            <button className="tb-btn" onClick={() => (location.hash = "#/admin/items")}>🔍 문항</button>
            <button className="tb-btn" onClick={() => (location.hash = "#/admin/corpus")}>📄 자료</button>
            <button className="tb-btn" onClick={() => (location.hash = "#/admin/qna")}>💬 검토</button>
            <button className="tb-btn" onClick={() => (location.hash = "#/admin/chats")}>🗂 대화</button>
            <button className="tb-btn" onClick={() => (location.hash = "#/admin/images")}>🖼 이미지</button>
            <button className="tb-btn" onClick={() => (location.hash = "#/admin/calendar")}>🗓 일정</button>
            <button className="tb-btn" onClick={() => (location.hash = "#/admin/guardians")}>🛡 보호자</button>
          </>}
        </div>
        <div className="tb-fn">
          {FN.map(([ic, lb, to]) => (
            <button key={to} className={"tb-fnbtn" + (isOn(to) ? " on" : "")} onClick={() => (location.hash = to)}>
              <span>{ic}</span><span>{lb}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── 학생앱(기존 전체) — 경로층 아래서 무수정 동작 ──
function StudentApp() {
  const hash = useHash();
  const { theme, toggle } = useTheme();
  return (
    <>
      <TopBar theme={theme} onToggleTheme={toggle} hash={hash} />
      <AppRoutes />
    </>
  );
}

const KNOWN_SEGS = ["", "walking", "running", "seirocco", "jongseong"];

function usePathSeg() {
  const read = () => location.pathname.split("/")[1] || "";
  const [seg, setSeg] = useState(read);
  useEffect(() => {
    const h = () => setSeg(read());
    window.addEventListener("popstate", h);
    window.addEventListener("pathchange", h);
    return () => { window.removeEventListener("popstate", h); window.removeEventListener("pathchange", h); };
  }, []);
  return [seg, setSeg];
}

// ── 경로층 라우터(P0): pathname 1단계 = 앱 선택, 해시 = 앱 내부(현행 그대로) ──
function PathRouter() {
  const { theme, toggle } = useTheme();
  const hash = useHash();
  const [seg, setSeg] = usePathSeg();
  const [session, setSession] = useState(undefined);

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => setSession(data.session ?? null));
    const { data: sub } = supabase.auth.onAuthStateChange((_e, s) => setSession(s ?? null));
    return () => sub.subscription.unsubscribe();
  }, []);

  // 경로 → 테마 스코프(신규 셸·향후 공용 컴포넌트용)
  useEffect(() => {
    document.documentElement.dataset.app =
      seg === "seirocco" ? "seirocco" : seg === "jongseong" ? "jongseong" : "ashrain";
  }, [seg]);

  // 미지의 경로 → 관문으로 정리
  useEffect(() => {
    if (!KNOWN_SEGS.includes(seg)) {
      history.replaceState(null, "", "/" + location.hash);
      setSeg("");
    }
  }, [seg, setSeg]);

  // 관문(/) + 로그인 → 마지막 역할 경로로 (주소만 교체, 리로드 없음)
  useEffect(() => {
    if (seg !== "" || !session) return;
    const last = session.user.user_metadata?.last_role || "student";
    const to = rolePath(last);
    history.replaceState(null, "", to + location.search + location.hash);
    setSeg(to.slice(1));
  }, [seg, session, setSeg]);

  // /walking ↔ /running 무음 동기화 — honor_path 기준. 컬럼 미존재·조회 실패는 조용히 통과.
  // 합격 공지 없음: 자격이 생기면 다음 접속부터 주소만 바뀌고, 미자격 /running 진입은 잠금 화면 없이 치환.
  useEffect(() => {
    if (!session || (seg !== "walking" && seg !== "running")) return;
    let alive = true;
    supabase.from("profiles").select("honor_path").eq("id", session.user.id).maybeSingle()
      .then(({ data, error }) => {
        if (!alive || error) return;
        const honor = !!data?.honor_path;
        if (seg === "running" && !honor) { history.replaceState(null, "", "/walking" + location.hash); setSeg("walking"); }
        else if (seg === "walking" && honor) { history.replaceState(null, "", "/running" + location.hash); setSeg("running"); }
      })
      .catch(() => {});
    return () => { alive = false; };
  }, [seg, session?.user?.id, setSeg]);

  if (seg === "walking" || seg === "running") return <StudentApp />;

  if (seg === "seirocco" || seg === "jongseong") {
    if (session === undefined) return null;
    if (!session) return <SplashAuth theme={theme} onToggleTheme={toggle} onSuccess={() => {}} />;
    const Shell = seg === "seirocco" ? SeiroccoApp : JongseongApp;
    return <Suspense fallback={null}><Shell /></Suspense>;
  }

  if (!KNOWN_SEGS.includes(seg)) return null;

  // seg === "" — 관문
  if (session === undefined) return null;
  if (session) return null; // 위 효과가 역할 경로로 옮기는 중
  // pushState는 hashchange를 발생시키지 않으므로 상태(hash) 대신 실제 값을 읽는다
  const liveHash = location.hash;
  if (liveHash && liveHash !== "#" && liveHash !== "#/") return <StudentApp />; // 레거시 비로그인 해시(#/signup, #/qr 등)
  return <Gate />;
}

export default function App() {
  return <PathRouter />;
}
