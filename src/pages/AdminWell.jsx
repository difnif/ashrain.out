// 관리자 — 우물·탭바 편집 (#/admin/well)
// 미리보기에서 이미지를 드러낸 채 동그란 우물을 직접 눌러 편집 모드로 들어간다.
// 크기 슬라이더(탭바·우물 자리·이미지)와 변주 이미지 업로드를 여기서 — 저장하면 app_settings.well_ui 로 전 학생에게 적용.
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import FeatureBar, { FbAct } from "../components/FeatureBar";
import { TabsRow } from "../components/Shell";
import { PlaceholderWell, useWellImgs, bustWellImgs } from "../components/Well";
import { WELL_VARIANTS, WELL_DEFAULT, clampWellCfg } from "../lib/well";

const VCHIPS = [["", "자동(실황)"], ...WELL_VARIANTS];

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
  const [variant, setVariant] = useState("");            // "" = 자동(실황)
  const [hour, setHour] = useState(() => new Date().getHours());
  const [heading, setHeading] = useState(0);
  const [bust, setBust] = useState(0);
  const [rmAsk, setRmAsk] = useState("");                // 삭제 2단계 확인 중인 키
  const imgs = useWellImgs(bust);
  const fileRef = useRef({});

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

  const upload = async (key, file) => {
    if (!file) return;
    setBusy(true);
    try {
      const old = imgs[key]?.name;
      const ext = (file.name.split(".").pop() || "png").toLowerCase();
      if (old && old !== `${key}.${ext}`) await supabase.storage.from("figures").remove([`well/${old}`]);
      const { error } = await supabase.storage.from("figures")
        .upload(`well/${key}.${ext}`, file, { upsert: true, contentType: file.type || "image/png" });
      if (error) setToast("업로드 실패: " + error.message);
      else { bustWellImgs(); setBust((b) => b + 1); setToast("올렸어요 — 배경이 투명한 정사각형 PNG가 가장 예뻐요"); }
    } finally { setBusy(false); }
  };

  const removeImg = async (key) => {
    const f = imgs[key]; if (!f) return;
    setBusy(true);
    const { error } = await supabase.storage.from("figures").remove([`well/${f.name}`]);
    if (error) setToast("삭제 실패: " + error.message);
    else { bustWellImgs(); setBust((b) => b + 1); setToast("지웠어요 — 이 변주는 자리그림으로 나와요"); }
    setRmAsk(""); setBusy(false);
  };

  const pvHash = "#/";
  const wellProps = useMemo(() => ({
    reveal: true,
    variantOverride: variant || null,
    hourOverride: hour,
    headingOverride: heading,
  }), [variant, hour, heading]);

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
            {VCHIPS.map(([k, l]) => (
              <button key={k || "auto"} className={"aw-chip" + (variant === k ? " on" : "")} onClick={() => setVariant(k)}>{l}</button>
            ))}
          </div>
          <div className={`aw-stage aw-st-${pvTheme}` + (edit ? " edit" : "")}>
            <div className="aw-fakepage" aria-hidden="true"><span /><span /><span /></div>
            <TabsRow theme={pvTheme} hash={pvHash} cfg={draft} onWell={() => setEdit((e) => !e)} wellProps={wellProps} />
          </div>
          <div className="aw-timeline">
            <Rg label="시각" v={hour} min={0} max={23} unit="시" on={setHour} />
            <Rg label="화면 방위" v={heading} min={0} max={359} unit="°" on={setHeading} />
            <p className="aw-hint">해 그림자가 시각·방위에 맞춰 도는지 여기서 확인해요. 실제 앱은 실시간 시각과 (되는 기기에서) 나침반을 써요.</p>
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
          <p className="aw-t">변주 이미지</p>
          <p className="aw-d">시간·날씨에 따라 우물이 갈아입는 그림들이에요. 없는 변주는 비슷한 것 → 자리그림 순서로 대신 나와요.
            <b> 배경을 투명하게 오려낸 정사각형 PNG</b>를 올려주세요(구멍이 가운데 오게).</p>
          <div className="aw-imgs">
            {WELL_VARIANTS.map(([key, label]) => (
              <div key={key} className="aw-img">
                <div className="aw-thumb">
                  {imgs[key] ? <img src={imgs[key].url} alt={label} /> : <PlaceholderWell variant={key} size={64} />}
                </div>
                <p className="aw-il">{label} {!imgs[key] && <em>자리그림</em>}</p>
                <div className="aw-ib">
                  <label className="aw-up">
                    올리기
                    <input ref={(el) => (fileRef.current[key] = el)} type="file" accept="image/png,image/webp,image/avif"
                      onChange={(e) => { upload(key, e.target.files?.[0]); e.target.value = ""; }} />
                  </label>
                  {imgs[key] && (rmAsk === key
                    ? <button className="aw-rm sure" onClick={() => removeImg(key)}>정말 지우기</button>
                    : <button className="aw-rm" onClick={() => setRmAsk(key)}>지우기</button>)}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="aw-card">
          <p className="aw-t">동작 방식</p>
          <p className="aw-d">
            우물은 대시보드 히어로와 같은 실황(온도·강수·구름)을 봐요 — 눈 오면 눈 쌓인 우물, 비 오면 물이 차고 파동,
            영하엔 결빙, 맑은 낮엔 맑은 물, 밤엔 깊은 어둠. 그 위에 시각대(새벽·아침·낮·노을·밤) 색 보정과
            태양 각도 그림자가 얹혀요. 흐린 날은 해 그림자가 부드러운 기본 그림자로 바뀌어요.
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
.aw-imgs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
@media (max-width: 430px) { .aw-imgs { grid-template-columns: 1fr 1fr; } }
.aw-img { border: 1px solid var(--awbd); border-radius: 12px; padding: 8px; display: flex; flex-direction: column; align-items: center; gap: 5px; }
.aw-thumb { width: 64px; height: 64px; display: flex; align-items: center; justify-content: center; }
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
