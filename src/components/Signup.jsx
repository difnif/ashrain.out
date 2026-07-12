import { useState } from "react";
import { supabase } from "../supabaseClient";

const CSS = `
.sg-root { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 24px 16px;
  box-sizing: border-box; font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.sg-light { background: #EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0DA95F; --in:#F4F6F8; --inbd:#D3D9DF; }
.sg-dark  { background: #0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#FFE03C; --in:#101116; --inbd:#2B2E36; }
.sg-card { width: 100%; max-width: 380px; background: var(--card); border: 1px solid var(--bd);
  border-radius: 16px; padding: 24px 22px; }
.sg-h { margin: 0 0 14px; color: var(--ink); font-size: 19px; }
.sg-in { width: 100%; box-sizing: border-box; background: var(--in); border: 1px solid var(--inbd); border-radius: 10px;
  color: var(--ink); font-size: 15px; padding: 12px 14px; outline: none; margin-bottom: 10px; }
.sg-btn { width: 100%; background: var(--ac); border: none; border-radius: 10px; font-size: 15px;
  font-weight: 800; padding: 13px 0; cursor: pointer; }
.sg-light .sg-btn { color: #fff; } .sg-dark .sg-btn { color: #14140F; }
.sg-msg { font-size: 12.5px; color: var(--mut); margin: 10px 2px 0; line-height: 1.6; }
.sg-back { display: inline-block; margin-top: 14px; font-size: 12.5px; color: var(--mut); cursor: pointer; text-decoration: underline; }
`;

export default function Signup({ theme }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");
  const [msg, setMsg] = useState("");
  const [busy, setBusy] = useState(false);

  const submit = async () => {
    if (!name || !email || pw.length < 6) { setMsg("이름, 이메일, 6자 이상 비밀번호를 입력해 주세요."); return; }
    setBusy(true);
    const { error } = await supabase.auth.signUp({ email, password: pw, options: { data: { name } } });
    setBusy(false);
    setMsg(error ? "가입에 실패했어요: " + error.message
      : "가입 완료! (이메일 확인이 켜져 있으면 메일함을 확인해 주세요) 로그인 화면으로 돌아가 로그인하세요.");
  };

  return (
    <div className={`sg-root sg-${theme}`}>
      <style>{CSS}</style>
      <div className="sg-card">
        <h1 className="sg-h">회원가입</h1>
        <input className="sg-in" placeholder="이름" value={name} onChange={(e) => setName(e.target.value)} />
        <input className="sg-in" placeholder="이메일" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="sg-in" type="password" placeholder="비밀번호 (6자 이상)" value={pw} onChange={(e) => setPw(e.target.value)} />
        <button className="sg-btn" onClick={submit} disabled={busy}>{busy ? "가입 중..." : "가입하기"}</button>
        {msg && <p className="sg-msg">{msg}</p>}
        <span className="sg-back" onClick={() => (location.hash = "")}>← 로그인으로 돌아가기</span>
      </div>
    </div>
  );
}
