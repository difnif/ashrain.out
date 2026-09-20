// ashrain.out — 홈 대시보드 (v3.0, ui-v3)
// 셸(App)이 상단·하단 내비를 그린다 — 이 화면은 자기 배경 + 콘텐츠만 렌더한다 (.hd-top 제거).
// 위는 단순(히어로·지갑·이어서 공부하기·오늘의 복습), 아래는 실데이터 카드 확장
// (주간 그래프·오답노트·내 질문·최근 응시 시험·자주 나온 실수·디데이·철학 배너·미리보기).
// 날씨: Open-Meteo → 단계 자동 선택, 히어로 우측 사다리꼴 + 디졸브, 추위는 채도·결빙 필터.
import { useEffect, useState, useCallback } from "react";
import { supabase } from "../supabaseClient";
import { SceneEditor } from "./AnimFigure";
import { BETA } from "../lib/beta";
import { readLastResult } from "../lib/setplay";
import { countOpenWrongNotes } from "../lib/wrongnotes";
import { CURRENCY, getBalances, onPoints } from "../lib/wallet";
import { UNIT_NAMES, summarizeAttempts } from "../lib/items";
import { loadRunsLocal, mergeRuns, describeRun, presetOf } from "../lib/exam";
import { mcLabel } from "../lib/misconceptions";
import { getRecentConcepts } from "../lib/review";
import { getWx } from "../lib/wx";
import ReviewCard from "./ReviewCard";

const CSS = `
.hd-root { min-height: 100vh; padding: 14px 14px 88px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; background: var(--bg); }
.hd-root * { box-sizing: border-box; }
.hd-light { --bg:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0D9488; --in:#F4F6F8; --bad:#DC2626; }
.hd-dark  { --bg:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#5EEAD4; --in:#101116; --bad:#F87171; }
.hd-wrap { max-width: 1200px; margin: 0 auto; }

/* ── 히어로 (전체 폭) ── */
.hd-hero { position: relative; border-radius: 20px; padding: 26px 22px 22px; color: #fff;
  overflow: hidden; margin-bottom: 12px; box-shadow: 0 6px 22px rgba(0,0,0,.14); min-height: 150px;
  transition: filter .6s ease, box-shadow .6s ease; }
.hd-sky { position: absolute; right: 0; top: 0; bottom: 0; width: 50%;
  clip-path: polygon(0 0, 100% 0, 100% 100%, 34% 100%);
  -webkit-mask-image: linear-gradient(100deg, transparent 2%, #000 30%);
  mask-image: linear-gradient(100deg, transparent 2%, #000 30%); }
.hd-sky img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.hd-hero-hi { font-size: 14px; opacity: .92; margin: 0; font-weight: 600; position: relative; }
.hd-hero-nick { font-size: 26px; font-weight: 800; margin: 4px 0 10px; position: relative; }
.hd-hero-greet { font-size: 16.5px; font-weight: 700; margin: 0; line-height: 1.55; position: relative; max-width: 58%; }
.hd-hero-time { position: absolute; left: 22px; bottom: 12px; font-size: 11.5px; opacity: .8; }
.hd-wxpen { position: absolute; right: 10px; bottom: 8px; z-index: 5; background: rgba(255,255,255,.85);
  border: none; border-radius: 8px; font-size: 12px; padding: 4px 7px; cursor: pointer; }

/* ── 지갑 줄 (전체 폭) ── */
.hd-wallet { display: flex; align-items: center; gap: 8px; margin: 0 0 12px; padding: 0 4px; }
.hd-wallet .hd-coin { display: inline-flex; align-items: center; gap: 4px; background: var(--card); border: 1px solid var(--bd);
  border-radius: 999px; padding: 4px 10px; font-size: 12px; font-weight: 800; color: var(--ink); }
.hd-wallet .hd-coin b { color: var(--ac); font-weight: 900; }
.hd-wallet .hd-coin.off { color: var(--mut); }
.hd-wallet .hd-coin.off b { color: var(--mut); }
.hd-wallet a { margin-left: auto; color: var(--mut); font-size: 11.5px; text-decoration: none; border-bottom: 1px dotted var(--bd); }

/* ── 카드 그리드: 폰 1열 → 700px 2열 → 1040px 3열 · 행 높이 정렬 ── */
.hd-grid { display: grid; grid-template-columns: 1fr; gap: 10px; grid-auto-flow: row dense; align-items: stretch; }
.hd-card { background: var(--card); border: 1px solid var(--bd); border-radius: 14px; padding: 14px 15px 15px;
  position: relative; display: flex; flex-direction: column; min-width: 0; }
.hd-card.wide { grid-column: 1 / -1; }
@media (min-width: 700px) {
  .hd-root { padding: 18px 20px 96px; }
  .hd-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
  .hd-w2 { grid-column: span 2; }
  .hd-hero { min-height: 170px; padding: 30px 26px 24px; }
  .hd-hero-greet { max-width: 66%; }
}
@media (min-width: 1040px) { .hd-grid { grid-template-columns: repeat(3, 1fr); } }

.hd-t { font-size: 12px; font-weight: 800; color: var(--mut); letter-spacing: .5px; margin: 0 0 8px; }
.hd-thead { display: flex; align-items: baseline; gap: 8px; margin: 0 0 8px; }
.hd-thead .hd-t { margin: 0; flex: 1; min-width: 0; }
.hd-tsub { font-size: 11.5px; font-weight: 600; color: var(--mut); white-space: nowrap; }
.hd-big { font-size: 20px; font-weight: 800; color: var(--ink); margin: 0; }
.hd-sub { font-size: 12px; color: var(--mut); margin: 4px 0 0; line-height: 1.6; }
.hd-bar { height: 8px; background: var(--in); border-radius: 999px; overflow: hidden; margin: 10px 0 6px; }
.hd-bar > div { height: 100%; background: var(--ac); border-radius: 999px; }
.hd-act { margin-top: auto; padding-top: 12px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.hd-go { display: inline-block; background: transparent; border: 1.5px solid var(--ac);
  border-radius: 999px; color: var(--ac); font-size: 12px; font-weight: 800; padding: 7px 13px; cursor: pointer; }
.hd-empty { background: var(--in); border: 1px dashed var(--bd); border-radius: 12px; padding: 14px 12px;
  font-size: 12.5px; color: var(--mut); line-height: 1.65; text-align: center; }

/* ── 목록 행 (이어서 공부하기 · 최근 응시 · 일정) ── */
.hd-rows { display: flex; flex-direction: column; gap: 6px; }
.hd-row { display: flex; align-items: center; gap: 10px; width: 100%; text-align: left; min-width: 0;
  background: var(--in); border: 1px solid var(--bd); border-radius: 12px; padding: 10px 12px;
  color: var(--ink); font-family: inherit; }
button.hd-row { cursor: pointer; }
button.hd-row:hover { border-color: var(--ac); }
.hd-row .ic { flex: none; font-size: 17px; }
.hd-row .tx { flex: 1; min-width: 0; }
.hd-row .tx b { display: block; font-size: 13.5px; font-weight: 800; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.hd-row .tx small { display: block; font-size: 11.5px; color: var(--mut); margin-top: 1px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.hd-row .rt { flex: none; font-size: 11.5px; color: var(--mut); }
.hd-mini { flex: none; border: 1.5px solid var(--ac); background: transparent; color: var(--ac);
  border-radius: 999px; font-size: 11.5px; font-weight: 800; padding: 6px 11px; white-space: nowrap; }
.hd-cont { display: grid; grid-template-columns: 1fr; gap: 8px; }
@media (min-width: 700px) { .hd-cont { grid-template-columns: 1fr 1fr; } }

/* ── 주간 그래프 ── */
.hd-week { display: flex; align-items: flex-end; gap: 6px; margin-top: 8px; }
.hd-wcol { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 3px; min-width: 0; }
.hd-wnum { font-size: 10px; font-weight: 700; color: var(--mut); height: 12px; line-height: 12px; }
.hd-wbar { width: 100%; max-width: 44px; background: var(--in); border: 1px solid var(--bd);
  border-radius: 6px 6px 2px 2px; position: relative; overflow: hidden; }
.hd-wbar > i { position: absolute; left: 0; right: 0; bottom: 0; background: var(--ac); display: block; }
.hd-wlab { font-size: 10px; color: var(--mut); }

/* ── 실수 칩 ── */
.hd-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.hd-chip { display: inline-flex; align-items: center; gap: 6px; max-width: 100%;
  border: 1px solid var(--bd); background: var(--in); border-radius: 999px; padding: 6px 11px;
  font-size: 12px; font-weight: 700; color: var(--ink); }
.hd-chip span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.hd-chip b { color: var(--bad); font-weight: 900; flex: none; }

/* ── 디데이 ── */
.hd-dbadge { flex: none; min-width: 46px; text-align: center; background: #EF4444; color: #fff;
  border-radius: 999px; font-size: 11px; font-weight: 800; padding: 5px 8px; }

/* ── 철학 배너 · 하단 ── */
.hd-philo { grid-column: 1 / -1; position: relative; border-radius: 16px; overflow: hidden; cursor: pointer;
  background: linear-gradient(120deg, #14343B 0%, #0D9488 130%); color: #fff; padding: 20px 130px 20px 20px;
  min-height: 108px; border: none; text-align: left; font-family: inherit; }
.hd-philo-eyebrow { font-size: 10.5px; letter-spacing: 2.5px; opacity: .85; margin: 0 0 6px; font-weight: 800; }
.hd-philo-t { font-size: 17px; font-weight: 800; margin: 0 0 6px; }
.hd-philo-d { font-size: 12px; opacity: .9; margin: 0; line-height: 1.6; }
.hd-philo-img { position: absolute; right: -6px; top: 0; bottom: 0; width: 120px; object-fit: cover;
  object-position: center top; opacity: .9; mask-image: linear-gradient(to right, transparent, #000 30%);
  -webkit-mask-image: linear-gradient(to right, transparent, #000 30%); }
.hd-philo-arrow { position: absolute; right: 12px; bottom: 10px; font-size: 16px; }
.hd-note { text-align: center; color: var(--mut); font-size: 11px; margin-top: 16px; line-height: 1.7; }
.hd-note a { color: var(--mut); }
.hd-pillar { border-width: 1.5px; border-color: var(--ac); }
.hd-pillar .hd-t { color: var(--ac); }
.hd-links { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-top: 10px; }
.hd-links a { color: var(--mut); font-size: 11.5px; text-decoration: none; border-bottom: 1px dotted var(--bd); }
.hd-beta { display: inline-block; font-size: 10px; font-weight: 800; color: #fff; background: #7C3AED; border-radius: 999px; padding: 1px 6px; margin-left: 6px; vertical-align: middle; }
`;

function readLastConcept() {
  try { const v = JSON.parse(localStorage.getItem("ash.lastConcept") || "null"); if (v && v.id) return v; } catch { /* 무시 */ }
  const r = getRecentConcepts();               // 복습용 최근 목록({id,title,at})으로 보강
  return r.length ? r[0] : null;
}
const fmtAgo = (at) => {
  if (!at) return "";
  const d = Math.round((Date.now() - at) / 86400000);
  return d <= 0 ? "오늘" : d === 1 ? "어제" : `${d}일 전`;
};
const fmtWhen = (iso) => {
  if (!iso) return "";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "";
  const day = (x) => `${x.getFullYear()}-${x.getMonth()}-${x.getDate()}`;
  const now = new Date(), yst = new Date(Date.now() - 86400000);
  if (day(d) === day(now)) return "오늘";
  if (day(d) === day(yst)) return "어제";
  return `${d.getMonth() + 1}/${d.getDate()}`;
};

const GREETS = [
  "저는 안녕 안 해요 😌", "복습은 하셨나요?", "오답노트, 열어봤나요?", "어제 배운 거 한 줄로 말해볼래요?",
  "오늘도 반가워요!", "어서 오세요 😊", "수학할 준비 됐나요?", "차근차근 가 봅시다",
  "꾸준함이 재능을 이겨요", "한 문제만 풀고 가도 성공!", "오늘의 공부, 시작해볼까요?", "숙제 먼저, 딴짓은 나중에!",
  "돌아온 걸 환영해요", "개념이 무기예요 🗡️", "궁금하면 물음표를 눌러요", "틀린 문제가 진짜 선생님이에요",
  "딱 5분만 집중해볼까요?", "어려우면 천천히 — 대신 멈추진 말기", "오늘 컨디션은 어때요?", "수학은 눈으로 말고 손으로!",
  "공식보다 '이유'를 기억해요", "지난 시험 오답, 다시 봤나요?", "작은 성공을 쌓는 중이에요", "포기만 안 하면 이기는 게임",
  "머리 말고 엉덩이로 공부하는 거예요", "오늘도 한 칸 성장 🌱", "모르는 건 부끄러운 게 아니에요", "쉬는 것도 공부의 일부예요",
  "계산 실수, 오늘은 꼭 잡아봅시다", "시작이 반 — 접속했으니 벌써 4분의 1!",
];

// ── 날씨 이미지 세트: 베이스(불투명) + 오버레이(검정 배경 → screen 합성) ──
const STYLE_BASE = "square sky illustration, flat minimal vector style, soft colors, no text, no letters, no numbers --style raw --no text, watermark";
const STYLE_OVER = "on pure black background, isolated glowing elements, flat minimal vector style, no text, no letters, no numbers --style raw --no text, watermark";
export const WEATHER_SCENES = [
  { id: "c", label: "☁️ 흐림 — 베이스", count: 6, style: STYLE_BASE,
    cuts: ["쾌청", "구름 조금", "구름 많음", "흐릿", "잔뜩 흐림", "먹구름"],
    cutPrompts: [
      "clear bright blue sky with a shining sun and one tiny cloud",
      "blue sky with a few small fluffy clouds, sun fully visible",
      "sky half covered with soft clouds, sun peeking through",
      "mostly cloudy sky, pale sun barely visible behind clouds",
      "overcast gray sky, thick continuous cloud layer, no sun",
      "dark heavy storm clouds covering the entire sky",
    ] },
  { id: "r", label: "🌧 비 — 베이스", count: 6, style: STYLE_BASE,
    cuts: ["이슬비", "부슬비", "보통 비", "장대비", "호우주의보", "호우경보"],
    cutPrompts: [
      "light drizzle falling from soft gray clouds, thin sparse raindrops",
      "gentle steady rain from gray clouds, small raindrops",
      "moderate rain with many raindrops, gray sky",
      "heavy rain pouring from dark clouds, thick rain streaks",
      "intense downpour, dense diagonal rain streaks, dark stormy sky",
      "extreme torrential rain, sheets of rain, very dark violent sky",
    ] },
  { id: "s", label: "❄️ 눈 — 베이스", count: 6, style: STYLE_BASE,
    cuts: ["눈발", "가벼운 눈", "펑펑", "수북수북", "폭설주의보", "폭설경보"],
    cutPrompts: [
      "a few snowflakes drifting in a pale winter sky",
      "light snowfall with small snowflakes, soft gray sky",
      "steady snowfall, many snowflakes falling",
      "heavy snowfall, thick large snowflakes filling the sky",
      "snowstorm with dense snow and low visibility",
      "extreme blizzard, whiteout of violent swirling snow",
    ] },
  { id: "f", label: "🥶 추위 — 오버레이(프레임)", count: 6, style: STYLE_OVER,
    cuts: ["쌀쌀", "추움", "성에 시작", "결빙", "한파주의보", "한파경보"],
    cutPrompts: [
      "thin frost sparkles at the four corners of the frame",
      "frost creeping along the edges, small ice crystals",
      "frost border framing all four edges, delicate ice patterns",
      "thick icy frame with small icicles hanging from the top edge",
      "heavy ice frame, long icicles, frozen crystals spreading inward",
      "fully frozen frame, huge icicles and cracked ice reaching toward the center",
    ] },
  { id: "h", label: "🥵 더위 — 오버레이", count: 6, style: STYLE_OVER,
    cuts: ["따뜻", "더움", "뙤약볕", "무더위", "폭염주의보", "폭염경보"],
    cutPrompts: [
      "a small soft warm sun glowing gently in the upper area",
      "a bright yellow sun with short bold rays",
      "a strong orange sun with long bold rays",
      "an intense blazing sun with visible heat shimmer waves",
      "a scorching red-orange sun with heat haze, and a small cloud wiping sweat",
      "an extreme blazing sun filling the top, exhausted sweating cloud characters below",
    ] },
  { id: "w", label: "💨 바람 — 오버레이", count: 6, style: STYLE_OVER,
    cuts: ["산들바람", "솔솔", "휘파람", "세찬 바람", "강풍주의보", "강풍경보"],
    cutPrompts: [
      "a small cloud with a calm cute face gently blowing a tiny puff of wind",
      "a cloud face blowing a soft breeze with a few curved wind lines",
      "a cloud face whistling while blowing wind, curved wind streams",
      "a cloud face frowning slightly, blowing strong wind with big swirling gust lines",
      "an upset cloud face blowing very strong wind, large gust swirls and flying leaves",
      "a furious scrunched-up cloud face blowing violent storm wind, huge gust swirls",
    ] },
];

const skyOf = (h) =>
  h < 6  ? ["linear-gradient(135deg,#1b2440 0%,#3b2f63 100%)", "고요한 새벽이에요"] :
  h < 11 ? ["linear-gradient(135deg,#2193b0 0%,#6dd5ed 100%)", "좋은 아침이에요"] :
  h < 17 ? ["linear-gradient(135deg,#0d9488 0%,#34d399 100%)", "활기찬 오후예요"] :
  h < 20 ? ["linear-gradient(135deg,#ee9ca7 0%,#b06ab3 100%)", "노을 지는 저녁이에요"] :
           ["linear-gradient(135deg,#141e30 0%,#243b55 100%)", "차분한 밤이에요"];

// 실황 분류는 lib/wx.js(pickWeather)로 옮겼다 — 우물(하단 탭바)과 같은 신호·같은 캐시를 쓴다.

const heroGrad = (wx, h) => {
  if (!wx) return skyOf(h)[0];
  if (wx.snowy) return "linear-gradient(135deg,#64748b,#9db1c7)";
  if (wx.rainy) return +wx.base[1] >= 5 ? "linear-gradient(135deg,#1f2937,#155e75)" : "linear-gradient(135deg,#475569,#0e7490)";
  if (wx.cloudLv >= 5) return "linear-gradient(135deg,#4b5563,#6b7280)";
  if (wx.cloudLv >= 3) return "linear-gradient(135deg,#5c7186,#38bdf8)";
  if (wx.t >= 31) return "linear-gradient(135deg,#f97316,#ef4444)";
  return skyOf(h)[0];
};

const coldFx = (t) => {
  if (t == null || t > 5) return {};
  const sat = t > 2 ? 0.8 : t > 0 ? 0.55 : t > -3 ? 0.3 : t > -8 ? 0.18 : 0.1;
  const fx = { filter: `saturate(${sat})` };
  if (t <= 0) {
    const g = t <= -12 ? 0.85 : t <= -8 ? 0.7 : t <= -3 ? 0.55 : 0.4;
    fx.boxShadow = `inset 0 0 0 3px rgba(205,235,255,${g}), inset 0 0 36px rgba(180,225,255,${g * 0.7}), 0 6px 22px rgba(0,0,0,.14)`;
  }
  return fx;
};

const WEEK0 = () => Array.from({ length: 7 }, () => ({ n: 0, ok: 0 }));

export default function HomeDash({ theme = "light", onToggleTheme }) { // eslint-disable-line no-unused-vars — 테마 토글은 마이페이지에서
  const [nick, setNick] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const [greet] = useState(() => GREETS[Math.floor(Math.random() * GREETS.length)]);
  const [wx, setWx] = useState(null);
  const [wxFiles, setWxFiles] = useState({});
  const [wxEdit, setWxEdit] = useState(false);
  const [dash, setDash] = useState({ wrongN: null, qna: null, week: null, attempts: null, topTags: null });
  const [runs, setRuns] = useState(null);       // null = 로딩 · [] = 없음 (test_runs + 로컬 병합)
  const [events, setEvents] = useState(null);   // null = 로딩 · [] = 없음 ({title, days})
  const [uid, setUid] = useState(null);
  const [prof, setProf] = useState(null);
  const [bal, setBal] = useState(null);         // { ash, drop, ready } · null = 아직/실패
  const lastConcept = readLastConcept();
  const lastSet = readLastResult();
  const now = new Date();
  const hi = skyOf(now.getHours())[1];
  const days = ["월", "화", "수", "목", "금", "토", "일"];
  const todayIdx = (now.getDay() + 6) % 7;

  useEffect(() => {
    let alive = true;
    supabase.auth.getUser().then(async ({ data }) => {
      const u = data?.user;
      if (!alive) return;
      if (!u) { setRuns(mergeRuns([], loadRunsLocal(), 5)); return; }
      setUid(u.id);
      const { data: p } = await supabase.from("profiles").select("username, role, grade").eq("id", u.id).maybeSingle();
      if (!alive) return;
      setNick(p?.username || ""); setIsAdmin(p?.role === "admin"); setProf(p || null);
      getBalances().then((b) => { if (alive) setBal(b); });
      // 실데이터 — 오답노트 수 · 내 질문 · 이번 주 풀이(요일·정답·실수 태그) · 최근 응시
      const since = new Date(Date.now() - 6 * 86400000); since.setHours(0, 0, 0, 0);
      const [wrongN, qnaRes, attRes, runRes] = await Promise.all([
        countOpenWrongNotes(u.id),
        supabase.from("concept_qna").select("id, status").eq("asked_by", u.id).order("created_at", { ascending: false }).limit(50),
        supabase.from("attempts").select("ts, correct, distractor_tag").eq("user_id", u.id).gte("ts", since.toISOString()).limit(1000),
        supabase.from("test_runs").select("id, test_type, unit_id, n, correct_n, score, max, finished_at, meta")
          .eq("user_id", u.id).order("finished_at", { ascending: false }).limit(10)
          .then((r) => r, () => ({ data: null, error: true })),   // 표가 아직 없을 수 있다 → 로컬만
      ]);
      if (!alive) return;
      const qna = qnaRes.error ? null : (qnaRes.data || []);
      const att = attRes.error ? [] : (attRes.data || []);
      const week = WEEK0();
      for (const a of att) {
        const i = (new Date(a.ts).getDay() + 6) % 7;
        week[i].n += 1; if (a.correct) week[i].ok += 1;
      }
      setDash({ wrongN, qna, week, attempts: att, topTags: summarizeAttempts(att).topTags });
      setRuns(mergeRuns(runRes.error ? [] : (runRes.data || []), loadRunsLocal(), 5));
    });
    // 다가오는 디데이 일정 (events.dday=true, 앞으로 2건) — 표가 없거나 실패해도 조용히 빈 상태
    const todayStr = new Date().toISOString().slice(0, 10);
    supabase.from("events").select("date, title").eq("dday", true).gte("date", todayStr).order("date").limit(2)
      .then(({ data, error }) => {
        if (!alive) return;
        if (error) { setEvents([]); return; }
        setEvents((data || []).map((e) => ({
          title: e.title,
          date: e.date,
          days: Math.round((new Date(e.date + "T00:00:00") - new Date(todayStr + "T00:00:00")) / 86400000),
        })));
      })
      .catch(() => { if (alive) setEvents([]); });
    getWx().then((w) => { if (alive && w) setWx(w); });
    // 복습 보상·쿠폰 등록 등으로 잔액이 바뀌면 다시 읽는다
    const off = onPoints(() => getBalances().then((b) => { if (alive && b) setBal(b); }));
    return () => { alive = false; off(); };
  }, []);

  const loadWxFiles = useCallback(async () => {
    const { data } = await supabase.storage.from("figures").list("weather/main", { limit: 100 });
    const map = {};
    for (const f of data || []) {
      const key = f.name.replace(/\.[^.]+$/, "");
      const { data: pu } = supabase.storage.from("figures").getPublicUrl(`weather/main/${f.name}`);
      map[key] = { name: f.name, url: pu.publicUrl + "?v=" + encodeURIComponent(f.updated_at || "") };
    }
    setWxFiles(map);
  }, []);
  useEffect(() => { loadWxFiles(); }, [loadWxFiles]);

  const skyImgs = wx ? [wx.base, ...wx.over].filter((k) => wxFiles[k]).map((k) => ({ k, url: wxFiles[k].url })) : [];
  const weekSum = dash.attempts ? dash.attempts.length : null;
  const weekOk = dash.attempts ? dash.attempts.filter((a) => a.correct).length : 0;
  const weekRate = weekSum ? Math.round((weekOk / weekSum) * 100) : null;

  return (
    <div className={`hd-root hd-${theme}`}>
      <style>{CSS}</style>
      <div className="hd-wrap">

        {/* ① 날씨 히어로 — 항상 전체 폭 */}
        <div className="hd-hero" style={{ background: heroGrad(wx, now.getHours()), ...coldFx(wx?.t) }}>
          {skyImgs.length > 0 && (
            <div className="hd-sky">
              {skyImgs.map(({ k, url }) => (
                <img key={k} src={url} alt="" style={{ mixBlendMode: k[0] === "f" || k[0] === "h" || k[0] === "w" ? "screen" : "normal" }} />
              ))}
            </div>
          )}
          <p className="hd-hero-hi">{hi}</p>
          <p className="hd-hero-nick">{nick || "친구"}님</p>
          <p className="hd-hero-greet">“{greet}”</p>
          <span className="hd-hero-time">{now.getMonth() + 1}월 {now.getDate()}일 · {days[todayIdx]}요일</span>
          {isAdmin && <button className="hd-wxpen" title="날씨 이미지 업로드" onClick={() => setWxEdit(true)}>🌦✏️</button>}
        </div>

        {/* ② 지갑 줄 — 항상 전체 폭 */}
        {uid && (
          <div className="hd-wallet" title="두 포인트는 서로 바꿀 수 없어요">
            <span className="hd-coin">{CURRENCY.ash.sym} <b>{bal ? Number(bal.ash || 0).toLocaleString() : "…"}</b></span>
            <span className={"hd-coin" + (bal && !bal.ready ? " off" : "")}>
              {CURRENCY.drop.sym} <b>{bal ? (bal.ready ? Number(bal.drop || 0).toLocaleString() : "준비 중") : "…"}</b>
            </span>
            <a href="#/me">지갑 · 내역 →</a>
          </div>
        )}

        <div className="hd-grid">

          {/* ③ 이어서 공부하기 — 마지막 개념 + 최근 세트, 한 카드 두 줄 */}
          <div className="hd-card hd-pillar wide">
            <p className="hd-t">▶️ 이어서 공부하기{BETA.on && <span className="hd-beta">{BETA.label}</span>}</p>
            <div className="hd-cont">
              {lastConcept ? (
                <button type="button" className="hd-row" onClick={() => (location.hash = `#/c/${encodeURIComponent(lastConcept.id)}`)}>
                  <span className="ic">📚</span>
                  <span className="tx"><b>{lastConcept.title || lastConcept.id}</b><small>{fmtAgo(lastConcept.at)} 본 개념이에요</small></span>
                  <span className="hd-mini">이어보기 →</span>
                </button>
              ) : (
                <button type="button" className="hd-row" onClick={() => (location.hash = "#/study/concept")}>
                  <span className="ic">📚</span>
                  <span className="tx"><b>개념부터 차근차근</b><small>학년·학기별 개념 카드를 읽고 예제로 확인해요</small></span>
                  <span className="hd-mini">개념 목록 →</span>
                </button>
              )}
              {lastSet ? (
                <button type="button" className="hd-row"
                  onClick={() => (location.hash = lastSet.conceptId ? `#/solve/set/${encodeURIComponent(lastSet.conceptId)}` : "#/study/practice")}>
                  <span className="ic">✏️</span>
                  <span className="tx">
                    <b>{lastSet.title || lastSet.conceptId || "최근 세트"} · {lastSet.ok}/{lastSet.n} 정답</b>
                    <small>{fmtAgo(lastSet.at)}에 푼 세트 — 같은 개념으로 다시 풀어요</small>
                  </span>
                  <span className="hd-mini">새 세트 →</span>
                </button>
              ) : (
                <button type="button" className="hd-row" onClick={() => (location.hash = "#/study/practice")}>
                  <span className="ic">✏️</span>
                  <span className="tx"><b>문항 세트로 확인</b><small>풀이 기록은 오답노트로 이어져요</small></span>
                  <span className="hd-mini">문제풀이 →</span>
                </button>
              )}
            </div>
          </div>

          {/* ④ 오늘의 복습 */}
          <div className="hd-card wide">
            <ReviewCard uid={uid} profile={prof} />
          </div>

          {/* ⑤ 이번 주 학습 그래프 + 정답률 */}
          <div className="hd-card wide">
            <div className="hd-thead">
              <p className="hd-t">📈 이번 주 학습</p>
              <span className="hd-tsub">{weekSum == null ? "…" : `합계 ${weekSum}문항${weekRate != null ? ` · 정답률 ${weekRate}%` : ""}`}</span>
            </div>
            {(() => {
              const w = dash.week || WEEK0();
              const mx = Math.max(1, ...w.map((x) => x.n));
              return (
                <div className="hd-week">
                  {w.map((v, i) => (
                    <div key={i} className="hd-wcol">
                      <span className="hd-wnum">{v.n || ""}</span>
                      <div className="hd-wbar" title={`${v.n}문항 · 맞힘 ${v.ok}`}
                        style={{ height: Math.max(v.n ? 10 : 4, Math.round((v.n / mx) * 64)), opacity: i === todayIdx ? 1 : 0.6 }}>
                        <i style={{ height: v.n ? `${Math.round((v.ok / v.n) * 100)}%` : 0 }} />
                      </div>
                      <span className="hd-wlab">{days[i]}</span>
                    </div>
                  ))}
                </div>
              );
            })()}
            {weekSum != null && weekSum > 0 && (
              <>
                <div className="hd-bar"><div style={{ width: `${weekRate}%` }} /></div>
                <p className="hd-sub" style={{ margin: 0 }}>진한 막대가 맞힌 문항이에요 · 맞힘 {weekOk} / {weekSum}</p>
              </>
            )}
            {weekSum === 0 && <p className="hd-sub">이번 주엔 아직 기록이 없어요. 한 세트만 풀어도 그래프가 생겨요.</p>}
          </div>

          {/* ⑥ 오답노트 */}
          <div className="hd-card">
            <p className="hd-t">📕 오답노트</p>
            <p className="hd-big">{dash.wrongN == null ? "…" : dash.wrongN === 0 ? "미복습 0문제" : `미복습 ${dash.wrongN}문제`}</p>
            <p className="hd-sub">{dash.wrongN === 0 ? "틀린 문제를 저장하면 여기에 쌓여요" : "다시 풀어서 정리해요"}</p>
            <div className="hd-act"><button className="hd-go" onClick={() => (location.hash = "#/learn/wrong")}>열어보기 →</button></div>
          </div>

          {/* ⑦ 내 질문 */}
          <div className="hd-card">
            <p className="hd-t">💬 내 질문</p>
            {dash.qna == null ? <p className="hd-big">…</p> : (() => {
              const done = dash.qna.filter((q) => q.status === "answered" || q.status === "adopted").length;
              const wait = dash.qna.filter((q) => q.status === "pending").length;
              return (
                <>
                  <p className="hd-big">{dash.qna.length === 0 ? "아직 없어요" : `답변 ${done}건`}</p>
                  <p className="hd-sub">{dash.qna.length === 0 ? "개념 단락이나 문항에서 물어볼 수 있어요" : wait ? `답변 기다리는 중 ${wait}건` : "질문게시판에서 다른 질문도 볼 수 있어요"}</p>
                </>
              );
            })()}
            <div className="hd-act"><button className="hd-go" onClick={() => (location.hash = "#/board/qna")}>질문게시판 →</button></div>
          </div>

          {/* ⑧ 최근 응시 시험 — test_runs + 로컬 병합, 최근 5건 */}
          <div className="hd-card hd-w2">
            <div className="hd-thead">
              <p className="hd-t">🧪 최근 응시 시험</p>
              {runs && runs.length > 0 && <span className="hd-tsub">{runs.length}건</span>}
            </div>
            {runs === null ? <p className="hd-sub" style={{ margin: 0 }}>불러오는 중…</p>
            : runs.length === 0 ? (
              <div className="hd-empty">아직 응시한 시험이 없어요.<br />단원 테스트·모의고사로 실력을 확인해 봐요.</div>
            ) : (
              <div className="hd-rows">
                {runs.map((r) => {
                  const d = describeRun(r, UNIT_NAMES);
                  return (
                    <button key={String(r.id)} type="button" className="hd-row" onClick={() => (location.hash = d.link)}>
                      <span className="ic">{presetOf(r.test_type)?.icon || "🧪"}</span>
                      <span className="tx">
                        <b>{d.name}{d.scope ? ` · ${d.scope}` : ""}</b>
                        <small>{d.score}{d.local ? " · 기기 저장" : ""}</small>
                      </span>
                      <span className="rt">{fmtWhen(d.when)}</span>
                    </button>
                  );
                })}
              </div>
            )}
            <div className="hd-act"><button className="hd-go" onClick={() => (location.hash = "#/study/exam")}>시험 보러 가기 →</button></div>
          </div>

          {/* ⑨ 자주 나온 실수 TOP — 이번 주 attempts 오개념 태그 집계 */}
          <div className="hd-card">
            <p className="hd-t">🎯 자주 나온 실수 TOP</p>
            {dash.topTags == null ? <p className="hd-sub" style={{ margin: 0 }}>불러오는 중…</p>
            : dash.topTags.length === 0 ? (
              <div className="hd-empty">이번 주엔 기록된 실수 패턴이 없어요.<br />문제를 풀면 자주 틀리는 이유를 짚어 드려요.</div>
            ) : (
              <div className="hd-chips">
                {dash.topTags.slice(0, 5).map(([tag, cnt]) => (
                  <span key={tag} className="hd-chip" title={tag}><span>{mcLabel(tag)}</span><b>×{cnt}</b></span>
                ))}
              </div>
            )}
            <div className="hd-act"><button className="hd-go" onClick={() => (location.hash = "#/learn/wrong")}>오답노트에서 정리 →</button></div>
          </div>

          {/* ⑩ 다가오는 일정 / 디데이 */}
          <div className="hd-card">
            <p className="hd-t">🗓 다가오는 일정</p>
            {events === null ? <p className="hd-sub" style={{ margin: 0 }}>불러오는 중…</p>
            : events.length === 0 ? (
              <div className="hd-empty">다가오는 디데이가 없어요.<br />시험·행사가 등록되면 여기에 보여요.</div>
            ) : (
              <div className="hd-rows">
                {events.map((e, i) => (
                  <div key={i} className="hd-row">
                    <span className="hd-dbadge">{e.days === 0 ? "D-DAY" : `D-${e.days}`}</span>
                    <span className="tx"><b>{e.title}</b><small>{e.date}</small></span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* ⑪ 철학 배너 */}
          <button className="hd-philo" onClick={() => (location.hash = "#/philosophy")}>
            <p className="hd-philo-eyebrow">ASHRAIN PHILOSOPHY</p>
            <p className="hd-philo-t">우리가 이렇게 가르치는 이유</p>
            <p className="hd-philo-d">유클리드에서 프로이덴탈까지 —<br />애쉬레인 설명 방식의 뿌리를 소개합니다</p>
            <img className="hd-philo-img" alt=""
              src="https://upload.wikimedia.org/wikipedia/commons/7/73/Frans_Hals_-_Portret_van_Ren%C3%A9_Descartes.jpg"
              onError={(e) => { e.currentTarget.style.display = "none"; }} />
            <span className="hd-philo-arrow">→</span>
          </button>
        </div>

        {/* ⑫ 베타 안내 + 미리보기 링크 */}
        <p className="hd-note">{BETA.notice}<br />불편한 점은 <a href={BETA.feedbackUrl} target="_blank" rel="noreferrer"><b>문의</b></a>로 알려 주세요.</p>
        <div className="hd-links">
          <span style={{ color: "var(--mut)", fontSize: 11.5 }}>미리보기</span>
          <a href="#/library">서재</a><a href="#/news">신문</a><a href="#/duty">조교</a>
        </div>
      </div>
      {wxEdit && <SceneEditor scenes={WEATHER_SCENES} dir="weather/main" files={wxFiles}
        onClose={() => setWxEdit(false)} onSaved={() => { setWxEdit(false); loadWxFiles(); }} />}
    </div>
  );
}
