// 풀이과정 검사하기 — #/solve/photo/check
// 문제집 페이지 촬영(여러 장 가능) → 문항·풀이 영역 자동 찾기 + 드래그로 고치기 → 영역마다 인식 → 식의 연결고리·암산·글씨 습관·오류 가설
// → 충실성·논리성·명료성·간결성·독창성 신호등(문항별·문서별) → 서술형 첨삭으로 볼 문항 고르기 → 없으면 끝, 있으면 채점·첨삭.
import { useMemo, useState } from "react";
import SolveShell, { useToast } from "../solve/SolveShell";
import MathText from "../../components/MathText";
import { trapText } from "../../lib/marking.js";
import { cropCanvas, canvasToBase64 } from "../../lib/camera";
import { photoCall } from "../../lib/photoApi";
import { newId } from "../../lib/deviceStore";
import Capture, { RegionPicker } from "./Capture";
import { EssayResult } from "./PhotoEssay";
import { Steps, Busy, Progress, ErrorNote, Lights, KeepNote, aggregateLights, thumbOf, saveDevice, titleOf, CRITERIA } from "./shared";

const LOAD = { low: "가벼움", mid: "보통", high: "많음 — 실수 위험" };
const HABIT = { size: "글씨 크기", messy: "난잡함", glyph: "헷갈리는 글자", align: "정렬·등호", unit: "단위", skip: "건너뜀", other: "기타" };
const EKIND = { calc: "계산", concept: "개념", reading: "문제 해석", transcription: "옮겨 적기", sign: "부호", unit: "단위", none: "없음" };
const ROLE = { setup: "식 세우기", transform: "변형", compute: "계산", answer: "답", other: "기타" };
const STEPS_PER_ITEM = 3;                    // 문항당 서버 호출 3회(문제 읽기 · 풀이 읽기 · 검사)

const nextNo = (boxes, kind) => {
  const used = new Set(boxes.filter((b) => b.kind === kind).map((b) => b.no));
  const other = boxes.filter((b) => b.kind !== kind).map((b) => b.no).sort((x, y) => x - y);
  for (const n of other) if (!used.has(n)) return n;            // 짝이 없는 번호부터
  return (Math.max(0, ...boxes.map((b) => b.no)) || 0) + 1;
};

export default function PhotoCheck() {
  const [toast, setToast] = useToast();
  const [pages, setPages] = useState([]);       // [{ id, cv, url, boxes:[{id,kind,no,box}], detecting, note }]
  const [adding, setAdding] = useState(true);   // 촬영 화면을 보이는가
  const [stage, setStage] = useState("edit");   // edit | run | result
  const [prog, setProg] = useState(null);       // { step, total, label, foot }
  const [items, setItems] = useState([]);       // 검사 결과 [{ id, pageIdx, no, p, a, out, err }]
  const [picked, setPicked] = useState({});     // 첨삭 받을 문항 { [itemId]: true }
  const [essays, setEssays] = useState({});     // { [itemId]: { busy, err, res } }
  const at = stage === "edit" ? (pages.length ? 1 : 0) : stage === "run" ? 2 : Object.keys(essays).length ? 3 : 2;

  const updatePage = (id, fn) => setPages((ps) => ps.map((pg) => (pg.id === id ? fn(pg) : pg)));

  // 페이지 사진을 고르면 바로 자동 탐지
  const onPicked = async (cv, url) => {
    const id = newId();
    setPages((ps) => [...ps, { id, cv, url, boxes: [], detecting: true, note: null }]);
    setAdding(false);
    try {
      const r = await photoCall("scan", { image: canvasToBase64(cv, 0.85), mode: "page" });
      const boxes = [
        ...(r.problems || []).map((b) => ({ id: newId(), kind: "q", no: b.no, box: b.box })),
        ...(r.answers || []).map((b) => ({ id: newId(), kind: "a", no: b.no, box: b.box })),
      ];
      updatePage(id, (pg) => ({ ...pg, boxes, detecting: false, note: boxes.length ? null : "자동으로 찾지 못했어요 — 아래 버튼으로 직접 잡아 주세요." }));
    } catch (e) {
      updatePage(id, (pg) => ({ ...pg, detecting: false, note: (e?.message || "자동 탐지 실패") + " — 직접 잡아 주세요." }));
    }
  };

  const pairs = useMemo(() => pages.flatMap((pg, pi) => {
    const qs = pg.boxes.filter((b) => b.kind === "q").sort((x, y) => x.no - y.no);
    return qs.map((q) => ({ pageIdx: pi, page: pg, no: q.no, q, a: pg.boxes.find((b) => b.kind === "a" && b.no === q.no) || null }));
  }), [pages]);
  const ready = pairs.filter((x) => x.a);

  const run = async () => {
    if (!ready.length) { setToast("문제와 답안이 짝지어진 문항이 없어요"); return; }
    setStage("run"); setItems([]); setPicked({}); setEssays({});
    const total = ready.length * STEPS_PER_ITEM;
    const say = (i, s, label) => setProg({ step: i * STEPS_PER_ITEM + s, total, label, foot: `${ready.length}문항 중 ${i + (s >= STEPS_PER_ITEM ? 1 : 0)}문항 끝남 · 문항마다 인식 2회와 검사 1회를 써요` });
    const out = [];
    for (let i = 0; i < ready.length; i++) {
      const pr = ready[i];
      const label = `${pages.length > 1 ? `${pr.pageIdx + 1}쪽 ` : ""}${pr.no}번`;
      const rec = { id: newId(), pageIdx: pr.pageIdx, no: pr.no, label, p: null, a: null, out: null, err: null, qthumb: null };
      try {
        say(i, 0, `${label} 문제 읽는 중…`);
        const qcv = cropCanvas(pr.page.cv, pr.q.box, 0.015);
        rec.qthumb = thumbOf(qcv, 360);
        const sp = await photoCall("scan", { image: canvasToBase64(qcv, 0.85), mode: "problem" });
        if (sp.unreadable) throw new Error("문항을 읽지 못했어요 — 문제 영역을 다시 잡아 주세요");
        rec.p = { question: sp.question, choices: sp.choices, qtype: sp.qtype, figure_note: sp.figure_note, unit_guess: sp.unit_guess, std: sp.std, warnings: sp.warnings };
        say(i, 1, `${label} 풀이 읽는 중…`);
        const acv = cropCanvas(pr.page.cv, pr.a.box, 0.015);
        const sa = await photoCall("scan", { image: canvasToBase64(acv, 0.85), mode: "answer" });
        if (sa.unreadable) throw new Error("풀이를 읽지 못했어요 — 답안 영역을 다시 잡아 주세요");
        rec.a = { answer: sa.answer, lines: sa.lines, final_answer: sa.final_answer, legibility: sa.legibility, thumb: thumbOf(acv, 360) };
        say(i, 2, `${label} 풀이 과정 검사 중…`);
        const r = await photoCall("process", { question: rec.p.question, figure_note: rec.p.figure_note, choices: rec.p.choices, answer: rec.a.answer, lines: rec.a.lines, legibility: rec.a.legibility, std: rec.p.std, unit: rec.p.unit_guess });
        rec.out = r;
        saveDevice({ id: rec.id, feature: "check", title: `${label} · ${titleOf(rec.p.question)}`, question: rec.p.question, figure_note: rec.p.figure_note, unit: rec.p.unit_guess, grade: r.std?.item_grade || rec.p.std?.item_grade || null, answer: rec.a.answer, result: r.result, retention: r.retention, thumb: rec.qthumb });
      } catch (e) {
        rec.err = e?.message || "검사 실패";
      }
      say(i, STEPS_PER_ITEM, `${label} 끝`);
      out.push(rec); setItems(out.slice());
    }
    setProg(null); setStage("result");
  };

  const gradePicked = async () => {
    const ids = items.filter((it) => picked[it.id] && it.out && !essays[it.id]?.res).map((it) => it.id);
    if (!ids.length) { setToast("첨삭 받을 문항을 골라 주세요"); return; }
    for (const id of ids) {
      const it = items.find((x) => x.id === id);
      setEssays((es) => ({ ...es, [id]: { busy: true } }));
      try {
        const r = await photoCall("essay", { question: it.p.question, figure_note: it.p.figure_note, choices: it.p.choices, answer: it.a.answer, std: it.p.std, unit: it.p.unit_guess });
        setEssays((es) => ({ ...es, [id]: { res: r } }));
        saveDevice({ feature: "essay", title: `${it.label} · ${titleOf(it.p.question)}`, question: it.p.question, figure_note: it.p.figure_note, unit: it.p.unit_guess, grade: r.std?.item_grade || null, answer: it.a.answer, result: r.result, retention: r.retention, thumb: it.a?.thumb || it.qthumb || null });
      } catch (e) {
        setEssays((es) => ({ ...es, [id]: { err: e?.message || "첨삭 실패" } }));
      }
    }
  };

  const docLights = useMemo(() => aggregateLights(items.filter((it) => it.out).map((it) => it.out.result)), [items]);
  const okItems = items.filter((it) => it.out);
  const anyPicked = okItems.some((it) => picked[it.id]);
  const essayDone = Object.values(essays).some((e) => e?.res);
  const backToEdit = () => { setStage("edit"); setItems([]); setEssays({}); setPicked({}); };

  return (
    <SolveShell title="풀이과정 검사" back="#/solve/photo" toast={toast}
      sub={stage === "edit" && !pages.length ? "문제집 페이지를 찍고, 문제와 내 풀이 영역을 잡아 주세요. 식이 어떻게 이어지는지, 암산이 과한지, 글씨 습관은 어떤지 신호등으로 봐요." : undefined}>
      <Steps list={["페이지 찍기", "영역 잡기", "검사 결과", "첨삭"]} at={at} />

      {stage === "edit" && (
        <>
          {pages.map((pg, pi) => (
            <PageEditor key={pg.id} page={pg} idx={pi} many={pages.length > 1}
              onChange={(boxes) => updatePage(pg.id, (x) => ({ ...x, boxes }))}
              onRemove={() => setPages((ps) => ps.filter((x) => x.id !== pg.id))} setToast={setToast} />
          ))}
          {(adding || !pages.length) && (
            <div className="sv-card">
              {pages.length > 0 && <div className="sv-sec" style={{ marginTop: 0 }}>{pages.length + 1}쪽</div>}
              <Capture mode="page" onPicked={onPicked} setToast={setToast} />
              {pages.length > 0 && <button className="sv-btn sm ghost" style={{ marginTop: 8 }} onClick={() => setAdding(false)}>추가 안 할래요</button>}
            </div>
          )}
          {pages.length > 0 && (
            <div className="sv-card">
              <div className="sv-sec" style={{ marginTop: 0 }}>검사할 문항 <span className="sv-small">· 문제와 풀이가 둘 다 잡힌 것만</span></div>
              {ready.length
                ? <div className="sv-small" style={{ lineHeight: 1.7 }}>{ready.map((x) => `${pages.length > 1 ? `${x.pageIdx + 1}쪽 ` : ""}${x.no}번`).join(" · ")} — {ready.length}문항</div>
                : <div className="sv-muted">아직 없어요. 각 문항의 문제 영역과 풀이 영역을 같은 번호로 잡아 주세요.</div>}
              {pairs.length > ready.length && <div className="sv-small" style={{ marginTop: 4, color: "var(--bad)" }}>풀이가 없는 문항 {pairs.length - ready.length}개는 건너뛰어요.</div>}
              <div className="ph-actions" style={{ marginTop: 10 }}>
                <button className="sv-btn pri" onClick={run} disabled={!ready.length || pages.some((x) => x.detecting)}>검사하기 ({ready.length}문항)</button>
                {!adding && <button className="sv-btn" onClick={() => setAdding(true)}>페이지 추가</button>}
              </div>
              <div className="sv-small" style={{ marginTop: 8 }}>문항마다 문제·풀이 인식 2회와 검사 1회를 써요. 사진은 서버에 남지 않아요.</div>
            </div>
          )}
        </>
      )}

      {stage === "run" && (
        <div className="sv-card">
          <Progress now={prog?.step || 0} total={prog?.total || ready.length * STEPS_PER_ITEM} label={prog?.label || "준비 중…"} foot={prog?.foot} />
          <div className="sv-small" style={{ marginTop: 10 }}>{items.length} / {ready.length} 문항 끝남</div>
        </div>
      )}

      {stage === "result" && (
        <>
          {okItems.length > 1 && (
            <div className="sv-card">
              <div className="sv-sec" style={{ marginTop: 0 }}>문서 전체 <span className="sv-small">· {okItems.length}문항</span></div>
              <Lights criteria={docLights} />
              <div className="ph-why">{CRITERIA.map((k) => docLights[k]?.light ? <span key={k} style={{ marginRight: 10 }}><b>{k}</b> {docLights[k].why}</span> : null)}</div>
            </div>
          )}
          {items.map((it) => <ItemResult key={it.id} it={it} pick={!!picked[it.id]} onPick={() => setPicked((p) => ({ ...p, [it.id]: !p[it.id] }))} essay={essays[it.id]} onFix={backToEdit} />)}
          {!okItems.length && (
            <div className="sv-card">
              <div className="ph-blank">
                <div className="tt">검사한 문항이 없어요</div>
                <div className="ds">문제 영역과 풀이 영역을 같은 번호로 잡았는지 확인하고 다시 검사해 주세요.</div>
              </div>
              <div className="ph-actions" style={{ marginTop: 12 }}>
                <button className="sv-btn pri" onClick={backToEdit}>영역 다시 잡기</button>
                <button className="sv-btn ghost" onClick={() => { location.hash = "#/solve/photo"; }}>촬영 모듈 홈으로</button>
              </div>
            </div>
          )}

          {okItems.length > 0 && (
            <div className="sv-card" style={{ borderColor: "color-mix(in srgb, var(--accent) 45%, var(--border))" }}>
              <div style={{ fontWeight: 800, fontSize: 15.5, marginBottom: 6 }}>서술형 첨삭으로 더 볼 문항이 있나요?</div>
              <div className="sv-small" style={{ marginBottom: 10, lineHeight: 1.6 }}>위 카드에서 문항을 체크하면 채점 기준표로 채점하고 어디를 어떻게 고칠지 첨삭해 줘요.</div>
              <div className="ph-actions">
                <button className="sv-btn pri" onClick={gradePicked} disabled={!anyPicked || Object.values(essays).some((e) => e?.busy)}>선택한 문항 첨삭받기</button>
                <button className="sv-btn" onClick={() => { location.hash = "#/solve/photo"; }}>{essayDone ? "끝내기" : "없어요, 끝낼래요"}</button>
                <button className="sv-btn ghost wide" onClick={backToEdit}>영역 다시 잡기</button>
              </div>
            </div>
          )}
        </>
      )}
    </SolveShell>
  );
}

/** 페이지 한 장 — 상자 보기·그리기·번호 배지 팝오버로 고치기 */
function PageEditor({ page, idx, many, onChange, onRemove, setToast }) {
  const [mode, setMode] = useState(null);        // 'q' | 'a' | null
  const [sel, setSel] = useState(null);
  const boxes = page.boxes;
  const set = (list) => onChange(list);

  const onDraw = (box) => {
    if (!mode) return;
    const nb = { id: newId(), kind: mode, no: nextNo(boxes, mode), box };
    set([...boxes, nb]); setSel(nb.id); setMode(null);
    setToast(`${nb.no}번 ${mode === "q" ? "문제" : "풀이"} 영역을 잡았어요`);
  };
  const bump = (b, d) => set(boxes.map((x) => (x.id === b.id ? { ...x, no: Math.max(1, x.no + d) } : x)));
  const setKind = (b, kind) => { if (b.kind !== kind) set(boxes.map((x) => (x.id === b.id ? { ...x, kind } : x))); };
  const moveBox = (b, box) => set(boxes.map((x) => (x.id === b.id ? { ...x, box } : x)));
  const del = (id) => { set(boxes.filter((b) => b.id !== id)); if (sel === id) setSel(null); };

  return (
    <div className="sv-card">
      <div className="sv-row" style={{ marginBottom: 8 }}>
        <div className="sv-sec" style={{ margin: 0, flex: 1 }}>{many ? `${idx + 1}쪽` : "페이지"}</div>
        <button className="sv-btn sm ghost" onClick={onRemove}>이 페이지 빼기</button>
      </div>
      <div className="sv-row wrap" style={{ gap: 12, marginBottom: 8 }}>
        <span className="ph-key"><i className="q" />문제</span>
        <span className="ph-key"><i className="a" />내 풀이</span>
        <span className="sv-small">번호 배지를 탭하면 그 자리에서 고쳐요</span>
      </div>
      {page.detecting && <div style={{ marginBottom: 8 }}><Busy text="문항과 풀이 자리를 찾는 중…" /></div>}
      {page.note && !page.detecting && <div className="sv-small" style={{ marginBottom: 8, color: "var(--bad)" }}>{page.note}</div>}
      <div className="ph-mode">
        <button className={"sv-chip q" + (mode === "q" ? " on" : "")} onClick={() => { setMode(mode === "q" ? null : "q"); setSel(null); }}>{mode === "q" ? "문제 영역을 드래그하세요" : "+ 문제 영역"}</button>
        <button className={"sv-chip a" + (mode === "a" ? " on" : "")} onClick={() => { setMode(mode === "a" ? null : "a"); setSel(null); }}>{mode === "a" ? "풀이 영역을 드래그하세요" : "+ 풀이 영역"}</button>
        {boxes.length > 0 && <button className="sv-chip" onClick={() => { set([]); setSel(null); }}>모두 지우기</button>}
      </div>
      <RegionPicker url={page.url} drawing={!!mode} selected={sel} editable
        boxes={boxes.map((b) => ({ ...b, label: `${b.no}번 ${b.kind === "q" ? "문제" : "풀이"}` }))}
        onDraw={onDraw} onMiss={() => setToast("영역이 너무 작아요 — 조금 더 크게 잡아 주세요")}
        onTapBox={(b) => setSel(sel === b.id ? null : b.id)} onMoveBox={moveBox}
        renderMenu={(b) => (
          <div className="ph-pop-in">
            <div className="ttl">{b.no}번 {b.kind === "q" ? "문제" : "내 풀이"} 고치기</div>
            <div className="rw">
              <button className="ph-pb" onClick={() => bump(b, -1)} aria-label="번호 줄이기">−</button>
              <span className="nm">{b.no}번</span>
              <button className="ph-pb" onClick={() => bump(b, 1)} aria-label="번호 늘리기">+</button>
            </div>
            <div className="rw">
              <button className={"ph-seg q" + (b.kind === "q" ? " on" : "")} aria-pressed={b.kind === "q"} onClick={() => setKind(b, "q")}>문제</button>
              <button className={"ph-seg a" + (b.kind === "a" ? " on" : "")} aria-pressed={b.kind === "a"} onClick={() => setKind(b, "a")}>내 풀이</button>
            </div>
            <div className="rw">
              <button className="ph-pb wide bad" onClick={() => del(b.id)}>삭제</button>
              <button className="ph-pb wide" onClick={() => setSel(null)}>닫기</button>
            </div>
          </div>
        )} />
      {!boxes.length && !page.detecting && <div className="sv-small" style={{ marginTop: 8, lineHeight: 1.6 }}>위 버튼을 누른 뒤 사진 위를 드래그해서 영역을 잡아요. 문제 하나에 문제 영역 1개 + 풀이 영역 1개, 같은 번호로.</div>}
    </div>
  );
}

/** 문항 하나의 검사 결과 카드 (+ 첨삭 선택 · 첨삭 결과) */
function ItemResult({ it, pick, onPick, essay, onFix }) {
  const r = it.out?.result;
  return (
    <div className={"ph-item" + (pick ? " sel" : "")}>
      <div className="hd"><span className="no">{it.no}</span><span>{it.label}</span>
        {r && <span className={"st " + (r.final_answer_ok ? "ok" : "bad")}>{r.final_answer_ok ? "답 맞음" : "답 확인 필요"}</span>}
        {it.err && <span className="st bad">실패</span>}
      </div>
      {it.err && <ErrorNote text={it.err} onShoot={onFix} shootLabel="영역 다시 잡기" home={false} />}
      {r && (
        <>
          <Lights criteria={r.criteria} compact />
          <div className="ph-why" style={{ marginTop: 6 }}>{CRITERIA.map((k) => r.criteria?.[k]?.why ? <div key={k}><b>{k}</b> {r.criteria[k].why}</div> : null)}</div>
          {r.summary && <div style={{ marginTop: 8, fontSize: 14, lineHeight: 1.65 }}><MathText text={r.summary} /></div>}
          <div className="ph-chips">
            <span className={"ph-chip" + (r.mental_load === "high" ? " warn" : "")}>암산 부담: {LOAD[r.mental_load] || r.mental_load}</span>
            {r.pitfall_tags?.map((t, i) => <span key={i} className="ph-chip warn">⚠ {trapText(t)}</span>)}
          </div>
          {r.mental_note && <div className="sv-small" style={{ marginTop: 6, lineHeight: 1.6 }}>{r.mental_note}</div>}
          {r.error?.found && (
            <div className="ph-fix" style={{ marginTop: 10 }}>
              <div className="w">어디서 틀렸을까 — {r.error.line ? `${r.error.line}번째 줄 · ` : ""}{EKIND[r.error.kind] || r.error.kind}</div>
              {r.error.hypothesis && <div><MathText text={r.error.hypothesis} /></div>}
              {r.error.fix && <div className="right" style={{ marginTop: 2 }}><MathText text={r.error.fix} /></div>}
            </div>
          )}
          {r.habits?.length > 0 && (
            <div style={{ marginTop: 10 }}>
              <div className="sv-small" style={{ marginBottom: 6 }}>실수를 줄이려면</div>
              <div className="sv-list">{r.habits.map((h, i) => <div key={i} className="ph-habit"><span className="k">{HABIT[h.kind] || h.kind}</span><span>{h.note}<span className="tip">→ {h.tip}</span></span></div>)}</div>
            </div>
          )}
          <details className="ph-more" style={{ marginTop: 10 }}>
            <summary><span className="ic">🔗</span><span>식의 연결고리 {r.chain?.length ? `(${r.chain.length}줄)` : ""}</span><span className="sub">읽어 낸 문제와 풀이</span></summary>
            <div className="bd">
              {r.chain?.length > 0 && (
                <ul className="ph-chain">
                  {r.chain.map((c, idx) => <li key={idx} className={c.ok === false ? "bad" : c.ok === true ? "ok" : ""}><span className="i">{c.i}</span><span><MathText text={c.text} /><span className="nt">{ROLE[c.role] || c.role}{c.note ? ` · ${c.note}` : ""}</span></span></li>)}
                </ul>
              )}
              <div className="sv-small" style={{ marginTop: 10 }}>문제</div>
              {it.qthumb && <img className="ph-thumb" src={it.qthumb} alt="" style={{ margin: "4px 0" }} />}
              <MathText as="div" className="ph-q" text={it.p?.question} style={{ fontSize: 14 }} />
              <div className="sv-small" style={{ marginTop: 10 }}>내 풀이(읽어 낸 것)</div>
              {it.a?.thumb && <img className="ph-thumb" src={it.a.thumb} alt="" style={{ margin: "4px 0" }} />}
              <MathText as="div" className="ph-ans" text={it.a?.answer} />
            </div>
          </details>
          <KeepNote retention={it.out.retention} />
          {!essay?.res && (
            <label className={"ph-check" + (pick ? " on" : "")} style={{ marginTop: 10 }}>
              <input type="checkbox" checked={pick} onChange={onPick} disabled={!!essay?.busy} />
              <span className="tx">{essay?.busy ? "첨삭 받는 중…" : "이 문항은 서술형 첨삭까지 받기"}</span>
            </label>
          )}
          {essay?.err && <div style={{ marginTop: 8 }}><ErrorNote text={essay.err} home={false} /></div>}
          {essay?.res && (
            <div style={{ marginTop: 12 }}>
              <div className="sv-sec">서술형 채점·첨삭</div>
              <EssayResult result={essay.res.result} />
              <KeepNote retention={essay.res.retention} />
            </div>
          )}
        </>
      )}
    </div>
  );
}
