// 관리자 — 우물·탭바 편집 (#/admin/well)
// 미리보기에서 이미지를 드러낸 채 동그란 우물을 직접 눌러 편집 모드로 들어간다.
// 크기 슬라이더(탭바·우물 자리·이미지)와 기본 우물 이미지 교체를 여기서 — 저장하면 app_settings.well_ui 로 전 학생에게 적용.
// 연출은 3가지: 맑음 = 해 그림자 · 흐림/비 = 감광 · 밤 = 중앙 조명.
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import FeatureBar, { FbAct } from "../components/FeatureBar";
import { TabsRow } from "../components/Shell";
import { useWellImg, bustWellImg, WELL_BUNDLED } from "../components/Well";
import { WELL_DEFAULT, clampWellCfg } from "../lib/well";

const MCHIPS = [["", "자동(실황)"], ["sun", "☀️ 맑음"], ["dim", "☁️ 흐림·비"], ["night", "🌙 밤"]];

function Rg({ label, v, min, max, step = 1, unit = "", on }) {
  return (
    <label className="aw-rg">
      <span className="aw-rl">{label}</span>
      <input type="range" min={min} max={max} step={step} value={v} onChange={(e) => on(Number(e.target.value))} />
      <span className="aw-rv">{v}{unit}</span>
    </label>
  );
}

export default function AdminWell({ theme = "light" }) {
  const [me, setMe] = useState(undefined); // undefined 로딩 | false 비관리자 | true
  const [draft, setDraft] = useState(() => {
    try { return clampWellCfg(localStorage.getItem("ash.wellui")); } catch { return clampWellCfg(null); }
  });
  const [edit, setEdit] = useState(false);
  const [dirty, setDirty] = useState(false);
  const [busy, setBusy] = useState(false);
  const [toast, setToast] = useState("");
  const [pvTheme, setPvTheme] = useState(theme);
  const [mode, setMode] = useState("");                  // "" = 자동(실황) | sun | dim | night
  const [hour, setHour] = useState(() => new Date().getHours());
  const [heading, setHeading] = useState(0);
  const [bust, setBust] = useState(0);
  const [rmAsk, setRmAsk] = useState(false);             // 삭제 2단계 확인
  const img = useWellImg(bust);                          // 스토리지 교체본 (없으면 번들)
  const fileRef = useRef(null);

  useEffect(() => {
    supabase.auth.getUser().then(async ({ data }) => {
      const u = data?.user; if (!u) { setMe(false); return; }
      const { data: p } = await supabase.from("profiles").select("role").eq("id", u.id).maybeSingle();
      setMe(p?.role === "admin");
    });
    supabase.from("app_settings").select("value").eq("key", "well_ui").maybeSingle()
      .then(({ data }) => { if (data?.value) setDraft(clampWellCfg(data.value)); })
      .catch(() => {});
  }, []);
  useEffect(() => { if (!toast) return; const t = setTimeout(() => setToast(""), 2600); return () => clearTimeout(t); }, [toast]);

  const set = (path, v) => {
    setDraft((c) => {
      const n = { ...c, [path[0]]: { ...c[path[0]], [path[1]]: v } };
      return n;
    });
    setDirty(true);
  };

  const save = async () => {
    if (busy) return;
    setBusy(true);
    const { error } = await supabase.from("app_settings")
      .upsert({ key: "well_ui", value: JSON.stringify(draft), updated_at: new Date().toISOString() }, { onConflict: "key" });
    if (!error) {
      try { localStorage.setItem("ash.wellui", JSON.stringify(draft)); } catch { /* 무시 */ }
      window.dispatchEvent(new Event("ash:wellui"));
      setDirty(false);
      setToast("저장했어요 — 학생앱 탭바에 바로 적용돼요");
    } else setToast("저장에 실패했어요: " + error.message);
    setBusy(false);
  };

  const upload = async (file) => {
    if (!file) return;
    setBusy(true);
    try {
      const old = img?.name;
      const ext = (file.name.split(".").pop() || "png").toLowerCase();
      if (old && old !== `base.${ext}`) await supabase.storage.from("figures").remove([`well/${old}`]);
      const { error } = await supabase.storage.from("figures")
        .upload(`well/base.${ext}`, file, { upsert: true, contentType: file.type || "image/png" });
      if (error) setToast("업로드 실패: " + error.message);
      else { bustWellImg(); setBust((b) => b + 1); setToast("교체했어요 — 배경이 투명한 정사각형 이미지가 가장 예뻐요"); }
    } finally { setBusy(false); }
  };

  const removeImg = async () => {
    if (!img) return;
    setBusy(true);
    const { error } = await supabase.storage.from("figures").remove([`well/${img.name}`]);
    if (error) setToast("삭제 실패: " + error.message);
    else { bustWellImg(); setBust((b) => b + 1); setToast("지웠어요 — 기본 우물 그림으로 돌아가요"); }
    setRmAsk(false); setBusy(false);
  };

  const pvHash = "#/";
  const wellProps = useMemo(() => ({
    reveal: true,
    modeOverride: mode || null,
    hourOverride: hour,
    headingOverride: heading,
  }), [mode, hour, heading]);

  if (me === undefined) return null;
  if (me === false) {
    return (<>
      <FeatureBar theme={theme} title="우물·탭바" back="#/" />
      <div className={`aw-root aw-${theme}`}><style>{CSS}</style>
        <p className="aw-note">관리자만 들어올 수 있는 곳이에요.</p>
      </div>
    </>);
  }

  return (<>
    <FeatureBar theme={theme} title="우물·탭바" sub="시간·날씨 따라 변하는 메인 테마"
      back="#/" actions={<FbAct pri onClick={save} title="전 학생에게 적용">{busy ? "저장 중…" : dirty ? "저장*" : "저장"}</FbAct>} />
    <div className={`aw-root aw-${theme}`}>
      <style>{CSS}</style>
      <div className="aw-wrap">

        <div className="aw-card">
          <p className="aw-t">미리보기</p>
          <p className="aw-d">아래 탭바의 <b>우물(동그란 부분)을 누르면 편집 모드</b>가 열려요. 이미지는 미리보기에서 항상 드러나 있어요.</p>
          <div className="aw-chips">
            {[["light", "☀️ 라이트"], ["dark", "🌙 다크"]].map(([k, l]) => (
              <button key={k} className={"aw-chip" + (pvTheme === k ? " on" : "")} onClick={() => setPvTheme(k)}>{l}</button>
            ))}
            <span className="aw-gap" />
            {MCHIPS.map(([k, l]) => (
              <button key={k || "auto"} className={"aw-chip" + (mode === k ? " on" : "")} onClick={() => setMode(k)}>{l}</button>
            ))}
          </div>
          <div className={`aw-stage aw-st-${pvTheme}` + (edit ? " edit" : "")}>
            <div className="aw-fakepage" aria-hidden="true"><span /><span /><span /></div>
            <TabsRow theme={pvTheme} hash={pvHash} cfg={draft} onWell={() => setEdit((e) => !e)} wellProps={wellProps} />
          </div>
          <div className="aw-timeline">
            <Rg label="시각" v={hour} min={0} max={23} unit="시" on={setHour} />
            <Rg label="화면 방위" v={heading} min={0} max={359} unit="°" on={setHeading} />
            <p className="aw-hint">맑음 상태에서 해 그림자가 시각·방위에 맞춰 도는지 확인해요. 실제 앱은 실시간 시각·실황과 (되는 기기에서) 나침반을 써요.</p>
          </div>
        </div>

        {edit && (
          <div className="aw-card" data-testid="aw-edit">
            <p className="aw-t">크기 조절</p>
            <Rg label="탭바 높이" v={draft.bar.h} min={40} max={80} unit="px" on={(v) => set(["bar", "h"], v)} />
            <Rg label="탭 크기" v={draft.bar.tab} min={70} max={130} unit="%" on={(v) => set(["bar", "tab"], v)} />
            <Rg label="우물 자리 지름" v={draft.btn.d} min={32} max={72} unit="px" on={(v) => set(["btn", "d"], v)} />
            <Rg label="위로 튀어나옴" v={draft.btn.dy} min={0} max={28} unit="px" on={(v) => set(["btn", "dy"], v)} />
            <Rg label="이미지 크기" v={draft.img.scale} min={100} max={340} unit="%" on={(v) => set(["img", "scale"], v)} />
            <Rg label="이미지 올리기(+위)" v={draft.img.dy} min={-40} max={40} unit="px" on={(v) => set(["img", "dy"], v)} />
            <div className="aw-toggles">
              {[["img", "on", "이미지 표시(학생앱)"], ["fx", "shadow", "해 그림자"], ["fx", "compass", "나침반 연동"]].map(([a, b, l]) => (
                <label key={a + b} className="aw-tg">
                  <input type="checkbox" checked={draft[a][b]} onChange={(e) => set([a, b], e.target.checked)} /> {l}
                </label>
              ))}
            </div>
            <p className="aw-hint">우물 자리(원)는 위치 표시일 뿐이에요 — 이미지는 그보다 크게 얹혀야 잘리지 않아요. 기본은 이미지 크기 200%.</p>
            <button className="aw-reset" onClick={() => { setDraft(clampWellCfg(null)); setDirty(true); }}>기본값으로</button>
          </div>
        )}

        <div className="aw-card">
          <p className="aw-t">기본 우물 이미지</p>
          <p className="aw-d">우물 그림은 <b>한 장</b>이에요(템페라 화풍 돌우물이 기본 내장). 다른 그림으로 바꾸려면
            <b> 배경을 투명하게 오려낸 정사각형 이미지</b>(구멍이 가운데)를 올려주세요. 지우면 기본 그림으로 돌아가요.</p>
          <div className="aw-imgs">
            <div className="aw-img">
              <div className="aw-thumb">
                <img src={img ? img.url : WELL_BUNDLED} alt="기본 우물" />
              </div>
              <p className="aw-il">{img ? "교체본 사용 중" : "기본 내장 그림"}</p>
              <div className="aw-ib">
                <label className="aw-up">
                  교체하기
                  <input ref={fileRef} type="file" accept="image/png,image/webp,image/avif"
                    onChange={(e) => { upload(e.target.files?.[0]); e.target.value = ""; }} />
                </label>
                {img && (rmAsk
                  ? <button className="aw-rm sure" onClick={removeImg}>정말 지우기</button>
                  : <button className="aw-rm" onClick={() => setRmAsk(true)}>지우기</button>)}
              </div>
            </div>
          </div>
        </div>

        <div className="aw-card">
          <p className="aw-t">동작 방식 — 연출 3가지</p>
          <p className="aw-d">
            우물은 대시보드 히어로와 같은 실황(강수·구름)과 시각만 봐요. <b>맑은 낮</b>엔 태양 각도를 계산해
            해시계처럼 짙은 그림자가 실시간으로 돌고 길이도 변해요 — 해가 낮을수록(아침·저녁, 겨울) 길고 한여름 한낮엔 짧아요
            (나침반 되는 기기는 폰 방향까지 반영). <b>흐리거나 비·눈</b>이면 그림자 없이
            명도만 낮아지고, <b>밤(20시~6시)</b>엔 우물 중앙에 조명이 비치는 연출이 들어가요.
          </p>
        </div>
      </div>
      {toast && <div className="aw-toast">{toast}</div>}
    </div>
  </>);
}

const CSS = `
.aw-root { min-height: 100vh; padding: 12px 14px 60px; box-sizing: border-box; background: var(--awbg); color: var(--awink);
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.aw-root * { box-sizing: border-box; }
.aw-light { --awbg:#EDEFF2; --awcard:#fff; --awbd:#DFE3E8; --awink:#1F2937; --awmut:#8A929C; --awac:#0D9488; }
.aw-dark { --awbg:#0B0C0F; --awcard:#15171C; --awbd:#23262D; --awink:#E2E8F0; --awmut:#8A929C; --awac:#5EEAD4; }
.aw-wrap { max-width: 560px; margin: 0 auto; display: flex; flex-direction: column; gap: 10px; }
.aw-card { background: var(--awcard); border: 1px solid var(--awbd); border-radius: 14px; padding: 14px; }
.aw-t { margin: 0 0 6px; font-size: 14px; font-weight: 800; }
.aw-d { margin: 0 0 10px; font-size: 12px; color: var(--awmut); line-height: 1.65; }
.aw-d b { color: var(--awink); }
.aw-note { text-align: center; color: var(--awmut); padding: 48px 0; }
.aw-chips { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px; align-items: center; }
.aw-gap { width: 6px; }
.aw-chip { background: none; border: 1px solid var(--awbd); border-radius: 999px; color: var(--awmut);
  font-size: 11.5px; font-weight: 700; padding: 5px 10px; cursor: pointer; font-family: inherit; }
.aw-chip.on { color: var(--awac); border-color: var(--awac); }
.aw-stage { border: 1px solid var(--awbd); border-radius: 14px; overflow: hidden; position: relative; }
.aw-stage.edit { outline: 2px solid var(--awac); outline-offset: -2px; }
.aw-st-light { background: #EDEFF2; }
.aw-st-dark { background: #0B0C0F; }
.aw-fakepage { height: 116px; display: flex; flex-direction: column; gap: 8px; padding: 14px 16px; opacity: .5; }
.aw-fakepage span { display: block; border-radius: 8px; background: var(--awbd); height: 26px; }
.aw-fakepage span:nth-child(2) { width: 70%; height: 16px; }
.aw-fakepage span:nth-child(3) { width: 45%; height: 16px; }
.aw-stage .sh-row { border-top: 1px solid var(--awbd); background: var(--awcard); }
.aw-st-dark .sh-row { background: #15171C; }
.aw-timeline { margin-top: 10px; }
.aw-rg { display: flex; align-items: center; gap: 10px; padding: 5px 0; }
.aw-rl { flex: none; width: 92px; font-size: 12px; font-weight: 700; }
.aw-rg input[type=range] { flex: 1; accent-color: var(--awac); }
.aw-rv { flex: none; width: 52px; text-align: right; font-size: 12px; color: var(--awmut); font-variant-numeric: tabular-nums; }
.aw-hint { margin: 8px 0 0; font-size: 11px; color: var(--awmut); line-height: 1.6; }
.aw-toggles { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 8px; }
.aw-tg { font-size: 12px; font-weight: 700; display: inline-flex; gap: 5px; align-items: center; }
.aw-tg input { accent-color: var(--awac); }
.aw-reset { margin-top: 10px; background: none; border: 1px solid var(--awbd); border-radius: 999px; color: var(--awmut);
  font-size: 11.5px; font-weight: 700; padding: 6px 12px; cursor: pointer; font-family: inherit; }
.aw-imgs { display: flex; gap: 8px; }
.aw-img { border: 1px solid var(--awbd); border-radius: 12px; padding: 12px; display: flex; flex-direction: column; align-items: center; gap: 6px; min-width: 170px; }
.aw-thumb { width: 104px; height: 104px; display: flex; align-items: center; justify-content: center; }
.aw-thumb img { max-width: 100%; max-height: 100%; }
.aw-il { margin: 0; font-size: 11.5px; font-weight: 700; }
.aw-il em { font-style: normal; color: var(--awmut); font-weight: 600; font-size: 10px; }
.aw-ib { display: flex; gap: 5px; }
.aw-up { background: var(--awac); color: #fff; border-radius: 999px; font-size: 10.5px; font-weight: 800;
  padding: 4px 10px; cursor: pointer; }
.aw-dark .aw-up { color: #08302B; }
.aw-up input { display: none; }
.aw-rm { background: none; border: 1px solid var(--awbd); border-radius: 999px; color: var(--awmut);
  font-size: 10.5px; font-weight: 700; padding: 4px 8px; cursor: pointer; font-family: inherit; }
.aw-rm.sure { color: #EF4444; border-color: #EF4444; }
.aw-toast { position: fixed; left: 50%; transform: translateX(-50%); bottom: 24px; background: #111827; color: #F9FAFB;
  border-radius: 999px; font-size: 12.5px; font-weight: 700; padding: 9px 16px; z-index: 130; }
`;
