import { useState, useRef } from "react";
import { supabase } from "../supabaseClient";
import { idToEmail, ID_RULE } from "../lib/auth";

const GRADES = ["초3","초4","초5","초6","중1","중2","중3","기타"];
const THIS_YEAR = new Date().getFullYear();
const YEARS = Array.from({ length: 20 }, (_, i) => THIS_YEAR - 8 - i); // 8세~27세 범위

const CSS = `
.sg-root { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 24px 16px;
  box-sizing: border-box; font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.sg-root * { box-sizing: border-box; }
.sg-light { background: #EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0DA95F; --in:#F4F6F8; --inbd:#D3D9DF; }
.sg-dark  { background: #0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#FFE03C; --in:#101116; --inbd:#2B2E36; }
.sg-card { width: 100%; max-width: 400px; background: var(--card); border: 1px solid var(--bd);
  border-radius: 16px; padding: 24px 22px; }
.sg-h { margin: 0 0 2px; color: var(--ink); font-size: 19px; }
.sg-cap { margin: 0 0 14px; color: var(--mut); font-size: 12px; }
.sg-sec { font-size: 11px; letter-spacing: 1.5px; color: var(--mut); font-weight: 700; margin: 16px 0 8px; }
.sg-in, .sg-sel { width: 100%; background: var(--in); border: 1px solid var(--inbd); border-radius: 10px;
  color: var(--ink); font-size: 14.5px; padding: 11px 13px; outline: none; margin-bottom: 8px; }
.sg-in:focus, .sg-sel:focus { border-color: var(--ac); }
.sg-row { display: flex; gap: 8px; } .sg-row > * { flex: 1; }
.sg-seg { display: flex; gap: 6px; margin-bottom: 8px; }
.sg-seg button { flex: 1; background: var(--in); border: 1px solid var(--inbd); border-radius: 10px;
  color: var(--mut); font-size: 13px; padding: 10px 0; cursor: pointer; }
.sg-seg button.on { border-color: var(--ac); color: var(--ink); font-weight: 700; }
.sg-photo { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }
.sg-ph-prev { width: 48px; height: 48px; border-radius: 9999px; background: var(--in); border: 1px solid var(--inbd);
  object-fit: cover; display: flex; align-items: center; justify-content: center; color: var(--mut); font-size: 18px; }
.sg-ph-btn { background: var(--in); border: 1px solid var(--inbd); border-radius: 8px; color: var(--mut);
  font-size: 12.5px; padding: 8px 12px; cursor: pointer; }
.sg-btn { width: 100%; margin-top: 14px; background: var(--ac); border: none; border-radius: 10px; font-size: 15px;
  font-weight: 800; padding: 13px 0; cursor: pointer; }
.sg-light .sg-btn { color: #fff; } .sg-dark .sg-btn { color: #14140F; }
.sg-btn:disabled { opacity: .6; }
.sg-msg { font-size: 12.5px; color: var(--mut); margin: 10px 2px 0; line-height: 1.6; white-space: pre-wrap; }
.sg-err { color: #DC2626; }
.sg-back { display: inline-block; margin-top: 14px; font-size: 12.5px; color: var(--mut); cursor: pointer; text-decoration: underline; }
`;

export default function Signup({ theme }) {
  const [f, setF] = useState({ id: "", pw: "", pw2: "", name: "", grade: "", gender: "", birthYear: "", school: "" });
  const [photo, setPhoto] = useState(null);       // File
  const [photoUrl, setPhotoUrl] = useState(null); // 미리보기
  const [msg, setMsg] = useState(""); const [err, setErr] = useState(""); const [busy, setBusy] = useState(false);
  const fileRef = useRef(null);
  const set = (k) => (e) => setF((s) => ({ ...s, [k]: e.target.value }));

  const pickPhoto = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setPhoto(file); setPhotoUrl(URL.createObjectURL(file));
  };

  const submit = async () => {
    setErr(""); setMsg("");
    const id = f.id.trim().toLowerCase();
    if (!ID_RULE.test(id)) { setErr("아이디는 영문 소문자·숫자·_ 4~16자예요."); return; }
    if (f.pw.length < 6) { setErr("비밀번호는 6자 이상이어야 해요."); return; }
    if (f.pw !== f.pw2) { setErr("비밀번호가 서로 달라요."); return; }
    if (!f.name.trim()) { setErr("이름을 입력해 주세요."); return; }
    if (!f.grade) { setErr("학년을 선택해 주세요."); return; }

    setBusy(true);
    const { data, error } = await supabase.auth.signUp({
      email: idToEmail(id), password: f.pw,
      options: { data: { username: id, name: f.name.trim(), grade: f.grade,
        gender: f.gender || "", birth_year: f.birthYear || "", school: f.school.trim() || "" } },
    });
    if (error) {
      setBusy(false);
      setErr(error.message.includes("already registered") ? "이미 사용 중인 아이디예요." : "가입 실패: " + error.message);
      return;
    }
    // 프로필 사진 (선택): 세션이 있으면 즉시 업로드
    if (photo && data.session) {
      const uid = data.user.id;
      const { error: upErr } = await supabase.storage.from("avatars")
        .upload(`${uid}/profile.png`, photo, { upsert: true });
      if (!upErr) {
        const { data: pub } = supabase.storage.from("avatars").getPublicUrl(`${uid}/profile.png`);
        await supabase.from("profiles").update({ avatar_url: pub.publicUrl }).eq("id", uid);
      }
    }
    setBusy(false);
    setMsg("가입 완료! 이제 아이디로 로그인할 수 있어요." + (photo && !data.session ? "\n(프로필 사진은 로그인 후 다시 설정해 주세요)" : ""));
  };

  return (
    <div className={`sg-root sg-${theme}`}>
      <style>{CSS}</style>
      <div className="sg-card">
        <h1 className="sg-h">회원가입</h1>
        <p className="sg-cap">* 표시는 필수예요</p>

        <p className="sg-sec">계정 *</p>
        <input className="sg-in" placeholder="아이디 (영문 소문자·숫자 4~16자)" value={f.id} onChange={set("id")} />
        <div className="sg-row">
          <input className="sg-in" type="password" placeholder="비밀번호 (6자 이상)" value={f.pw} onChange={set("pw")} />
          <input className="sg-in" type="password" placeholder="비밀번호 확인" value={f.pw2} onChange={set("pw2")} />
        </div>

        <p className="sg-sec">기본 정보 *</p>
        <div className="sg-row">
          <input className="sg-in" placeholder="이름" value={f.name} onChange={set("name")} />
          <select className="sg-sel" value={f.grade} onChange={set("grade")}>
            <option value="">학년 선택</option>
            {GRADES.map((g) => <option key={g} value={g}>{g}</option>)}
          </select>
        </div>

        <p className="sg-sec">선택 정보</p>
        <div className="sg-seg">
          {[["", "선택 안 함"], ["male", "남"], ["female", "여"]].map(([v, l]) => (
            <button key={v} className={f.gender === v ? "on" : ""} onClick={() => setF((s) => ({ ...s, gender: v }))}>{l}</button>
          ))}
        </div>
        <div className="sg-row">
          <select className="sg-sel" value={f.birthYear} onChange={set("birthYear")}>
            <option value="">출생년도</option>
            {YEARS.map((y) => <option key={y} value={y}>{y}년</option>)}
          </select>
          <input className="sg-in" placeholder="학교 (예: 백석중)" value={f.school} onChange={set("school")} />
        </div>
        <div className="sg-photo">
          {photoUrl ? <img className="sg-ph-prev" src={photoUrl} alt="미리보기" /> : <span className="sg-ph-prev">📷</span>}
          <button className="sg-ph-btn" onClick={() => fileRef.current?.click()}>{photo ? "사진 바꾸기" : "프로필 사진 올리기"}</button>
          <input ref={fileRef} type="file" accept="image/*" style={{ display: "none" }} onChange={pickPhoto} />
        </div>

        <button className="sg-btn" onClick={submit} disabled={busy}>{busy ? "가입 중..." : "가입하기"}</button>
        {err && <p className="sg-msg sg-err">{err}</p>}
        {msg && <p className="sg-msg">{msg}</p>}
        <span className="sg-back" onClick={() => (location.hash = "")}>← 로그인으로 돌아가기</span>
      </div>
    </div>
  );
}
