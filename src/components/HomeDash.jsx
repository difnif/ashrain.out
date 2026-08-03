// ashrain.out — 홈 대시보드 (v2.0)
// sticky 유저 바 · 디데이 로고 · 날씨 이미지 시스템(베이스 18 + 오버레이 18 = 36셀)
// 날씨: Open-Meteo → 단계 자동 선택, 히어로 우측 사다리꼴 + 디졸브, 추위는 채도·결빙 필터
import { useEffect, useState, useCallback } from "react";
import { supabase } from "../supabaseClient";
import { SceneEditor } from "./AnimFigure";

const CSS = `
.hd-root { min-height: 100vh; padding: 0 14px 60px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; background: var(--bg); }
.hd-root * { box-sizing: border-box; }
.hd-light { --bg:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0D9488; --in:#F4F6F8; }
.hd-dark  { --bg:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#5EEAD4; --in:#101116; }
.hd-wrap { max-width: 680px; margin: 0 auto; }
.hd-top { position: sticky; top: 0; z-index: 40; background: var(--bg);
  margin: 0 -14px 12px; padding: 10px 14px 10px; }
.hd-row1 { display: flex; gap: 7px; flex-wrap: wrap; align-items: center; margin-bottom: 8px; }
.hd-sp { flex: 1; }
.hd-fn { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; }
.hd-fnbtn { background: var(--card); border: 1px solid var(--bd); border-radius: 12px; padding: 9px 0 8px;
  color: var(--ink); cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 2px; }
.hd-fnbtn span:first-child { font-size: 16px; }
.hd-fnbtn span:last-child { font-size: 11.5px; font-weight: 800; }
.hd-logo { height: 30px; }
.hd-light .hd-logo { filter: grayscale(1) brightness(0); }
.hd-dday { min-width: 34px; height: 34px; border-radius: 999px; background: #EF4444; color: #fff;
  display: flex; align-items: center; justify-content: center; font-size: 11.5px; font-weight: 800; padding: 0 7px; }
.hd-btn { background: var(--card); border: 1px solid var(--bd); border-radius: 999px; color: var(--ink);
  font-size: 12px; font-weight: 700; padding: 8px 12px; cursor: pointer; }
.hd-hero { position: relative; border-radius: 20px; padding: 26px 22px 22px; color: #fff;
  overflow: hidden; margin-bottom: 14px; box-shadow: 0 6px 22px rgba(0,0,0,.14); min-height: 150px;
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
.hd-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
@media (max-width: 480px) { .hd-grid { grid-template-columns: 1fr; } }
.hd-card { background: var(--card); border: 1px solid var(--bd); border-radius: 14px; padding: 14px 15px; position: relative; }
.hd-card.wide { grid-column: 1 / -1; }
.hd-t { font-size: 12px; font-weight: 800; color: var(--mut); letter-spacing: .5px; margin: 0 0 8px; }
.hd-big { font-size: 20px; font-weight: 800; color: var(--ink); margin: 0; }
.hd-sub { font-size: 12px; color: var(--mut); margin: 4px 0 0; line-height: 1.6; }
.hd-bar { height: 8px; background: var(--in); border-radius: 999px; overflow: hidden; margin: 10px 0 6px; }
.hd-bar > div { height: 100%; background: var(--ac); border-radius: 999px; }
.hd-go { display: inline-block; margin-top: 10px; background: transparent; border: 1.5px solid var(--ac);
  border-radius: 999px; color: var(--ac); font-size: 12px; font-weight: 800; padding: 7px 13px; cursor: pointer; }
.hd-demo { position: absolute; top: 10px; right: 12px; font-size: 9.5px; font-weight: 800;
  color: var(--mut); border: 1px solid var(--bd); border-radius: 5px; padding: 1px 5px; opacity: .8; }
.hd-week { display: flex; align-items: flex-end; gap: 6px; height: 64px; margin-top: 8px; }
.hd-wcol { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.hd-wbar { width: 100%; background: var(--ac); border-radius: 5px 5px 2px 2px; opacity: .85; }
.hd-wlab { font-size: 10px; color: var(--mut); }
.hd-philo { grid-column: 1 / -1; position: relative; border-radius: 16px; overflow: hidden; cursor: pointer;
  background: linear-gradient(120deg, #14343B 0%, #0D9488 130%); color: #fff; padding: 20px 130px 20px 20px;
  min-height: 108px; border: none; text-align: left; }
.hd-philo-eyebrow { font-size: 10.5px; letter-spacing: 2.5px; opacity: .85; margin: 0 0 6px; font-weight: 800; }
.hd-philo-t { font-size: 17px; font-weight: 800; margin: 0 0 6px; }
.hd-philo-d { font-size: 12px; opacity: .9; margin: 0; line-height: 1.6; }
.hd-philo-img { position: absolute; right: -6px; top: 0; bottom: 0; width: 120px; object-fit: cover;
  object-position: center top; opacity: .9; mask-image: linear-gradient(to right, transparent, #000 30%);
  -webkit-mask-image: linear-gradient(to right, transparent, #000 30%); }
.hd-philo-arrow { position: absolute; right: 12px; bottom: 10px; font-size: 16px; }
.hd-note { text-align: center; color: var(--mut); font-size: 11px; margin-top: 16px; line-height: 1.7; }
`;

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

function pickWeather(c) {
  const t = c.temperature_2m, p = c.precipitation || 0, code = c.weather_code,
        cc = c.cloud_cover ?? 0, ws = c.wind_speed_10m || 0;
  const snowy = [71, 73, 75, 77, 85, 86].includes(code);
  const rainy = !snowy && ([51,53,55,56,57,61,63,65,66,67,80,81,82,95,96,99].includes(code) || p > 0);
  let base;
  if (snowy)      base = "s" + (p >= 7 ? 6 : p >= 5 ? 5 : p >= 3 ? 4 : p >= 1.5 ? 3 : p >= 0.5 ? 2 : 1);
  else if (rainy) base = "r" + (p >= 20 ? 6 : p >= 10 ? 5 : p >= 5 ? 4 : p >= 2 ? 3 : p >= 0.5 ? 2 : 1);
  else            base = "c" + Math.min(6, Math.max(1, Math.round(cc / 20) + 1));
  const over = [];
  if (t <= 5)       over.push("f" + (t <= -15 ? 6 : t <= -12 ? 5 : t <= -8 ? 4 : t <= -3 ? 3 : t <= 0 ? 2 : 1));
  else if (t >= 26) over.push("h" + (t >= 35 ? 6 : t >= 33 ? 5 : t >= 31 ? 4 : t >= 29 ? 3 : t >= 27.5 ? 2 : 1));
  if (ws >= 4)      over.push("w" + (ws >= 21 ? 6 : ws >= 14 ? 5 : ws >= 11 ? 4 : ws >= 8 ? 3 : ws >= 6 ? 2 : 1));
  return { base, over, t, snowy, rainy, cloudLv: +(base[0] === "c" ? base[1] : 6) };
}

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

export default function HomeDash({ theme = "light", onToggleTheme }) {
  const [nick, setNick] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const [greet] = useState(() => GREETS[Math.floor(Math.random() * GREETS.length)]);
  const [wx, setWx] = useState(null);
  const [wxFiles, setWxFiles] = useState({});
  const [wxEdit, setWxEdit] = useState(false);
  const [dday, setDday] = useState(null);
  const now = new Date();
  const hi = skyOf(now.getHours())[1];
  const days = ["월", "화", "수", "목", "금", "토", "일"];

  useEffect(() => {
    supabase.auth.getUser().then(async ({ data }) => {
      const u = data?.user; if (!u) return;
      const { data: p } = await supabase.from("profiles").select("username, role").eq("id", u.id).maybeSingle();
      setNick(p?.username || ""); setIsAdmin(p?.role === "admin");
    });
    const today = new Date().toISOString().slice(0, 10);
    supabase.from("events").select("date, title").eq("dday", true).gte("date", today)
      .order("date").limit(1).then(({ data }) => {
        if (data?.[0]) {
          const d = Math.round((new Date(data[0].date + "T00:00:00") - new Date(today + "T00:00:00")) / 86400000);
          setDday({ days: d, title: data[0].title });
        }
      });
    fetch("https://api.open-meteo.com/v1/forecast?latitude=37.66&longitude=126.83&current=temperature_2m,precipitation,weather_code,cloud_cover,wind_speed_10m")
      .then((r) => r.json()).then((j) => { if (j?.current) setWx(pickWeather(j.current)); }).catch(() => {});
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
  const week = [35, 55, 20, 70, 45, 85, 30];

  return (
    <div className={`hd-root hd-${theme}`}>
      <style>{CSS}</style>
      <div className="hd-wrap">
        <div className="hd-top">
          <div className="hd-row1">
            {dday ? (
              <div className="hd-dday" title={dday.title}>{dday.days === 0 ? "D-DAY" : `D-${dday.days}`}</div>
            ) : (
              <img className="hd-logo" src="/brand/ashrain_logo.png" alt="ashrain" />
            )}
            <span className="hd-sp" />
            <button className="hd-btn" onClick={() => (location.hash = "#/me")}>👤 마이페이지</button>
            <a className="hd-btn" style={{ textDecoration: "none", display: "flex", alignItems: "center", gap: 5 }}
              href="https://www.instagram.com/ashrain.out" target="_blank" rel="noreferrer" title="앱 문의">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 3a6 6 0 0 0-3.7 10.7c.6.5 1 1.3 1 2.1v.2h5.4v-.2c0-.8.4-1.6 1-2.1A6 6 0 0 0 12 3z" />
                <path d="M9.5 19h5" /><path d="M10.5 21.5h3" />
              </svg> 문의
            </a>
            {onToggleTheme && <button className="hd-btn" onClick={onToggleTheme}>{theme === "dark" ? "☀️" : "🌙"}</button>}
            {isAdmin && <>
              <button className="hd-btn" onClick={() => (location.hash = "#/admin/concepts")}>📚 개념 등록</button>
              <button className="hd-btn" onClick={() => (location.hash = "#/admin/qna")}>💬 질문 검토</button>
              <button className="hd-btn" onClick={() => (location.hash = "#/admin/chats")}>🗂 질문대화</button>
              <button className="hd-btn" onClick={() => (location.hash = "#/admin/images")}>🖼 이미지 현황</button>
              <button className="hd-btn" onClick={() => (location.hash = "#/admin/calendar")}>🗓 시험일정</button>
            </>}
          </div>
          <div className="hd-fn">
            {[["📚", "개념", "learn"], ["🧮", "연산", "calc"], ["📕", "오답", "wrong"], ["🗝️", "힌트", "hint"]].map(([ic, lb, c]) => (
              <button key={c} className="hd-fnbtn"
                onClick={() => { sessionStorage.setItem("home_cat", c); location.hash = "#/learn"; }}>
                <span>{ic}</span><span>{lb}</span>
              </button>
            ))}
            <button className="hd-fnbtn" onClick={() => (location.hash = "#/board")}>
              <span>💬</span><span>질문</span>
            </button>
          </div>
        </div>

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
          <span className="hd-hero-time">{now.getMonth() + 1}월 {now.getDate()}일 · {days[(now.getDay() + 6) % 7]}요일</span>
          {isAdmin && <button className="hd-wxpen" title="날씨 이미지 업로드" onClick={() => setWxEdit(true)}>🌦✏️</button>}
        </div>

        <div className="hd-grid">
          <div className="hd-card wide">
            <span className="hd-demo">DEMO</span>
            <p className="hd-t">▶ 이어서 학습</p>
            <p className="hd-big">A01 · 소수와 합성수</p>
            <div className="hd-bar"><div style={{ width: "60%" }} /></div>
            <p className="hd-sub">단락 3/5 읽음 · 어제 저녁에 보다 멈췄어요</p>
            <button className="hd-go" onClick={() => (location.hash = "#/c/m1-1-01")}>이어보기 →</button>
          </div>
          <div className="hd-card">
            <span className="hd-demo">DEMO</span>
            <p className="hd-t">🔥 연속 출석</p>
            <p className="hd-big">12일째</p>
            <p className="hd-sub">이번 주 5일 접속 — 최고 기록까지 3일!</p>
          </div>
          <div className="hd-card">
            <span className="hd-demo">DEMO</span>
            <p className="hd-t">📕 오답노트</p>
            <p className="hd-big">미복습 4문제</p>
            <p className="hd-sub">정수와 유리수 2 · 소인수분해 2</p>
          </div>
          <div className="hd-card wide">
            <span className="hd-demo">DEMO</span>
            <p className="hd-t">📈 이번 주 학습 시간 <span style={{ fontWeight: 600 }}>· 합계 5시간 40분</span></p>
            <div className="hd-week">
              {week.map((v, i) => (
                <div key={i} className="hd-wcol">
                  <div className="hd-wbar" style={{ height: `${v}%`, opacity: i === (now.getDay() + 6) % 7 ? 1 : 0.5 }} />
                  <span className="hd-wlab">{days[i]}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="hd-card">
            <span className="hd-demo">DEMO</span>
            <p className="hd-t">⚡ 연산 스피드</p>
            <p className="hd-big">92점 · 4분 12초</p>
            <p className="hd-sub">지난 기록보다 38초 빨라졌어요</p>
          </div>
          <div className="hd-card">
            <span className="hd-demo">DEMO</span>
            <p className="hd-t">💬 내 질문</p>
            <p className="hd-big">답변 완료 1건</p>
            <p className="hd-sub">A01-1 약수 질문에 답이 달렸어요</p>
            <button className="hd-go" onClick={() => (location.hash = "#/board")}>보러 가기 →</button>
          </div>
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

        <p className="hd-note">대시보드 수치는 데모예요 — 활동 기록 기능이 연결되면 실제 데이터로 채워집니다.</p>
      </div>
      {wxEdit && <SceneEditor scenes={WEATHER_SCENES} dir="weather/main" files={wxFiles}
        onClose={() => setWxEdit(false)} onSaved={() => { setWxEdit(false); loadWxFiles(); }} />}
    </div>
  );
}
