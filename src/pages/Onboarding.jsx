// src/pages/Onboarding.jsx — 소셜(구글/카카오) 첫 로그인 후 정보 완성 (해시 라우트: #/onboarding)
import { useEffect, useState } from 'react';
import {
  supabase, api, otpSend, otpVerify,
  normPhone, quickCheckCode, normCode, codeRoleType,
} from '../lib/authx';

export default function Onboarding() {
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const [ready, setReady] = useState(false);

  const [code, setCode] = useState('');
  const [nickname, setNickname] = useState('');
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [phoneToken, setPhoneToken] = useState('');
  const [done, setDone] = useState(false);
  const [merge, setMerge] = useState(null);       // 409 응답
  const [mergeSent, setMergeSent] = useState(false);

  useEffect(() => {
    (async () => {
      const { data } = await supabase.auth.getSession();
      if (!data?.session) { window.location.hash = '#/login'; return; }
      setReady(true);
    })();
  }, []);

  const run = async (fn) => {
    setErr(''); setBusy(true);
    try { await fn(); } catch (e) { setErr(e.message || String(e)); }
    setBusy(false);
  };

  const sendOtp = () => run(async () => {
    const p = normPhone(phone);
    if (!p) throw new Error('휴대폰 번호를 확인해주세요');
    await otpSend(p, 'social');
    setOtpSent(true);
  });

  const verify = () => run(async () => {
    const p = normPhone(phone);
    const r = await otpVerify(p, 'social', otp);
    setPhoneToken(r.phone_token);
  });

  const submit = () => run(async () => {
    if (!phoneToken) throw new Error('전화번호 인증을 먼저 완료해주세요');
    if (!quickCheckCode(code)) throw new Error('고유번호를 다시 확인해주세요');
    if (codeRoleType(code) === 9) throw new Error('체험 코드는 사용할 수 없어요. 학원에서 받은 정식 코드를 입력해주세요.');
    try {
      await api('account', {
        action: 'social-complete',
        phone_token: phoneToken,
        member_code: normCode(code),
        nickname: nickname || undefined,
      }, { auth: true });
      setDone(true);
      setTimeout(() => { window.location.hash = '#/'; }, 1200);
    } catch (e) {
      if (e.status === 409 && e.data?.merge_required) { setMerge(e.data); return; }
      throw e;
    }
  });

  const requestMerge = () => run(async () => {
    await api('account', { action: 'merge-request', phone_token: phoneToken }, { auth: true });
    setMergeSent(true);
  });

  if (!ready) return null;

  if (merge) {
    return (
      <div className="ob-wrap"><Style />
        <h2 className="ob-title">계정 통합이 필요해요</h2>
        {mergeSent ? (
          <div className="ob-card">
            <p className="ob-desc">통합 신청이 접수됐어요. 학원 선생님이 확인하면 기존 계정(<b>{merge.existing?.username}</b>)의
              오답노트·즐겨찾기가 이 계정으로 옮겨져요. 처리까지 시간이 걸릴 수 있어요.</p>
            <a className="ob-btn ob-btn-main" href="#/">홈으로</a>
          </div>
        ) : (
          <div className="ob-card">
            <p className="ob-desc">이 전화번호로 이미 가입된 계정(<b>{merge.existing?.username}</b>)이 있어요.
              규칙상 두 계정은 하나로 통합한 뒤 이용할 수 있어요.</p>
            <button className="ob-btn ob-btn-main" disabled={busy} onClick={requestMerge}>이 계정으로 통합 신청하기</button>
            <a className="ob-btn" href="#/find">기존 계정으로 로그인할래요</a>
          </div>
        )}
        {err && <p className="ob-err">{err}</p>}
      </div>
    );
  }

  return (
    <div className="ob-wrap"><Style />
      <h2 className="ob-title">환영해요! 정보를 완성해주세요</h2>
      <p className="ob-desc">소셜 로그인은 완료됐어요. 학원 고유번호와 전화번호 인증만 하면 바로 시작할 수 있어요.</p>

      <div className="ob-card">
        <label className="ob-label">학원에서 받은 고유번호</label>
        <input className="ob-input ob-code" value={code} onChange={(e) => setCode(e.target.value)}
          placeholder="ASH37-1A2B3CD-4E5" autoCapitalize="characters" />

        <label className="ob-label">닉네임 (선택)</label>
        <input className="ob-input" value={nickname} onChange={(e) => setNickname(e.target.value)} />

        <label className="ob-label">휴대폰 번호</label>
        <div className="ob-row">
          <input className="ob-input" inputMode="numeric" value={phone}
            onChange={(e) => setPhone(e.target.value)} placeholder="01012345678" disabled={otpSent} />
          <button className="ob-btn" disabled={busy} onClick={sendOtp}>{otpSent ? '재발송' : '인증번호 발송'}</button>
        </div>
        {otpSent && !phoneToken && (
          <div className="ob-row">
            <input className="ob-input" inputMode="numeric" maxLength={6} value={otp}
              onChange={(e) => setOtp(e.target.value)} placeholder="인증번호 6자리" />
            <button className="ob-btn" disabled={busy} onClick={verify}>확인</button>
          </div>
        )}
        {phoneToken && <p className="ob-ok">전화번호 인증 완료</p>}

        <button className="ob-btn ob-btn-main" disabled={busy || done} onClick={submit}>
          {done ? '완료! 이동 중…' : '시작하기'}
        </button>
      </div>

      {err && <p className="ob-err">{err}</p>}
    </div>
  );
}

function Style() {
  return (
    <style>{`
      .ob-wrap{max-width:420px;margin:0 auto;padding:20px 16px 48px;color:var(--text,#1c1c1e)}
      .ob-title{margin:4px 0 8px;font-size:22px}
      .ob-desc{font-size:14px;line-height:1.6;color:var(--muted,#4b5563);margin:0 0 12px}
      .ob-card{background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:8px}
      .ob-label{font-size:13px;color:var(--muted,#6b7280);margin-top:6px}
      .ob-input{width:100%;box-sizing:border-box;padding:12px;border:1px solid var(--border,#d6d9de);border-radius:10px;font-size:16px;background:var(--surface,#fff);color:inherit}
      .ob-code{letter-spacing:1px}
      .ob-row{display:flex;gap:8px}
      .ob-row .ob-input{flex:1}
      .ob-btn{padding:12px 14px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);font-size:15px;text-align:center;text-decoration:none;color:inherit;white-space:nowrap}
      .ob-btn-main{background:var(--accent,#3b82f6);border-color:var(--accent,#3b82f6);color:#fff;margin-top:8px}
      .ob-btn:disabled{opacity:.5}
      .ob-ok{font-size:12px;color:var(--good,#16a34a);margin:0}
      .ob-err{font-size:13px;color:var(--bad,#dc2626);margin-top:10px;text-align:center}
    `}</style>
  );
}
