// src/pages/Onboarding.jsx — 소셜 첫 로그인 온보딩 v2.0 (해시 라우트: #/onboarding)
// v2.0 전면 개편: 고유번호 필수 → 나이 확인 필수로 전환.
//  · 소셜(구글·카카오) 로그인은 나이 정보를 주지 않으므로 여기서 생년월일을 필수로 받는다.
//  · 만 14세 미만 → 전화 인증 없이 저장 후 보호자 동의(#/guardian)로 안내(동의 확인 전까지 개념 열람만).
//  · 만 14세 이상 → 휴대폰 본인 인증(5분 타이머) 후 완료.
//  · 고유번호는 선택 — 있으면 즉시 확정(AI 기능 활성화), 없어도 진행 가능.
// 서버: /api/account { action: 'social-onboard' }
import { useEffect, useState } from 'react';
import BirthInput from '../shared/BirthInput';
import {
  supabase, api, otpSend, otpVerify,
  normPhone, quickCheckCode, normCode, fmtCode, codeRoleType,
} from '../lib/authx';

function fmtLeft(s) {
  return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0');
}
function fullAge(birth) {
  const b = new Date(birth + 'T00:00:00');
  if (isNaN(b)) return null;
  const t = new Date();
  let a = t.getFullYear() - b.getFullYear();
  if (t.getMonth() < b.getMonth() || (t.getMonth() === b.getMonth() && t.getDate() < b.getDate())) a--;
  return a;
}

export default function Onboarding() {
  const [me, setMe] = useState(undefined);       // undefined 로딩 | null 비로그인 | {user, prof}
  const [step, setStep] = useState(1);           // 1 정보 → 2 전화(성인) → 3 완료
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const [mergeInfo, setMergeInfo] = useState(null);
  const [doneMinor, setDoneMinor] = useState(false);

  const [name, setName] = useState('');
  const [birth, setBirth] = useState('');
  const [nickname, setNickname] = useState('');
  const [code, setCode] = useState('');

  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [otpEnd, setOtpEnd] = useState(null);
  const [otpLeft, setOtpLeft] = useState(0);

  useEffect(() => {
    (async () => {
      const { data: { session } } = await supabase.auth.getSession();
      if (!session) { setMe(null); return; }
      const { data: prof } = await supabase.from('profiles')
        .select('name, nickname, birth_date, is_minor, phone_verified, role')
        .eq('id', session.user.id).maybeSingle();
      setMe({ user: session.user, prof: prof || {} });
      const meta = session.user.user_metadata || {};
      setName((prof?.name && prof.name !== '학생' ? prof.name : '') || meta.full_name || meta.name || '');
      setNickname(prof?.nickname || meta.nickname || '');
    })();
  }, []);

  useEffect(() => {
    if (!otpEnd) return;
    const tick = () => setOtpLeft(Math.max(0, Math.ceil((otpEnd - Date.now()) / 1000)));
    tick();
    const t = setInterval(tick, 500);
    return () => clearInterval(t);
  }, [otpEnd]);
  const otpExpired = !!otpEnd && otpLeft === 0;

  const run = async (fn) => {
    setErr(''); setBusy(true);
    try { await fn(); } catch (e) { setErr(e.message || String(e)); }
    setBusy(false);
  };

  const go = (hash) => { location.hash = hash; setTimeout(() => location.reload(), 60); };

  const checkInfo = () => {
    if (name.trim().length < 2) throw new Error('이름을 입력해주세요');
    const age = fullAge(birth);
    if (age == null || age < 5 || age > 90) throw new Error('생년월일을 확인해주세요');
    const raw = normCode(code);
    if (raw) {
      if (!quickCheckCode(code)) throw new Error('고유번호를 다시 확인해주세요. 없으면 비워두고 진행할 수 있어요.');
      if (codeRoleType(code) === 9) throw new Error('체험 코드는 여기서 쓸 수 없어요. 없으면 비워두고 진행해주세요.');
    }
    return age;
  };

  const submit = (phoneToken) => api('account', {
    action: 'social-onboard',
    name: name.trim(),
    birth_date: birth,
    ...(nickname.trim() ? { nickname: nickname.trim() } : {}),
    ...(normCode(code) ? { member_code: normCode(code) } : {}),
    ...(phoneToken ? { phone_token: phoneToken } : {}),
  });

  const next = () => run(async () => {
    const age = checkInfo();
    if (age < 14) {
      // 만 14세 미만 — 전화 없이 바로 저장, 보호자 동의로
      try {
        await submit(null);
      } catch (e) {
        if (e.status === 409 && e.data?.merge_required) { setMergeInfo(e.data); return; }
        throw e;
      }
      setDoneMinor(true);
      setStep(3);
      return;
    }
    setStep(2);
  });

  const sendCode = () => run(async () => {
    const p = normPhone(phone);
    if (!p) throw new Error('휴대폰 번호를 확인해주세요 (예: 01012345678)');
    await otpSend(p, 'social');
    setOtpSent(true); setOtp('');
    setOtpEnd(Date.now() + 5 * 60e3);
  });

  const verifyAndFinish = () => run(async () => {
    if (otpExpired) throw new Error('입력 시간이 지났어요 — 인증번호를 다시 발송해주세요');
    const p = normPhone(phone);
    const r = await otpVerify(p, 'social', otp);
    try {
      await submit(r.phone_token);
    } catch (e) {
      if (e.status === 409 && e.data?.merge_required) { setMergeInfo(e.data); return; }
      throw e;
    }
    setOtpEnd(null);
    setDoneMinor(false);
    setStep(3);
  });

  const logoutOther = async () => { await supabase.auth.signOut(); go('#/'); };

  if (me === undefined) return <div className="ob-wrap"><Style /><p className="ob-hint">불러오는 중…</p></div>;

  if (me === null) return (
    <div className="ob-wrap"><Style />
      <h2 className="ob-title">로그인이 필요해요</h2>
      <button className="ob-btn ob-main" onClick={() => go('#/')}>로그인 화면으로</button>
    </div>
  );

  if (mergeInfo) return (
    <div className="ob-wrap"><Style />
      <h2 className="ob-title">이미 가입된 번호예요</h2>
      <p className="ob-desc">이 전화번호로 가입된 계정(<b>{mergeInfo.existing?.username}</b>)이 있어요.
        이 소셜 계정 대신 기존 계정으로 로그인해주세요.</p>
      <button className="ob-btn ob-main" onClick={logoutOther}>기존 계정으로 로그인하기</button>
      <button className="ob-btn" onClick={() => setMergeInfo(null)}>돌아가기</button>
      <p className="ob-hint">기존 계정을 쓸 수 없는 상황이면 학원 선생님께 계정 통합을 요청해주세요.</p>
    </div>
  );

  // 이미 온보딩을 마친 계정
  if (me.prof?.birth_date && step !== 3) return (
    <div className="ob-wrap"><Style />
      <h2 className="ob-title">이미 확인이 끝난 계정이에요 ✓</h2>
      {me.prof.is_minor && !me.prof.phone_verified && (
        <p className="ob-note">만 14세 미만 계정은 <b>보호자 동의</b>가 확인되어야 전체 기능이 열려요.</p>
      )}
      <button className="ob-btn ob-main" onClick={() => go('#/')}>홈으로</button>
      {me.prof.is_minor && (
        <button className="ob-btn" onClick={() => go('#/guardian')}>보호자 동의 진행하기</button>
      )}
    </div>
  );

  return (
    <div className="ob-wrap">
      <Style />
      <h2 className="ob-title">처음 오셨네요! 👋</h2>
      <p className="ob-sub">
        {me.user.email ? <><b>{me.user.email}</b> 계정으로 로그인했어요. </> : null}
        서비스 이용을 위해 몇 가지만 확인할게요.
        <span className="ob-out" onClick={logoutOther}> 다른 계정으로</span>
      </p>

      {step === 1 && (
        <div className="ob-card">
          <label className="ob-label">이름 <i className="ob-req">필수</i></label>
          <input className="ob-inp" value={name} onChange={(e) => setName(e.target.value)} placeholder="실명" />

          <label className="ob-label">생년월일 <i className="ob-req">필수 — 만 14세 미만은 보호자 동의가 필요해요</i></label>
          <BirthInput value={birth} onChange={setBirth} inputClass="ob-inp" />

          <label className="ob-label">닉네임 <i className="ob-opt">선택</i></label>
          <input className="ob-inp" value={nickname} onChange={(e) => setNickname(e.target.value)} placeholder="앱에서 표시될 이름" />

          <label className="ob-label">학원 고유번호 <i className="ob-opt">선택 — AI 기능 활성화</i></label>
          <input className="ob-inp ob-code" value={code} onChange={(e) => setCode(e.target.value)}
            placeholder="ASH37-1A2B3CD-4E5 (없으면 비워두세요)" autoCapitalize="characters" />
          {normCode(code).length === 15 && <p className="ob-hint">{fmtCode(code)}</p>}

          <button className="ob-btn ob-main" disabled={busy} onClick={next}>다음</button>
        </div>
      )}

      {step === 2 && (
        <div className="ob-card">
          <p className="ob-note">만 14세 이상은 <b>휴대폰 본인 인증</b>이 필요해요.</p>
          <label className="ob-label">휴대폰 번호</label>
          <div className="ob-row">
            <input className="ob-inp" inputMode="numeric" value={phone} disabled={otpSent && !otpExpired}
              onChange={(e) => { setPhone(e.target.value); setOtpSent(false); setOtpEnd(null); }}
              placeholder="01012345678" />
            <button className="ob-btn" disabled={busy} onClick={sendCode}>{otpSent ? '재발송' : '인증번호 발송'}</button>
          </div>
          {otpSent && (
            <>
              <div className="ob-row">
                <input className="ob-inp" inputMode="numeric" maxLength={6} value={otp}
                  onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))} placeholder="인증번호 6자리" />
                <button className="ob-btn ob-main" disabled={busy || otp.length !== 6 || otpExpired}
                  onClick={verifyAndFinish}>확인</button>
              </div>
              <p className="ob-timer">
                {otpExpired ? '입력 시간이 지났어요 — 인증번호를 다시 발송해주세요' : `남은 입력 시간 ${fmtLeft(otpLeft)}`}
              </p>
            </>
          )}
          <button className="ob-btn ob-ghost" disabled={busy} onClick={() => { setStep(1); setOtpEnd(null); setOtpSent(false); }}>← 이전</button>
        </div>
      )}

      {step === 3 && (
        <div className="ob-card">
          {doneMinor ? (
            <>
              <h3 className="ob-done">확인 완료 — 한 단계 남았어요</h3>
              <p className="ob-desc">만 14세 미만 학생은 법에 따라 <b>보호자(법정대리인) 동의</b>가 필요해요.
                동의가 확인되기 전까지는 개념 열람만 가능해요. 보호자님과 함께 진행해주세요.</p>
              <button className="ob-btn ob-main" onClick={() => go('#/guardian')}>보호자 동의 진행하기</button>
              <button className="ob-btn" onClick={() => go('#/')}>나중에 하고 개념 먼저 볼래요</button>
            </>
          ) : (
            <>
              <h3 className="ob-done">환영해요, 모든 준비가 끝났어요 🎉</h3>
              <button className="ob-btn ob-main" onClick={() => go('#/')}>시작하기</button>
            </>
          )}
        </div>
      )}

      {err && <p className="ob-err">{err}</p>}
    </div>
  );
}

function Style() {
  return (
    <style>{`
      .ob-wrap { max-width: 420px; margin: 0 auto; padding: 28px 16px 56px; }
      .ob-title { font-size: 1.35rem; margin: 0 0 6px; }
      .ob-sub { font-size: .86rem; opacity: .75; line-height: 1.6; margin: 0 0 14px; }
      .ob-out { text-decoration: underline; cursor: pointer; opacity: .7; }
      .ob-card { border: 1px solid rgba(127,127,127,.22); background: rgba(127,127,127,.05);
        border-radius: 14px; padding: 16px; display: flex; flex-direction: column; gap: 8px; }
      .ob-label { font-size: .8rem; opacity: .7; margin-top: 6px; }
      .ob-req { font-style: normal; font-size: .7rem; color: #e05252; margin-left: 4px; }
      .ob-opt { font-style: normal; font-size: .7rem; opacity: .55; margin-left: 4px; }
      .ob-inp { width: 100%; box-sizing: border-box; padding: 11px 12px; border-radius: 10px;
        border: 1px solid rgba(127,127,127,.32); background: rgba(255,255,255,.55);
        color: inherit; font-size: .95rem; }
      [data-theme="dark"] .ob-inp { background: rgba(0,0,0,.25); }
      .ob-code { letter-spacing: 1px; font-variant-numeric: tabular-nums; }
      .ob-row { display: flex; gap: 8px; }
      .ob-row .ob-inp { flex: 1; }
      .ob-btn { padding: 11px 14px; border-radius: 10px; font-size: .92rem; cursor: pointer;
        border: 1px solid rgba(127,127,127,.3); background: rgba(127,127,127,.08);
        color: inherit; white-space: nowrap; }
      .ob-btn:disabled { opacity: .45; cursor: default; }
      .ob-main { background: rgba(74,107,176,.18); border-color: rgba(74,107,176,.55);
        font-weight: 700; margin-top: 8px; }
      .ob-main:not(:disabled):hover { background: rgba(74,107,176,.3); }
      .ob-ghost { border-style: dashed; opacity: .7; }
      .ob-note { font-size: .82rem; line-height: 1.6; padding: 9px 12px; border-radius: 10px;
        background: rgba(74,107,176,.12); border: 1px solid rgba(74,107,176,.4); margin: 0; }
      .ob-hint { font-size: .76rem; opacity: .55; margin: 2px 0 0; }
      .ob-timer { font-size: .78rem; color: #e05252; font-weight: 700; margin: 2px 0 0;
        font-variant-numeric: tabular-nums; }
      .ob-done { margin: 0 0 4px; font-size: 1.05rem; }
      .ob-desc { font-size: .86rem; line-height: 1.65; margin: 0 0 6px; }
      .ob-err { font-size: .84rem; color: #e05252; margin: 12px 0 0; text-align: center; }
    `}</style>
  );
}
