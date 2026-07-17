import { useState } from "react";
import { supabase } from "../supabaseClient";

// ashrain.out — 개념 검색 (v0.3.3)
// src/components/ConceptSearch.jsx — Home.jsx(v0.3.3)가 개념 탭 상단에서 import 합니다.
//
// 설계 원칙 (토큰 남용 방지):
// - 기본은 "로컬 검색": 제목·부제·단원명 문자열 매칭 — 0원, 즉시, 오프라인 OK
// - AI는 보조 버튼: /api/ai(task:find)가 개념 id 목록"만" 반환 → 여기서 실존 개념만 카드로 렌더
//   AI가 쓴 문장은 화면에 절대 나가지 않음 (자유 텍스트 채널 자체가 없음 = 탈옥해도 얻을 게 없음)
// - 입력 100자 제한 · 대화 이력 없음 · 서버가 계정별 일일 한도 차단(429)

const normTxt = (s) => String(s || "").toLowerCase().replace(/\s+/g, "");

const CSS = `
.cs-wrap { margin:2px 0 16px; }
.cs-bar { display:flex; align-items:center; gap:8px; background:var(--card); border:1px solid var(--bd);
  border-radius:12px; padding:4px 6px 4px 12px; }
.cs-bar span { color:var(--mut); font-size:14px; }
.cs-in { flex:1; min-width:0; background:transparent; border:none; outline:none; color:var(--ink);
  font-size:14.5px; padding:9px 0; }
.cs-x { border:none; background:transparent; color:var(--mut); font-size:15px; cursor:pointer; padding:6px 8px; }
.cs-sec { font-size:12.5px; font-weight:800; color:var(--mut); letter-spacing:.5px; margin:12px 2px 6px; }
.cs-item { display:block; text-decoration:none; background:var(--card); border:1px solid var(--bd);
  border-radius:11px; padding:10px 13px; margin-bottom:6px; }
.cs-item b { display:block; color:var(--ink); font-size:14px; }
.cs-item span { display:block; color:var(--mut); font-size:12px; margin-top:2px; }
.cs-ai { width:100%; margin-top:8px; padding:11px; border-radius:11px; border:1px solid var(--bd);
  background:transparent; color:var(--mut); font-size:13.5px; cursor:pointer; }
.cs-ai.hot { border-color:var(--ac); color:var(--ac); font-weight:800; }
.cs-ai:disabled { opacity:.5; }
.cs-none { color:var(--mut); font-size:13px; text-align:center; padding:14px 0 4px; line-height:1.6; }
`;

export default function ConceptSearch({ uid, concepts, unitNames, say }) {
  const [q, setQ] = useState("");
  const [aiRows, setAiRows] = useState(null);   // null=안 물어봄 | [] = 결과 없음 | rows
  const [busy, setBusy] = useState(false);

  const query = q.trim();

  // ── 로컬 검색: 모든 토큰이 (제목+부제+단원명)에 포함되면 매칭 ──
  let local = [];
  if (query.length >= 1) {
    const tokens = query.split(/\s+/).map(normTxt).filter(Boolean);
    local = concepts
      .map((c) => {
        const title = normTxt(c.title);
        const hay = title + normTxt(c.subtitle) + normTxt(unitNames?.[c.unit_id] || c.unit_id);
        if (!tokens.every((t) => hay.includes(t))) return null;
        const score = title.startsWith(normTxt(query)) ? 3 : tokens.some((t) => title.includes(t)) ? 2 : 1;
        return { c, score };
      })
      .filter(Boolean)
      .sort((a, b) => b.score - a.score || (a.c.sort_order || 0) - (b.c.sort_order || 0))
      .slice(0, 12)
      .map((x) => x.c);
  }

  async function askAi() {
    if (!uid) { say("로그인 후 이용할 수 있어요"); return; }
    setBusy(true);
    setAiRows(null);
    try {
      const { data: sess } = await supabase.auth.getSession();
      const token = sess?.session?.access_token;
      if (!token) throw new Error("세션이 만료됐어요 — 다시 로그인해 주세요");
      const r = await fetch("/api/ai", {
        method: "POST",
        headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
        body: JSON.stringify({ task: "find", query }),
      });
      const j = await r.json();
      if (!r.ok) throw new Error(j?.error || "요청 실패");
      // 서버가 실존 id만 돌려주지만, 여기서도 목록에 있는 개념만 카드로 (이중 안전장치)
      const rows = (j.ids || []).map((id) => concepts.find((c) => c.id === id)).filter(Boolean);
      setAiRows(rows);
    } catch (err) {
      say("검색 실패: " + (err?.message || String(err)));
    }
    setBusy(false);
  }

  function clear() { setQ(""); setAiRows(null); }

  const Card = ({ c, key: _k }) => (
    <a key={c.id} className="cs-item" href={`#/c/${c.id}`}>
      <b>{c.title}</b>
      <span>{unitNames?.[c.unit_id] || c.unit_id}{c.subtitle ? ` · ${c.subtitle}` : ""}</span>
    </a>
  );

  return (
    <div className="cs-wrap">
      <style>{CSS}</style>
      <div className="cs-bar">
        <span>🔍</span>
        <input
          className="cs-in"
          value={q}
          maxLength={100}
          placeholder="개념 검색 — 예: 근의 공식, 인수분해"
          onChange={(e) => { setQ(e.target.value); setAiRows(null); }}
        />
        {q && <button className="cs-x" onClick={clear}>✕</button>}
      </div>

      {query.length >= 1 && (
        <>
          {local.length > 0 && (
            <>
              <p className="cs-sec">검색 결과 {local.length}</p>
              {local.map((c) => <Card key={c.id} c={c} />)}
            </>
          )}
          {local.length === 0 && aiRows === null && !busy && (
            <p className="cs-none">이름으로는 못 찾았어요 — 아래 버튼으로 AI에게 물어보세요.<br />
              (예: "x가 두 개 나오는 방정식 푸는 법"처럼 설명해도 돼요)</p>
          )}
          {query.length >= 2 && (
            <button className={"cs-ai" + (local.length === 0 ? " hot" : "")} disabled={busy} onClick={askAi}>
              {busy ? "⏳ 관련 개념 찾는 중…" : local.length === 0 ? "🤖 AI로 개념 찾기" : "🤖 원하는 게 없나요? AI로 찾기"}
            </button>
          )}
          {aiRows !== null && (
            aiRows.length > 0 ? (
              <>
                <p className="cs-sec">🤖 AI 추천</p>
                {aiRows.map((c) => <Card key={c.id} c={c} />)}
              </>
            ) : (
              <p className="cs-none">관련 개념을 찾지 못했어요 — 수학 개념에 대한 질문인지 확인해 주세요.</p>
            )
          )}
        </>
      )}
    </div>
  );
}
