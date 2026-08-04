// src/components/AdminContentStatus.jsx
// 콘텐츠 적용 현황판 — contentAudit.json(전수 감사 스냅샷)을 렌더링
// 의존성: React만. 스타일 인라인(테일윈드/외부 CSS 불필요).
import React, { useMemo, useState } from 'react';
import audit from '../data/contentAudit.json';

const UNIT_NAMES = {
  'm1-1': '중1 1학기', 'm1-2': '중1 2학기', 'm2-1': '중2 1학기', 'm2-2': '중2 2학기',
  'm3-1': '중3 1학기', 'm3-2': '중3 2학기', 'h1-1': '고1 상', 'h1-2': '고1 하',
  'h2-1': '고2 대수', 'h2-2': '고2 미적분1', 'h3-1': '고3 미적분2', 'h3-2': '고3 확률과 통계',
  'h3-3': '고3 기하',
};
const MARK = {
  O: { txt: 'O', bg: '#dcfce7', fg: '#15803d' },
  '△': { txt: '△', bg: '#fef3c7', fg: '#b45309' },
  X: { txt: '·', bg: '#fee2e2', fg: '#b91c1c' },
};
const S = {
  wrap: { padding: '24px 20px 60px', maxWidth: 1280, margin: '0 auto', fontFamily: 'inherit', color: '#1f2937' },
  h1: { fontSize: 22, fontWeight: 800, margin: '0 0 4px' },
  sub: { fontSize: 13, color: '#6b7280', marginBottom: 18 },
  strip: { display: 'flex', flexWrap: 'wrap', gap: 10, marginBottom: 18 },
  chip: (active) => ({
    border: '1px solid #e5e7eb', borderRadius: 10, padding: '8px 12px', minWidth: 108,
    cursor: 'pointer', background: active ? '#eef2ff' : '#fff',
    boxShadow: active ? 'inset 0 0 0 2px #6366f1' : 'none',
  }),
  chipLabel: { fontSize: 12, fontWeight: 700, marginBottom: 4 },
  bar: { height: 6, borderRadius: 3, background: '#f3f4f6', overflow: 'hidden' },
  barIn: (p) => ({ height: '100%', width: `${p}%`, background: p >= 80 ? '#22c55e' : p >= 40 ? '#f59e0b' : '#ef4444' }),
  ctrl: { display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap', marginBottom: 12 },
  select: { padding: '7px 10px', border: '1px solid #d1d5db', borderRadius: 8, fontSize: 13, background: '#fff' },
  input: { padding: '7px 10px', border: '1px solid #d1d5db', borderRadius: 8, fontSize: 13, minWidth: 200 },
  tblWrap: { overflow: 'auto', border: '1px solid #e5e7eb', borderRadius: 12, maxHeight: '70vh' },
  th: { position: 'sticky', top: 0, background: '#f9fafb', fontSize: 12, fontWeight: 700,
        padding: '10px 8px', borderBottom: '1px solid #e5e7eb', whiteSpace: 'nowrap', zIndex: 2 },
  tdName: { padding: '8px 10px', fontSize: 13, borderBottom: '1px solid #f3f4f6', whiteSpace: 'nowrap' },
  cell: (m) => ({ textAlign: 'center', fontSize: 12, fontWeight: 800, borderBottom: '1px solid #f3f4f6',
                  background: m.bg, color: m.fg, padding: '6px 4px', minWidth: 44 }),
  note: { fontSize: 12, color: '#6b7280', marginTop: 10, lineHeight: 1.7 },
};

export default function AdminContentStatus() {
  const { items, labels, concepts, total, generated, source, unitStats } = audit;
  const [unit, setUnit] = useState('all');
  const [q, setQ] = useState('');
  const [gapItem, setGapItem] = useState(null); // 항목 클릭 → 그 항목의 빈칸(X/△)만 보기

  const units = useMemo(
    () => Object.keys(unitStats).sort(),
    [unitStats]
  );
  const scoped = useMemo(
    () => concepts.filter((c) => unit === 'all' || c.unit === unit),
    [concepts, unit]
  );
  const pct = useMemo(() => {
    const out = {};
    items.forEach((k) => {
      const o = scoped.filter((c) => c.items[k] === 'O').length;
      out[k] = scoped.length ? Math.round((o * 100) / scoped.length) : 0;
    });
    return out;
  }, [items, scoped]);

  const rows = useMemo(() => {
    let r = scoped;
    if (q.trim()) {
      const t = q.trim();
      r = r.filter((c) => c.id.includes(t) || c.title.includes(t));
    }
    if (gapItem) r = r.filter((c) => c.items[gapItem] !== 'O');
    return r;
  }, [scoped, q, gapItem]);

  return (
    <div style={S.wrap}>
      <h1 style={S.h1}>📋 콘텐츠 적용 현황판</h1>
      <div style={S.sub}>
        총 {total}개 개념 · 감사 기준 {generated} · {source}
        {unit !== 'all' && ` · 현재 범위: ${UNIT_NAMES[unit] || unit} (${scoped.length}개)`}
      </div>

      <div style={S.strip}>
        {items.map((k) => (
          <div key={k} style={S.chip(gapItem === k)} onClick={() => setGapItem(gapItem === k ? null : k)}
               title="클릭하면 이 항목의 빈칸(△·X)만 모아 봅니다">
            <div style={S.chipLabel}>{labels[k]}</div>
            <div style={{ fontSize: 12, color: '#374151', marginBottom: 4 }}>{pct[k]}%</div>
            <div style={S.bar}><div style={S.barIn(pct[k])} /></div>
          </div>
        ))}
      </div>

      <div style={S.ctrl}>
        <select style={S.select} value={unit} onChange={(e) => setUnit(e.target.value)}>
          <option value="all">전체 학기</option>
          {units.map((u) => <option key={u} value={u}>{UNIT_NAMES[u] || u}</option>)}
        </select>
        <input style={S.input} placeholder="개념 ID·제목 검색" value={q} onChange={(e) => setQ(e.target.value)} />
        {gapItem && (
          <button style={{ ...S.select, cursor: 'pointer' }} onClick={() => setGapItem(null)}>
            "{labels[gapItem]}" 빈칸 모드 해제 ✕
          </button>
        )}
        <span style={{ fontSize: 12, color: '#6b7280' }}>{rows.length}개 표시</span>
      </div>

      <div style={S.tblWrap}>
        <table style={{ borderCollapse: 'collapse', width: '100%' }}>
          <thead>
            <tr>
              <th style={{ ...S.th, textAlign: 'left', left: 0, zIndex: 3 }}>개념</th>
              {items.map((k) => (
                <th key={k} style={{ ...S.th, cursor: 'pointer' }}
                    onClick={() => setGapItem(gapItem === k ? null : k)}>{labels[k]}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((c) => (
              <tr key={c.id}>
                <td style={S.tdName}>
                  <b>{c.id}</b>&nbsp; {c.title}
                  <span style={{ color: '#9ca3af', fontSize: 11 }}> · {UNIT_NAMES[c.unit] || c.unit}</span>
                </td>
                {items.map((k) => {
                  const m = MARK[c.items[k]] || MARK.X;
                  return <td key={k} style={S.cell(m)}>{m.txt}</td>;
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={S.note}>
        판정 기준 — <b>O</b> 해당 요소가 정식 형식으로 존재 · <b>△</b> 부분 적용(예: 재회·예고 문구는 있으나
        전용 슬롯 없음, 한자 표기만 있고 파자 없음) · <b>·</b> 미적용. 항목 칩이나 열 제목을 클릭하면 그 항목의
        빈칸만 모아 보는 <b>빈칸 채우기 모드</b>가 됩니다. 콘텐츠가 갱신되면 감사 스크립트로
        contentAudit.json만 재생성해 교체 업로드하면 반영돼요.
      </div>
    </div>
  );
}
