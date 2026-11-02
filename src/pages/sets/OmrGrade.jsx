// ashrain.out — 컨셉 문제: OMR 카드 사진 → 자동 판독(grid.js) → 확인(고치기) → 채점 → 틀린 문항 해설로
// 카드(v2)는 3쪽 — 정수 · 두 수 · 보기는 동그라미, 분수는 손으로 쓰는 칸. 쪽 아래쪽 띠에 세트 · 쪽 번호가 있어 어느 순서로 찍어도 된다.
// 예전에 인쇄한 카드(v1, 2쪽 · 분수도 동그라미 · 띠가 위쪽)도 띠의 자리로 알아보고 그대로 읽는다.
// 일차함수 범주(lin)는 2쪽 손글씨 카드 — 답(수 · 식 · 점)은 한 줄 칸에 손으로 쓰고 보기만 동그라미(예전 판 없음).
// 동그라미 · 칸의 글씨 유무는 이 기기 안에서 읽는다. 손으로 쓴 칸만 잘라(사진 전체가 아니라) AI(/api/ai task "omr")가 읽는다.
import { useMemo, useRef, useState } from "react";
import { judge, saveAttempt, saveOmrResult, pad2 } from "../../lib/conceptsets";
import { layoutCard, readCardPhoto, handCrops, CONF_OK } from "../../lib/omr/grid.js";
import { fileToCanvas } from "../../lib/camera";
import { answerHtml, LV_COLOR, safeHtml } from "./render";
import { flagName, omrKindName, reasonText, LEVELS } from "./labels";
import { handSheets } from "./omrhand";
import { readSheets } from "./recognize";

const tick = () => new Promise((r) => setTimeout(r, 30));
const PLACE = { int: "예: 12", frac: "예: 5/12", pick: "예: ㄱ, ㄷ", pair: "예: 14, 21", num: "예: −3 · 3/4 · 0.5", lin: "예: y = −2x + 3", pt: "예: (2, −1)" };
const EMPTY = { raw: "", conf: null, flag: null, src: null };

/** 확인이 필요한 줄: 동그라미를 흐리게 · 두 개 칠함 · 자리 빔, 또는 손글씨를 AI 가 못 읽음 */
const needsCheck = (r) => !!r && ((r.src === "omr" && r.raw && (r.flag || (r.conf ?? 1) < CONF_OK)) || (r.src === "ai" && r.flag === "hand"));

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
    const hand = a?.flag === "hand";
    const blank = !a || (!a.raw && !hand);
    const warn = a && !hand && (a.flag || a.conf < CONF_OK);
    ctx.lineWidth = 4 * sc;
    ctx.strokeStyle = hand ? "rgba(37,99,235,.9)" : blank ? "rgba(140,140,140,.7)" : warn ? "rgba(234,160,0,.95)" : "rgba(22,163,74,.9)";
    ctx.strokeRect((b.x - 3) * sc, (b.y - 3) * sc, (b.w + 6) * sc, (b.h + 6) * sc);
  }
  try { return cv.toDataURL("image/jpeg", 0.78); } catch { return null; }
}

export default function OmrGrade({ catId, set, uid, say }) {
  const cards = useMemo(() => {
    const s = { cat: catId, no: set.no, title: set.title, short: set.short, items: set.items };
    return catId === "prob" ? { 2: layoutCard(s), 1: layoutCard(s, { ver: 1 }) } : { 2: layoutCard(s) };
  }, [catId, set]);
  const [ver, setVer] = useState(2);             // 찍은 카드의 판 — 예전 카드를 찍으면 1
  const card = cards[ver];
  const byNo = useMemo(() => Object.fromEntries(set.items.map((it) => [it.no, it])), [set]);
  const [pages, setPages] = useState({});        // "판:쪽" → { preview, n, bandOk }
  const [rows, setRows] = useState(() => Object.fromEntries(set.items.map((it) => [it.no, { ...EMPTY }])));
  const [busy, setBusy] = useState("");
  const [pending, setPending] = useState(null);  // { imageData } — 쪽을 못 읽은 사진
  const [result, setResult] = useState(null);
  const camRef = useRef(null), fileRef = useRef(null);

  async function apply(res) {
    const p = res.card.pages[res.page];
    setVer(res.ver);
    const nHand = res.answers.filter((a) => a.flag === "hand").length;
    setPages((x) => ({ ...x, [`${res.ver}:${res.page}`]: { preview: previewOf(res, p), n: res.answers.filter((a) => a.raw || a.flag === "hand").length, bandOk: res.bandOk } }));
    setRows((x) => {
      const n = { ...x };
      for (const a of res.answers) n[a.no] = a.flag === "hand" ? { raw: "", conf: 0, flag: "reading", src: "ai" } : { raw: a.raw, conf: a.conf, flag: a.flag, src: "omr" };
      return n;
    });
    let aiNote = "", aiErr = null;
    if (nHand) {
      // 손글씨 칸(분수 · 일차함수의 답): 그 칸만 잘라 AI 로
      setBusy(`손으로 쓴 답 ${nHand}개를 AI가 읽는 중…`);
      const crops = handCrops(res);
      let reads = {};
      try {
        const r = await readSheets(handSheets(crops));
        reads = r.reads; aiErr = r.error;
      } catch (e) { aiErr = e?.message || "손글씨를 읽지 못했어요"; }
      setRows((x) => {
        const n = { ...x };
        for (const c of crops) {
          if (n[c.no]?.src === "me") continue;                 // 기다리는 사이 학생이 직접 쓴 칸은 그대로
          const v = String(reads[c.no] ?? "").trim();
          n[c.no] = v ? { raw: v, conf: 0.8, flag: "ai", src: "ai" } : { raw: "", conf: 0, flag: "hand", src: "ai" };
        }
        return n;
      });
      const ok = crops.filter((c) => String(reads[c.no] ?? "").trim()).length;
      aiNote = ok ? ` · 손글씨 ${ok}개는 AI가 읽었어요` : "";
      if (ok < crops.length && !aiErr) aiNote += ` · ${crops.length - ok}개는 직접 써 주세요`;
    }
    const nWarn = res.answers.filter((a) => a.flag !== "hand" && a.raw && (a.flag || a.conf < CONF_OK)).length;
    say(aiErr ? `${res.page + 1}쪽을 읽었어요 — ${aiErr}` : `${res.page + 1}쪽을 읽었어요${aiNote}${nWarn ? ` — 노란 칸 ${nWarn}개는 꼭 확인해 주세요` : ""}`);
  }

  async function readFile(f) {
    const isImg = (f.type || "").startsWith("image/") || /\.(jpe?g|png|webp|heic|heif)$/i.test(f.name || "");
    if (!isImg) { say("사진 파일만 올릴 수 있어요"); return; }
    const cv = await fileToCanvas(f, 1600);
    const ctx = cv.getContext("2d", { willReadFrequently: true });
    const imageData = ctx.getImageData(0, 0, cv.width, cv.height);
    await tick();
    const res = readCardPhoto(imageData, cards);
    if (res.ok) await apply(res);
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
    const res = readCardPhoto(pending.imageData, cards, { page: idx });
    setPending(null);
    try { if (res.ok) await apply(res); else say(reasonText(res.reason, res.band || {})); }
    finally { setBusy(""); }
  };
  const edit = (no, v) => setRows((x) => ({ ...x, [no]: { raw: v, conf: 1, flag: null, src: "me" } }));

  const nRead = Object.keys(pages).length;
  const warnNos = set.items.filter((it) => needsCheck(rows[it.no])).map((it) => it.no);
  const nAi = set.items.filter((it) => rows[it.no].src === "ai" && rows[it.no].flag === "ai").length;
  const nFilled = set.items.filter((it) => String(rows[it.no].raw || "").trim()).length;
  const reading = set.items.some((it) => rows[it.no].flag === "reading");

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
  const reset = () => { setPages({}); setVer(2); setRows(Object.fromEntries(set.items.map((it) => [it.no, { ...EMPTY }]))); setResult(null); setPending(null); };

  const inputs = (
    <>
      <input ref={camRef} type="file" accept="image/*" capture="environment" hidden onChange={(e) => { onFiles(e.target.files); e.target.value = ""; }} />
      <input ref={fileRef} type="file" accept="image/*" multiple hidden onChange={(e) => { onFiles(e.target.files); e.target.value = ""; }} />
    </>
  );

  if (result) return <OmrResult catId={catId} set={set} byNo={byNo} result={result} onRetry={reset} onEdit={() => setResult(null)} />;

  const range = (p) => `${p.blocks[0].no}~${p.blocks[p.blocks.length - 1].no}번`;
  return (
    <div className="cs-wrap">
      {inputs}
      <div className="cs-card cs-shot">
        <div className="cs-ch"><b>📷 카드 찍기</b><span>쪽마다 한 장씩, 순서는 상관없어요</span></div>
        <ul className="cs-tips">
          <li><b>네 모서리의 검은 네모</b>가 모두 나오게, 위에서 똑바로 찍어요.</li>
          <li>그림자 없이 밝은 곳에서 · 카드는 평평하게 펴서.</li>
          <li>동그라미는 이 기기 안에서 읽어요. <b>손으로 쓴 칸</b>({catId === "lin" ? "수 · 식 · 점" : "분수"})만 잘라 AI가 읽어요(로그인 필요).</li>
        </ul>
        <div className="cs-pages">
          {card.pages.map((p) => {
            const got = pages[`${ver}:${p.index}`];
            return <span key={p.index} className={"cs-pg" + (got ? " on" : "")}>{p.index + 1}쪽 {got ? `✓ ${got.n}칸` : "— 아직"}<small>{range(p)}</small></span>;
          })}
        </div>
        {ver === 1 && <p className="cs-dnote">예전 카드(2쪽)로 읽고 있어요. 새 카드는 동그라미가 크고 분수를 손으로 써요 — 「자료」에서 인쇄할 수 있어요.</p>}
        <div className="cs-dbtns">
          <button className="sv-btn pri" disabled={!!busy} onClick={() => camRef.current?.click()}>📷 카메라로 찍기</button>
          <button className="sv-btn" disabled={!!busy} onClick={() => fileRef.current?.click()}>🖼 사진 고르기</button>
        </div>
        {busy && <div className="cs-busy"><i className="sp" />{busy}</div>}
        {pending && (
          <div className="cs-pending">
            <b>이 사진은 몇 쪽인가요?</b>
            <div className="cs-dbtns">{card.pages.map((p) => <button key={p.index} className="sv-btn sm" onClick={() => pickPage(p.index)}>{p.index + 1}쪽 ({range(p)})</button>)}<button className="sv-btn sm ghost" onClick={() => setPending(null)}>취소</button></div>
          </div>
        )}
        <p className="cs-dnote">카드가 없으면 세트 화면의 「자료」에서 OMR 카드를 골라 인쇄하세요. 카드 없이 답을 직접 써서 채점해도 돼요.</p>
      </div>

      {nRead > 0 && (
        <div className="cs-previews">
          {card.pages.map((p) => pages[`${ver}:${p.index}`]?.preview && (
            <figure key={p.index} className="cs-prv"><img src={pages[`${ver}:${p.index}`].preview} alt={`${p.index + 1}쪽 판독`} /><figcaption>{p.index + 1}쪽 · 초록 = 읽음 · 파랑 = 손글씨(AI) · 노랑 = 확인 · 회색 = 빈칸</figcaption></figure>
          ))}
        </div>
      )}

      <div className="cs-sec">읽은 답 확인 <small>{nFilled}/50 · 고칠 칸은 눌러서 고쳐요</small></div>
      {warnNos.length > 0 && <div className="cs-warn">⚠ 노란 칸 {warnNos.length}개({warnNos.join(", ")}번)는 사진과 비교해 확인해 주세요. 「?」는 읽지 못한 자리, 빈 노란 칸은 AI가 못 읽은 손글씨예요.</div>}
      {nAi > 0 && <div className="cs-ainote">✍ 손으로 쓴 답 {nAi}개는 AI가 읽었어요 — 카드와 한 번 비교해 주세요.</div>}
      {card.pages.map((p) => (
        <div key={p.index} className="cs-ogrp">
          <div className="cs-ogh">{p.index + 1}쪽 {pages[`${ver}:${p.index}`] ? "" : <small>· 아직 안 찍음 — 찍거나 직접 써도 돼요</small>}</div>
          <div className="cs-orows">
            {p.blocks.map((b) => {
              const r = rows[b.no];
              const warn = needsCheck(r);
              const note = r.flag === "reading" ? flagName("reading") : warn ? flagName(r.flag) || "흐림" : r.src === "ai" && r.flag === "ai" ? flagName("ai") : "";
              return (
                <label key={b.no} className={"cs-orow" + (warn ? " warn" : "") + (r.src === "me" ? " me" : "") + (r.src === "ai" && r.flag === "ai" ? " ai" : "")}>
                  <span className="no">{b.no}</span>
                  <span className="kd">{omrKindName(b.kind, b.ak)}</span>
                  <input className="sv-in" value={r.raw} placeholder={r.flag === "reading" ? "읽는 중…" : PLACE[b.ak || b.kind]} inputMode={b.kind === "int" ? "numeric" : "text"}
                    onChange={(e) => edit(b.no, e.target.value)} aria-label={`${b.no}번 답`} />
                  {note && <em className={warn ? "" : "info"}>{note}</em>}
                </label>
              );
            })}
          </div>
        </div>
      ))}
      <button className="sv-btn pri full cs-gradebtn" disabled={!nFilled || !!busy || reading} onClick={grade}>채점하기 ({nFilled}문항 답함)</button>
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
