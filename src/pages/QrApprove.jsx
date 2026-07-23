// src/pages/QrApprove.jsx — 폰에서 QR 스캔 후 열리는 승인 화면 (해시 라우트: #/qr-approve?sid=...)
import { useEffect, useState } from 'react';
import { supabase, api } from '../lib/authx';

function getSid() {
  const h = window.location.hash;                 // "#/qr-approve?sid=xxxx"
  const i = h.indexOf('?');
  if (i < 0) return null;
  return new URLSearchParams(h.slice(i + 1)).get('sid');
}

export default function QrApprove() {
  const [state, setState] = useState('check');    // check | need-login | ready | done | error
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState('');
  const sid = getSid();

  useEffect(() => {
    (async () => {
      if (!sid) { setState('error'); setMsg('잘못된 QR이에요. PC에서 QR을 다시 띄워 스캔해주세요.'); return; }
      const { data } = await supabase.auth.getSession();
      setState(data?.session ? 'ready' : 'need-login');
    })();
  }, [sid]);

  const approve = async () => {
    setBusy(true); setMsg('');
    try {
      await api('qr', { action: 'approve', qr_id: sid }, { auth: true });
      setState('done');
    } catch (e) {
      setState('error');
      setMsg(e.message || String(e));
    }
    setBusy(false);
  };

  return (
    <div className="qa-wrap"><Style />
      <h2 className="qa-title">PC 로그인 승인</h2>

      {state === 'check' && <p className="qa-desc">확인 중…</p>}

      {state === 'need-login' && (
        <div className="qa-card">
          <p className="qa-desc">먼저 이 폰에서 로그인한 뒤, PC의 QR을 다시 스캔해주세요.</p>
          <a className="qa-btn qa-btn-main" href="#/login">로그인하러 가기</a>
        </div>
      )}

      {state === 'ready' && (
        <div className="qa-card">
          <p className="qa-desc">지금 보고 있는 PC 화면을 <b>내 계정으로 로그인</b>시킬까요?
            내가 요청한 게 아니라면 승인하지 마세요.</p>
          <button className="qa-btn qa-btn-main" disabled={busy} onClick={approve}>
            이 PC 로그인 승인
          </button>
          <a className="qa-btn" href="#/">취소</a>
        </div>
      )}

      {state === 'done' && (
        <div className="qa-card">
          <p className="qa-desc">승인 완료! PC 화면이 곧 로그인돼요. 이 창은 닫아도 돼요.</p>
          <a className="qa-btn qa-btn-main" href="#/">홈으로</a>
        </div>
      )}

      {state === 'error' && (
        <div className="qa-card">
          <p className="qa-err">{msg || '처리하지 못했어요.'}</p>
          <a className="qa-btn" href="#/">홈으로</a>
        </div>
      )}
    </div>
  );
}

function Style() {
  return (
    <style>{`
      .qa-wrap{max-width:420px;margin:0 auto;padding:24px 16px 48px;color:var(--text,#1c1c1e)}
      .qa-title{margin:4px 0 12px;font-size:22px}
      .qa-card{background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:10px}
      .qa-desc{font-size:14px;line-height:1.7;margin:0}
      .qa-btn{padding:13px 14px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);font-size:15px;text-align:center;text-decoration:none;color:inherit}
      .qa-btn-main{background:var(--accent,#3b82f6);border-color:var(--accent,#3b82f6);color:#fff}
      .qa-btn:disabled{opacity:.6}
      .qa-err{font-size:13px;color:var(--bad,#dc2626);margin:0}
    `}</style>
  );
}
