// 시록고 — 게임 (#/games) · 강사(와 관리자)가 직접 해 보며 다듬는 게임 자리. 조교 모드에서는 열리지 않는다(SeiroccoApp 의 AST).
// 지금은 굴뚝새(1막 · 베타) 하나 — src/features/games/gulttuksae.html. 설계 문서는 BG-보드게임 프로젝트의 claude/굴뚝새.md.
// 게임은 HTML 한 장이다. 이 화면이 열릴 때만 내려받고(따로 나뉜 파일), 샌드박스 iframe(allow-scripts — 앱의 저장소 · 로그인 세션에 닿지 않는다)에 띄운다.
// 관리자 게임(src/pages/AdminGames.jsx)과 같은 약속을 쓴다:
//   테마 — 처음엔 문서에 data-theme 으로 심고, 앱 테마가 바뀌면 { type: "ash-theme", theme } 을 넘긴다(판이 새로 시작되지 않는다).
//   전체 화면 — 게임이 Fullscreen API 를 먼저 쓰고, 막힌 기기에서는 { type: "ash-immersive", on } 을 보내면 iframe 을 화면 가득 띄운다.
//   저장 — { type: "ash-store-get" | "ash-store-set", key, data } 를 받아 이 기기의 localStorage("ashrain.games.<key>")에 맡아 두고
//          { type: "ash-store", key, data } 로 돌려준다(이 iframe 에서 온 것만, 20KB 까지).
import { useEffect, useMemo, useRef, useState } from "react";
import { useTheme } from "../../../lib/theme";

const GAME = { key: "gulttuksae", title: "굴뚝새", sub: "질문으로 건너는 겨울 · 1막 스페이스 · 베타",
  load: () => import("../../../features/games/gulttuksae.html?raw") };
const STORE_PREFIX = "ashrain.games.";
const themeOf = (t) => (t === "light" ? "light" : "dark");

export default function Games() {
  const { theme } = useTheme();
  const [html, setHtml] = useState(null);
  const [err, setErr] = useState("");
  const [imm, setImm] = useState(false);
  const frame = useRef(null);
  const themeNow = useRef(theme);
  themeNow.current = theme;

  useEffect(() => {
    let alive = true;
    GAME.load()
      .then((m) => { if (alive) setHtml(m.default); })
      .catch(() => { if (alive) setErr("게임을 불러오지 못했어요. 새로고침해 주세요."); });
    return () => { alive = false; };
  }, []);

  // 게임이 보내는 전체 화면 · 저장 요청 — 이 iframe 에서 온 것만
  useEffect(() => {
    const on = (e) => {
      if (!frame.current || e.source !== frame.current.contentWindow) return;
      const d = e.data;
      if (!d || typeof d !== "object") return;
      if (d.type === "ash-immersive") { setImm(!!d.on); return; }
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
  const doc = useMemo(() => html && html.replace('<html lang="ko">', `<html lang="ko" data-theme="${themeOf(themeNow.current)}">`), [html]);
  const post = () => frame.current?.contentWindow?.postMessage({ type: "ash-theme", theme: themeOf(themeNow.current) }, "*");
  useEffect(() => { post(); }, [theme]);

  return (
    <div className={"sg-root" + (imm ? " sg-imm" : "")}>
      <style>{CSS}</style>
      <div className="sg-head">
        <b>게임</b>
        <span className="sg-sub">{GAME.title} — {GAME.sub} · 강사가 해 보며 다듬는 중</span>
      </div>
      {err ? <p className="sg-note">{err}</p>
        : !doc ? <p className="sg-note">여는 중…</p>
        : <iframe ref={frame} className="sg-frame" title={GAME.title} srcDoc={doc} sandbox="allow-scripts"
            allow="fullscreen; autoplay" allowFullScreen onLoad={post} />}
    </div>
  );
}

const CSS = `
.ap-wrap.g-wide { max-width: 1280px; }
.sg-root { display: flex; flex-direction: column; gap: 8px; }
.sg-head { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; font-size: 14px; color: var(--ink); }
.sg-sub { color: var(--mut); font-size: 12.5px; }
.sg-frame { width: 100%; height: calc(100vh - 200px); height: calc(100dvh - 200px); min-height: 560px;
  border: 1px solid var(--bd); border-radius: 14px; display: block; background: transparent; }
.sg-imm .sg-frame { position: fixed; inset: 0; width: 100vw; height: 100vh; height: 100dvh; min-height: 0;
  border: 0; border-radius: 0; z-index: 1000; }
.sg-note { text-align: center; padding: 48px 16px; margin: 0; font-size: 14px; color: var(--mut); }
`;
