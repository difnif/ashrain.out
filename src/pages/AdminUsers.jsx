// src/pages/AdminUsers.jsx — 유저 관리 (해시 라우트: #/admin/users, admin 전용)
import { useEffect, useState } from 'react';
import { supabase, api } from '../lib/authx';

const ROLE_LABEL = {
  admin: '관리자', teacher: '선생님', assistant: '조교',
  parent: '학부모', student: '학생', trial: '체험',
};

export default function AdminUsers() {
  const [ok, setOk] = useState(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');

  const [q, setQ] = useState('');
  const [users, setUsers] = useState([]);
  const [tempPw, setTempPw] = useState({});      // uid → 임시비번
  const [pick, setPick] = useState({ primary: null, merged: null });
  const [mergeReport, setMergeReport] = useState(null);
  const [pending, setPending] = useState([]);    // 통합 신청 대기
  const [nameOf, setNameOf] = useState({});      // uid → username

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

  const search = () => run(async () => {
    const r = await api('admin', { action: 'find-users', q }, { auth: true });
    setUsers(r.users || []);
  });

  const resetPw = (uid) => run(async () => {
    if (!window.confirm('이 회원의 비밀번호를 임시 비밀번호로 바꿀까요?')) return;
    const r = await api('admin', { action: 'reset-user-pw', user_id: uid }, { auth: true });
    setTempPw((t) => ({ ...t, [uid]: r.temp_password }));
  });

  const doMerge = () => run(async () => {
    if (!pick.primary || !pick.merged) throw new Error('남길 계정과 흡수할 계정을 각각 선택해주세요');
    if (!window.confirm('통합을 실행할까요? 흡수 계정은 로그인이 차단돼요.')) return;
    const r = await api('admin', {
      action: 'merge-users', primary_user: pick.primary, merged_user: pick.merged,
    }, { auth: true });
    setMergeReport(r.report || []);
    setPick({ primary: null, merged: null });
    await loadPending();
  });

  const loadPending = () => run(async () => {
    const { data: reqs } = await supabase.from('merge_requests')
      .select('*').eq('status', 'pending').order('requested_at', { ascending: false }).limit(20);
    setPending(reqs || []);
    const ids = [...new Set((reqs || []).flatMap((r) => [r.primary_user, r.merged_user]))];
    if (ids.length) {
      const { data: ps } = await supabase.from('profiles')
        .select('id, username, nickname').in('id', ids);
      const map = {};
      (ps || []).forEach((p) => { map[p.id] = p.username || p.nickname || p.id.slice(0, 8); });
      setNameOf(map);
    }
  });

  const execPending = (r) => run(async () => {
    if (!window.confirm(`${nameOf[r.merged_user] || '?'} → ${nameOf[r.primary_user] || '?'} 통합을 실행할까요?`)) return;
    const res = await api('admin', {
      action: 'merge-users', primary_user: r.primary_user, merged_user: r.merged_user, reason: r.reason,
    }, { auth: true });
    setMergeReport(res.report || []);
    await loadPending();
  });

  if (ok === null) return null;
  if (ok === false) return <div className="au-wrap"><Style /><p className="au-err">관리자만 접근할 수 있어요.</p></div>;

  return (
    <div className="au-wrap"><Style />
      <h2 className="au-title">유저 관리</h2>

      <div className="au-card">
        <div className="au-row">
          <input className="au-input" value={q} onChange={(e) => setQ(e.target.value)}
            placeholder="아이디 / 닉네임 / 전화번호 검색"
            onKeyDown={(e) => e.key === 'Enter' && search()} />
          <button className="au-btn au-btn-main" disabled={busy} onClick={search}>검색</button>
        </div>

        {users.map((u) => (
          <div className="au-item" key={u.id}>
            <div className="au-item-top">
              <b>{u.username || '(아이디 없음)'}</b>
              <span className="au-badge">{ROLE_LABEL[u.role] || u.role}</span>
              {u.merged_into && <span className="au-badge au-badge-off">통합됨</span>}
            </div>
            <div className="au-item-sub">
              {u.nickname ? `${u.nickname} · ` : ''}{u.phone || '전화 없음'}
              {u.member_code ? ` · ${u.member_code}` : ''}
              {u.role === 'trial' && u.trial_expires_at
                ? ` · 만료 ${new Date(u.trial_expires_at).toLocaleString('ko-KR')}` : ''}
            </div>
            {tempPw[u.id] && <p className="au-ok">임시 비밀번호: <b>{tempPw[u.id]}</b> (회원에게 전달 후 변경 안내)</p>}
            <div className="au-row">
              <button className="au-btn au-mini" onClick={() => resetPw(u.id)}>임시 비번</button>
              <button className={'au-btn au-mini' + (pick.primary === u.id ? ' on' : '')}
                onClick={() => setPick((p) => ({ ...p, primary: p.primary === u.id ? null : u.id }))}>
                남길 계정{pick.primary === u.id ? ' ✓' : ''}
              </button>
              <button className={'au-btn au-mini' + (pick.merged === u.id ? ' on' : '')}
                onClick={() => setPick((p) => ({ ...p, merged: p.merged === u.id ? null : u.id }))}>
                흡수할 계정{pick.merged === u.id ? ' ✓' : ''}
              </button>
            </div>
          </div>
        ))}

        {(pick.primary || pick.merged) && (
          <button className="au-btn au-btn-main" disabled={busy} onClick={doMerge}>
            선택한 두 계정 통합 실행
          </button>
        )}
      </div>

      <div className="au-card">
        <div className="au-row au-between">
          <h3 className="au-sub">통합 신청 대기</h3>
          <button className="au-btn au-mini" disabled={busy} onClick={loadPending}>불러오기</button>
        </div>
        {pending.length === 0 && <p className="au-hint">대기 중인 신청이 없어요.</p>}
        {pending.map((r) => (
          <div className="au-item" key={r.id}>
            <div className="au-item-sub">
              <b>{nameOf[r.merged_user] || r.merged_user.slice(0, 8)}</b> →{' '}
              <b>{nameOf[r.primary_user] || r.primary_user.slice(0, 8)}</b>
              {' '}({r.reason}) · {new Date(r.requested_at).toLocaleString('ko-KR')}
            </div>
            <div className="au-row">
              <button className="au-btn au-mini" onClick={() => execPending(r)}>통합 실행</button>
            </div>
          </div>
        ))}
      </div>

      {mergeReport && (
        <div className="au-card">
          <h3 className="au-sub">통합 결과</h3>
          {mergeReport.length === 0 && <p className="au-hint">이관할 데이터가 없었어요.</p>}
          {mergeReport.map((t) => (
            <p className="au-hint" key={t.tbl}>{t.tbl}: {t.moved}건 이동{t.skipped ? `, ${t.skipped}건 중복 건너뜀` : ''}</p>
          ))}
        </div>
      )}

      {err && <p className="au-err">{err}</p>}
    </div>
  );
}

function Style() {
  return (
    <style>{`
      .au-wrap{max-width:560px;margin:0 auto;padding:20px 16px 48px;color:var(--text,#1c1c1e)}
      .au-title{margin:4px 0 12px;font-size:22px}
      .au-sub{margin:0;font-size:15px}
      .au-card{background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:8px;margin-bottom:12px}
      .au-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
      .au-between{justify-content:space-between}
      .au-input{padding:10px;border:1px solid var(--border,#d6d9de);border-radius:10px;font-size:14px;flex:1;background:var(--surface,#fff);color:inherit;box-sizing:border-box}
      .au-btn{padding:10px 12px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);font-size:14px;color:inherit}
      .au-btn-main{background:var(--accent,#3b82f6);border-color:var(--accent,#3b82f6);color:#fff}
      .au-btn:disabled{opacity:.5}
      .au-mini{padding:6px 10px;font-size:12px}
      .au-mini.on{background:var(--accent,#3b82f6);border-color:var(--accent,#3b82f6);color:#fff}
      .au-item{border-top:1px solid var(--border,#eef0f3);padding:10px 0 8px;display:flex;flex-direction:column;gap:6px}
      .au-item-top{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
      .au-item-sub{font-size:12px;color:var(--muted,#8a8f98)}
      .au-badge{font-size:11px;padding:2px 8px;border-radius:999px;background:var(--surface2,#f1f2f4)}
      .au-badge-off{background:#fee2e2;color:#991b1b}
      .au-ok{font-size:13px;color:var(--good,#16a34a);margin:0}
      .au-hint{font-size:12px;color:var(--muted,#8a8f98);margin:0}
      .au-err{font-size:13px;color:var(--bad,#dc2626);text-align:center}
    `}</style>
  );
}
