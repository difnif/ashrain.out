import { useState, useEffect } from "react";
import { supabase } from "../supabaseClient";
import { idToEmail } from "../lib/auth";
import { api, getLastLoginMethod, recordLoginMethod } from "../lib/authx";

// ASH RAIN 스플래시 + 로그인 (듀얼 테마)
// props: theme('light'|'dark'), onToggleTheme(), onSuccess(session)
// 배경 사진을 쓰려면 라이트 테마에서 --bg-image 를 채우면 됨 (아래 CSS 참고)

const L = {
  ashrain: "/brand/layer_ashrain.png",
  out: "/brand/layer_out.png",
  stroke: "/brand/layer_stroke.png",
  ver: "/brand/layer_ver.png",
};

const CSS = `
.ar-root { min-height: 100vh; font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif;
  display: flex; align-items: center; justify-content: center; padding: 24px 16px; box-sizing: border-box;
  position: relative; overflow: hidden; transition: background .4s; }
.ar-root *, .ar-root *::before, .ar-root *::after { box-sizing: border-box; }
.th-dark { background: radial-gradient(1200px 800px at 50% 20%, #16171B 0%, #0B0B0E 55%, #060608 100%);
  --card-bg: rgba(23,24,28,.92); --card-bd: #26282F; --input-bg: #101116; --input-bd: #2B2E36;
  --text: #E7EAF0; --muted: #6B7280; --label: #7C8592; --ph: #4B5563;
  --accent: #FFE03C; --accent-tx: #14140F; --link: #8FA8C4; --link-h: #B9D0E8; --sep: #3A3D45;
  --focus: #4F7EA8; --focus-ring: rgba(79,126,168,.18); --ctrl-bg: rgba(23,24,28,.8); --ctrl-tx: #9CA3AF;
  --logo-filter: drop-shadow(0 0 20px rgba(255,224,60,.15)); }
.th-light {
  /* 배경 사진 적용 지점: 아래 한 줄을 사진 경로로 교체
     background: linear-gradient(rgba(238,241,244,.82), rgba(200,206,213,.88)), url('/brand/rainy_street.jpg') center/cover; */
  background: linear-gradient(to bottom, #EFF1F4 0%, #E3E6EA 55%, #C9CED5 78%, #B8BEC6 100%);
  --card-bg: rgba(255,255,255,.9); --card-bd: #D9DEE4; --input-bg: #F4F6F8; --input-bd: #D3D9DF;
  --text: #1F2937; --muted: #8A929C; --label: #6B7480; --ph: #9AA3AD;
  --accent: #0DA95F; --accent-tx: #FFFFFF; --link: #55708C; --link-h: #33526F; --sep: #C3C9D0;
  --focus: #0DA95F; --focus-ring: rgba(13,169,95,.18); --ctrl-bg: rgba(255,255,255,.75); --ctrl-tx: #6B7480;
  --logo-filter: hue-rotate(88deg) saturate(1.35) brightness(.88)
                 drop-shadow(0 0 14px rgba(255,200,60,.65)) drop-shadow(0 0 30px rgba(255,190,60,.35)); }
.ar-drop { position: absolute; top: -14px; border-radius: 2px; animation: ar-fall linear infinite; pointer-events: none; }
.th-dark .ar-drop { width: 2px; background: linear-gradient(to bottom, rgba(148,163,184,0), rgba(148,163,184,.4)); }
.th-light .ar-drop { width: 1.5px; transform-origin: top; rotate: 9deg;
  background: linear-gradient(to bottom, rgba(110,130,155,0), rgba(110,130,155,.5));
  animation-duration: calc(var(--d) * .45) !important; }
@keyframes ar-fall { from { transform: translateY(-6vh); } to { transform: translateY(112vh); } }
.ar-stage { position: relative; width: 100%; max-width: 400px; display: flex; flex-direction: column; align-items: center; }
.ar-logobox { position: relative; width: 82%; max-width: 330px; animation: ar-boxseq 2.4s cubic-bezier(.25,.8,.3,1) both; }
@keyframes ar-boxseq { 0%,46% { transform: scale(2.05) translate(7%, 26%); } 72%,100% { transform: scale(1) translate(0,0); } }
.ar-logobox img { width: 100%; display: block; filter: var(--logo-filter); transition: filter .4s; }
.ar-layer { position: absolute; inset: 0; }
.ar-l1 { position: relative; animation: ar-wipe 1.15s ease-in-out .1s both; }
.ar-l2 { animation: ar-wipe .55s ease-in-out 1.7s both; }
.ar-l3 { animation: ar-wipe .45s cubic-bezier(.3,.1,.3,1) 2.3s both; }
.ar-l4 { animation: ar-wipe .4s ease-out 2.75s both; }
@keyframes ar-wipe { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0% 0 0); } }
.ar-reflect { display: none; }
.th-light .ar-reflect { display: block; position: relative; width: 82%; max-width: 330px; height: 0; }
.th-light .ar-rbox { position: absolute; left: 0; right: 0; top: 6px; transform: scaleY(-1) skewX(-3deg);
  filter: blur(3px); opacity: 0; animation: ar-reflectin 1.2s ease-out 3.0s both;
  -webkit-mask-image: linear-gradient(to top, rgba(0,0,0,.55), transparent 72%);
  mask-image: linear-gradient(to top, rgba(0,0,0,.55), transparent 72%); }
@keyframes ar-reflectin { to { opacity: .34; } }
.ar-rbox img { width: 100%; display: block; position: absolute; inset: 0; filter: var(--logo-filter); }
.ar-rbox img:first-child { position: relative; }
.ar-tag { margin: 14px 0 0; font-size: 12px; letter-spacing: 4px; color: var(--muted); text-transform: uppercase;
  animation: ar-fadein .8s ease-out 3.3s both; }
@keyframes ar-fadein { from { opacity: 0; } }
.ar-card { width: 100%; margin-top: 26px; background: var(--card-bg); border: 1px solid var(--card-bd);
  border-radius: 16px; padding: 24px 22px 20px; backdrop-filter: blur(4px); animation: ar-cardin .7s ease-out 3.05s both; }
@keyframes ar-cardin { from { opacity: 0; transform: translateY(18px); } }
.ar-social { display: flex; flex-direction: column; gap: 8px; }
.ar-so { display: flex; align-items: center; justify-content: center; gap: 8px; width: 100%;
  border: none; border-radius: 10px; font-size: 14px; font-weight: 700; padding: 12px 0; cursor: pointer;
  transition: filter .15s; }
.ar-so:hover { filter: brightness(.96); }
.ar-so-ic { font-weight: 800; }
.ar-so-kakao { background: #FEE500; color: #191600; }
.ar-so-google { background: #FFFFFF; color: #3C4043; border: 1px solid #D3D9DF; }
.ar-so-apple { background: #000; color: #fff; }
.ar-or { display: flex; align-items: center; gap: 10px; margin: 14px 0 12px; color: var(--sep); }
.ar-or::before, .ar-or::after { content: ""; flex: 1; height: 1px; background: var(--sep); }
.ar-or span { font-size: 11px; color: var(--muted); }
.ar-field { margin-bottom: 12px; }
.ar-label { display: block; font-size: 11px; letter-spacing: 1.5px; color: var(--label); margin: 0 0 6px 2px; }
.ar-input { width: 100%; background: var(--input-bg); border: 1px solid var(--input-bd); border-radius: 10px;
  color: var(--text); font-size: 15px; padding: 12px 14px; outline: none; }
.ar-input::placeholder { color: var(--ph); }
.ar-input:focus { border-color: var(--focus); box-shadow: 0 0 0 3px var(--focus-ring); }
.ar-btn { width: 100%; margin-top: 6px; background: var(--accent); color: var(--accent-tx); border: none; border-radius: 10px;
  font-size: 15px; font-weight: 800; letter-spacing: 1px; padding: 13px 0; cursor: pointer; }
.th-light .ar-btn { box-shadow: 0 2px 10px rgba(13,169,95,.3); }
.ar-btn:disabled { opacity: .6; cursor: wait; }
.ar-links { margin-top: 16px; display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 12.5px; }
.ar-links a { color: var(--link); text-decoration: none; cursor: pointer; }
.ar-links a:hover { color: var(--link-h); text-decoration: underline; }
.ar-sep { color: var(--sep); }
.ar-msg { margin: 12px 2px 0; font-size: 12.5px; color: var(--link); }
.ar-last { margin-left: 6px; font-size: 10px; font-style: normal; font-weight: 700;
  background: rgba(0,0,0,.14); padding: 2px 7px; border-radius: 999px; vertical-align: 1px; }
.ar-last-inv { background: rgba(255,255,255,.28); }
.ar-ver { position: absolute; bottom: 18px; right: 22px; font-size: 11px; color: var(--muted); font-style: italic; }
.ar-ctrl, .ar-themebtn { position: absolute; top: 16px; background: var(--ctrl-bg); border: 1px solid var(--card-bd);
  color: var(--ctrl-tx); font-size: 12px; border-radius: 8px; padding: 6px 12px; cursor: pointer; }
.ar-ctrl { right: 18px; } .ar-themebtn { left: 18px; }
.ar-done .ar-logobox, .ar-done .ar-l1, .ar-done .ar-l2, .ar-done .ar-l3, .ar-done .ar-l4,
.ar-done .ar-card, .ar-done .ar-tag, .ar-done .ar-rbox { animation: none !important; }
.ar-done .ar-logobox { transform: none; }
.ar-done .ar-l1, .ar-done .ar-l2, .ar-done .ar-l3, .ar-done .ar-l4 { clip-path: inset(0 0 0 0); }
.ar-done .ar-card, .ar-done .ar-tag { opacity: 1; transform: none; }
.th-light.ar-done .ar-rbox { opacity: .34; }
@media (prefers-reduced-motion: reduce) {
  .ar-drop, .ar-logobox, .ar-l1, .ar-l2, .ar-l3, .ar-l4, .ar-card, .ar-tag, .ar-rbox { animation: none !important; }
  .ar-logobox { transform: none; }
  .ar-l1, .ar-l2, .ar-l3, .ar-l4 { clip-path: inset(0 0 0 0); }
  .ar-card, .ar-tag { opacity: 1; } .th-light .ar-rbox { opacity: .34; }
}`;

const DROPS = [
  ["6%",26,9.5,0,.5],["14%",18,12,2.2,.35],["23%",30,8.2,4.1,.45],["31%",16,13.5,1.3,.3],
  ["42%",24,10.4,5.6,.4],["51%",20,11.8,3,.3],["60%",28,9,0.8,.5],["69%",15,14.2,6.4,.28],
  ["77%",25,10,2.9,.42],["85%",19,12.6,5.1,.33],["93%",27,8.8,1.7,.48],
];

function LogoLayers() {
  return (<>
    <img className="ar-l1" src={L.ashrain} alt="ASH RAIN." />
    <img className="ar-layer ar-l2" src={L.out} alt="Out" />
    <img className="ar-layer ar-l3" src={L.stroke} alt="" aria-hidden="true" />
    <img className="ar-layer ar-l4" src={L.ver} alt="2026.07.ver" />
  </>);
}

export default function SplashAuth({ theme = "light", onToggleTheme, onSuccess }) {
  const [id, setId] = useState("");
  const [pw, setPw] = useState("");
  const [msg, setMsg] = useState("");
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);
  const [run, setRun] = useState(0);

  useEffect(() => {
    setDone(false);
    const t = setTimeout(() => setDone(true), 4000);
    return () => clearTimeout(t);
  }, [run]);

  const oauth = async (provider) => {
    setMsg("");
    recordLoginMethod(provider);
    const { error } = await supabase.auth.signInWithOAuth({
      provider,
      options: { redirectTo: window.location.origin },
    });
    if (error) setMsg("소셜 로그인 연결에 실패했어요. 잠시 후 다시 시도해 주세요.");
  };

  const login = async () => {
    if (!id || !pw) { setMsg("아이디와 비밀번호를 입력해 주세요."); return; }
    setBusy(true); setMsg("");
    try {
      // 서버 경유: 아이디→이메일 해석(구계정 가상이메일 + 신계정 실이메일 모두), 레이트리밋 포함
      const r = await api("account", { action: "login", username: id, password: pw });
      const { error } = await supabase.auth.setSession({
        access_token: r.session.access_token,
        refresh_token: r.session.refresh_token,
      });
      if (error) throw new Error(error.message);
      recordLoginMethod("id");
      setBusy(false);
      onSuccess?.(r.session);
    } catch (e1) {
      // 서버 미배포 등 예외 시 구방식 폴백
      const { data, error } = await supabase.auth.signInWithPassword({ email: idToEmail(id), password: pw });
      setBusy(false);
      if (error) { setMsg(e1.message || "로그인에 실패했어요. 아이디/비밀번호를 확인해 주세요."); return; }
      recordLoginMethod("id");
      onSuccess?.(data.session);
    }
  };

  const last = getLastLoginMethod();

  return (
    <div className={`ar-root th-${theme}` + (done ? " ar-done" : "")} key={run}>
      <style>{CSS}</style>
      {DROPS.map(([left, h, d, delay, o], i) => (
        <span key={i} className="ar-drop"
          style={{ left, height: h, opacity: o, "--d": `${d}s`, animationDuration: `${d}s`, animationDelay: `${delay}s` }} />
      ))}
      <button className="ar-themebtn" onClick={onToggleTheme}>{theme === "light" ? "🌙 다크" : "🌧 라이트"}</button>
      <button className="ar-ctrl" onClick={() => (done ? setRun((r) => r + 1) : setDone(true))}>
        {done ? "↻ 인트로 다시보기" : "건너뛰기 »"}
      </button>
      <div className="ar-stage">
        <div className="ar-logobox"><LogoLayers /></div>
        <div className="ar-reflect" aria-hidden="true"><div className="ar-rbox"><LogoLayers /></div></div>
        <p className="ar-tag">MATH · EVERY DAY</p>
        <div className="ar-card">
          <div className="ar-social">
            <button className="ar-so ar-so-kakao" onClick={() => oauth("kakao")}>
              <span className="ar-so-ic">💬</span> 카카오로 시작하기{last === "kakao" && <em className="ar-last">최근</em>}
            </button>
            <button className="ar-so ar-so-google" onClick={() => oauth("google")}>
              <span className="ar-so-ic">G</span> Google로 시작하기{last === "google" && <em className="ar-last">최근</em>}
            </button>
            {/* 애플 로그인: Apple 개발자 계정 + Supabase Provider 설정 후 아래 주석 해제
            <button className="ar-so ar-so-apple" onClick={() => oauth("apple")}>
              <span className="ar-so-ic"></span> Apple로 시작하기
            </button> */}
          </div>
          <div className="ar-or"><span>또는 이메일로</span></div>
          <div className="ar-field">
            <label className="ar-label" htmlFor="ar-id">아이디</label>
            <input id="ar-id" className="ar-input" placeholder="아이디" value={id} onChange={(e) => setId(e.target.value)} />
          </div>
          <div className="ar-field">
            <label className="ar-label" htmlFor="ar-pw">PASSWORD</label>
            <input id="ar-pw" className="ar-input" type="password" placeholder="비밀번호" value={pw}
              onChange={(e) => setPw(e.target.value)} onKeyDown={(e) => e.key === "Enter" && login()} />
          </div>
          <button className="ar-btn" onClick={login} disabled={busy}>{busy ? "확인 중..." : "로그인"}{!busy && last === "id" && <em className="ar-last ar-last-inv">최근</em>}</button>
          {msg && <p className="ar-msg">{msg}</p>}
          <div className="ar-links">
            <a href="#/signup">회원가입</a><span className="ar-sep">|</span>
            <a href="#/find">아이디·비번 찾기</a><span className="ar-sep">|</span>
            <a href="#/trial">무료체험</a><span className="ar-sep">|</span>
            <a href="#/qr">QR 로그인</a>
          </div>
        </div>
      </div>
      <span className="ar-ver">2026.07.ver</span>
    </div>
  );
}
