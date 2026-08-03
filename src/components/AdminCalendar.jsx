// ashrain.out — 시험 일정 캘린더 (v1.0, 관리자 전용)
// 날짜 클릭 → 제목·디데이 등록. dday=true인 가장 가까운 미래 일정이 홈 로고를 D-n으로 바꿉니다.
import { useEffect, useState, useCallback } from "react";
import { supabase } from "../supabaseClient";

const CSS = `
.ac-root { min-height: 100vh; padding: 18px 12px 60px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.ac-light { background:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0DA95F; --in:#F4F6F8; }
.ac-dark  { background:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#FFE03C; --in:#101116; }
.ac-wrap { max-width: 560px; margin: 0 auto; }
.ac-top { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.ac-h { color: var(--ink); font-size: 18px; font-weight: 800; margin: 0; flex: 1; }
.ac-back { color: var(--mut); font-size: 13px; cursor: pointer; text-decoration: underline; }
.ac-mon { display: flex; align-items: center; justify-content: center; gap: 14px; margin-bottom: 10px; }
.ac-mt { color: var(--ink); font-size: 16px; font-weight: 800; min-width: 110px; text-align: center; }
.ac-nav { background: var(--card); border: 1px solid var(--bd); border-radius: 8px; color: var(--ink);
  font-size: 14px; padding: 5px 11px; cursor: pointer; }
.ac-cal { background: var(--card); border: 1px solid var(--bd); border-radius: 14px; padding: 10px; }
.ac-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 3px; }
.ac-dow { text-align: center; font-size: 11px; font-weight: 800; color: var(--mut); padding: 4px 0; }
.ac-day { position: relative; aspect-ratio: 1; border-radius: 9px; border: 1px solid transparent;
  background: transparent; cursor: pointer; font-size: 13px; color: var(--ink); }
.ac-day:hover { background: var(--in); }
.ac-day.out { opacity: .3; }
.ac-day.today { border-color: var(--ac); font-weight: 800; }
.ac-day.sel { background: var(--ac); color: #fff; font-weight: 800; }
.ac-dark .ac-day.sel { color: #0B0C0F; }
.ac-dot { position: absolute; left: 50%; transform: translateX(-50%); bottom: 5px; width: 5px; height: 5px;
  border-radius: 999px; background: var(--ac); }
.ac-dot.dd { background: #EF4444; }
.ac-form { display: flex; gap: 7px; margin-top: 12px; align-items: center; flex-wrap: wrap; }
.ac-in { flex: 1; min-width: 160px; background: var(--in); border: 1px solid var(--bd); border-radius: 10px;
  color: var(--ink); font-size: 13.5px; padding: 10px 12px; outline: none; }
.ac-chk { display: flex; align-items: center; gap: 5px; font-size: 12.5px; color: var(--ink); font-weight: 700; }
.ac-add { background: var(--ac); border: none; border-radius: 10px; color: #fff; font-size: 13px;
  font-weight: 800; padding: 10px 16px; cursor: pointer; }
.ac-dark .ac-add { color: #0B0C0F; }
.ac-list { margin-top: 14px; }
.ac-row { display: flex; align-items: center; gap: 9px; background: var(--card); border: 1px solid var(--bd);
  border-radius: 10px; padding: 9px 12px; margin-bottom: 6px; }
.ac-rd { font-size: 12px; font-weight: 800; color: var(--mut); white-space: nowrap; }
.ac-rt { flex: 1; font-size: 13.5px; color: var(--ink); }
.ac-dd { font-size: 10.5px; font-weight: 800; color: #EF4444; border: 1px solid #EF4444;
  border-radius: 5px; padding: 1px 5px; }
.ac-del { background: none; border: none; color: var(--mut); font-size: 13px; cursor: pointer; }
.ac-empty { color: var(--mut); text-align: center; padding: 24px 0 10px; font-size: 13px; }
`;

const pad = (n) => String(n).padStart(2, "0");
const iso = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;

export default function AdminCalendar({ theme = "light" }) {
  const [allowed, setAllowed] = useState(null);
  const [cur, setCur] = useState(() => { const d = new Date(); return new Date(d.getFullYear(), d.getMonth(), 1); });
  const [events, setEvents] = useState([]);
  const [sel, setSel] = useState(iso(new Date()));
  const [title, setTitle] = useState("");
  const [ddayOn, setDdayOn] = useState(true);

  useEffect(() => {
    supabase.auth.getUser().then(async ({ data }) => {
      const { data: p } = await supabase.from("profiles").select("role").eq("id", data?.user?.id).maybeSingle();
      setAllowed(p?.role === "admin");
    });
  }, []);

  const load = useCallback(async () => {
    const from = iso(cur);
    const to = iso(new Date(cur.getFullYear(), cur.getMonth() + 1, 0));
    const { data } = await supabase.from("events").select("*").gte("date", from).lte("date", to).order("date");
    setEvents(data || []);
  }, [cur]);
  useEffect(() => { if (allowed) load(); }, [allowed, load]);

  const add = async () => {
    if (!title.trim()) return;
    const { error } = await supabase.from("events").insert({ date: sel, title: title.trim(), dday: ddayOn });
    if (error) { alert("저장 실패: " + error.message + " (2026-08_events.sql 실행 여부 확인)"); return; }
    setTitle(""); load();
  };
  const del = async (id) => { await supabase.from("events").delete().eq("id", id); load(); };

  if (allowed === false) return (
    <div className={`ac-root ac-${theme}`}><style>{CSS}</style><p className="ac-empty">관리자 전용 화면입니다.</p></div>
  );

  const y = cur.getFullYear(), m = cur.getMonth();
  const first = new Date(y, m, 1), startDow = first.getDay();
  const daysIn = new Date(y, m + 1, 0).getDate();
  const cells = [];
  for (let i = 0; i < startDow; i++) cells.push(null);
  for (let d = 1; d <= daysIn; d++) cells.push(d);
  const todayIso = iso(new Date());
  const evOf = (dstr) => events.filter((e) => e.date === dstr);

  return (
    <div className={`ac-root ac-${theme}`}>
      <style>{CSS}</style>
      <div className="ac-wrap">
        <div className="ac-top">
          <h1 className="ac-h">🗓 시험 일정</h1>
          <span className="ac-back" onClick={() => (location.hash = "")}>← 홈</span>
        </div>
        <div className="ac-mon">
          <button className="ac-nav" onClick={() => setCur(new Date(y, m - 1, 1))}>◀</button>
          <span className="ac-mt">{y}년 {m + 1}월</span>
          <button className="ac-nav" onClick={() => setCur(new Date(y, m + 1, 1))}>▶</button>
        </div>
        <div className="ac-cal">
          <div className="ac-grid">
            {["일","월","화","수","목","금","토"].map((d) => <div key={d} className="ac-dow">{d}</div>)}
            {cells.map((d, i) => {
              if (d === null) return <div key={"e" + i} />;
              const dstr = `${y}-${pad(m + 1)}-${pad(d)}`;
              const evs = evOf(dstr);
              return (
                <button key={dstr}
                  className={"ac-day" + (dstr === todayIso ? " today" : "") + (dstr === sel ? " sel" : "")}
                  onClick={() => setSel(dstr)}>
                  {d}
                  {evs.length > 0 && <span className={"ac-dot" + (evs.some((e) => e.dday) ? " dd" : "")} />}
                </button>
              );
            })}
          </div>
          <div className="ac-form">
            <span style={{ fontSize: 12.5, fontWeight: 800, color: "var(--mut)" }}>{sel.slice(5).replace("-", "/")}</span>
            <input className="ac-in" placeholder="일정 제목 (예: 1학기 기말고사)" value={title}
              onChange={(e) => setTitle(e.target.value)} onKeyDown={(e) => e.key === "Enter" && add()} />
            <label className="ac-chk"><input type="checkbox" checked={ddayOn} onChange={(e) => setDdayOn(e.target.checked)} /> 디데이</label>
            <button className="ac-add" onClick={add}>추가</button>
          </div>
        </div>
        <div className="ac-list">
          {events.length === 0 && <p className="ac-empty">이 달에 등록된 일정이 없어요</p>}
          {events.map((e) => (
            <div key={e.id} className="ac-row">
              <span className="ac-rd">{e.date.slice(5).replace("-", "/")}</span>
              <span className="ac-rt">{e.title}</span>
              {e.dday && <span className="ac-dd">D-DAY</span>}
              <button className="ac-del" onClick={() => del(e.id)}>🗑</button>
            </div>
          ))}
        </div>
        <p className="ac-empty" style={{ paddingTop: 14 }}>
          디데이로 체크된 가장 가까운 일정이 유저 홈 로고 자리에 D-n으로 표시돼요.
        </p>
      </div>
    </div>
  );
}
