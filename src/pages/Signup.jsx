// src/pages/Signup.jsx — raindrop 가입 v2 (해시 라우트: #/signup)
// v2 변경:
// · 첫 화면에서 만 14세 이상/미만 선택 → 미만은 전화 인증 없이 가입하고, 로그인 후 보호자 동의(#/guardian)로 해금
// · 필수: 이름, 생년월일, 아이디, 비밀번호, 이메일 (+만 14세 이상은 휴대폰 인증)
//   선택: 닉네임, 주소, 고유번호(있으면 AI 기능 활성화 — 없어도 가입 가능, 나중에 등록 가능)
// · 생년월일과 선택한 나이대가 어긋나면 진행 불가(만 나이 기준)
import { useState } from 'react';
import {
  supabase, api, otpSend, otpVerify,
  normPhone, quickCheckCode, normCode, fmtCode, codeRoleType,
  recordLoginMethod, PW_MIN,
} from '../lib/authx';

// 만 나이 계산 (생년월일 기준)
function fullAge(birth) {
  const b = new Date(birth + 'T00:00:00');
  if (isNaN(b)) return null;
  const t = new Date();
  let a = t.getFullYear() - b.getFullYear();
  if (t.getMonth() < b.getMonth() || (t.getMonth() === b.getMonth() && t.getDate() < b.getDate())) a--;
  return a;
}

export default function Signup() {
  const [step, setStep] = useState(0);         // 0 나이대 → 1 전화(성인) → 2 정보 → 3 완료
  const [minor, setMinor] = useState(null);    // true = 만 14세 미만
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');

  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [phoneToken, setPhoneToken] = useState('');

  const [name, setName] = useState('');
  const [birth, setBirth] = useState('');      // YYYY-MM-DD
  const [username, setUsername] = useState('');
  const [uState, setUState] = useState(null);  // null | 'ok' | 'dup' | 'fmt'
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');
  const [nickname, setNickname] = useState('');
  const [email, setEmail] = useState('');
  const [address, setAddress] = useState('');
  const [code, setCode] = useState('');        // 고유번호 (선택)
  const [mergeInfo, setMergeInfo] = useState(null);
  const [academyName, setAcademyName] = useState('');

  const run = async (fn) => {
    setErr(''); setBusy(true);
    try { await fn(); } catch (e) { setErr(e.message || String(e)); }
    setBusy(false);
  };

  const pickAge = (isMinor) => { setMinor(isMinor); setErr(''); setStep(isMinor ? 2 : 1); };

  const sendOtp = () => run(async () => {
    const p = normPhone(phone);
    if (!p) throw new Error('휴대폰 번호를 확인해주세요 (예: 01012345678)');
    await otpSend(p, 'signup');
    setOtpSent(true);
  });

  const verifyOtp = () => run(async () => {
    const p = normPhone(phone);
    const r = await otpVerify(p, 'signup', otp);
    setPhoneToken(r.phone_token);
    setStep(2);
  });

  const checkUsername = () => run(async () => {
    const r = await api('account', { action: 'check-username', username: username.toLowerCase() });
    setUState(r.available ? 'ok' : (r.why === 'format' ? 'fmt' : 'dup'));
  });

  const submit = () => run(async () => {
    if (name.trim().length < 2) throw new Error('이름을 입력해주세요');
    const age = fullAge(birth);
    if (age == null || age < 5 || age > 90) throw new Error('생년월일을 확인해주세요 (예: 2013-05-14)');
    if (minor && age >= 14) throw new Error('생년월일 기준 만 14세 이상이에요. 첫 화면에서 [만 14세 이상]으로 다시 진행해주세요.');
    if (!minor && age < 14) throw new Error('생년월일 기준 만 14세 미만이에요. 첫 화면에서 [만 14세 미만]으로 다시 진행해주세요.');
    if (uState !== 'ok') throw new Error('아이디 중복 확인을 해주세요');
    if (password.length < PW_MIN) throw new Error(`비밀번호는 ${PW_MIN}자 이상이어야 합니다`);
    if (password !== password2) throw new Error('비밀번호 확인이 일치하지 않습니다');
    if (!email.includes('@')) throw new Error('이메일을 확인해주세요');
    const rawCode = normCode(code);
    if (rawCode) {
      if (!quickCheckCode(code)) throw new Error('고유번호를 다시 확인해주세요. 없으면 비워두고 가입할 수 있어요.');
      if (codeRoleType(code) === 9) throw new Error('체험 코드입니다. 로그인 화면의 [체험으로 시작하기]를 이용해주세요.');
    }

    let reserve;
    try {
      reserve = await api('account', {
        action: 'reserve',
        minor: !!minor,
        ...(minor ? {} : { phone_token: phoneToken }),
        ...(rawCode ? { member_code: rawCode } : {}),
        username: username.toLowerCase(),
        email,
      });
    } catch (e) {
      if (e.status === 409 && e.data?.merge_required) { setMergeInfo(e.data); return; }
      throw e;
    }
    setAcademyName(reserve.academy_name || '');

    const { error } = await supabase.auth.signUp({
      email, password,
      options: {
        data: {
          username: username.toLowerCase(),
          nickname: nickname || username,
          name: name.trim(),
          birth_year: birth.slice(0, 4),
          birth_date: birth,
          ...(address.trim() ? { address: address.trim() } : {}),
          is_minor: !!minor,
          ...(rawCode ? { member_code: rawCode } : {}),
          signup_token: reserve.reserve_token,
        },
        emailRedirectTo: window.location.origin + window.location.pathname,
      },
    });
    if (error) {
      if (/registered/i.test(error.message)) throw new Error('이미 가입된 이메일입니다. 아이디/비밀번호 찾기를 이용해주세요.');
      throw new Error('가입 실패: ' + error.message);
    }
    recordLoginMethod('id');
    setStep(3);
  });

  if (mergeInfo) {
    return (
      <div className="su-wrap">
        <Style />
        <h2 className="su-title">이미 가입된 번호예요</h2>
        <p className="su-desc">
          이 전화번호로 가입된 계정(<b>{mergeInfo.existing?.username}</b>)이 있어요.
          새로 만들지 말고 기존 계정으로 로그인해주세요.
        </p>
        <a className="su-btn su-btn-main" href="#/find">아이디·비밀번호 찾기</a>
        <button className="su-btn" onClick={() => setMergeInfo(null)}>돌아가기</button>
        <p className="su-hint">기존 계정을 계속 쓸 수 없는 상황이면 학원 선생님께 계정 통합을 요청해주세요.</p>
      </div>
    );
  }

  const STEPS = minor ? ['나이 확인', '계정 정보', '완료'] : ['나이 확인', '전화 인증', '계정 정보', '완료'];
  const stepIdx = minor ? (step === 0 ? 0 : step === 2 ? 1 : 2) : step;

  return (
    <div className="su-wrap">
      <Style />
      <h2 className="su-title">회원가입</h2>
      <div className="su-steps">
        {STEPS.map((s, i) => (
          <span key={s} className={'su-step' + (i === stepIdx ? ' on' : i < stepIdx ? ' done' : '')}>{s}</span>
        ))}
      </div>

      {step === 0 && (
        <div className="su-card">
          <p className="su-desc"><b>나이를 알려주세요.</b> 만 14세 미만 학생은 법에 따라
            가입 후 <b>보호자(법정대리인) 동의</b>가 필요해요.</p>
          <button className="su-btn su-btn-main" disabled={busy} onClick={() => pickAge(false)}>만 14세 이상이에요</button>
          <button className="su-btn" disabled={busy} onClick={() => pickAge(true)}>만 14세 미만이에요 (보호자 동의 필요)</button>
          <p className="su-hint">만 나이 기준이에요. 생년월일 입력 시 자동으로 다시 확인돼요.</p>
        </div>
      )}

      {step === 1 && !minor && (
        <div className="su-card">
          <label className="su-label">휴대폰 번호 (본인 인증)</label>
          <div className="su-row">
            <input className="su-input" inputMode="numeric" value={phone}
              onChange={(e) => setPhone(e.target.value)} placeholder="01012345678" disabled={otpSent} />
            <button className="su-btn" disabled={busy} onClick={sendOtp}>
              {otpSent ? '재발송' : '인증번호 발송'}
            </button>
          </div>
          {otpSent && (
            <>
              <label className="su-label">인증번호 6자리</label>
              <div className="su-row">
                <input className="su-input" inputMode="numeric" maxLength={6} value={otp}
                  onChange={(e) => setOtp(e.target.value)} placeholder="123456" />
                <button className="su-btn su-btn-main" disabled={busy} onClick={verifyOtp}>확인</button>
              </div>
            </>
          )}
          <button className="su-btn su-ghost" disabled={busy} onClick={() => { setStep(0); setMinor(null); }}>← 나이 다시 선택</button>
        </div>
      )}

      {step === 2 && (
        <div className="su-card">
          {minor && (
            <p className="su-note">만 14세 미만은 휴대폰 인증 없이 가입돼요.
              가입 후 로그인하면 <b>보호자 동의</b>를 진행하게 되고, 동의가 확인되어야 전체 기능이 열려요.</p>
          )}

          <label className="su-label">이름 <i className="su-req">필수</i></label>
          <input className="su-input" value={name} onChange={(e) => setName(e.target.value)} placeholder="실명" />

          <label className="su-label">생년월일 <i className="su-req">필수</i></label>
          <input className="su-input" type="date" value={birth} onChange={(e) => setBirth(e.target.value)} />

          <label className="su-label">아이디 <i className="su-req">필수</i></label>
          <div className="su-row">
            <input className="su-input" value={username}
              onChange={(e) => { setUsername(e.target.value); setUState(null); }}
              placeholder="영문 소문자/숫자 4~20자" autoCapitalize="none" />
            <button className="su-btn" disabled={busy} onClick={checkUsername}>중복 확인</button>
          </div>
          {uState === 'ok' && <p className="su-ok">사용할 수 있는 아이디예요</p>}
          {uState === 'dup' && <p className="su-err">이미 사용 중인 아이디예요</p>}
          {uState === 'fmt' && <p className="su-err">영문 소문자·숫자·_ 만 4~20자로 입력해주세요</p>}

          <label className="su-label">비밀번호 (8자 이상) <i className="su-req">필수</i></label>
          <input className="su-input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <label className="su-label">비밀번호 확인 <i className="su-req">필수</i></label>
          <input className="su-input" type="password" value={password2} onChange={(e) => setPassword2(e.target.value)} />

          <label className="su-label">이메일 (인증 메일이 발송돼요) <i className="su-req">필수</i></label>
          <input className="su-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} autoCapitalize="none" />

          <label className="su-label">닉네임 (앱에서 표시될 이름) <i className="su-opt">선택</i></label>
          <input className="su-input" value={nickname} onChange={(e) => setNickname(e.target.value)} placeholder="비우면 아이디로 표시" />

          <label className="su-label">주소 <i className="su-opt">선택</i></label>
          <input className="su-input" value={address} onChange={(e) => setAddress(e.target.value)} placeholder="예: 서울시 ○○구 (동까지만 적어도 돼요)" />

          <label className="su-label">학원 고유번호 <i className="su-opt">선택 — AI 기능 활성화</i></label>
          <input className="su-input su-code" value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="ASH37-1A2B3CD-4E5 (없으면 비워두세요)" autoCapitalize="characters" />
          {normCode(code).length === 15 && <p className="su-hint">{fmtCode(code)}</p>}
          <p className="su-hint">고유번호가 없어도 가입돼요. 나중에 학원에서 받아 등록하면 AI 기능이 열려요.</p>

          <button className="su-btn su-btn-main" disabled={busy} onClick={submit}>가입하기</button>
          <button className="su-btn su-ghost" disabled={busy}
            onClick={() => { setStep(minor ? 0 : 1); if (minor) setMinor(null); }}>← 이전</button>
        </div>
      )}

      {step === 3 && (
        <div className="su-card">
          <h3 className="su-sub">거의 다 됐어요 📮</h3>
          <p className="su-desc">
            {academyName ? <b>{academyName} </b> : ''}가입 정보가 등록됐어요.
            <b> {email}</b> 메일함에서 인증 링크를 누르면 가입이 완료돼요.
          </p>
          {minor && (
            <p className="su-note">로그인하면 <b>보호자 동의</b> 화면으로 안내돼요.
              보호자님과 함께 진행해주세요 — 동의가 확인되어야 전체 기능이 열려요.</p>
          )}
          <a className="su-btn su-btn-main" href="#/login">로그인 화면으로</a>
          <p className="su-hint">메일이 안 보이면 스팸함을 확인해주세요.</p>
        </div>
      )}

      {err && <p className="su-err su-global">{err}</p>}
    </div>
  );
}

function Style() {
  return (
    <style>{`
      .su-wrap{max-width:420px;margin:0 auto;padding:20px 16px 48px;color:var(--text,#1c1c1e)}
      .su-title{margin:4px 0 12px;font-size:22px}
      .su-steps{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap}
      .su-step{font-size:12px;padding:4px 10px;border-radius:999px;background:var(--surface2,#f1f2f4);color:var(--muted,#8a8f98)}
      .su-step.on{background:var(--accent,#3b82f6);color:#fff}
      .su-step.done{background:var(--surface3,#e4e7eb);color:var(--text,#333)}
      .su-card{background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:8px}
      .su-label{font-size:13px;color:var(--muted,#6b7280);margin-top:6px}
      .su-req{font-style:normal;font-size:11px;color:var(--bad,#dc2626);margin-left:4px}
      .su-opt{font-style:normal;font-size:11px;color:var(--muted,#8a8f98);margin-left:4px}
      .su-input{width:100%;box-sizing:border-box;padding:12px;border:1px solid var(--border,#d6d9de);border-radius:10px;font-size:16px;background:var(--surface,#fff);color:inherit}
      .su-code{letter-spacing:1px;font-variant-numeric:tabular-nums}
      .su-row{display:flex;gap:8px}
      .su-row .su-input{flex:1}
      .su-btn{padding:12px 14px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);font-size:15px;text-align:center;text-decoration:none;color:inherit;white-space:nowrap;cursor:pointer}
      .su-btn-main{background:var(--accent,#3b82f6);border-color:var(--accent,#3b82f6);color:#fff;margin-top:8px}
      .su-ghost{border-style:dashed;color:var(--muted,#8a8f98)}
      .su-btn:disabled{opacity:.5}
      .su-hint{font-size:12px;color:var(--muted,#8a8f98);margin:4px 0 0}
      .su-note{font-size:12.5px;line-height:1.6;padding:9px 12px;border-radius:10px;background:var(--surface2,#f1f2f4);margin:0}
      .su-desc{font-size:14px;line-height:1.6}
      .su-sub{margin:0}
      .su-ok{font-size:12px;color:var(--good,#16a34a);margin:0}
      .su-err{font-size:13px;color:var(--bad,#dc2626);margin:0}
      .su-global{margin-top:12px;text-align:center}
    `}</style>
  );
}
