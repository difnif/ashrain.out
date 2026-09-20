// 서술형 답안 자가채점 — #/solve/essay (문항 고르기) · #/solve/essay/<itemId> (풀기)
// 흐름(한 화면, 단계별로 열림): ① 문제 → ② 내 답안(글/사진) 제출 → ③ 채점 기준을 보며 스스로 채점 → ④ 모범답안·해설 + 한 줄 평
// · 자동 채점·LLM 없음. 점수는 훈련용 "예상 점수" — 공식 성적이 아니다.
// · 모범답안·해설은 학생이 답안을 제출한 뒤에만 보인다.
// · 저장: essay_grades (없으면 조용히 localStorage 만) + attempts(logAttempt, setId "essay")
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../../supabaseClient";
import SolveShell, { useToast } from "./SolveShell";
import ItemPicker from "./ItemPicker";
import ItemQuestion from "../../components/ItemQuestion";
import ItemFigure from "../../components/ItemFigure";
import MathText from "../../components/MathText";
import { fetchItem, hasRubric, logAttempt, solutionLevels, countLive, conceptOf, UNIT_NAMES } from "../../lib/items";
import { kindOf, correctChoiceIndex, CIRCLED } from "../../lib/answers";
import { saveItemWrongNotes } from "../../lib/wrongnotes";
import { askAboutItem } from "../../lib/ask";
import { computeScore, partialPoints, fullPoints, verdict, reviewList, allMarked, saveResult, loadResults, MARK_LABEL } from "../../lib/essay.js";

const CSS = `
.es-meta { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; margin-bottom: 8px; font-size: 11.5px; color: var(--muted); }
.es-tag { border: 1px solid var(--border); border-radius: 999px; padding: 1px 8px; }
.es-tag.hi { border-color: var(--accent); color: var(--accent); font-weight: 800; }
.es-timer { margin-left: auto; font-variant-numeric: tabular-nums; font-weight: 700; }
.es-note { font-size: 13.5px; font-weight: 700; color: var(--accent); margin: 8px 0 0; line-height: 1.6; }
.es-mine { white-space: pre-wrap; line-height: 1.65; font-size: 15px; padding: 10px 12px; border-radius: 12px; background: var(--surface2); word-break: break-word; }
.es-photo { margin-top: 10px; }
.es-photo img { display: block; max-width: 100%; max-height: 380px; border-radius: 12px; border: 1px solid var(--border); background: #fff; }
.es-photo .rm { margin-top: 6px; }
.es-el { padding: 12px 0; border-top: 1px solid var(--border); }
.es-el:first-child { border-top: none; padding-top: 2px; }
.es-el-h { display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 14.5px; }
.es-el-h .no { flex: none; min-width: 22px; height: 22px; border-radius: 999px; background: var(--surface2); display: inline-flex; align-items: center; justify-content: center; font-size: 12px; }
.es-el-h .pt { margin-left: auto; flex: none; font-size: 12.5px; color: var(--muted); font-weight: 700; }
.es-el-h .pt.got { color: var(--text); }
.es-crit { font-size: 14px; line-height: 1.6; margin: 6px 0 4px; word-break: keep-all; }
.es-sub { display: flex; gap: 6px; font-size: 12.5px; color: var(--muted); line-height: 1.55; margin: 2px 0; }
.es-sub b { flex: none; font-weight: 800; }
.es-seg { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-top: 10px; }
.es-seg button { min-height: 44px; border-radius: 12px; border: 1.5px solid var(--border); background: var(--surface); color: var(--text); font-weight: 800; font-size: 13.5px; cursor: pointer; padding: 8px 4px; line-height: 1.3; }
.es-seg button small { display: block; font-size: 11px; color: var(--muted); font-weight: 700; }
.es-seg button.on.full { border-color: var(--good); color: var(--good); background: color-mix(in srgb, var(--good) 14%, var(--surface)); }
.es-seg button.on.partial { border-color: var(--accent); color: var(--accent); background: color-mix(in srgb, var(--accent) 14%, var(--surface)); }
.es-seg button.on.zero { border-color: var(--bad); color: var(--bad); background: color-mix(in srgb, var(--bad) 12%, var(--surface)); }
.es-seg button.on small { color: inherit; }
.es-seg button:disabled { cursor: default; opacity: .7; }
.es-chk { display: flex; gap: 10px; align-items: flex-start; padding: 10px 12px; border: 1px solid var(--border); border-radius: 12px; background: var(--surface); cursor: pointer; }
.es-chk.on { border-color: var(--accent); }
.es-chk input { width: 20px; height: 20px; margin: 2px 0 0; flex: none; accent-color: var(--accent); }
.es-chk .tx { flex: 1; font-size: 14px; line-height: 1.55; }
.es-chk .ef { display: block; font-size: 12px; color: var(--muted); margin-top: 3px; font-weight: 700; }
.es-total { display: flex; align-items: baseline; gap: 6px; margin: 14px 0 6px; }
.es-total .big { font-size: 28px; font-weight: 900; letter-spacing: -0.5px; line-height: 1; }
.es-total .of { color: var(--muted); font-size: 14px; font-weight: 700; }
.es-total .vd { margin-left: auto; font-size: 13px; font-weight: 800; color: var(--accent); }
.es-ans { font-size: 17px; font-weight: 800; color: var(--good); line-height: 1.6; }
.es-tog { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; }
.es-tog button { min-height: 44px; border-radius: 12px; border: 1.5px solid var(--border); background: var(--surface); color: var(--text); font-weight: 800; font-size: 14px; cursor: pointer; }
.es-tog button.on.ok { border-color: var(--good); color: var(--good); background: color-mix(in srgb, var(--good) 14%, var(--surface)); }
.es-tog button.on.bad { border-color: var(--bad); color: var(--bad); background: color-mix(in srgb, var(--bad) 12%, var(--surface)); }
.es-tog button:disabled { cursor: default; opacity: .75; }
.es-det summary { cursor: pointer; font-size: 13px; color: var(--muted); font-weight: 700; padding: 6px 0; }
.es-det ul { margin: 4px 0 0 18px; padding: 0; font-size: 13px; line-height: 1.6; color: var(--muted); }
.es-verdict { font-size: 21px; font-weight: 900; letter-spacing: -0.3px; margin: 2px 0 4px; }
.es-model { padding: 10px 12px; border-radius: 10px; background: var(--surface2); font-size: 14.5px; line-height: 1.65; }
.es-lv { margin-top: 12px; font-size: 14.5px; line-height: 1.65; }
.es-lv-t { font-weight: 800; font-size: 13.5px; color: var(--accent); margin-bottom: 4px; }
.es-lv ol { margin: 4px 0 4px 20px; padding: 0; }
.es-lv li { margin: 3px 0; }
.es-lv p { margin: 3px 0; }
.es-rv { display: flex; flex-direction: column; gap: 8px; margin-top: 8px; }
.es-rv .it { padding: 10px 12px; border-radius: 12px; border: 1px dashed var(--border); font-size: 13.5px; line-height: 1.6; }
.es-rv .it b { display: block; font-size: 13px; }
.es-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 12px; }
.es-recent .sv-item .no { min-width: auto; padding: 0 8px; font-variant-numeric: tabular-nums; }
.es-hint { font-size: 12.5px; color: var(--muted); margin-top: 8px; line-height: 1.55; }
`;

const fmtTime = (sec) => `${Math.floor(sec / 60)}:${String(sec % 60).padStart(2, "0")}`;
const snippetOf = (item, n = 70) => String(item?.question || "").replace(/\[\[|\]\]/g, "").replace(/\s+/g, " ").trim().slice(0, n);
const fmtDate = (iso) => { const d = new Date(iso); return Number.isNaN(d.getTime()) ? "" : `${d.getMonth() + 1}/${d.getDate()}`; };
function uuid() {
  try { if (crypto?.randomUUID) return crypto.randomUUID(); } catch { /* 비보안 컨텍스트 */ }
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 10);
}

/** 사진 → 긴 변 ≤ cap px 의 JPEG Blob */
function loadImage(file) {
  return new Promise((res, rej) => {
    const im = new Image();
    im.onload = () => res(im);
    im.onerror = () => rej(new Error("사진을 열 수 없어요"));
    im.src = URL.createObjectURL(file);
  });
}
async function downscaleJpeg(file, cap = 1400, q = 0.85) {
  const im = await loadImage(file);
  try {
    const sc = Math.min(1, cap / Math.max(im.naturalWidth || im.width, im.naturalHeight || im.height));
    const cv = document.createElement("canvas");
    cv.width = Math.max(1, Math.round((im.naturalWidth || im.width) * sc));
    cv.height = Math.max(1, Math.round((im.naturalHeight || im.height) * sc));
    cv.getContext("2d").drawImage(im, 0, 0, cv.width, cv.height);
    return await new Promise((res, rej) => cv.toBlob((b) => (b ? res(b) : rej(new Error("이미지 변환에 실패했어요"))), "image/jpeg", q));
  } finally { URL.revokeObjectURL(im.src); }
}

/** 정답 표시용 — 객관식은 보기 텍스트로 (보기를 숨긴 채 풀었으니 번호만으로는 알 수 없다) */
function answerText(item) {
  if (kindOf(item) === "choice") {
    const i = correctChoiceIndex(item);
    if (i >= 0 && item.choices?.[i] != null) return `${CIRCLED[i] || i + 1} ${item.choices[i]}`;
  }
  return String(item?.answer ?? "");
}

export default function Essay({ itemId }) {
  return itemId ? <EssaySolve itemId={itemId} key={itemId} /> : <EssayPicker />;
}

// ── 문항 고르기 ───────────────────────────────────────────────────────────────

function EssayPicker() {
  const [n, setN] = useState(null);          // 채점 기준 있는 공개 문항 수
  const [recent, setRecent] = useState([]);
  useEffect(() => {
    let alive = true;
    countLive({ withRubric: true }).then((c) => { if (alive) setN(c); }).catch(() => { if (alive) setN(0); });
    setRecent(loadResults().slice(0, 5));
    return () => { alive = false; };
  }, []);

  return (
    <SolveShell title="서술형 자가채점" back="#/tools/essay" sub="풀이 과정을 쓰고, 채점 기준을 보며 스스로 점수를 매겨요. 훈련용 예상 점수라서 공식 성적은 아니에요.">
      <style>{CSS}</style>
      {recent.length > 0 && (
        <div className="sv-card es-recent">
          <div className="sv-sec" style={{ marginTop: 0 }}>최근 채점</div>
          <div className="sv-list">
            {recent.map((r, i) => (
              <button key={(r.itemId || "") + i} className="sv-item" onClick={() => { if (r.itemId) location.hash = `#/solve/essay/${r.itemId}`; }}>
                <span className={"no " + (r.max > 0 && r.total >= r.max ? "sv-ok" : "")}>{r.total ?? 0}/{r.max ?? 0}</span>
                <span className="tx">{r.snippet || "(문항)"}</span>
                <span className="rt">{fmtDate(r.at)}</span>
              </button>
            ))}
          </div>
          <div className="es-hint">누르면 같은 문항을 다시 풀 수 있어요.</div>
        </div>
      )}
      {n === null && <div className="sv-muted">서술형 문항을 찾는 중…</div>}
      {n === 0 && (
        <div>
          <div className="sv-empty">아직 공개된 서술형 문항이 없어요 — 곧 열려요.<br />채점 기준이 붙은 문항이 공개되면 여기서 바로 풀 수 있어요.</div>
          <div className="es-actions">
            <button className="sv-btn" onClick={() => (location.hash = "#/study/practice")}>공부하기 홈</button>
            <button className="sv-btn ghost" onClick={() => { setN(null); countLive({ withRubric: true }).then(setN).catch(() => setN(0)); }}>다시 확인</button>
          </div>
        </div>
      )}
      {n > 0 && (
        <ItemPicker mode="item" filter={{ withRubric: true }} hint="채점 기준이 있는 문항만 보여요. 단원 → 개념 → 문항 순으로 골라요."
          onPickItem={(it) => { if (it?.id) location.hash = `#/solve/essay/${it.id}`; }} />
      )}
    </SolveShell>
  );
}

// ── 풀기 ─────────────────────────────────────────────────────────────────────

function EssaySolve({ itemId }) {
  const [toast, say] = useToast();
  const [uid, setUid] = useState(null);
  const [item, setItem] = useState(null);
  const [state, setState] = useState("loading");      // loading | ready | missing | norubric | error
  const [phase, setPhase] = useState("answer");       // answer | grade | done
  // ② 내 답안
  const [text, setText] = useState("");
  const [photo, setPhoto] = useState(null);           // { path, url } | { busy:true } | null
  const camRef = useRef(null), fileRef = useRef(null);
  const startRef = useRef(Date.now());
  const [elapsed, setElapsed] = useState(0);
  // ③ 채점
  const [marks, setMarks] = useState({});             // { [no]: "full"|"partial"|"zero" }
  const [checked, setChecked] = useState([]);         // 체크한 실수거리 index
  const [correct, setCorrect] = useState(null);       // 내 답이 맞았나요? true|false|null
  const [finishing, setFinishing] = useState(false);
  const [final, setFinal] = useState(null);           // 채점 완료 시점의 점수
  const [wn, setWn] = useState(null);                 // null | "busy" | "done"
  const gradeRef = useRef(null), doneRef = useRef(null);

  useEffect(() => { supabase.auth.getUser().then(({ data }) => setUid(data?.user?.id || null)).catch(() => {}); }, []);

  useEffect(() => {
    let alive = true;
    setState("loading");
    fetchItem(itemId).then((it) => {
      if (!alive) return;
      if (!it) { setState("missing"); return; }
      setItem(it);
      setState(hasRubric(it) ? "ready" : "norubric");
    }).catch(() => { if (alive) setState("error"); });
    return () => { alive = false; };
  }, [itemId]);

  // 타이머 — 답안 제출까지
  useEffect(() => {
    if (phase !== "answer") return;
    const t = setInterval(() => setElapsed(Math.floor((Date.now() - startRef.current) / 1000)), 1000);
    return () => clearInterval(t);
  }, [phase]);

  const rubric = item?.solution?.rubric || null;
  const rItems = useMemo(() => (Array.isArray(rubric?.items) ? rubric.items.filter(Boolean) : []), [rubric]);
  const rChecks = useMemo(() => (Array.isArray(rubric?.checks) ? rubric.checks : []), [rubric]);
  const principles = useMemo(() => (Array.isArray(rubric?.principles) ? rubric.principles.filter((p) => typeof p === "string" && p.trim()) : []), [rubric]);
  const score = useMemo(() => computeScore(rubric, marks, checked), [rubric, marks, checked]);
  const levels = useMemo(() => (item ? solutionLevels(item) : []), [item]);
  const canSubmit = !!(text.trim() || photo?.path) && !photo?.busy;
  const canFinish = allMarked(rubric, marks) && correct !== null && !finishing;

  // ── 사진 ──
  async function onFile(e) {
    const f = e.target.files?.[0];
    e.target.value = "";
    if (!f) return;
    if (!uid) { say("로그인 정보를 확인하는 중이에요. 잠시 뒤 다시 시도해 주세요"); return; }
    setPhoto({ busy: true });
    try {
      const blob = await downscaleJpeg(f, 1400, 0.85);
      const path = `${uid}/essay/${uuid()}.jpg`;
      const { error } = await supabase.storage.from("notes").upload(path, blob, { contentType: "image/jpeg" });
      if (error) throw error;
      const { data } = await supabase.storage.from("notes").createSignedUrl(path, 3600);
      setPhoto({ path, url: data?.signedUrl || URL.createObjectURL(blob) });
    } catch (err) {
      say("사진을 올리지 못했어요: " + (err?.message || "다시 시도해 주세요"));
      setPhoto(null);
    }
  }
  async function removePhoto() {
    const p = photo?.path;
    setPhoto(null);
    if (p) { try { await supabase.storage.from("notes").remove([p]); } catch { /* 침묵 */ } }
  }

  // ── ② 제출 → ③ 채점 ──
  function submit() {
    if (!canSubmit) { say("풀이를 쓰거나 사진을 올려 주세요"); return; }
    setElapsed(Math.floor((Date.now() - startRef.current) / 1000));
    setPhase("grade");
    setTimeout(() => gradeRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 50);
  }
  const setMark = (no, m) => setMarks((prev) => ({ ...prev, [no]: m }));
  const toggleCheck = (i) => setChecked((prev) => (prev.includes(i) ? prev.filter((x) => x !== i) : [...prev, i]));

  // ── ③ 채점 완료 → ④ 해설 + 저장 ──
  async function finish() {
    if (!canFinish || !item) return;
    setFinishing(true);
    const sc = computeScore(rubric, marks, checked);
    const vd = verdict(sc.total, sc.max);
    const answer_text = text.trim() || null;
    const image_path = photo?.path || null;
    let synced = false;
    if (uid) {
      try {
        const { error } = await supabase.from("essay_grades").insert({
          user_id: uid, item_id: item.id, answer_text, image_path,
          scores: { marks, checks: checked, perElement: sc.perElement, correct, elapsedSec: elapsed, verdict: vd },
          total: sc.total, max: sc.max,
        });
        synced = !error;
      } catch { synced = false; }     // 표가 아직 없을 수 있다 — 아래 localStorage 로 이어 간다
    }
    saveResult({ itemId: item.id, snippet: snippetOf(item), unitId: item.unit_id || null, conceptId: conceptOf(item), total: sc.total, max: sc.max, correct, synced });
    if (uid) logAttempt({ uid, item, rawAnswer: answer_text || image_path, correct: !!correct, solutionSeen: true, elapsedSec: elapsed, setId: "essay" });
    setFinal(sc);
    setPhase("done");
    setFinishing(false);
    setTimeout(() => doneRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 50);
  }

  async function addWrongNote() {
    if (!uid || !item || wn) return;
    setWn("busy");
    const my = (text.trim() || (photo?.path ? "(사진 답안)" : "")).slice(0, 120);
    const r = await saveItemWrongNotes({ uid, entries: [{ item, myAnswer: my, tag: null }], source: "서술형" });
    if (r.error) { say("오답노트 저장에 실패했어요"); setWn(null); return; }
    say(r.added ? "오답노트에 추가했어요 📕" : "이미 오답노트에 있어요");
    setWn("done");
  }

  // ── 상태별 화면 ──
  const shell = (children) => (
    <SolveShell title="서술형 자가채점" back="#/tools/essay" toast={toast}
      right={<button className="sv-btn sm" onClick={() => (location.hash = "#/solve/essay")}>다른 문항</button>}>
      <style>{CSS}</style>
      {children}
    </SolveShell>
  );
  if (state === "loading") return shell(<div className="sv-muted">문항을 불러오는 중…</div>);
  if (state === "missing") return shell(<div className="sv-empty">문항을 찾을 수 없어요.<br />비공개로 바뀌었거나 없는 문항이에요.</div>);
  if (state === "error") return shell(<div className="sv-empty">문항을 불러오지 못했어요.<br />잠시 뒤 다시 시도해 주세요.</div>);
  if (state === "norubric") return shell(<div className="sv-empty">이 문항에는 아직 채점 기준이 없어요.<br />채점 기준이 있는 다른 문항을 골라 주세요.</div>);

  const locked = phase !== "answer";
  const showDone = phase === "done" && final;
  const rv = showDone ? reviewList(rubric, final) : [];
  const needsNote = showDone && (final.total < final.max || correct === false);
  const DIFF = { 1: "쉬움", 2: "보통", 3: "표준", 4: "심화", 5: "도전" };

  return shell(
    <>
      {/* ① 문제 */}
      <div className="sv-card">
        <div className="es-meta">
          <span className="es-tag hi">서술형</span>
          {item.unit_id && <span className="es-tag">{UNIT_NAMES[item.unit_id] || item.unit_id}</span>}
          {item.difficulty ? <span className="es-tag">{DIFF[item.difficulty] || `난이도 ${item.difficulty}`}</span> : null}
          <span className="es-tag">배점 {score.max}점</span>
          <span className="es-timer">⏱ {fmtTime(elapsed)}</span>
        </div>
        <ItemQuestion item={item} showChoices={false} />
        <p className="es-note">풀이 과정을 써서 답을 구하세요.</p>
      </div>

      {/* ② 내 답안 */}
      <div className="sv-card">
        <div className="sv-sec" style={{ marginTop: 0 }}>내 답안{locked && <span className="sv-badge">제출됨</span>}</div>
        {!locked ? (
          <>
            <textarea className="sv-in sv-ta" value={text} onChange={(e) => setText(e.target.value)} rows={6}
              placeholder="풀이 과정과 답을 써요. 사진으로 올려도 돼요" />
            <div className="sv-row wrap" style={{ marginTop: 8, gap: 6 }}>
              <button className="sv-btn sm" disabled={!!photo?.busy} onClick={() => camRef.current?.click()}>📷 사진 찍기</button>
              <button className="sv-btn sm" disabled={!!photo?.busy} onClick={() => fileRef.current?.click()}>🖼 앨범에서 고르기</button>
              {photo?.busy && <span className="sv-small">사진을 올리는 중…</span>}
              <input ref={camRef} type="file" accept="image/*" capture="environment" hidden onChange={onFile} />
              <input ref={fileRef} type="file" accept="image/*" hidden onChange={onFile} />
            </div>
          </>
        ) : (
          text.trim() ? <div className="es-mine">{text.trim()}</div> : null
        )}
        {photo?.url && (
          <div className="es-photo">
            <img src={photo.url} alt="내 답안 사진" />
            {!locked && <button className="sv-btn sm ghost rm" onClick={removePhoto}>사진 지우기</button>}
          </div>
        )}
        {locked && !text.trim() && !photo?.url && <div className="sv-muted">(답안 없음)</div>}
        {!locked && (
          <>
            <button className="sv-btn pri full" style={{ marginTop: 12 }} disabled={!canSubmit} onClick={submit}>답안 제출</button>
            <div className="es-hint">제출하면 답안을 고칠 수 없고, 채점 기준이 열려요. 시간은 {fmtTime(elapsed)} 흘렀어요.</div>
          </>
        )}
      </div>

      {/* ③ 채점 기준 */}
      {locked && (
        <div className="sv-card" ref={gradeRef}>
          <div className="sv-sec" style={{ marginTop: 0 }}>채점 기준 — 내 답안과 비교해 스스로 표시해요</div>
          {rItems.map((it, idx) => {
            const no = it.no ?? idx + 1;
            const pts = fullPoints(it), pp = partialPoints(it);
            const m = marks[no];
            const pe = score.perElement.find((p) => String(p.no) === String(no));
            return (
              <div className="es-el" key={no}>
                <div className="es-el-h">
                  <span className="no">{no}</span>
                  <span>{it.element || `요소 ${no}`}</span>
                  <span className={"pt" + (m ? " got" : "")}>{m ? `${pe?.got ?? 0} / ${pts}점` : `${pts}점`}</span>
                </div>
                {it.criterion && <MathText as="div" className="es-crit" text={it.criterion} />}
                {it.partial && <div className="es-sub"><b>부분</b><MathText text={it.partial} /></div>}
                {it.zero && <div className="es-sub"><b>0점</b><MathText text={it.zero} /></div>}
                <div className="es-seg" role="radiogroup" aria-label={`요소 ${no} 채점`}>
                  {[["full", pts], ["partial", pp], ["zero", 0]].map(([k, p]) => (
                    <button key={k} type="button" role="radio" aria-checked={m === k} disabled={showDone}
                      className={k + (m === k ? " on" : "")} onClick={() => setMark(no, k)}>
                      {MARK_LABEL[k]}{k !== "zero" && <small>{p}점</small>}
                    </button>
                  ))}
                </div>
                {pe?.reason?.startsWith("실수거리") && <div className="es-hint" style={{ color: "var(--bad)" }}>{pe.reason} — 아래 실수거리 체크 때문에 {pe.got}점으로 조정됐어요.</div>}
              </div>
            );
          })}

          {rChecks.length > 0 && (
            <>
              <div className="sv-sec">실수거리 확인 — 해당하면 체크해요</div>
              <div className="sv-list">
                {rChecks.map((c, i) => {
                  if (!c) return null;
                  const on = checked.includes(i);
                  return (
                    <label key={i} className={"es-chk" + (on ? " on" : "")}>
                      <input type="checkbox" checked={on} disabled={showDone} onChange={() => toggleCheck(i)} />
                      <span className="tx">
                        <MathText text={c.text || ""} />
                        <span className="ef">
                          {c.element_no != null ? `요소 ${c.element_no}` : "해당 요소"} → {c.effect === "불인정" ? "불인정 (0점)" : c.effect === "부분" ? "부분 점수까지만 인정" : (c.effect || "")}
                        </span>
                      </span>
                    </label>
                  );
                })}
              </div>
            </>
          )}

          <div className="es-total">
            <span className="big">{score.total}</span><span className="of">/ {score.max}점</span>
            <span className="vd">예상 점수</span>
          </div>
          <div className="sv-bar"><i style={{ width: `${score.max ? Math.round((score.total / score.max) * 100) : 0}%` }} /></div>

          {principles.length > 0 && (
            <details className="es-det" style={{ marginTop: 10 }}>
              <summary>채점 원칙 보기</summary>
              <ul>{principles.map((p, i) => <li key={i}><MathText text={p} /></li>)}</ul>
            </details>
          )}

          <div className="sv-sec">정답</div>
          <MathText as="div" className="es-ans" text={answerText(item)} />
          <div className="sv-muted" style={{ marginTop: 8 }}>내 답이 맞았나요?</div>
          <div className="es-tog">
            <button type="button" disabled={showDone} className={"ok" + (correct === true ? " on" : "")} onClick={() => setCorrect(true)}>맞음</button>
            <button type="button" disabled={showDone} className={"bad" + (correct === false ? " on" : "")} onClick={() => setCorrect(false)}>틀림</button>
          </div>

          {!showDone && (
            <>
              <button className="sv-btn pri full" style={{ marginTop: 14 }} disabled={!canFinish} onClick={finish}>{finishing ? "저장 중…" : "채점 완료"}</button>
              {!canFinish && !finishing && (
                <div className="es-hint">
                  {!allMarked(rubric, marks) ? "모든 요소에 정확·부분·0점 중 하나를 표시해 주세요. " : ""}
                  {correct === null ? "정답 여부(맞음/틀림)도 골라 주세요." : ""}
                </div>
              )}
            </>
          )}
        </div>
      )}

      {/* ④ 모범답안·해설 + 한 줄 평 */}
      {showDone && (
        <>
          <div className="sv-card" ref={doneRef}>
            <div className="sv-sec" style={{ marginTop: 0 }}>결과</div>
            <div className="es-verdict">{verdict(final.total, final.max)}</div>
            <div className="es-total" style={{ margin: "0 0 6px" }}>
              <span className="big">{final.total}</span><span className="of">/ {final.max}점</span>
              <span className={"vd " + (correct ? "sv-ok" : "sv-bad")} style={{ color: correct ? "var(--good)" : "var(--bad)" }}>{correct ? "답 맞음" : "답 틀림"}</span>
            </div>
            <div className="sv-bar"><i style={{ width: `${final.max ? Math.round((final.total / final.max) * 100) : 0}%` }} /></div>
            <div className="es-hint">스스로 매긴 예상 점수예요. 실제 시험의 채점과는 다를 수 있어요.</div>
            {rv.length > 0 && (
              <>
                <div className="sv-sec">다시 볼 것</div>
                <div className="es-rv">
                  {rv.map((r) => (
                    <div className="it" key={r.no}>
                      <b>요소 {r.no} · {r.element} — {r.got}/{r.points}점 ({r.reason})</b>
                      {r.criterion && <MathText text={r.criterion} />}
                    </div>
                  ))}
                </div>
              </>
            )}
            {rv.length === 0 && <div className="sv-ok" style={{ marginTop: 10 }}>모든 요소를 채웠어요. 다른 문항으로 이어 가요!</div>}
          </div>

          <div className="sv-card">
            <div className="sv-sec" style={{ marginTop: 0 }}>모범답안 · 해설</div>
            {item.solution?.model_answer ? <MathText as="div" className="es-model" text={item.solution.model_answer} /> : null}
            {levels.map((lv, i) => (
              <div className="es-lv" key={i}>
                <div className="es-lv-t">{lv?.title || `${i + 1}단계`}</div>
                {Array.isArray(lv?.figure) && lv.figure.length > 0 && <ItemFigure figure={lv.figure} width={300} />}
                {Array.isArray(lv?.steps) && lv.steps.length > 0 && (
                  <ol>{lv.steps.map((s, j) => <li key={j}><MathText text={s} /></li>)}</ol>
                )}
                {lv?.text ? <MathText as="p" text={lv.text} /> : null}
              </div>
            ))}
            {!item.solution?.model_answer && !levels.length && <div className="sv-muted">이 문항의 해설은 아직 준비되지 않았어요.</div>}
          </div>

          <div className="es-actions">
            {needsNote && (
              <button className="sv-btn" disabled={wn === "busy" || wn === "done" || !uid} onClick={addWrongNote}>
                {wn === "done" ? "오답노트에 담김" : wn === "busy" ? "담는 중…" : "📕 오답노트에 추가"}
              </button>
            )}
            <button className="sv-btn" onClick={() => askAboutItem(item)}>💬 질문하기</button>
            <button className="sv-btn pri" onClick={() => (location.hash = "#/solve/essay")}>다른 문항</button>
            <button className="sv-btn ghost" onClick={() => (location.hash = "#/study/practice")}>공부하기 홈</button>
          </div>
        </>
      )}
    </>
  );
}
