// 학습 도구 리프 페이지 래퍼 — 오답노트·사진 힌트·스피드 연산을 셸 없이(FeatureBar만) 단독으로 띄운다.
// 예전에는 Home(#/learn) 카테고리 탭 안에 있었으나, ui-v3 부터 도구함(#/tools)에서 바로 들어온다.
import { useEffect, useState } from "react";
import { supabase } from "../supabaseClient";
import { UNIT_NAMES } from "../lib/items";
import FeatureBar from "../components/FeatureBar";
import WrongNote from "../components/WrongNote";
import Hint from "../components/Hint";
import Calc from "../components/Calc";

const KINDS = {
  wrong: { title: "오답노트", C: WrongNote },
  hint: { title: "사진 힌트", C: Hint },
  calc: { title: "스피드 연산", C: Calc },
};

const CSS = `
.lf-root { min-height: 100vh; padding: 0 14px 40px; box-sizing: border-box; background: var(--pbg);
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.lf-root * { box-sizing: border-box; }
.lf-light { --pbg:#EDEFF2; --ink:#1F2937; --mut:#8A929C; --card:#fff; --bd:#DFE3E8; --ac:#0DA95F; --in:#F4F6F8; --inbd:#D3D9DF; }
.lf-dark  { --pbg:#0B0C0F; --ink:#E2E8F0; --mut:#6B7280; --card:#15171C; --bd:#23262D; --ac:#FFE03C; --in:#101116; --inbd:#2B2E36; }
.lf-wrap { max-width: 680px; margin: 0 auto; padding-top: 12px; color: var(--ink); }
.lf-toast { position: fixed; left: 50%; transform: translateX(-50%); bottom: 24px; z-index: 90;
  background: var(--ink); color: var(--pbg); font-size: 12.5px; font-weight: 700; border-radius: 999px; padding: 9px 16px; }
`;

export default function ToolLeaf({ kind, theme = "light" }) {
  const k = KINDS[kind] || KINDS.wrong;
  const [uid, setUid] = useState(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const [toast, setToast] = useState("");
  useEffect(() => {
    supabase.auth.getUser().then(async ({ data }) => {
      const u = data?.user; if (!u) return;
      setUid(u.id);
      const { data: p } = await supabase.from("profiles").select("role").eq("id", u.id).maybeSingle();
      setIsAdmin(p?.role === "admin");
    });
  }, []);
  const say = (m) => { setToast(m); setTimeout(() => setToast(""), 2200); };
  const C = k.C;
  return (
    <>
      <FeatureBar theme={theme} title={k.title} back="#/tools" />
      <div className={`lf-root lf-${theme}`}>
        <style>{CSS}</style>
        <div className="lf-wrap">
          <C uid={uid} isAdmin={isAdmin} unitNames={UNIT_NAMES} say={say} />
        </div>
        {toast && <div className="lf-toast">{toast}</div>}
      </div>
    </>
  );
}
