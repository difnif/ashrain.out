import { useEffect, useState } from "react";
import { listConcepts } from "../lib/concepts";
import { supabase } from "../supabaseClient";

const UNIT_NAMES = { "m1-1": "중1 1학기", "m1-2": "중1 2학기", "m2-1": "중2 1학기", "m2-2": "중2 2학기" };

const CSS = `
.hm-root { min-height: 100vh; padding: 20px 14px 40px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.hm-light { background: #EDEFF2; --ink:#1F2937; --mut:#8A929C; --card:#fff; --bd:#DFE3E8; --ac:#0DA95F; }
.hm-dark  { background: #0B0C0F; --ink:#E2E8F0; --mut:#6B7280; --card:#15171C; --bd:#23262D; --ac:#FFE03C; }
.hm-wrap { max-width: 768px; margin: 0 auto; }
.hm-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-wrap: wrap; margin-bottom: 18px; }
.hm-logo { height: 34px; }
.hm-btns { display: flex; gap: 6px; flex-wrap: wrap; }
.hm-me { display: flex; align-items: center; gap: 5px; }
.hm-me img { width: 20px; height: 20px; border-radius: 9999px; object-fit: cover; }
.hm-btn { background: var(--card); border: 1px solid var(--bd); color: var(--mut); font-size: 12px;
  border-radius: 8px; padding: 6px 12px; cursor: pointer; }
.hm-unit { font-size: 13px; font-weight: 800; color: var(--mut); letter-spacing: 1px; margin: 20px 0 8px; }
.hm-item { display: block; background: var(--card); border: 1px solid var(--bd); border-radius: 12px;
  padding: 14px 16px; margin-bottom: 8px; text-decoration: none; }
.hm-item b { color: var(--ink); font-size: 15px; }
.hm-item span { display: block; color: var(--mut); font-size: 12.5px; margin-top: 2px; }
.hm-empty { color: var(--mut); font-size: 14px; text-align: center; padding: 40px 0; }
`;

export default function Home({ theme, onToggleTheme }) {
  const [concepts, setConcepts] = useState([]);
  const [err, setErr] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const [me, setMe] = useState(null);
  useEffect(() => {
    listConcepts().then(setConcepts).catch(() => setErr("목록을 불러오지 못했어요."));
    supabase.auth.getUser().then(({ data }) =>
      data.user && supabase.from("profiles").select("role, name, avatar_url").eq("id", data.user.id).single()
        .then(({ data: p }) => { setIsAdmin(p?.role === "admin"); setMe(p); }));
  }, []);

  const units = [...new Set(concepts.map((c) => c.unit_id))];
  return (
    <div className={`hm-root hm-${theme}`}>
      <style>{CSS}</style>
      <div className="hm-wrap">
        <div className="hm-head">
          <img className="hm-logo" src="/brand/ashrain_logo.png" alt="ASH RAIN. Out" />
          <div className="hm-btns">
            {isAdmin && <button className="hm-btn" onClick={() => (location.hash = "#/admin/concepts")}>📚 개념 등록</button>}
            {isAdmin && <button className="hm-btn" onClick={() => (location.hash = "#/admin/qna")}>💬 질문 검토</button>}
            <button className="hm-btn hm-me" onClick={() => (location.hash = "#/me")}>
              {me?.avatar_url ? <img src={me.avatar_url} alt="" /> : "👤"} {me?.name || "마이페이지"}
            </button>
            <button className="hm-btn" onClick={onToggleTheme}>{theme === "light" ? "🌙" : "🌧"}</button>
          </div>
        </div>
        {err && <p className="hm-empty">{err}</p>}
        {!err && concepts.length === 0 && <p className="hm-empty">아직 등록된 개념이 없어요. (supabase/seed.sql 실행)</p>}
        {units.map((u) => (
          <div key={u}>
            <p className="hm-unit">{UNIT_NAMES[u] || u}</p>
            {concepts.filter((c) => c.unit_id === u).map((c) => (
              <a key={c.id} className="hm-item" href={`#/c/${c.id}`}>
                <b>{String(c.sort_order).padStart(2, "0")}. {c.title}</b>
                <span>{c.subtitle}</span>
              </a>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
