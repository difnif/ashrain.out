// ashrain.out — 컨셉 문제: OMR 카드 사진 → 자동 판독(grid.js) → 확인(고치기) → 채점 → 틀린 문항 해설로
// 카드는 2쪽(쪽마다 25문항). 쪽 위쪽 띠에 세트 · 쪽 번호가 있어 어느 순서로 찍어도 된다.
// 사진은 이 기기 안에서만 읽고 어디에도 올리지 않는다.
import { useMemo, useRef, useState } from "react";
import { judge, saveAttempt, saveOmrResult, pad2 } from "../../lib/conceptsets";
import { layoutCard, readCardPhoto, CONF_OK } from "../../lib/omr/grid.js";
import { fileToCanvas } from "../../lib/camera";
import { answerHtml, LV_COLOR, safeHtml } from "./render";
import { flagName, omrKindName, reasonText, LEVELS } from "./labels";

const tick = () => new Promise((r) => setTimeout(r, 30));
const PLACE = { int: "예: 12", frac: "예: 5/12", pick: "예: ㄱ, ㄷ", pair: "예: 14, 21" };

/** 판독 결과 → 미리보기(워프된 카드 + 칸 표시) dataURL */
function previewOf(res, page) {
  const wp = res.warped;
  if (!wp || typeof document === "undefined") return null;
  const cv = document.createElement("canvas");
  cv.width = wp.width; cv.height = wp.height;
  const ctx = cv.getContext("2d");
  const im = ctx.createImageData(wp.width, wp.height);
  for (let i = 0; i < wp.gray.length; i++) { const v = wp.gray[i]; im.data[i * 4] = v; im.data[i * 4 + 1] = v; im.data[i * 4 + 2] = v; im.data[i * 4 + 3] = 255; }
  ctx.putImageData(im, 0, 0);
  const sc = wp.scale || 1;
  for (const b of page.blocks) {
    const a = res.answers.find((x) => x.no === b.no);
    const blank = !a || !a.raw;
    const warn = a && (a.flag || a.conf < CONF_OK);
    ctx.lineWidth = 4 * sc;
    ctx.strokeStyle = blank ? "rgba(140,140,140,.7)" : warn ? "rgba(234,160,0,.95)" : "rgba(22,163,74,.9)";
    ctx.strokeRect((b.x - 3) * sc, (b.y - 3) * sc, (b.w + 6) * sc, (b.h + 6) * sc);
  }
  try { return cv.toDataURL("image/jpeg", 0.78); } catch { return null; }
}

export default function OmrGrade({ catId, set, uid, say }) {
  const card = useMemo(() => layoutCard({ cat: catId, no: set.no, title: set.title, short: set.short, items: set.items }), [catId, set]);
  const byNo = useMemo(() => Object.fromEntries(set.items.map((it) => [it.no, it])), [set]);
  const [pages, setPages] = useState({});        // index → { preview, n, bandOk }
  const [rows, setRows] = useState(() => Object.fromEntries(set.items.map((it) => [it.no, { raw: "", conf: null, flag: null, src: null }])));
  const [busy, setBusy] = useState("");
  const [pending, setPending] = useState(null);  // { imageData } — 쪽을 못 읽은 사진
  const [result, setResult] = useState(null);
  const camRef = useRef(null), fileRef = useRef(null);

  const apply = (res) => {
    const p = card.pages[res.page];
    setPages((x) => ({ ...x, [res.page]: { preview: previewOf(res, p), n: res.answers.filter((a) => a.raw).length, bandOk: res.bandOk } }));
    setRows((x) => {
      const n = { ...x };
      for (const a of res.answers) n[a.no] = { raw: a.raw, conf: a.conf, flag: a.flag, src: "omr" };
      return n;
    });
    const nWarn = res.answers.filter((a) => a.raw && (a.flag || a.conf < CONF_OK)).length;
    say(`${res.page + 1}쪽을 읽었어요${nWarn ? ` — 노란 칸 ${nWarn}개는 꼭 확인해 주세요` : ""}`);
  };

  async function readFile(f) {
    const isImg = (f.type || "").startsWith("image/") || /\.(jpe?g|png|webp|heic|heif)$/i.test(f.name || "");
    if (!isImg) { say("사진 파일만 올릴 수 있어요"); return; }
    const cv = await fileToCanvas(f, 1600);
    const ctx = cv.getContext("2d", { willReadFrequently: true });
    const imageData = ctx.getImageData(0, 0, cv.width, cv.height);
    await tick();
    const res = readCardPhoto(imageData, card);
    if (res.ok) apply(res);
    else if (res.reason === "band") { setPending({ imageData }); say(reasonText("band")); }
    else say(reasonText(res.reason, res.band || {}));
  }
  async function onFiles(list) {
    const files = [...(list || [])].slice(0, 4);
    if (!files.length) return;
    setResult(null);
    for (let i = 0; i < files.length; i++) {
      setBusy(files.length > 1 ? `사진 ${i + 1}/${files.length} 읽는 중…` : "사진을 읽는 중…");
      await tick();
      try { await readFile(files[i]); } catch (e) { say(e?.message || "사진을 열지 못했어요"); }
    }
    setBusy("");
  }
  const pickPage = async (idx) => {
    if (!pending) return;
    setBusy("다시 읽는 중…"); await tick();
    const res = readCardPhoto(pending.imageData, card, { page: idx });
    setPending(null); setBusy("");
    if (res.ok) apply(res); else say(reasonText(res.reason, res.band || {}));
  };
  const edit = (no, v) => setRows((x) => ({ ...x, [no]: { raw: v, conf: 1, flag: null, src: "me" } }));

  const nRead = Object.keys(pages).length;
  const warnNos = set.items.filter((it) => { const r = rows[it.no]; return r.src === "omr" && r.raw && (r.flag || (r.conf ?? 1) < CONF_OK); }).map((it) => it.no);
  const nFilled = set.items.filter((it) => String(rows[it.no].raw || "").trim()).length;

  const grade = () => {
    const out = set.items.map((it) => {
      const raw = String(rows[it.no].raw || "").trim();
      const j = judge(it, raw);
      return { no: it.no, id: it.id, lv: it.lv, raw, ok: j.ok === true, blank: !raw, unread: raw.includes("?"), note: j.note };
    });
    for (const r of out) if (r.raw && !r.unread) saveAttempt(catId, set.no, r.id, r.raw, r.ok);
    const score = out.filter((r) => r.ok).length;
    saveOmrResult(catId, set.no, { score, n: out.length, answers: Object.fromEntries(out.map((r) => [r.no, r.raw])) });
    setResult({ out, score });
    window.scrollTo?.({ top: 0, behavior: "smooth" });
  };
  const reset = () => { setPages({}); setRows(Object.fromEntries(set.items.map((it) => [it.no, { raw: "", conf: null, flag: null, src: null }]))); setResult(null); setPending(null); };

  const inputs = (
    <>
      <input ref={camRef} type="file" accept="image/*" capture="environment" hidden onChange={(e) => { onFiles(e.target.files); e.target.value = ""; }} />
      <input ref={fileRef} type="file" accept="image/*" multiple hidden onChange={(e) => { onFiles(e.target.files); e.target.value = ""; }} />
    </>
  );

  if (result) return <OmrResult catId={catId} set={set} byNo={byNo} result={result} onRetry={reset} onEdit={() => setResult(null)} />;

  return (
    <div className="cs-wrap">
      {inputs}
      <div className="cs-card cs-shot">
        <div className="cs-ch"><b>📷 카드 찍기</b><span>쪽마다 한 장씩, 순서는 상관없어요</span></div>
        <ul className="cs-tips">
          <li><b>네 모서리의 검은 네모</b>가 모두 나오게, 위에서 똑바로 찍어요.</li>
          <li>그림자 없이 밝은 곳에서 · 카드는 평평하게 펴서.</li>
          <li>사진은 이 기기 안에서만 읽고 어디에도 올리지 않아요.</li>
        </ul>
        <div className="cs-pages">
          {card.pages.map((p) => (
            <span key={p.index} className={"cs-pg" + (pages[p.index] ? " on" : "")}>{p.index + 1}쪽 {pages[p.index] ? `✓ ${pages[p.index].n}칸` : "— 아직"}<small>{p.blocks[0].no}~{p.blocks[p.blocks.length - 1].no}번</small></span>
          ))}
        </div>
        <div className="cs-dbtns">
          <button className="sv-btn pri" disabled={!!busy} onClick={() => camRef.current?.click()}>📷 카메라로 찍기</button>
          <button className="sv-btn" disabled={!!busy} onClick={() => fileRef.current?.click()}>🖼 사진 고르기</button>
        </div>
        {busy && <div className="cs-busy"><i className="sp" />{busy}</div>}
        {pending && (
          <div className="cs-pending">
            <b>이 사진은 몇 쪽인가요?</b>
            <div className="cs-dbtns">{card.pages.map((p) => <button key={p.index} className="sv-btn sm" onClick={() => pickPage(p.index)}>{p.index + 1}쪽 ({p.blocks[0].no}~{p.blocks[p.blocks.length - 1].no}번)</button>)}<button className="sv-btn sm ghost" onClick={() => setPending(null)}>취소</button></div>
          </div>
        )}
        <p className="cs-dnote">카드가 없으면 세트 화면의 「자료」에서 OMR 카드를 골라 인쇄하세요. 카드 없이 답을 직접 써서 채점해도 돼요.</p>
      </div>

      {nRead > 0 && (
        <div className="cs-previews">
          {card.pages.map((p) => pages[p.index]?.preview && (
            <figure key={p.index} className="cs-prv"><img src={pages[p.index].preview} alt={`${p.index + 1}쪽 판독`} /><figcaption>{p.index + 1}쪽 · 초록 = 읽음 · 노랑 = 확인 · 회색 = 빈칸</figcaption></figure>
          ))}
        </div>
      )}

      <div className="cs-sec">읽은 답 확인 <small>{nFilled}/50 · 고칠 칸은 눌러서 고쳐요</small></div>
      {warnNos.length > 0 && <div className="cs-warn">⚠ 노란 칸 {warnNos.length}개({warnNos.join(", ")}번)는 사진과 비교해 확인해 주세요. 「?」는 읽지 못한 자리예요.</div>}
      {card.pages.map((p) => (
        <div key={p.index} className="cs-ogrp">
          <div className="cs-ogh">{p.index + 1}쪽 {pages[p.index] ? "" : <small>· 아직 안 찍음 — 찍거나 직접 써도 돼요</small>}</div>
          <div className="cs-orows">
            {p.blocks.map((b) => {
              const r = rows[b.no];
              const warn = r.src === "omr" && r.raw && (r.flag || (r.conf ?? 1) < CONF_OK);
              return (
                <label key={b.no} className={"cs-orow" + (warn ? " warn" : "") + (r.src === "me" ? " me" : "")}>
                  <span className="no">{b.no}</span>
                  <span className="kd">{omrKindName(b.kind)}</span>
                  <input className="sv-in" value={r.raw} placeholder={PLACE[b.kind]} inputMode={b.kind === "int" ? "numeric" : "text"}
                    onChange={(e) => edit(b.no, e.target.value)} aria-label={`${b.no}번 답`} />
                  {warn && <em>{flagName(r.flag) || "흐림"}</em>}
                </label>
              );
            })}
          </div>
        </div>
      ))}
      <button className="sv-btn pri full cs-gradebtn" disabled={!nFilled || !!busy} onClick={grade}>채점하기 ({nFilled}문항 답함)</button>
      <p className="cs-dnote">「?」가 남은 칸과 빈칸은 틀린 것으로 셉니다. 분수는 값이 같으면 정답이에요(기약분수가 아니면 해설에서 알려 줘요).</p>
    </div>
  );
}

function OmrResult({ catId, set, byNo, result, onRetry, onEdit }) {
  const [all, setAll] = useState(false);
  const { out, score } = result;
  const wrong = out.filter((r) => !r.ok);
  const byLv = LEVELS.map((lv) => { const xs = out.filter((r) => r.lv === lv); return [lv, xs.filter((r) => r.ok).length, xs.length]; });
  const go = (no) => { location.hash = `#/sets/${catId}/${pad2(set.no)}/q/${no}`; };
  const show = all ? out : wrong;
  return (
    <div className="cs-wrap">
      <div className="cs-card cs-score">
        <div className="big"><b>{score}</b><span>/ {out.length}</span></div>
        <div className="lvs">{byLv.map(([lv, ok, n]) => <span key={lv}><i style={{ background: LV_COLOR[lv] }}>{lv}</i>{ok}/{n}</span>)}</div>
        <div className="cs-dbtns">
          {wrong.length > 0 && <button className="sv-btn pri" onClick={() => go(wrong[0].no)}>틀린 문제 해설 보기 ({wrong.length})</button>}
          <button className="sv-btn" onClick={onEdit}>답 고치기</button>
          <button className="sv-btn" onClick={onRetry}>새로 찍기</button>
        </div>
      </div>
      <div className="cs-sec">{all ? "전체 문항" : "틀린 문항"} <small>{show.length}</small>
        <button className="sv-btn sm ghost" style={{ marginLeft: "auto" }} onClick={() => setAll((a) => !a)}>{all ? "틀린 것만" : "전체 보기"}</button></div>
      {show.length === 0 ? <div className="sv-empty">모두 맞혔어요 🎉</div> : (
        <div className="cs-list">
          {show.map((r) => {
            const it = byNo[r.no];
            return (
              <button key={r.no} className="cs-row cs-rrow" onClick={() => go(r.no)}>
                <span className="no">{r.no}</span>
                <span className="lv" style={{ background: LV_COLOR[it.lv] }}>{it.lv}</span>
                <span className="tx"><b dangerouslySetInnerHTML={{ __html: safeHtml(it.ty) }} />
                  <small>내 답 {r.blank ? "무응답" : r.unread ? `${r.raw} (읽지 못함)` : r.raw} · 정답 <span dangerouslySetInnerHTML={{ __html: answerHtml(it) }} /></small></span>
                <span className={"st " + (r.ok ? "ok" : "bad")}>{r.ok ? "✓" : "✗"}</span>
              </button>
            );
          })}
        </div>
      )}
      <p className="cs-dnote">채점 결과는 이 기기에 저장돼 세트 화면의 진도에 반영돼요. 문항을 누르면 3단 해설로 가요.</p>
    </div>
  );
}
