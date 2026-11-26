// 관리자 — 게임 (#/admin/games · #/admin/games/po · #/admin/games/sb)
// 학생 공개 전까지 관리자 전용 게임 세 가지:
//   · 기울기 샷(#/admin/games) — 일차함수 당구(포켓볼 · 사구 · 컬링, 혼자 · 둘이 번갈아) — src/features/games/slope-shot.html
//   · 포의 민족(#/admin/games/po) — 이차함수 포격전(스토리 12장 · 2인 대전 · 프리 모드) — src/features/games/po-minjok.html
//   · 선빵스타즈(#/admin/games/sb) — 가진 직선 y = ax + b 위로만 달리는 3대3 난투(문제를 많이 푼 상태로 시작) — src/features/games/sbstars.html
// 게임은 HTML 한 장이다. 관리자 확인이 끝난 뒤에만 내려받고(따로 나뉜 파일),
// 샌드박스 iframe(allow-scripts — 앱의 저장소 · 로그인 세션에 닿지 않는다)에 띄운다. 전체 화면 · 소리를 위해 allow="fullscreen; autoplay".
// 테마: 처음엔 문서에 data-theme 으로 심고(번쩍임 없음), 앱 테마가 바뀌면 postMessage 로 넘긴다(판이 새로 시작되지 않는다).
// 전체 화면: 게임이 Fullscreen API 를 먼저 쓰고, 막힌 기기에서는 { type: "ash-immersive", on } 을 보내면 여기서 상단 바를 숨긴다.
// 진행 저장: 샌드박스라 게임이 localStorage 를 못 쓴다 — { type: "ash-store-get" | "ash-store-set", key, data } 를 받아
//   이 기기의 localStorage("ashrain.games.<key>")에 맡아 두고 { type: "ash-store", key, data } 로 돌려준다(이 iframe 에서 온 것만, 20KB 까지).
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import FeatureBar, { FbAct } from "../components/FeatureBar";

const GAMES = {
  slope: { title: "기울기 샷", hash: "#/admin/games", load: () => import("../features/games/slope-shot.html?raw") },
  po: { title: "포의 민족", hash: "#/admin/games/po", load: () => import("../features/games/po-minjok.html?raw") },
  sb: { title: "선빵스타즈", hash: "#/admin/games/sb", load: () => import("../features/games/sbstars.html?raw") },
};
const STORE_PREFIX = "ashrain.games.";
const themeMsg = (theme) => ({ type: "ash-theme", theme: theme === "light" ? "light" : "dark" });

export default function AdminGames({ theme = "dark", game = "slope" }) {
  const g = GAMES[game] ? game : "slope";
  const [me, setMe] = useState(undefined);    // undefined 확인 중 | false 비관리자 | true
  const [html, setHtml] = useState(null);      // { game, text }
  const [err, setErr] = useState("");
  const [immersive, setImmersive] = useState(false);
  const frame = useRef(null);
  const themeNow = useRef(theme);
  themeNow.current = theme;

  useEffect(() => {
    let alive = true;
    supabase.auth.getUser().then(async ({ data }) => {
      const u = data?.user; if (!u) { if (alive) setMe(false); return; }
      const { data: p } = await supabase.from("profiles").select("role").eq("id", u.id).maybeSingle();
      if (alive) setMe(p?.role === "admin");
    }).catch(() => { if (alive) setMe(false); });
    return () => { alive = false; };
  }, []);

  useEffect(() => {
    if (me !== true) return;
    let alive = true;
    setErr(""); setImmersive(false);
    GAMES[g].load()
      .then((m) => { if (alive) setHtml({ game: g, text: m.default }); })
      .catch(() => { if (alive) setErr("게임을 불러오지 못했어요. 새로고침해 주세요."); });
    return () => { alive = false; };
  }, [me, g]);

  // 게임이 보내는 몰입 모드(상단 바 숨김) · 진행 저장 요청 — 이 iframe 에서 온 것만
  useEffect(() => {
    const on = (e) => {
      if (!frame.current || e.source !== frame.current.contentWindow) return;
      const d = e.data;
      if (!d || typeof d !== "object") return;
      if (d.type === "ash-immersive") { setImmersive(!!d.on); return; }
      if ((d.type !== "ash-store-get" && d.type !== "ash-store-set") || !/^[a-z0-9-]{1,40}$/.test(d.key || "")) return;
      const k = STORE_PREFIX + d.key;
      if (d.type === "ash-store-set") {
        try { const s = JSON.stringify(d.data ?? null); if (s.length <= 20000) localStorage.setItem(k, s); } catch { /* 저장소가 막혀도 게임은 돈다 */ }
        return;
      }
      let data = null;
      try { data = JSON.parse(localStorage.getItem(k) || "null"); } catch { data = null; }
      e.source.postMessage({ type: "ash-store", key: d.key, data }, "*");
    };
    window.addEventListener("message", on);
    return () => window.removeEventListener("message", on);
  }, []);

  // 문서가 처음 올 때의 테마를 심는다 — 이후 테마가 바뀌어도 srcDoc 은 그대로(다시 읽히지 않게)
  const doc = useMemo(() => html && html.game === g && html.text.replace('<html lang="ko">',
    `<html lang="ko" data-theme="${themeMsg(themeNow.current).theme}">`), [html, g]);
  const post = () => frame.current?.contentWindow?.postMessage(themeMsg(themeNow.current), "*");
  useEffect(() => { post(); }, [theme]);

  if (me === undefined) return null;
  const tabs = me ? Object.entries(GAMES).map(([id, x]) => (
    <FbAct key={id} pri={id === g} onClick={() => { if (location.hash !== x.hash) location.hash = x.hash; }}>{x.title}</FbAct>
  )) : null;
  return (
    <div className={`ag-root ag-${theme}${immersive ? " ag-imm" : ""}`}>
      <style>{CSS}</style>
      <FeatureBar theme={theme} title="게임" sub={me ? "관리자 전용" : undefined} back="#/" actions={tabs} />
      {!me ? <p className="ag-note">관리자만 들어올 수 있는 곳이에요.</p>
        : err ? <p className="ag-note">{err}</p>
        : !doc ? <p className="ag-note">여는 중…</p>
        : <iframe key={g} ref={frame} className="ag-frame" title={GAMES[g].title} srcDoc={doc} sandbox="allow-scripts"
            allow="fullscreen; autoplay" allowFullScreen onLoad={post} />}
    </div>
  );
}

const CSS = `
.ag-root { display: flex; flex-direction: column; height: 100vh; height: 100dvh; background: var(--agbg); color: var(--agmut); }
.ag-dark { --agbg: #1A140D; --agmut: #A79A80; }
.ag-light { --agbg: #F1E8D5; --agmut: #7E6F54; }
.ag-root .fb { flex: none; }
.ag-imm .fb { display: none; }
.ag-frame { flex: 1 1 auto; min-height: 0; width: 100%; border: 0; display: block; background: var(--agbg); }
.ag-note { text-align: center; padding: 48px 16px; margin: 0; font-size: 14px;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
`;
