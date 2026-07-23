// src/pages/StaffJoin.jsx — 스태프 가입 (비공개 해시 라우트: #/staff-join)
// 원장님이 발급한 초대코드가 있어야만 진행됩니다.
import { useState } from 'react';
import {
  supabase, api, otpSend, otpVerify, normPhone, recordLoginMethod, PW_MIN,
} from '../lib/authx';

export default function StaffJoin() {
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const [done, setDone] = useState(false);

  const [invite, setInvite] = useState('');
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [phoneToken, setPhoneToken] = useState('');

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');
  const [nickname, setNickname] = useState('');
  const [email, setEmail] = useState('');

  const run = async (fn) => {
    setErr(''); setBusy(true);
    try { await fn(); } catch (e) { setErr(e.message || String(e)); }
    setBusy(false);
  };

  const sendOtp = () => run(async () => {
    const p = normPhone(phone);
    if (!p) throw new Error('휴대폰 번호를 확인해주세요');
    await otpSend(p, 'signup');
    setOtpSent(true);
  });

  const verify = () => run(async () => {
    const p = normPhone(phone);
    const r = await otpVerify(p, 'signup', otp);
    setPhoneToken(r.phone_token);
  });

  const submit = () => run(async () => {
    if (!invite.trim()) throw new Error('초대코드를 입력해주세요');
    if (!phoneToken) throw new Error('전화번호 인증을 완료해주세요');
    if (password.length < PW_MIN) throw new Error(`비밀번호는 ${PW_MIN}자 이상이어야 합니다`);
    if (password !== password2) throw new Error('비밀번호 확인이 일치하지 않습니다');

    const r = await api('account', {
      action: 'staff-join',
      invite_code: invite.trim(),
      phone_token: phoneToken,
      username: username.toLowerCase(),
      password,
      nickname: nickname || undefined,
      email,
    });

    if (r.session) {
      await supabase.auth.setSession({
        access_token: r.session.access_token,
        refresh_token: r.session.refresh_token,
      });
      recordLoginMethod('id');
      setDone(true);
      setTimeout(() => { window.location.hash = '#/'; }, 1000);
    } else {
      setDone(true);
    }
  });

  return (
    <div className="sj-wrap"><Style />
      <h2 className="sj-title">스태프 가입</h2>
      <p className="sj-desc">초대코드를 받은 선생님·조교만 가입할 수 있어요.</p>

      {done ? (
        <div className="sj-card">
          <p className="sj-desc">가입이 완료됐어요. 홈으로 이동해요.</p>
          <a className="sj-btn sj-btn-main" href="#/">홈으로</a>
        </div>
      ) : (
        <div className="sj-card">
          <label className="sj-label">초대코드</label>
          <input className="sj-input" value={invite} onChange={(e) => setInvite(e.target.value)} autoCapitalize="none" />

          <label className="sj-label">휴대폰 번호</label>
          <div className="sj-row">
            <input className="sj-input" inputMode="numeric" value={phone}
              onChange={(e) => setPhone(e.target.value)} placeholder="01012345678" disabled={otpSent} />
            <button className="sj-btn" disabled={busy} onClick={sendOtp}>{otpSent ? '재발송' : '인증번호 발송'}</button>
          </div>
          {otpSent && !phoneToken && (
            <div className="sj-row">
              <input className="sj-input" inputMode="numeric" maxLength={6} value={otp}
                onChange={(e) => setOtp(e.target.value)} placeholder="인증번호 6자리" />
              <button className="sj-btn" disabled={busy} onClick={verify}>확인</button>
            </div>
          )}
          {phoneToken && <p className="sj-ok">전화번호 인증 완료</p>}

          <label className="sj-label">아이디</label>
          <input className="sj-input" value={username} onChange={(e) => setUsername(e.target.value)}
            placeholder="영문 소문자/숫자 4~20자" autoCapitalize="none" />
          <label className="sj-label">비밀번호 (8자 이상)</label>
          <input className="sj-input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <label className="sj-label">비밀번호 확인</label>
          <input className="sj-input" type="password" value={password2} onChange={(e) => setPassword2(e.target.value)} />
          <label className="sj-label">닉네임 (선택)</label>
          <input className="sj-input" value={nickname} onChange={(e) => setNickname(e.target.value)} />
          <label className="sj-label">이메일</label>
          <input className="sj-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} autoCapitalize="none" />

          <button className="sj-btn sj-btn-main" disabled={busy} onClick={submit}>가입하기</button>
        </div>
      )}

      {err && <p className="sj-err">{err}</p>}
    </div>
  );
}

function Style() {
  return (
    <style>{`
      .sj-wrap{max-width:420px;margin:0 auto;padding:20px 16px 48px;color:var(--text,#1c1c1e)}
      .sj-title{margin:4px 0 6px;font-size:22px}
      .sj-desc{font-size:14px;line-height:1.6;color:var(--muted,#4b5563);margin:0 0 12px}
      .sj-card{background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:8px}
      .sj-label{font-size:13px;color:var(--muted,#6b7280);margin-top:6px}
      .sj-input{width:100%;box-sizing:border-box;padding:12px;border:1px solid var(--border,#d6d9de);border-radius:10px;font-size:16px;background:var(--surface,#fff);color:inherit}
      .sj-row{display:flex;gap:8px}
      .sj-row .sj-input{flex:1}
      .sj-btn{padding:12px 14px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);font-size:15px;text-align:center;text-decoration:none;color:inherit;white-space:nowrap}
      .sj-btn-main{background:var(--accent,#3b82f6);border-color:var(--accent,#3b82f6);color:#fff;margin-top:8px}
      .sj-btn:disabled{opacity:.5}
      .sj-ok{font-size:12px;color:var(--good,#16a34a);margin:0}
      .sj-err{font-size:13px;color:var(--bad,#dc2626);margin-top:10px;text-align:center}
    `}</style>
  );
}
