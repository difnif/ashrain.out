// 관리자 — 게임 (#/admin/games)
// 일차함수 그래프 학습 게임 「기울기 샷」(포켓볼 · 사구 · 컬링, 혼자 · 둘이 번갈아). 학생 공개 전까지 관리자 전용.
// 게임은 HTML 한 장(src/features/games/slope-shot.html)이다. 관리자 확인이 끝난 뒤에만 내려받고(따로 나뉜 파일),
// 샌드박스 iframe(allow-scripts — 앱의 저장소 · 로그인 세션에 닿지 않는다)에 띄운다.
// 테마: 처음엔 문서에 data-theme 으로 심고(번쩍임 없음), 앱 테마가 바뀌면 postMessage 로 넘긴다(판이 새로 시작되지 않는다).
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import FeatureBar from "../components/FeatureBar";

const themeMsg = (theme) => ({ type: "ash-theme", theme: theme === "light" ? "light" : "dark" });

export default function AdminGames({ theme = "dark" }) {
  const [me, setMe] = useState(undefined);    // undefined 확인 중 | false 비관리자 | true
  const [html, setHtml] = useState(null);
  const [err, setErr] = useState("");
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
    import("../features/games/slope-shot.html?raw")
      .then((m) => { if (alive) setHtml(m.default); })
      .catch(() => { if (alive) setErr("게임을 불러오지 못했어요. 새로고침해 주세요."); });
    return () => { alive = false; };
  }, [me]);

  // 문서가 처음 올 때의 테마를 심는다 — 이후 테마가 바뀌어도 srcDoc 은 그대로(다시 읽히지 않게)
  const doc = useMemo(() => html && html.replace('<html lang="ko">',
    `<html lang="ko" data-theme="${themeMsg(themeNow.current).theme}">`), [html]);
  const post = () => frame.current?.contentWindow?.postMessage(themeMsg(themeNow.current), "*");
  useEffect(() => { post(); }, [theme]);

  if (me === undefined) return null;
  return (
    <div className={`ag-root ag-${theme}`}>
      <style>{CSS}</style>
      <FeatureBar theme={theme} title="게임" sub={me ? "기울기 샷 · 관리자 전용" : undefined} back="#/" />
      {!me ? <p className="ag-note">관리자만 들어올 수 있는 곳이에요.</p>
        : err ? <p className="ag-note">{err}</p>
        : !doc ? <p className="ag-note">여는 중…</p>
        : <iframe ref={frame} className="ag-frame" title="기울기 샷" srcDoc={doc} sandbox="allow-scripts" onLoad={post} />}
    </div>
  );
}

const CSS = `
.ag-root { display: flex; flex-direction: column; height: 100vh; height: 100dvh; background: var(--agbg); color: var(--agmut); }
.ag-dark { --agbg: #1A140D; --agmut: #A79A80; }
.ag-light { --agbg: #F1E8D5; --agmut: #7E6F54; }
.ag-root .fb { flex: none; }
.ag-frame { flex: 1 1 auto; min-height: 0; width: 100%; border: 0; display: block; background: var(--agbg); }
.ag-note { text-align: center; padding: 48px 16px; margin: 0; font-size: 14px;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
`;
