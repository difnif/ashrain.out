import { useEffect, useRef, useState } from "react";
import { listConcepts } from "../lib/concepts";
import { supabase } from "../supabaseClient";

// ashrain.out — 홈(개념 목록) 화면 (patch v0.1.8)
// 이 파일을 src/components/Home.jsx 에 덮어쓰고,
// 동봉된 2026-07_fav_categories.sql 을 Supabase SQL Editor에서 1회 실행하면 됩니다.
//
// [모든 유저 공통]
// - 학년 → 학기 → 대단원 3단계 트리, 기본은 전부 접힘, 여러 개 동시 열기 가능
// [유저별 개인 설정 — 계정 단위 저장, 다른 유저에게 영향 없음]
// - 대단원 우측 별표로 즐겨찾기(최대 10개), 상단 즐겨찾기 탭에 칩으로 표시
// - 10개 초과 등록 시 팝업에서 해제할 항목 선택 또는 등록 취소
// - 칩을 꾹 누르면 편집 모드: 노출 순서 이동 + 색상 변경 (전체 트리에도 색 반영)
// - 즐겨찾기 해제 시 색상은 기본값으로 복귀. 트리 구조 자체는 절대 변하지 않음.

const UNIT_NAMES = { "m1-1": "중1 1학기", "m1-2": "중1 2학기", "m2-1": "중2 1학기", "m2-2": "중2 2학기" };

// 대단원 구성: [제목, 시작 번호, 끝 번호] — 표준 교육과정 기준
const CHAPTERS = {
  "m1-1": [
    ["소인수분해", 1, 8],
    ["정수와 유리수", 9, 18],
    ["문자와 식", 19, 28],
    ["좌표평면과 그래프", 29, 34],
  ],
  "m1-2": [
    ["기본 도형과 작도", 1, 6],
    ["평면도형", 7, 11],
    ["입체도형", 12, 16],
    ["자료의 정리와 해석", 17, 21],
  ],
  "m2-1": [
    ["수와 식의 계산", 1, 6],
    ["부등식과 연립방정식", 7, 15],
    ["일차함수", 16, 23],
  ],
  "m2-2": [
    ["도형의 성질", 1, 4],
    ["도형의 닮음과 피타고라스 정리", 5, 11],
    ["확률", 12, 14],
  ],
};
const chaptersOf = (unit) => CHAPTERS[unit] || [["전체", 1, 999]];

// 즐겨찾기 색상 팔레트 (첫 항목 null = 기본색)
const PALETTE = [null, "#F472B6", "#F87171", "#F59E0B", "#34D399", "#60A5FA", "#A78BFA"];

const CSS = `
.hm-root { min-height: 100vh; padding: 20px 14px 40px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.hm-light { background: #EDEFF2; --ink:#1F2937; --mut:#8A929C; --card:#fff; --bd:#DFE3E8; --ac:#0DA95F; }
.hm-dark  { background: #0B0C0F; --ink:#E2E8F0; --mut:#6B7280; --card:#15171C; --bd:#23262D; --ac:#FFE03C; }
.hm-wrap { max-width: 768px; margin: 0 auto; }
.hm-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; flex-wrap: wrap; gap: 8px; }
.hm-logo { height: 34px; }
.hm-btns { display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }
.hm-btn { background: var(--card); border: 1px solid var(--bd); color: var(--mut); font-size: 12px;
  border-radius: 8px; padding: 6px 12px; cursor: pointer; }
.hm-me img { width: 18px; height: 18px; border-radius: 50%; vertical-align: -4px; margin-right: 3px; }
.hm-empty { color: var(--mut); font-size: 14px; text-align: center; padding: 40px 0; }

/* 즐겨찾기 탭 */
.hm-sec { font-size: 13px; font-weight: 800; color: var(--mut); letter-spacing: 1px; margin: 4px 0 8px; }
.hm-favwrap { background: var(--card); border: 1px solid var(--bd); border-radius: 14px; padding: 12px 14px; margin-bottom: 14px; }
.hm-chips { display: flex; flex-wrap: wrap; gap: 8px; }
.hm-chip { border: 1px solid var(--bd); background: transparent; color: var(--ink); border-radius: 999px;
  padding: 7px 12px; font-size: 13px; cursor: pointer; user-select: none; -webkit-user-select: none; touch-action: manipulation; }
.hm-chip small { color: var(--mut); margin-right: 4px; font-size: 11px; }
.hm-chip.on { border-color: var(--ac); box-shadow: 0 0 0 1px var(--ac) inset; }
.hm-hint { color: var(--mut); font-size: 11.5px; margin: 9px 2px 0; }
.hm-panel { margin-top: 11px; border-top: 1px dashed var(--bd); padding-top: 11px; }
.hm-ptitle { font-size: 12.5px; color: var(--mut); margin: 0 0 8px; }

/* 편집 모드 */
.hm-erow { display: flex; align-items: center; gap: 8px; padding: 8px 0; border-bottom: 1px dashed var(--bd); }
.hm-erow:last-of-type { border-bottom: none; }
.hm-ebtn { background: var(--card); border: 1px solid var(--bd); color: var(--ink); border-radius: 8px;
  width: 30px; height: 30px; cursor: pointer; font-size: 12px; }
.hm-ebtn:disabled { opacity: .3; }
.hm-ename { flex: 1; font-size: 13.5px; color: var(--ink); min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.hm-ename small { color: var(--mut); margin-right: 4px; }
.hm-dots { display: flex; gap: 5px; }
.hm-dot { width: 20px; height: 20px; border-radius: 50%; border: 2px solid var(--bd); cursor: pointer; padding: 0; background: var(--card); }
.hm-dot.sel { border-color: var(--ink); }
.hm-done { margin-top: 12px; width: 100%; padding: 9px; border-radius: 10px; border: 1px solid var(--ac);
  background: transparent; color: var(--ac); font-weight: 700; cursor: pointer; font-size: 13.5px; }

/* 트리 */
.hm-row { display: flex; align-items: center; gap: 8px; background: var(--card); border: 1px solid var(--bd);
  border-radius: 12px; padding: 12px 14px; margin-bottom: 8px; cursor: pointer; color: var(--ink);
  user-select: none; -webkit-user-select: none; }
.hm-car { color: var(--mut); font-size: 12px; width: 13px; flex: none; }
.hm-tw { flex: 1; font-weight: 700; font-size: 14.5px; min-width: 0; }
.hm-cnt { color: var(--mut); font-size: 12px; flex: none; }
.hm-lv2 { margin-left: 12px; }
.hm-lv3 { margin-left: 24px; }
.hm-lv3 .hm-row { border-left: 3px solid var(--bd); }
.hm-star { background: none; border: none; font-size: 18px; line-height: 1; cursor: pointer; color: var(--mut); padding: 2px 4px; flex: none; }
.hm-star.on { color: var(--ac); }

/* 개념 링크 */
.hm-list { margin: 2px 0 12px 36px; }
.hm-item { display: block; background: var(--card); border: 1px solid var(--bd); border-radius: 12px;
  padding: 14px 16px; margin-bottom: 8px; text-decoration: none; }
.hm-item b { color: var(--ink); font-size: 15px; }
.hm-item span { display: block; color: var(--mut); font-size: 12.5px; margin-top: 2px; }
.hm-small { color: var(--mut); font-size: 12.5px; padding: 6px 2px; }

/* 팝업(즐겨찾기 초과) */
.hm-modal-bg { position: fixed; inset: 0; background: rgba(0,0,0,.45); display: flex; align-items: center;
  justify-content: center; z-index: 50; padding: 20px; }
.hm-modal { background: var(--card); border: 1px solid var(--bd); border-radius: 16px; max-width: 420px;
  width: 100%; padding: 18px; color: var(--ink); max-height: 80vh; overflow-y: auto; }
.hm-modal h3 { margin: 0 0 6px; font-size: 16px; }
.hm-modal p { color: var(--mut); font-size: 12.5px; margin: 0 0 10px; }
.hm-mrow { display: flex; align-items: center; gap: 9px; padding: 7px 0; font-size: 14px; }
.hm-mdot { width: 12px; height: 12px; border-radius: 50%; flex: none; }
.hm-mbtns { display: flex; gap: 8px; margin-top: 14px; }
.hm-mbtn { flex: 1; padding: 9px; border-radius: 10px; border: 1px solid var(--bd); background: transparent;
  color: var(--ink); cursor: pointer; font-size: 13.5px; }
.hm-mbtn.pri { border-color: var(--ac); color: var(--ac); font-weight: 700; }
.hm-mbtn:disabled { opacity: .4; }

.hm-toast { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); background: var(--ink);
  color: var(--card); padding: 9px 16px; border-radius: 999px; font-size: 13px; z-index: 60; white-space: nowrap; }
`;

export default function Home({ theme, onToggleTheme }) {
  const [concepts, setConcepts] = useState([]);
  const [err, setErr] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const [me, setMe] = useState(null);
  const [uid, setUid] = useState(null);

  const [open, setOpen] = useState(() => new Set()); // 기본: 전부 접힘
  const [favs, setFavs] = useState([]);              // [{cat_id, position, color}]
  const [selCat, setSelCat] = useState(null);        // 즐겨찾기 탭에서 열어 둔 카테고리
  const [editMode, setEditMode] = useState(false);
  const [pending, setPending] = useState(null);      // 10개 초과 시 등록 대기 중인 catId
  const [pick, setPick] = useState(() => new Set()); // 팝업에서 해제 선택
  const [toast, setToast] = useState("");
  const lp = useRef({ t: null, fired: false });

  useEffect(() => {
    listConcepts().then(setConcepts).catch(() => setErr("목록을 불러오지 못했어요."));
    supabase.auth.getUser().then(async ({ data }) => {
      if (!data.user) return;
      setUid(data.user.id);
      const { data: p } = await supabase.from("profiles")
        .select("name, avatar_url, role").eq("id", data.user.id).single();
      if (p) { setMe(p); setIsAdmin(p.role === "admin"); }
      const { data: f, error } = await supabase.from("user_fav_categories")
        .select("cat_id, position, color").eq("user_id", data.user.id).order("position");
      if (!error && f) setFavs(f);
    });
  }, []);

  function say(msg) { setToast(msg); setTimeout(() => setToast(""), 2000); }

  // ── 트리 헬퍼 ──
  const units = [...new Set(concepts.map((c) => c.unit_id))].sort();
  const grades = [...new Set(units.map((u) => u.slice(0, 2)))].sort();
  const semestersOf = (g) => units.filter((u) => u.startsWith(g + "-"));
  const inUnit = (u) => concepts.filter((c) => c.unit_id === u);
  const inChapter = (u, ch) =>
    inUnit(u).filter((c) => c.sort_order >= ch[1] && c.sort_order <= ch[2])
      .sort((a, b) => a.sort_order - b.sort_order);
  const favMap = Object.fromEntries(favs.map((f) => [f.cat_id, f]));
  function catInfo(catId) {
    const [unit, idx] = catId.split(":");
    const ch = chaptersOf(unit)[+idx];
    return { unit, title: ch ? ch[0] : catId, short: unit.replace("m", ""), ch };
  }
  function toggleOpen(key) {
    setOpen((prev) => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });
  }

  // ── 즐겨찾기 ──
  async function toggleFav(catId) {
    if (!uid) { say("로그인하면 즐겨찾기를 쓸 수 있어요"); return; }
    const ex = favMap[catId];
    if (ex) {
      setFavs(favs.filter((f) => f.cat_id !== catId));   // 해제 → 색상도 함께 기본값 복귀
      if (selCat === catId) setSelCat(null);
      const { error } = await supabase.from("user_fav_categories")
        .delete().eq("user_id", uid).eq("cat_id", catId);
      if (error) say("해제 실패: " + error.message);
    } else if (favs.length >= 10) {
      setPending(catId); setPick(new Set());             // 초과 → 팝업
    } else {
      const row = { cat_id: catId, position: favs.length ? Math.max(...favs.map((f) => f.position)) + 1 : 0, color: null };
      setFavs([...favs, row]);
      const { error } = await supabase.from("user_fav_categories").insert({ ...row, user_id: uid });
      if (error) { setFavs(favs); say("저장 실패 — SQL(2026-07_fav_categories.sql) 실행 여부를 확인해 주세요"); }
    }
  }

  async function confirmSwap() {
    const del = [...pick];
    const rest = favs.filter((f) => !pick.has(f.cat_id));
    const row = { cat_id: pending, position: rest.length ? Math.max(...rest.map((f) => f.position)) + 1 : 0, color: null };
    setFavs([...rest, row]);
    setPending(null);
    if (selCat && del.includes(selCat)) setSelCat(null);
    await supabase.from("user_fav_categories").delete().eq("user_id", uid).in("cat_id", del);
    const { error } = await supabase.from("user_fav_categories").insert({ ...row, user_id: uid });
    if (error) say("저장 실패: " + error.message);
  }

  async function move(i, dir) {
    const j = i + dir;
    if (j < 0 || j >= favs.length) return;
    const a = { ...favs[i] }, b = { ...favs[j] };
    const pa = a.position; a.position = b.position; b.position = pa;
    const next = [...favs]; next[i] = b; next[j] = a;
    setFavs(next);
    await supabase.from("user_fav_categories").upsert([
      { user_id: uid, cat_id: a.cat_id, position: a.position, color: a.color },
      { user_id: uid, cat_id: b.cat_id, position: b.position, color: b.color },
    ]);
  }

  async function setColor(catId, color) {
    setFavs(favs.map((f) => (f.cat_id === catId ? { ...f, color } : f)));
    await supabase.from("user_fav_categories").update({ color }).eq("user_id", uid).eq("cat_id", catId);
  }

  // 칩 꾹 누르기 → 편집 모드
  function chipDown() {
    lp.current.fired = false;
    lp.current.t = setTimeout(() => {
      lp.current.fired = true;
      setSelCat(null);
      setEditMode(true);
      if (navigator.vibrate) navigator.vibrate(15);
    }, 500);
  }
  function chipCancel() { clearTimeout(lp.current.t); }
  function chipUp(catId) {
    clearTimeout(lp.current.t);
    if (!lp.current.fired && !editMode) setSelCat((s) => (s === catId ? null : catId));
  }

  const selInfo = selCat ? catInfo(selCat) : null;
  const selList = selInfo?.ch ? inChapter(selInfo.unit, selInfo.ch) : [];

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
        {!err && concepts.length === 0 && <p className="hm-empty">아직 등록된 개념이 없어요.</p>}

        {/* ── 즐겨찾기 탭 (개인 설정) ── */}
        {uid && favs.length > 0 && (
          <div className="hm-favwrap" onContextMenu={(e) => e.preventDefault()}>
            <p className="hm-sec">⭐ 즐겨찾기</p>

            {!editMode && (
              <>
                <div className="hm-chips">
                  {favs.map((f) => {
                    const info = catInfo(f.cat_id);
                    return (
                      <button
                        key={f.cat_id}
                        className={"hm-chip" + (selCat === f.cat_id ? " on" : "")}
                        style={f.color ? { background: f.color + "22", borderColor: f.color } : null}
                        onPointerDown={chipDown}
                        onPointerUp={() => chipUp(f.cat_id)}
                        onPointerMove={chipCancel}
                        onPointerLeave={chipCancel}
                      >
                        <small>{info.short}</small>{info.title}
                      </button>
                    );
                  })}
                </div>
                <p className="hm-hint">칩을 누르면 개념이 펼쳐지고, 꾹 누르면 순서·색상을 편집할 수 있어요.</p>
                {selCat && selInfo && (
                  <div className="hm-panel">
                    <p className="hm-ptitle">{UNIT_NAMES[selInfo.unit] || selInfo.unit} · {selInfo.title}</p>
                    {selList.map((c) => (
                      <a key={c.id} className="hm-item" href={`#/c/${c.id}`}>
                        <b>{String(c.sort_order).padStart(2, "0")}. {c.title}</b>
                        <span>{c.subtitle}</span>
                      </a>
                    ))}
                    {selList.length === 0 && <p className="hm-small">이 단원에는 아직 개념이 없어요.</p>}
                  </div>
                )}
              </>
            )}

            {editMode && (
              <>
                {favs.map((f, i) => {
                  const info = catInfo(f.cat_id);
                  return (
                    <div key={f.cat_id} className="hm-erow">
                      <button className="hm-ebtn" onClick={() => move(i, -1)} disabled={i === 0}>▲</button>
                      <button className="hm-ebtn" onClick={() => move(i, 1)} disabled={i === favs.length - 1}>▼</button>
                      <span className="hm-ename"><small>{info.short}</small>{info.title}</span>
                      <div className="hm-dots">
                        {PALETTE.map((col) => (
                          <button
                            key={col || "def"}
                            className={"hm-dot" + ((f.color || null) === col ? " sel" : "")}
                            style={col ? { background: col, borderColor: col } : null}
                            title={col ? "" : "기본색"}
                            onClick={() => setColor(f.cat_id, col)}
                          />
                        ))}
                      </div>
                    </div>
                  );
                })}
                <button className="hm-done" onClick={() => setEditMode(false)}>편집 완료</button>
              </>
            )}
          </div>
        )}

        {/* ── 전체 트리: 학년 → 학기 → 대단원 (모든 유저 공통, 기본 접힘) ── */}
        {grades.map((g) => (
          <div key={g}>
            <div className="hm-row" onClick={() => toggleOpen(g)}>
              <span className="hm-car">{open.has(g) ? "▾" : "▸"}</span>
              <span className="hm-tw">중{g[1]}</span>
              <span className="hm-cnt">{semestersOf(g).reduce((s, u) => s + inUnit(u).length, 0)}개</span>
            </div>

            {open.has(g) && semestersOf(g).map((u) => (
              <div key={u} className="hm-lv2">
                <div className="hm-row" onClick={() => toggleOpen(u)}>
                  <span className="hm-car">{open.has(u) ? "▾" : "▸"}</span>
                  <span className="hm-tw">{u.slice(-1)}학기</span>
                  <span className="hm-cnt">{inUnit(u).length}개</span>
                </div>

                {open.has(u) && chaptersOf(u).map((ch, i) => {
                  const catId = `${u}:${i}`;
                  const fav = favMap[catId];
                  const list = inChapter(u, ch);
                  return (
                    <div key={catId} className="hm-lv3">
                      <div className="hm-row" style={fav?.color ? { borderLeftColor: fav.color } : null}
                        onClick={() => toggleOpen(catId)}>
                        <span className="hm-car">{open.has(catId) ? "▾" : "▸"}</span>
                        <span className="hm-tw">{ch[0]}</span>
                        <span className="hm-cnt">{list.length}개</span>
                        <button
                          className={"hm-star" + (fav ? " on" : "")}
                          style={fav?.color ? { color: fav.color } : null}
                          onClick={(e) => { e.stopPropagation(); toggleFav(catId); }}
                          aria-label="즐겨찾기"
                        >{fav ? "★" : "☆"}</button>
                      </div>
                      {open.has(catId) && (
                        <div className="hm-list">
                          {list.map((c) => (
                            <a key={c.id} className="hm-item" href={`#/c/${c.id}`}>
                              <b>{String(c.sort_order).padStart(2, "0")}. {c.title}</b>
                              <span>{c.subtitle}</span>
                            </a>
                          ))}
                          {list.length === 0 && <p className="hm-small">이 단원에는 아직 개념이 없어요.</p>}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            ))}
          </div>
        ))}

        {/* ── 즐겨찾기 10개 초과 팝업 ── */}
        {pending && (
          <div className="hm-modal-bg" onClick={() => setPending(null)}>
            <div className="hm-modal" onClick={(e) => e.stopPropagation()}>
              <h3>즐겨찾기가 가득 찼어요 (10개)</h3>
              <p>「{catInfo(pending).title}」을(를) 등록하려면 해제할 항목을 선택하세요.</p>
              {favs.map((f) => {
                const info = catInfo(f.cat_id);
                return (
                  <label key={f.cat_id} className="hm-mrow">
                    <input
                      type="checkbox"
                      checked={pick.has(f.cat_id)}
                      onChange={(e) => {
                        const next = new Set(pick);
                        e.target.checked ? next.add(f.cat_id) : next.delete(f.cat_id);
                        setPick(next);
                      }}
                    />
                    <span className="hm-mdot" style={{ background: f.color || "var(--bd)" }} />
                    <span><small style={{ color: "var(--mut)" }}>{info.short}</small> {info.title}</span>
                  </label>
                );
              })}
              <div className="hm-mbtns">
                <button className="hm-mbtn" onClick={() => setPending(null)}>등록 취소</button>
                <button className="hm-mbtn pri" disabled={pick.size === 0} onClick={confirmSwap}>
                  {pick.size ? `${pick.size}개 해제하고 등록` : "해제하고 등록"}
                </button>
              </div>
            </div>
          </div>
        )}

        {toast && <div className="hm-toast">{toast}</div>}
      </div>
    </div>
  );
}
