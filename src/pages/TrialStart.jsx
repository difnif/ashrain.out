// src/pages/TrialStart.jsx — 체험 코드로 24시간 체험 시작 (해시 라우트: #/trial)
import { useState } from 'react';
import {
  supabase, api, quickCheckCode, normCode, codeRoleType, recordLoginMethod,
} from '../lib/authx';

export default function TrialStart() {
  const [code, setCode] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const [expires, setExpires] = useState(null);

  const start = async () => {
    setErr(''); setBusy(true);
    try {
      if (!quickCheckCode(code)) throw new Error('체험 코드를 다시 확인해주세요');
      if (codeRoleType(code) !== 9) throw new Error('체험 코드가 아니에요. 정식 고유번호는 회원가입에서 사용해주세요.');

      const r = await api('account', { action: 'trial-start', member_code: normCode(code) });
      const { error } = await supabase.auth.signInWithPassword({
        email: r.email, password: r.password,
      });
      if (error) throw new Error('체험 계정 로그인 실패: ' + error.message);

      recordLoginMethod('trial');
      setExpires(new Date(r.expires_at));
      setTimeout(() => { window.location.hash = '#/'; }, 1500);
    } catch (e) {
      setErr(e.message || String(e));
    }
    setBusy(false);
  };

  return (
    <div className="tr-wrap"><Style />
      <h2 className="tr-title">체험으로 시작하기</h2>
      <p className="tr-desc">학원에서 받은 체험 코드를 입력하면 지금부터 <b>24시간</b> 동안 모든 학습 기능을 써볼 수 있어요.
        가입 절차도, 개인정보 입력도 없어요.</p>

      <div className="tr-card">
        <input className="tr-input" value={code} onChange={(e) => setCode(e.target.value)}
          placeholder="ASH37-9A2B3CD-4E5" autoCapitalize="characters" />
        <button className="tr-btn tr-btn-main" disabled={busy || !!expires} onClick={start}>
          {expires ? '시작됐어요! 이동 중…' : '체험 시작'}
        </button>
        {expires && (
          <p className="tr-ok">
            {expires.toLocaleString('ko-KR', { month: 'numeric', day: 'numeric', hour: 'numeric', minute: '2-digit' })}
            까지 이용할 수 있어요.
          </p>
        )}
      </div>

      {err && <p className="tr-err">{err}</p>}
      <p className="tr-hint">체험이 마음에 들면 학원 선생님께 정식 고유번호를 요청해주세요.</p>
    </div>
  );
}

function Style() {
  return (
    <style>{`
      .tr-wrap{max-width:420px;margin:0 auto;padding:24px 16px 48px;color:var(--text,#1c1c1e)}
      .tr-title{margin:4px 0 8px;font-size:22px}
      .tr-desc{font-size:14px;line-height:1.6;color:var(--muted,#4b5563);margin:0 0 14px}
      .tr-card{background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:10px}
      .tr-input{width:100%;box-sizing:border-box;padding:14px;border:1px solid var(--border,#d6d9de);border-radius:10px;font-size:17px;letter-spacing:1px;text-align:center;background:var(--surface,#fff);color:inherit}
      .tr-btn{padding:13px 14px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);font-size:15px}
      .tr-btn-main{background:var(--accent,#3b82f6);border-color:var(--accent,#3b82f6);color:#fff}
      .tr-btn:disabled{opacity:.6}
      .tr-ok{font-size:13px;color:var(--good,#16a34a);text-align:center;margin:0}
      .tr-err{font-size:13px;color:var(--bad,#dc2626);margin-top:10px;text-align:center}
      .tr-hint{font-size:12px;color:var(--muted,#8a8f98);margin-top:12px;text-align:center}
    `}</style>
  );
}
