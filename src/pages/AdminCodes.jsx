// src/pages/AdminCodes.jsx — 고유번호 발급/관리 (해시 라우트: #/admin/codes, admin 전용)
import { useEffect, useState } from 'react';
import { supabase, api, fmtCode } from '../lib/authx';

const ROLE_OPTS = [
  { v: 1, label: '학생' }, { v: 2, label: '학부모' }, { v: 3, label: '조교' },
  { v: 5, label: '선생님' }, { v: 9, label: '체험' },
];
const STATUS_LABEL = { issued: '발급됨', reserved: '가입중', used: '사용됨', revoked: '중지' };

export default function AdminCodes() {
  const [ok, setOk] = useState(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');

  // 발급 폼
  const [roleType, setRoleType] = useState(1);
  const [birthYear, setBirthYear] = useState('');
  const [count, setCount] = useState(10);
  const [note, setNote] = useState('');
  const [issued, setIssued] = useState([]);
  const [warning, setWarning] = useState('');

  // 목록
  const [rows, setRows] = useState([]);
  const [statusF, setStatusF] = useState('');
  const [decoded, setDecoded] = useState({});

  // 초대코드
  const [invite, setInvite] = useState(null);

  useEffect(() => {
    (async () => {
      const { data: s } = await supabase.auth.getSession();
      if (!s?.session) { setOk(false); return; }
      const { data: p } = await supabase.from('profiles')
        .select('role').eq('id', s.session.user.id).maybeSingle();
      setOk(p?.role === 'admin');
    })();
  }, []);

  const run = async (fn) => {
    setErr(''); setBusy(true);
    try { await fn(); } catch (e) { setErr(e.message || String(e)); }
    setBusy(false);
  };

  const issue = () => run(async () => {
    setIssued([]); setWarning('');
    const body = { action: 'issue-codes', role_type: roleType, count: +count || 1, note };
    if (roleType !== 9 && birthYear) body.birth_year = +birthYear;
    const r = await api('admin', body, { auth: true });
    setIssued(r.codes || []);
    setWarning(r.warning || '');
  });

  const load = () => run(async () => {
    const r = await api('admin', {
      action: 'list-codes', limit: 100, ...(statusF ? { status: statusF } : {}),
    }, { auth: true });
    setRows(r.rows || []);
  });

  const decode = (code) => run(async () => {
    const r = await api('admin', { action: 'decode-code', code }, { auth: true });
    setDecoded((d) => ({ ...d, [code]: r }));
  });

  const revoke = (code) => run(async () => {
    await api('admin', { action: 'revoke-code', code }, { auth: true });
    await load();
  });

  const makeInvite = () => run(async () => {
    const r = await api('admin', { action: 'create-invite', role: 'admin', expires_days: 7 }, { auth: true });
    setInvite(r);
  });

  const cleanupTrials = () => run(async () => {
    const r = await api('admin', { action: 'cleanup-trials' }, { auth: true });
    alert(`만료 체험계정 ${r.blocked}개를 차단했어요.`);
  });

  const copyAll = async () => {
    try { await navigator.clipboard.writeText(issued.join('\n')); alert('복사했어요'); }
    catch { alert('복사 실패 — 길게 눌러 직접 복사해주세요'); }
  };

  if (ok === null) return null;
  if (ok === false) return <div className="ac-wrap"><Style /><p className="ac-err">관리자만 접근할 수 있어요.</p></div>;

  return (
    <div className="ac-wrap"><Style />
      <h2 className="ac-title">고유번호 관리</h2>

      <div className="ac-card ac-noprint">
        <h3 className="ac-sub">발급하기</h3>
        <div className="ac-row">
          <select className="ac-input" value={roleType} onChange={(e) => setRoleType(+e.target.value)}>
            {ROLE_OPTS.map((o) => <option key={o.v} value={o.v}>{o.label}</option>)}
          </select>
          {roleType !== 9 && (
            <input className="ac-input" inputMode="numeric" placeholder="출생년도 (예: 2012)"
              value={birthYear} onChange={(e) => setBirthYear(e.target.value)} />
          )}
        </div>
        <div className="ac-row">
          <input className="ac-input" inputMode="numeric" placeholder="수량 (최대 200)"
            value={count} onChange={(e) => setCount(e.target.value)} />
          <input className="ac-input" placeholder="메모 (예: 3월 신규반)"
            value={note} onChange={(e) => setNote(e.target.value)} />
        </div>
        <button className="ac-btn ac-btn-main" disabled={busy} onClick={issue}>발급</button>
        {warning && <p className="ac-warn">{warning}</p>}
      </div>

      {issued.length > 0 && (
        <div className="ac-card">
          <div className="ac-row ac-between ac-noprint">
            <h3 className="ac-sub">발급 결과 {issued.length}건</h3>
            <div className="ac-row">
              <button className="ac-btn" onClick={copyAll}>전체 복사</button>
              <button className="ac-btn" onClick={() => window.print()}>🖨 인쇄</button>
            </div>
          </div>
          <div className="ac-coupons">
            {issued.map((c) => (
              <div className="ac-coupon" key={c}>
                <div className="ac-coupon-brand">ashrain.out {roleType === 9 ? '체험권' : '가입 코드'}</div>
                <div className="ac-coupon-code">{c}</div>
                <div className="ac-coupon-hint">{roleType === 9 ? '로그인 화면 → 체험으로 시작하기' : '회원가입에서 입력'}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="ac-card ac-noprint">
        <div className="ac-row ac-between">
          <h3 className="ac-sub">발급 내역</h3>
          <div className="ac-row">
            <select className="ac-input" value={statusF} onChange={(e) => setStatusF(e.target.value)}>
              <option value="">전체</option>
              {Object.entries(STATUS_LABEL).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
            </select>
            <button className="ac-btn" disabled={busy} onClick={load}>불러오기</button>
          </div>
        </div>
        {rows.map((r) => (
          <div className="ac-item" key={r.code}>
            <div className="ac-item-top">
              <span className="ac-code">{r.code_fmt}</span>
              <span className={'ac-status s-' + r.status}>{STATUS_LABEL[r.status] || r.status}</span>
            </div>
            <div className="ac-item-sub">
              {(ROLE_OPTS.find((o) => o.v === r.role_type) || {}).label || r.role_type}
              {r.note ? ` · ${r.note}` : ''} · {new Date(r.issued_at).toLocaleDateString('ko-KR')}
              {decoded[r.code] && (
                <b> · 해독: {decoded[r.code].regYear}년 등록{decoded[r.code].birthYear ? ` / ${decoded[r.code].birthYear}년생` : ''}</b>
              )}
            </div>
            <div className="ac-row">
              {!decoded[r.code] && <button className="ac-btn ac-mini" onClick={() => decode(r.code)}>해독</button>}
              {['issued', 'reserved'].includes(r.status) && (
                <button className="ac-btn ac-mini" onClick={() => revoke(r.code)}>중지</button>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="ac-card ac-noprint">
        <h3 className="ac-sub">기타</h3>
        <div className="ac-row">
          <button className="ac-btn" disabled={busy} onClick={makeInvite}>스태프 초대코드 만들기</button>
          <button className="ac-btn" disabled={busy} onClick={cleanupTrials}>만료 체험계정 정리</button>
        </div>
        {invite && (
          <p className="ac-ok">초대코드: <b>{invite.invite_code}</b> ({invite.expires_days}일 유효) —
            가입 주소: <b>{window.location.origin + window.location.pathname}#/staff-join</b></p>
        )}
      </div>

      {err && <p className="ac-err">{err}</p>}
    </div>
  );
}

function Style() {
  return (
    <style>{`
      .ac-wrap{max-width:560px;margin:0 auto;padding:20px 16px 48px;color:var(--text,#1c1c1e)}
      .ac-title{margin:4px 0 12px;font-size:22px}
      .ac-sub{margin:0 0 4px;font-size:15px}
      .ac-card{background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:8px;margin-bottom:12px}
      .ac-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
      .ac-between{justify-content:space-between}
      .ac-input{padding:10px;border:1px solid var(--border,#d6d9de);border-radius:10px;font-size:14px;background:var(--surface,#fff);color:inherit;flex:1;min-width:120px;box-sizing:border-box}
      .ac-btn{padding:10px 12px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);font-size:14px;color:inherit}
      .ac-btn-main{background:var(--accent,#3b82f6);border-color:var(--accent,#3b82f6);color:#fff}
      .ac-btn:disabled{opacity:.5}
      .ac-mini{padding:6px 10px;font-size:12px}
      .ac-item{border-top:1px solid var(--border,#eef0f3);padding:10px 0 8px;display:flex;flex-direction:column;gap:6px}
      .ac-item-top{display:flex;justify-content:space-between;align-items:center;gap:8px}
      .ac-code{font-family:ui-monospace,monospace;font-size:14px;font-weight:700;letter-spacing:.5px}
      .ac-item-sub{font-size:12px;color:var(--muted,#8a8f98)}
      .ac-status{font-size:11px;padding:2px 8px;border-radius:999px;background:var(--surface2,#f1f2f4)}
      .ac-status.s-used{background:#dcfce7;color:#166534}
      .ac-status.s-revoked{background:#fee2e2;color:#991b1b}
      .ac-status.s-reserved{background:#fef9c3;color:#854d0e}
      .ac-ok{font-size:13px;color:var(--good,#16a34a);word-break:break-all}
      .ac-warn{font-size:13px;color:#b45309}
      .ac-err{font-size:13px;color:var(--bad,#dc2626);text-align:center}
      .ac-coupons{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
      .ac-coupon{border:1.5px dashed var(--border,#c9cdd3);border-radius:12px;padding:12px;text-align:center}
      .ac-coupon-brand{font-size:11px;color:var(--muted,#8a8f98)}
      .ac-coupon-code{font-family:ui-monospace,monospace;font-weight:800;font-size:15px;letter-spacing:.5px;margin:6px 0}
      .ac-coupon-hint{font-size:10px;color:var(--muted,#a1a6ae)}
      @media print {
        .ac-noprint{display:none !important}
        .ac-wrap{max-width:none;padding:0}
        .ac-card{border:none}
        .ac-coupons{grid-template-columns:repeat(3,1fr)}
        .ac-coupon{break-inside:avoid}
      }
    `}</style>
  );
}
