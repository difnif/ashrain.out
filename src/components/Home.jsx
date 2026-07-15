import { useEffect, useRef, useState } from "react";
import { listConcepts } from "../lib/concepts";
import { supabase } from "../supabaseClient";
import WrongNote from "./WrongNote";
import Calc from "./Calc";
import Hint from "./Hint";

// ashrain.out — 홈 화면 (patch v0.3.0)
// [v0.3.0 변경]
// - 힌트 탭이 실제 기능으로 연결: 문제 사진 → AI 접근법 힌트 + 내 기록 (Hint.jsx, api/ai.js 필요)
// - 연산 탭은 Calc.jsx v0.3.0과 함께 배포 (선생님 자료 · 답안지 채점 · 오답노트 연동)
// 이 파일을 src/components/Home.jsx 에 덮어쓰세요. Calc.jsx / AdminCalc.jsx 와 함께 배포!
// (v0.2.1의 WrongNote.jsx / AdminWrongNotes.jsx 는 그대로 두면 됩니다)
//
// [v0.2.2 변경]
// - 연산 탭이 실제 풀이 화면으로 연결: 단원 선택 → 문제 수·난이도 → 랜덤 추출 → 문제별 타이머 → 채점 → 틀린 것만 다시 (Calc.jsx)
// - 관리자: 연산 탭 안의 🛠 버튼 → 문제 JSON 파일 등록·유닛 관리 (AdminCalc.jsx)
// - 세트 방식 → 문제 은행 방식 전환: 이전 세트 테이블 참조 제거, calc_units/calc_problems 사용 (schema_calc_v2.sql 필요)
//
// [v0.2.1 SQL — 학생 이름 포함 버전으로 RPC 교체 (SQL Editor에서 실행)]
// drop function if exists admin_list_wrong_notes();
// create or replace function admin_list_wrong_notes()
// returns table ( id uuid, user_id uuid, student_name text, image_path text, unit_id text,
//   concept_id text, reason text, source text, tags text[], status text, memo text, created_at timestamptz )
// language sql stable security definer set search_path = public as $$
//   select w.id, w.user_id, p.name, w.image_path, w.unit_id, w.concept_id, w.reason, w.source,
//          w.tags, w.status, case when s.share_wrong_memo then w.memo else null end, w.created_at
//   from wrong_notes w join user_settings s on s.user_id = w.user_id
//   left join profiles p on p.id = w.user_id
//   where is_admin() and s.share_wrong_notes order by w.created_at desc $$;

const UNIT_NAMES = {
  "m1-1": "중1 1학기", "m1-2": "중1 2학기", "m2-1": "중2 1학기", "m2-2": "중2 2학기",
  "m3-1": "중3 1학기", "m3-2": "중3 2학기",
  "h1-1": "공통수학1", "h1-2": "공통수학2",
  "h2-1": "대수", "h2-2": "미적분1",
  "h3-1": "미적분2", "h3-2": "확률과 통계", "h3-3": "기하",
};

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
  "m3-1": [["제곱근과 실수", 1, 6], ["다항식의 곱셈과 인수분해", 7, 13], ["이차방정식", 14, 21], ["이차함수", 22, 30]],
  "m3-2": [["삼각비", 1, 5], ["원의 성질", 6, 11], ["통계", 12, 14]],
  "h1-1": [["다항식", 1, 3], ["방정식과 부등식", 4, 13], ["경우의 수", 14, 16], ["행렬", 17, 18]],
  "h1-2": [["도형의 방정식", 1, 7], ["집합과 명제", 8, 15], ["함수", 16, 20]],
  "h2-1": [["지수함수와 로그함수", 1, 7], ["삼각함수", 8, 11], ["수열", 12, 17]],
  "h2-2": [["함수의 극한과 연속", 1, 4], ["미분", 5, 12], ["적분", 13, 15]],
  "h3-1": [["수열의 극한", 1, 4], ["미분법", 5, 12], ["적분법", 13, 18]],
  "h3-2": [["경우의 수", 1, 3], ["확률", 4, 7], ["통계", 8, 14]],
  "h3-3": [["이차곡선", 1, 7], ["공간도형과 공간좌표", 8, 13], ["벡터", 14, 21]],
};
const chaptersOf = (unit) => CHAPTERS[unit] || [["전체", 1, 999]];

// 학년·학기 라벨 (m→중, h→고 / 정렬은 중등 먼저, 학년 순)
const GRADE_PREFIX = { m: "중", h: "고" };
const gradeLabel = (g) => (GRADE_PREFIX[g[0]] || "") + g[1];
const gradeRank = (g) => (g[0] === "m" ? 0 : 100) + Number(g[1]);
const semLabel = (u) => (u[0] === "m" ? `${u.slice(-1)}학기` : UNIT_NAMES[u] || u);
const unitShort = (u) => (u[0] === "m" ? u.slice(1) : "고" + u.slice(1));

// 즐겨찾기 색상 팔레트 (첫 항목 null = 기본색)
const PALETTE = [null, "#F472B6", "#F87171", "#F59E0B", "#34D399", "#60A5FA", "#A78BFA"];

// 카테고리 탭
const CATS = [
  ["concept", "📖", "개념"],
  ["calc", "🧮", "연산"],
  ["wrong", "📕", "오답"],
  ["hint", "💡", "힌트"],
];

// 환경설정 — 공유 토글 (키, 제목, 설명)
const TOGGLES = [
  ["share_wrong_notes", "오답 사진·분류 공유", "내 오답 사진과 분류(단원·원인·태그·복습 상태)를 선생님이 볼 수 있어요."],
  ["share_wrong_memo", "오답 메모까지 공유", "위 항목이 켜져 있을 때만, 오답에 적은 메모가 함께 보여요."],
  ["share_hint_data", "힌트 기록 공유", "힌트로 질문한 문제 사진과 AI 답변 기록을 선생님이 볼 수 있어요."],
  ["share_calc_records", "연산 기록 공유", "연산 세트의 점수와 걸린 시간을 선생님이 볼 수 있어요."],
];
const DEFAULT_SHARE = { share_wrong_notes: false, share_wrong_memo: false, share_hint_data: false, share_calc_records: false };


const CSS = `
.hm-root { min-height: 100vh; padding: 20px 14px 40px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.hm-light { background: #EDEFF2; --ink:#1F2937; --mut:#8A929C; --card:#fff; --bd:#DFE3E8; --ac:#0DA95F; }
.hm-dark  { background: #0B0C0F; --ink:#E2E8F0; --mut:#6B7280; --card:#15171C; --bd:#23262D; --ac:#FFE03C; }
.hm-wrap { max-width: 768px; margin: 0 auto; }
.hm-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; flex-wrap: wrap; gap: 8px; }
.hm-logo { height: 34px; }
.hm-btns { display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }
.hm-btn { background: var(--card); border: 1px solid var(--bd); color: var(--mut); font-size: 12px;
  border-radius: 8px; padding: 6px 12px; cursor: pointer; }
.hm-me img { width: 18px; height: 18px; border-radius: 50%; vertical-align: -4px; margin-right: 3px; }
.hm-empty { color: var(--mut); font-size: 14px; text-align: center; padding: 40px 0; }

/* 카테고리 4탭 */
.hm-cats { display: flex; gap: 6px; margin-bottom: 16px; }
.hm-cat { flex: 1; text-align: center; padding: 10px 2px; border-radius: 12px; border: 1px solid var(--bd);
  background: var(--card); color: var(--mut); font-size: 13.5px; font-weight: 700; cursor: pointer;
  user-select: none; -webkit-user-select: none; }
.hm-cat.on { color: var(--ac); border-color: var(--ac); box-shadow: 0 0 0 1px var(--ac) inset; }

/* 카테고리 패널 공통 */
.hm-acts { display: flex; gap: 8px; margin: 2px 0 14px; }
.hm-act { flex: 1; padding: 13px 8px; border-radius: 12px; border: 1px solid var(--ac); background: transparent;
  color: var(--ac); font-weight: 800; font-size: 14px; cursor: pointer; }
.hm-card { display: block; width: 100%; text-align: left; background: var(--card); border: 1px solid var(--bd);
  border-radius: 12px; padding: 12px 14px; margin-bottom: 8px; color: var(--ink); cursor: pointer; box-sizing: border-box; }
.hm-card b { font-size: 14.5px; }
.hm-card span { display: block; color: var(--mut); font-size: 12.5px; margin-top: 2px; }
.hm-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 8px; }
.hm-shot { border: 1px solid var(--bd); border-radius: 12px; overflow: hidden; background: var(--card);
  cursor: pointer; padding: 0; text-align: left; }
.hm-shot img { width: 100%; aspect-ratio: 3 / 4; object-fit: cover; display: block; background: rgba(0,0,0,.06); }
.hm-shot p { margin: 0; padding: 8px 10px 9px; font-size: 12.5px; color: var(--ink); }
.hm-vimg { width: 100%; border-radius: 10px; border: 1px solid var(--bd); margin-bottom: 10px; }
.hm-vtxt { white-space: pre-wrap; font-size: 13.5px; line-height: 1.65; color: var(--ink);
  background: rgba(127,127,127,.07); border-radius: 10px; padding: 12px; }

/* 환경설정 — 스위치 */
.hm-srow { display: flex; align-items: flex-start; gap: 10px; padding: 11px 0; border-bottom: 1px dashed var(--bd); }
.hm-srow:last-of-type { border-bottom: none; }
.hm-stxt { flex: 1; min-width: 0; }
.hm-stxt b { font-size: 14px; color: var(--ink); display: block; margin-bottom: 2px; }
.hm-stxt span { font-size: 12px; color: var(--mut); line-height: 1.5; }
.hm-sw { position: relative; width: 44px; height: 26px; border-radius: 999px; border: 1px solid var(--bd);
  background: var(--bd); cursor: pointer; flex: none; padding: 0; transition: background .15s; margin-top: 2px; }
.hm-sw::after { content: ""; position: absolute; top: 2px; left: 2px; width: 20px; height: 20px;
  border-radius: 50%; background: var(--card); transition: left .15s; }
.hm-sw.on { background: var(--ac); border-color: var(--ac); }
.hm-sw.on::after { left: 20px; }
.hm-sw:disabled { opacity: .35; cursor: default; }
.hm-snote { color: var(--mut); font-size: 11.5px; margin: 10px 2px 0; line-height: 1.6; }

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

/* 팝업 */
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

  const [cat, setCat] = useState("concept");         // 현재 카테고리 탭
  const [open, setOpen] = useState(() => new Set()); // 기본: 전부 접힘
  const [favs, setFavs] = useState([]);              // [{cat_id, position, color}]
  const [selCat, setSelCat] = useState(null);        // 즐겨찾기 탭에서 열어 둔 카테고리
  const [editMode, setEditMode] = useState(false);
  const [pending, setPending] = useState(null);      // 10개 초과 시 등록 대기 중인 catId
  const [pick, setPick] = useState(() => new Set()); // 팝업에서 해제 선택
  const [toast, setToast] = useState("");
  const lp = useRef({ t: null, fired: false });

  // v0.2.0 — 카테고리 데이터 (탭 첫 진입 시에만 로드)
  const [imgUrl, setImgUrl] = useState({});          // storage path → 서명 URL
  const [viewer, setViewer] = useState(null);        // 공유 자료 상세 {title, path, comment, extra}

  // v0.2.0 — 환경설정(공유) 모달
  const [cfgOpen, setCfgOpen] = useState(false);
  const [share, setShare] = useState(null);

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

  // 탭 진입 시 해당 카테고리 데이터 로드
  useEffect(() => {
  }, [cat, uid]); // eslint-disable-line react-hooks/exhaustive-deps

  async function signAll(rows) {
    for (const r of rows || []) {
      if (!r.image_path) continue;
      const { data } = await supabase.storage.from("notes").createSignedUrl(r.image_path, 3600);
      if (data?.signedUrl) setImgUrl((m) => ({ ...m, [r.image_path]: data.signedUrl }));
    }
  }

  function say(msg) { setToast(msg); setTimeout(() => setToast(""), 2200); }

  // ── 환경설정(공유) ──
  async function openCfg() {
    if (!uid) { say("로그인하면 설정할 수 있어요"); return; }
    setCfgOpen(true);
    if (share === null) {
      const { data } = await supabase.from("user_settings").select("*").eq("user_id", uid).maybeSingle();
      setShare(data ? { ...DEFAULT_SHARE, ...data } : { ...DEFAULT_SHARE });
    }
  }
  async function flipShare(key) {
    const next = { ...share, [key]: !share[key] };
    if (key === "share_wrong_notes" && share.share_wrong_notes) next.share_wrong_memo = false; // 사진 공유를 끄면 메모도 함께 OFF
    setShare(next);
    const { error } = await supabase.from("user_settings").upsert({
      user_id: uid,
      share_wrong_notes: next.share_wrong_notes,
      share_wrong_memo: next.share_wrong_memo,
      share_hint_data: next.share_hint_data,
      share_calc_records: next.share_calc_records,
      updated_at: new Date().toISOString(),
    });
    if (error) { setShare(share); say("저장 실패: " + error.message); }
  }

  // ── 트리 헬퍼 ──
  const units = [...new Set(concepts.map((c) => c.unit_id))].sort();
  const grades = [...new Set(units.map((u) => u.slice(0, 2)))].sort((a, b) => gradeRank(a) - gradeRank(b));
  const semestersOf = (g) => units.filter((u) => u.startsWith(g + "-"));
  const inUnit = (u) => concepts.filter((c) => c.unit_id === u);
  const inChapter = (u, ch) =>
    inUnit(u).filter((c) => c.sort_order >= ch[1] && c.sort_order <= ch[2])
      .sort((a, b) => a.sort_order - b.sort_order);
  const favMap = Object.fromEntries(favs.map((f) => [f.cat_id, f]));
  function catInfo(catId) {
    const [unit, idx] = catId.split(":");
    const ch = chaptersOf(unit)[+idx];
    return { unit, title: ch ? ch[0] : catId, short: unitShort(unit), ch };
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
            <button className="hm-btn" onClick={openCfg}>⚙ 설정</button>
            <button className="hm-btn hm-me" onClick={() => (location.hash = "#/me")}>
              {me?.avatar_url ? <img src={me.avatar_url} alt="" /> : "👤"} {me?.name || "마이페이지"}
            </button>
            <button className="hm-btn" onClick={onToggleTheme}>{theme === "light" ? "🌙" : "🌧"}</button>
          </div>
        </div>

        {/* ── 카테고리 4탭 ── */}
        <div className="hm-cats">
          {CATS.map(([id, icon, label]) => (
            <button key={id} className={"hm-cat" + (cat === id ? " on" : "")} onClick={() => setCat(id)}>
              {icon} {label}
            </button>
          ))}
        </div>

        {/* ════════ 📖 개념 ════════ */}
        {cat === "concept" && (
          <>
            {err && <p className="hm-empty">{err}</p>}
            {!err && concepts.length === 0 && <p className="hm-empty">아직 등록된 개념이 없어요.</p>}

            {/* 즐겨찾기 탭 (개인 설정) */}
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

            {/* 전체 트리: 학년 → 학기 → 대단원 */}
            {grades.map((g) => (
              <div key={g}>
                <div className="hm-row" onClick={() => toggleOpen(g)}>
                  <span className="hm-car">{open.has(g) ? "▾" : "▸"}</span>
                  <span className="hm-tw">{gradeLabel(g)}</span>
                  <span className="hm-cnt">{semestersOf(g).reduce((s, u) => s + inUnit(u).length, 0)}개</span>
                </div>

                {open.has(g) && semestersOf(g).map((u) => (
                  <div key={u} className="hm-lv2">
                    <div className="hm-row" onClick={() => toggleOpen(u)}>
                      <span className="hm-car">{open.has(u) ? "▾" : "▸"}</span>
                      <span className="hm-tw">{semLabel(u)}</span>
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
          </>
        )}

        {/* ════════ 🧮 연산 ════════ */}
        {cat === "calc" && (
          <Calc uid={uid} isAdmin={isAdmin} unitNames={UNIT_NAMES} say={say} />
        )}

        {/* ════════ 📕 오답 ════════ */}
        {cat === "wrong" && (
          <WrongNote uid={uid} isAdmin={isAdmin} unitNames={UNIT_NAMES} say={say} />
        )}

        {/* ════════ 💡 힌트 ════════ */}
        {cat === "hint" && (
          <Hint uid={uid} isAdmin={isAdmin} unitNames={UNIT_NAMES} say={say} />
        )}

        {/* ── 공유 자료 상세 뷰어 ── */}
        {viewer && (
          <div className="hm-modal-bg" onClick={() => setViewer(null)}>
            <div className="hm-modal" onClick={(e) => e.stopPropagation()}>
              <h3>{viewer.title}</h3>
              {imgUrl[viewer.path] && <img className="hm-vimg" src={imgUrl[viewer.path]} alt="" />}
              {viewer.comment && <p>💬 {viewer.comment}</p>}
              {viewer.extra && <div className="hm-vtxt">{viewer.extra}</div>}
              <div className="hm-mbtns">
                <button className="hm-mbtn pri" onClick={() => setViewer(null)}>닫기</button>
              </div>
            </div>
          </div>
        )}

        {/* ── 환경설정: 데이터 공유 ── */}
        {cfgOpen && (
          <div className="hm-modal-bg" onClick={() => setCfgOpen(false)}>
            <div className="hm-modal" onClick={(e) => e.stopPropagation()}>
              <h3>⚙ 데이터 공유 설정</h3>
              <p>선생님(관리자)에게 내 학습 데이터를 보여줄지 항목별로 정해요. 다른 친구들은 어떤 경우에도 내 데이터를 볼 수 없어요.</p>
              {share === null && <p className="hm-small">불러오는 중…</p>}
              {share !== null && TOGGLES.map(([key, title, desc]) => {
                const dep = key === "share_wrong_memo" && !share.share_wrong_notes;
                return (
                  <div key={key} className="hm-srow">
                    <div className="hm-stxt"><b>{title}</b><span>{desc}</span></div>
                    <button
                      className={"hm-sw" + (share[key] && !dep ? " on" : "")}
                      disabled={dep}
                      onClick={() => flipShare(key)}
                      aria-label={title}
                    />
                  </div>
                );
              })}
              <p className="hm-snote">기본값은 전부 꺼짐이에요. 켜고 끄는 즉시 저장되며, 언제든 다시 끌 수 있어요.</p>
              <div className="hm-mbtns">
                <button className="hm-mbtn pri" onClick={() => setCfgOpen(false)}>완료</button>
              </div>
            </div>
          </div>
        )}

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
