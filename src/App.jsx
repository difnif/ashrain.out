import { useEffect, useState } from "react";
import { supabase } from "./supabaseClient";
import { useTheme } from "./lib/theme";
import SplashAuth from "./components/SplashAuth";
import Signup from "./components/Signup";
import Home from "./components/Home";
import ConceptViewer from "./components/ConceptViewer";
import AdminQna from "./components/AdminQna";
import AdminConcepts from "./components/AdminConcepts";
import MyPage from "./components/MyPage";
import PortraitStudio from "./features/portrait/PortraitStudio";

function useHash() {
  const [hash, setHash] = useState(location.hash);
  useEffect(() => {
    const h = () => setHash(location.hash);
    window.addEventListener("hashchange", h);
    return () => window.removeEventListener("hashchange", h);
  }, []);
  return hash;
}

export default function App() {
  const { theme, toggle } = useTheme();
  const hash = useHash();
  const [session, setSession] = useState(undefined); // undefined = 로딩 중

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => setSession(data.session ?? null));
    const { data: sub } = supabase.auth.onAuthStateChange((_e, s) => setSession(s));
    return () => sub.subscription.unsubscribe();
  }, []);

  if (session === undefined) return null;

  // 비로그인 라우트
  if (!session) {
    if (hash.startsWith("#/signup")) return <Signup theme={theme} />;
    return <SplashAuth theme={theme} onToggleTheme={toggle} onSuccess={() => (location.hash = "")} />;
  }

  // 로그인 라우트
  const c = hash.match(/^#\/c\/(.+)$/);
  if (c) return <ConceptViewer conceptId={decodeURIComponent(c[1])} theme={theme} />;
  if (hash.startsWith("#/portrait")) {
    return (
      <PortraitStudio onDone={async (blob) => {
        const uid = session.user.id;
        const { error } = await supabase.storage.from("avatars")
          .upload(`${uid}/portrait.png`, blob, { upsert: true, contentType: "image/png" });
        if (!error) {
          const { data } = supabase.storage.from("avatars").getPublicUrl(`${uid}/portrait.png`);
          await supabase.from("profiles").update({ avatar_url: data.publicUrl }).eq("id", uid);
          alert("초상화가 프로필에 저장됐어요!");
          location.hash = "";
        } else alert("저장에 실패했어요. 잠시 후 다시 시도해 주세요.");
      }} />
    );
  }
  if (hash.startsWith("#/admin/qna")) return <AdminQna theme={theme} />;
  if (hash.startsWith("#/admin/concepts")) return <AdminConcepts theme={theme} />;
  if (hash.startsWith("#/me")) return <MyPage theme={theme} onToggleTheme={toggle} />;
  return <Home theme={theme} onToggleTheme={toggle} />;
}
