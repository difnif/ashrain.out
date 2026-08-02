// ashrain.out — 이미지 등록 현황 (v1.0, 관리자 전용)
// 전 개념의 sequence 씬 컷을 훑어 위치/이름/등록여부를 리스트로. 위치 클릭 → 개념 페이지.
import { useEffect, useState } from "react";
import { supabase } from "../supabaseClient";
import { qcode, UNIT_LETTER, UNIT_NAME } from "../lib/qcode";

const CSS = `
.ai-root { min-height: 100vh; padding: 18px 12px 60px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.ai-light { background:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0DA95F; }
.ai-dark  { background:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#FFE03C; }
.ai-wrap { max-width: 720px; margin: 0 auto; }
.ai-top { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.ai-h { color: var(--ink); font-size: 18px; font-weight: 800; margin: 0; flex: 1; }
.ai-back { color: var(--mut); font-size: 13px; cursor: pointer; text-decoration: underline; }
.ai-filters { display: flex; gap: 8px; margin-bottom: 10px; flex-wrap: wrap; align-items: center; }
.ai-sel { background: var(--card); border: 1px solid var(--bd); border-radius: 10px; color: var(--ink); font-size: 13px; padding: 8px 10px; }
.ai-tgl { background: transparent; border: 1px solid var(--bd); border-radius: 999px; color: var(--mut);
  font-size: 12.5px; font-weight: 700; padding: 7px 12px; cursor: pointer; }
.ai-tgl.on { border-color: var(--ac); color: var(--ac); }
.ai-sum { font-size: 12.5px; color: var(--mut); margin: 0 0 10px; }
.ai-row { display: flex; align-items: center; gap: 10px; background: var(--card); border: 1px solid var(--bd);
  border-radius: 10px; padding: 9px 12px; margin-bottom: 6px; }
.ai-code { font-size: 11.5px; font-weight: 800; letter-spacing: .5px; color: var(--ac); cursor: pointer;
  text-decoration: underline; white-space: nowrap; }
.ai-name { flex: 1; min-width: 0; color: var(--ink); font-size: 13.5px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ai-key { font-size: 11px; color: var(--mut); white-space: nowrap; }
.ai-ok { font-size: 13px; font-weight: 800; color: var(--ac); }
.ai-no { font-size: 13px; font-weight: 800; color: #DC2626; }
.ai-empty { color: var(--mut); text-align: center; padding: 36px 0; font-size: 14px; }
`;

export default function AdminImages({ theme = "light" }) {
  const [allowed, setAllowed] = useState(null);
  const [rows, setRows] = useState(null);
  const [f, setF] = useState({ letter: "", onlyMissing: true });

  useEffect(() => {
    (async () => {
      const { data: { user } } = await supabase.auth.getUser();
      const { data: prof } = await supabase.from("profiles").select("role").eq("id", user?.id).maybeSingle();
      if (prof?.role !== "admin") { setAllowed(false); return; }
      setAllowed(true);
      const { data: cs } = await supabase.from("concepts").select("id, title, blocks");
      const targets = []; // { concept_id, title, block_id, scene }
      for (const c of cs || []) {
        for (const b of c.blocks || []) {
          for (const s of b.figure?.scenes || []) {
            if (s.anim !== "diagram" && s.count > 0) targets.push({ concept_id: c.id, title: c.title, block_id: b.id, scene: s });
          }
        }
      }
      // 블록 폴더 단위로 storage 목록 (중복 제거)
      const dirs = [...new Set(targets.map((t) => `${t.concept_id}/${t.block_id}`))];
      const have = {};
      await Promise.all(dirs.map(async (d) => {
        const { data } = await supabase.storage.from("figures").list(d, { limit: 100 });
        have[d] = new Set((data || []).map((x) => x.name.replace(/\.[^.]+$/, "")));
      }));
      const out = [];
      for (const t of targets) {
        const dir = `${t.concept_id}/${t.block_id}`;
        for (let i = 1; i <= t.scene.count; i++) {
          const key = `${t.scene.id}${i}`;
          out.push({
            concept_id: t.concept_id, title: t.title, block_id: t.block_id, key,
            code: qcode(t.concept_id, t.block_id),
            name: t.scene.cuts?.[i - 1] || `${t.scene.label} ${i}컷`,
            ok: have[dir]?.has(key) || false,
          });
        }
      }
      setRows(out);
    })();
  }, []);

  if (allowed === false) return (
    <div className={`ai-root ai-${theme}`}><style>{CSS}</style><p className="ai-empty">관리자 전용 화면입니다.</p></div>
  );

  const shown = (rows || []).filter((r) =>
    (!f.letter || r.code.startsWith(f.letter)) && (!f.onlyMissing || !r.ok));
  const done = (rows || []).filter((r) => r.ok).length;

  return (
    <div className={`ai-root ai-${theme}`}>
      <style>{CSS}</style>
      <div className="ai-wrap">
        <div className="ai-top">
          <h1 className="ai-h">🖼 이미지 등록 현황</h1>
          <span className="ai-back" onClick={() => (location.hash = "")}>← 홈</span>
        </div>
        <div className="ai-filters">
          <select className="ai-sel" value={f.letter} onChange={(e) => setF((s) => ({ ...s, letter: e.target.value }))}>
            <option value="">전체 과정</option>
            {Object.entries(UNIT_LETTER).map(([u, l]) => <option key={l} value={l}>{l} · {UNIT_NAME[u]}</option>)}
          </select>
          <button className={"ai-tgl" + (f.onlyMissing ? " on" : "")}
            onClick={() => setF((s) => ({ ...s, onlyMissing: !s.onlyMissing }))}>미등록만 보기</button>
        </div>
        {rows === null ? <p className="ai-empty">불러오는 중…</p> : (
          <>
            <p className="ai-sum">전체 {rows.length}컷 중 등록 {done} · 미등록 {rows.length - done}</p>
            {shown.length === 0 && <p className="ai-empty">{f.onlyMissing ? "미등록 컷이 없어요 🎉" : "대상 컷이 없어요"}</p>}
            {shown.map((r, i) => (
              <div key={i} className="ai-row">
                <span className="ai-code" onClick={() => (location.hash = `#/c/${encodeURIComponent(r.concept_id)}`)}>{r.code}</span>
                <span className="ai-name">{r.name}</span>
                <span className="ai-key">{r.key}</span>
                <span className={r.ok ? "ai-ok" : "ai-no"}>{r.ok ? "O" : "X"}</span>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
}
