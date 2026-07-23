import { useEffect, useState, useRef } from "react";
import { supabase } from "../supabaseClient";
import SecurityCard from "./SecurityCard";
import PointsCard from "./PointsCard";
import { fmtCode } from "../lib/authx";

const GRADES = ["초3","초4","초5","초6","중1","중2","중3","기타"];
const THIS_YEAR = new Date().getFullYear();
const YEARS = Array.from({ length: 20 }, (_, i) => THIS_YEAR - 8 - i);

const CSS = `
.mp-root { min-height: 100vh; padding: 20px 14px 40px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.mp-root * { box-sizing: border-box; }
.mp-light { background:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0DA95F; --in:#F4F6F8; --inbd:#D3D9DF; }
.mp-dark  { background:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#FFE03C; --in:#101116; --inbd:#2B2E36; }
.mp-wrap { max-width: 460px; margin: 0 auto; }
.mp-h { color: var(--ink); font-size: 19px; margin: 0 0 14px; }
.mp-card { background: var(--card); border: 1px solid var(--bd); border-radius: 16px; padding: 18px 20px; margin-bottom: 12px; }
.mp-sec { font-size: 11px; letter-spacing: 1.5px; color: var(--mut); font-weight: 700; margin: 0 0 10px; }
.mp-ava { display: flex; align-items: center; gap: 14px; }
.mp-ava img, .mp-ava-ph { width: 64px; height: 64px; border-radius: 9999px; object-fit: cover;
  background: var(--in); border: 1px solid var(--inbd); display: flex; align-items: center; justify-content: center;
  font-size: 24px; color: var(--mut); }
.mp-ava-btns { display: flex; flex-direction: column; gap: 6px; }
.mp-mini { background: var(--in); border: 1px solid var(--inbd); border-radius: 8px; color: var(--mut);
  font-size: 12px; padding: 7px 12px; cursor: pointer; text-align: center; text-decoration: none; }
.mp-in, .mp-sel { width: 100%; background: var(--in); border: 1px solid var(--inbd); border-radius: 10px;
  color: var(--ink); font-size: 14.5px; padding: 11px 13px; outline: none; margin-bottom: 8px; }
.mp-in:focus, .mp-sel:focus { border-color: var(--ac); }
.mp-in:disabled { opacity: .6; }
.mp-row { display: flex; gap: 8px; } .mp-row > * { flex: 1; }
.mp-seg { display: flex; gap: 6px; margin-bottom: 8px; }
.mp-seg button { flex: 1; background: var(--in); border: 1px solid var(--inbd); border-radius: 10px;
  color: var(--mut); font-size: 13px; padding: 10px 0; cursor: pointer; }
.mp-seg button.on { border-color: var(--ac); color: var(--ink); font-weight: 700; }
.mp-btn { width: 100%; background: var(--ac); border: none; border-radius: 10px; font-size: 14.5px;
  font-weight: 800; padding: 12px 0; cursor: pointer; }
.mp-light .mp-btn { color: #fff; } .mp-dark .mp-btn { color: #14140F; }
.mp-out { width: 100%; background: transparent; border: 1px solid var(--bd); border-radius: 10px;
  color: var(--mut); font-size: 14px; font-weight: 700; padding: 12px 0; cursor: pointer; }
.mp-out:hover { color: #DC2626; border-color: #DC2626; }
.mp-msg { font-size: 12.5px; color: var(--ac); margin: 8px 2px 0; }
.mp-err { color: #DC2626; }
.mp-back { color: var(--mut); font-size: 12.5px; cursor: pointer; text-decoration: underline; }
.mp-tgl { display: flex; align-items: center; justify-content: space-between; padding: 10px 2px; }
.mp-tgl span { color: var(--ink); font-size: 14px; }
.mp-tgl small { display: block; color: var(--mut); font-size: 11.5px; margin-top: 2px; }
.mp-sw { position: relative; width: 44px; height: 24px; border-radius: 9999px; border: none; cursor: pointer;
  background: var(--inbd); transition: background .15s; flex-shrink: 0; }
.mp-sw.on { background: var(--ac); }
.mp-sw::after { content: ""; position: absolute; top: 3px; left: 3px; width: 18px; height: 18px;
  border-radius: 9999px; background: #fff; transition: left .15s; }
.mp-sw.on::after { left: 23px; }
`;

function Toggle({ on, onChange }) {
  return <button className={"mp-sw" + (on ? " on" : "")} onClick={() => onChange(!on)} aria-pressed={on} />;
}

export default function MyPage({ theme, onToggleTheme }) {
  const [p, setP] = useState(null);
  const [pw, setPw] = useState(""); const [pw2, setPw2] = useState("");
  const [msg, setMsg] = useState(""); const [err, setErr] = useState("");
  const [pwMsg, setPwMsg] = useState("");
  const fileRef = useRef(null);
  const set = (k) => (e) => setP((s) => ({ ...s, [k]: e.target.value }));

  useEffect(() => {
    supabase.auth.getUser().then(async ({ data }) => {
      if (!data.user) return;
      const { data: prof } = await supabase.from("profiles").select("*").eq("id", data.user.id).single();
      setP(prof ? { ...prof, settings: prof.settings || {} } : prof);
    });
  }, []);

  const save = async () => {
    setMsg(""); setErr("");
    const { error } = await supabase.from("profiles").update({
      name: p.name, grade: p.grade, school: p.school,
      gender: p.gender || null, birth_year: p.birth_year || null,
    }).eq("id", p.id);
    error ? setErr("저장 실패: " + error.message) : setMsg("✓ 저장했어요.");
  };

  const setSetting = async (key, value) => {
    const settings = { ...p.settings, [key]: value };
    setP((s) => ({ ...s, settings }));
    await supabase.from("profiles").update({ settings }).eq("id", p.id);
  };

  const changePw = async () => {
    setPwMsg("");
    if (pw.length < 6) { setPwMsg("비밀번호는 6자 이상이어야 해요."); return; }
    if (pw !== pw2) { setPwMsg("비밀번호가 서로 달라요."); return; }
    const { error } = await supabase.auth.updateUser({ password: pw });
    setPwMsg(error ? "변경 실패: " + error.message : "✓ 비밀번호를 바꿨어요.");
    if (!error) { setPw(""); setPw2(""); }
  };

  const pickPhoto = async (e) => {
    const f = e.target.files?.[0];
    if (!f || !p) return;
    const { error } = await supabase.storage.from("avatars").upload(`${p.id}/profile.png`, f, { upsert: true });
    if (error) { setErr("사진 업로드에 실패했어요."); return; }
    const { data: pub } = supabase.storage.from("avatars").getPublicUrl(`${p.id}/profile.png`);
    const url = pub.publicUrl + "?t=" + Date.now();
    await supabase.from("profiles").update({ avatar_url: url }).eq("id", p.id);
    setP((s) => ({ ...s, avatar_url: url }));
  };

  if (!p) return <div className={`mp-root mp-${theme}`}><style>{CSS}</style></div>;
  const st = p.settings;

  return (
    <div className={`mp-root mp-${theme}`}>
      <style>{CSS}</style>
      <div className="mp-wrap">
        <h1 className="mp-h">마이페이지 <span className="mp-back" style={{ float: "right", fontWeight: 400 }} onClick={() => (location.hash = "")}>← 홈</span></h1>

        <div className="mp-card">
          <p className="mp-sec">프로필</p>
          <div className="mp-ava">
            {p.avatar_url ? <img src={p.avatar_url} alt="프로필" /> : <span className="mp-ava-ph">👤</span>}
            <div className="mp-ava-btns">
              <button className="mp-mini" onClick={() => fileRef.current?.click()}>사진 바꾸기</button>
              <a className="mp-mini" href="#/portrait">🖼 초상화 필터로 만들기</a>
            </div>
            <input ref={fileRef} type="file" accept="image/*" style={{ display: "none" }} onChange={pickPhoto} />
          </div>
        </div>

        <div className="mp-card">
          <p className="mp-sec">내 정보</p>
          <input className="mp-in" value={p.username || ""} disabled placeholder="아이디" />
          {p.phone && <input className="mp-in" value={p.phone.replace(/(\d{3})(\d{3,4})(\d{4})/, "$1-$2-$3")} disabled placeholder="전화번호" />}
          {p.real_email && <input className="mp-in" value={p.real_email} disabled placeholder="이메일" />}
          {p.member_code && <input className="mp-in" value={"고유번호 " + fmtCode(p.member_code)} disabled />}
          <div className="mp-row">
            <input className="mp-in" value={p.name || ""} onChange={set("name")} placeholder="이름" />
            <select className="mp-sel" value={p.grade || ""} onChange={set("grade")}>
              <option value="">학년</option>
              {GRADES.map((g) => <option key={g} value={g}>{g}</option>)}
            </select>
          </div>
          <div className="mp-seg">
            {[["", "선택 안 함"], ["male", "남"], ["female", "여"]].map(([v, l]) => (
              <button key={v} className={(p.gender || "") === v ? "on" : ""} onClick={() => setP((s) => ({ ...s, gender: v }))}>{l}</button>
            ))}
          </div>
          <div className="mp-row">
            <select className="mp-sel" value={p.birth_year || ""} onChange={set("birth_year")}>
              <option value="">출생년도</option>
              {YEARS.map((y) => <option key={y} value={y}>{y}년</option>)}
            </select>
            <input className="mp-in" value={p.school || ""} onChange={set("school")} placeholder="학교" />
          </div>
          <button className="mp-btn" onClick={save}>저장</button>
          {msg && <p className="mp-msg">{msg}</p>}
          {err && <p className="mp-msg mp-err">{err}</p>}
        </div>

        <div className="mp-card">
          <p className="mp-sec">환경설정</p>
          <div className="mp-tgl">
            <span>다크 테마<small>재의 밤 · 검정 바탕에 노란 손글씨</small></span>
            <Toggle on={theme === "dark"} onChange={() => onToggleTheme?.()} />
          </div>
          <div className="mp-tgl">
            <span>알림 받기<small>숙제·답변 알림 (기능 준비 중)</small></span>
            <Toggle on={st.notify !== false} onChange={(v) => setSetting("notify", v)} />
          </div>
          <div className="mp-tgl">
            <span>효과음<small>정답·오답 사운드 (기능 준비 중)</small></span>
            <Toggle on={st.sound !== false} onChange={(v) => setSetting("sound", v)} />
          </div>
        </div>

        <PointsCard />

        <SecurityCard profile={p} />

        <div className="mp-card">
          <p className="mp-sec">계정</p>
          <div className="mp-row">
            <input className="mp-in" type="password" placeholder="새 비밀번호" value={pw} onChange={(e) => setPw(e.target.value)} />
            <input className="mp-in" type="password" placeholder="한 번 더" value={pw2} onChange={(e) => setPw2(e.target.value)} />
          </div>
          <button className="mp-btn" onClick={changePw}>비밀번호 바꾸기</button>
          {pwMsg && <p className={"mp-msg" + (pwMsg.startsWith("✓") ? "" : " mp-err")}>{pwMsg}</p>}
        </div>

        <button className="mp-out" onClick={async () => { await supabase.auth.signOut(); location.hash = ""; }}>로그아웃</button>
      </div>
    </div>
  );
}
