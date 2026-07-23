// src/pages/FindAccount.jsx — 아이디 찾기 / 비밀번호 재설정 (해시 라우트: #/find)
import { useEffect, useState } from 'react';
import {
  supabase, api, otpSend, otpVerify, normPhone, PW_MIN,
} from '../lib/authx';

const PROVIDER_LABEL = { google: '구글', kakao: '카카오', email: '아이디' };

export default function FindAccount() {
  const [tab, setTab] = useState('id');        // 'id' | 'pw'
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');

  // 공통 전화 인증
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [phoneToken, setPhoneToken] = useState('');

  // 아이디 찾기 결과
  const [accounts, setAccounts] = useState(null);

  // 비번 재설정
  const [username, setUsername] = useState('');
  const [newPw, setNewPw] = useState('');
  const [newPw2, setNewPw2] = useState('');
  const [pwDone, setPwDone] = useState(false);

  // 이메일 재설정 링크로 되돌아온 경우 (recovery 세션)
  const [recovery, setRecovery] = useState(false);
  useEffect(() => {
    const { data: sub } = supabase.auth.onAuthStateChange((event) => {
      if (event === 'PASSWORD_RECOVERY') setRecovery(true);
    });
    return () => sub.subscription.unsubscribe();
  }, []);

  const purpose = tab === 'id' ? 'find' : 'reset';
  const resetOtp = () => { setOtp(''); setOtpSent(false); setPhoneToken(''); setAccounts(null); };

  const run = async (fn) => {
    setErr(''); setBusy(true);
    try { await fn(); } catch (e) { setErr(e.message || String(e)); }
    setBusy(false);
  };

  const sendOtp = () => run(async () => {
    const p = normPhone(phone);
    if (!p) throw new Error('휴대폰 번호를 확인해주세요');
    await otpSend(p, purpose);
    setOtpSent(true);
  });

  const verify = () => run(async () => {
    const p = normPhone(phone);
    const r = await otpVerify(p, purpose, otp);
    setPhoneToken(r.phone_token);
    if (tab === 'id') {
      const f = await api('account', { action: 'find-id', phone_token: r.phone_token });
      setAccounts(f.accounts || []);
    }
  });

  const doReset = () => run(async () => {
    if (newPw.length < PW_MIN) throw new Error(`비밀번호는 ${PW_MIN}자 이상이어야 합니다`);
    if (newPw !== newPw2) throw new Error('비밀번호 확인이 일치하지 않습니다');
    await api('account', {
      action: 'reset-pw', phone_token: phoneToken,
      username: username.toLowerCase(), new_password: newPw,
    });
    setPwDone(true);
  });

  const doRecoveryUpdate = () => run(async () => {
    if (newPw.length < PW_MIN) throw new Error(`비밀번호는 ${PW_MIN}자 이상이어야 합니다`);
    if (newPw !== newPw2) throw new Error('비밀번호 확인이 일치하지 않습니다');
    const { error } = await supabase.auth.updateUser({ password: newPw });
    if (error) throw new Error(error.message);
    setPwDone(true);
  });

  // ---------- 이메일 링크 복귀 화면 ----------
  if (recovery) {
    return (
      <div className="fa-wrap"><Style />
        <h2 className="fa-title">새 비밀번호 설정</h2>
        {pwDone ? (
          <div className="fa-card">
            <p className="fa-desc">비밀번호가 변경됐어요. 새 비밀번호로 로그인해주세요.</p>
            <a className="fa-btn fa-btn-main" href="#/login">로그인으로</a>
          </div>
        ) : (
          <div className="fa-card">
            <label className="fa-label">새 비밀번호 (8자 이상)</label>
            <input className="fa-input" type="password" value={newPw} onChange={(e) => setNewPw(e.target.value)} />
            <label className="fa-label">새 비밀번호 확인</label>
            <input className="fa-input" type="password" value={newPw2} onChange={(e) => setNewPw2(e.target.value)} />
            <button className="fa-btn fa-btn-main" disabled={busy} onClick={doRecoveryUpdate}>변경하기</button>
          </div>
        )}
        {err && <p className="fa-err">{err}</p>}
      </div>
    );
  }

  return (
    <div className="fa-wrap"><Style />
      <h2 className="fa-title">아이디·비밀번호 찾기</h2>
      <div className="fa-tabs">
        <button className={'fa-tab' + (tab === 'id' ? ' on' : '')} onClick={() => { setTab('id'); resetOtp(); setErr(''); }}>아이디 찾기</button>
        <button className={'fa-tab' + (tab === 'pw' ? ' on' : '')} onClick={() => { setTab('pw'); resetOtp(); setErr(''); }}>비밀번호 재설정</button>
      </div>

      <div className="fa-card">
        {tab === 'pw' && (
          <>
            <label className="fa-label">아이디</label>
            <input className="fa-input" value={username} onChange={(e) => setUsername(e.target.value)} autoCapitalize="none" />
          </>
        )}

        <label className="fa-label">가입할 때 인증한 휴대폰 번호</label>
        <div className="fa-row">
          <input className="fa-input" inputMode="numeric" value={phone}
            onChange={(e) => setPhone(e.target.value)} placeholder="01012345678" disabled={otpSent} />
          <button className="fa-btn" disabled={busy} onClick={sendOtp}>{otpSent ? '재발송' : '인증번호 발송'}</button>
        </div>

        {otpSent && !phoneToken && (
          <div className="fa-row">
            <input className="fa-input" inputMode="numeric" maxLength={6} value={otp}
              onChange={(e) => setOtp(e.target.value)} placeholder="인증번호 6자리" />
            <button className="fa-btn fa-btn-main" disabled={busy} onClick={verify}>확인</button>
          </div>
        )}

        {/* 아이디 찾기 결과 */}
        {tab === 'id' && accounts && (
          accounts.length ? (
            <div className="fa-list">
              {accounts.map((a) => (
                <div className="fa-item" key={a.username}>
                  <div className="fa-item-id">{a.username}</div>
                  <div className="fa-item-sub">
                    {a.nickname ? `${a.nickname} · ` : ''}{a.email_masked || ''}
                    {a.providers?.length ? (
                      <span className="fa-badges">
                        {a.providers.map((p) => (
                          <span className="fa-badge" key={p}>{PROVIDER_LABEL[p] || p}</span>
                        ))}
                      </span>
                    ) : null}
                  </div>
                </div>
              ))}
              <a className="fa-btn fa-btn-main" href="#/login">로그인하러 가기</a>
            </div>
          ) : (
            <p className="fa-desc">이 번호로 가입된 계정이 없어요. 회원가입을 진행해주세요.</p>
          )
        )}

        {/* 비번 재설정 */}
        {tab === 'pw' && phoneToken && !pwDone && (
          <>
            <label className="fa-label">새 비밀번호 (8자 이상)</label>
            <input className="fa-input" type="password" value={newPw} onChange={(e) => setNewPw(e.target.value)} />
            <label className="fa-label">새 비밀번호 확인</label>
            <input className="fa-input" type="password" value={newPw2} onChange={(e) => setNewPw2(e.target.value)} />
            <button className="fa-btn fa-btn-main" disabled={busy} onClick={doReset}>비밀번호 변경</button>
          </>
        )}
        {tab === 'pw' && pwDone && (
          <>
            <p className="fa-desc">비밀번호가 변경됐어요. 새 비밀번호로 로그인해주세요.</p>
            <a className="fa-btn fa-btn-main" href="#/login">로그인으로</a>
          </>
        )}
      </div>

      {err && <p className="fa-err">{err}</p>}
      <p className="fa-hint">전화번호가 바뀌었거나 인증이 안 되면 학원 선생님께 문의해주세요.</p>
    </div>
  );
}

function Style() {
  return (
    <style>{`
      .fa-wrap{max-width:420px;margin:0 auto;padding:20px 16px 48px;color:var(--text,#1c1c1e)}
      .fa-title{margin:4px 0 12px;font-size:22px}
      .fa-tabs{display:flex;gap:8px;margin-bottom:12px}
      .fa-tab{flex:1;padding:10px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);color:inherit}
      .fa-tab.on{background:var(--accent,#3b82f6);border-color:var(--accent,#3b82f6);color:#fff}
      .fa-card{background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:8px}
      .fa-label{font-size:13px;color:var(--muted,#6b7280);margin-top:6px}
      .fa-input{width:100%;box-sizing:border-box;padding:12px;border:1px solid var(--border,#d6d9de);border-radius:10px;font-size:16px;background:var(--surface,#fff);color:inherit}
      .fa-row{display:flex;gap:8px}
      .fa-row .fa-input{flex:1}
      .fa-btn{padding:12px 14px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);font-size:15px;text-align:center;text-decoration:none;color:inherit;white-space:nowrap}
      .fa-btn-main{background:var(--accent,#3b82f6);border-color:var(--accent,#3b82f6);color:#fff;margin-top:6px}
      .fa-btn:disabled{opacity:.5}
      .fa-list{display:flex;flex-direction:column;gap:8px;margin-top:6px}
      .fa-item{border:1px solid var(--border,#e5e7eb);border-radius:10px;padding:10px 12px}
      .fa-item-id{font-weight:700}
      .fa-item-sub{font-size:12px;color:var(--muted,#8a8f98);display:flex;gap:6px;align-items:center;flex-wrap:wrap}
      .fa-badges{display:inline-flex;gap:4px}
      .fa-badge{font-size:11px;padding:2px 6px;border-radius:999px;background:var(--surface2,#f1f2f4)}
      .fa-desc{font-size:14px;line-height:1.6;margin:6px 0 0}
      .fa-hint{font-size:12px;color:var(--muted,#8a8f98);margin-top:12px;text-align:center}
      .fa-err{font-size:13px;color:var(--bad,#dc2626);margin-top:10px;text-align:center}
    `}</style>
  );
}
