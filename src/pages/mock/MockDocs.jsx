// ashrain.out — 학교별 모의고사 자료 보기(#/mock/<id>/doc/<자료>) · 정답과 채점 기준(#/mock/<id>/key)
//   자료 보기: 문제지 · 빠른 정답지 · 해설지 … 를 쪽 그림으로 화면 폭에 맞춰 펼친다(확대 · 쪽 이동 · 받기 · 인쇄).
//   정답과 채점 기준: 선택형 정답표(번호 · 정답 · 배점 · 단원 — 시험지를 채점했으면 내 답 · ○ ✗도) + 서답형 답 · 채점 요소.
import { useEffect, useMemo, useRef, useState } from "react";
import { fileUrl, fmtBytes, downloadName, readMockPaper, gradeMock, choiceText, CIRCLED } from "../../lib/mockexams";
import { Rich, avKnown } from "./parts";
import { avItem } from "../../lib/av";

const ZOOMS = [1, 1.25, 1.5, 2];

/** PDF 받기 — 앱이 받아 한글 이름을 붙인다(막히면 서버가 이름을 붙이는 ?download= 주소로) */
export async function downloadDoc(exam, doc, schoolShort, say) {
  const name = downloadName(exam, doc, schoolShort);
  const url = fileUrl(exam, doc.pdf);
  try {
    const r = await fetch(url);
    if (!r.ok) throw new Error(String(r.status));
    const blob = await r.blob();
    const u = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = u; a.download = name; a.rel = "noopener";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(u), 30000);
    say?.(`${doc.label}를 받았어요`);
  } catch {
    const a = document.createElement("a");
    a.href = `${url}?download=${encodeURIComponent(name)}`; a.rel = "noopener";
    document.body.appendChild(a); a.click(); a.remove();
    say?.(`${doc.label}를 받는 중이에요`);
  }
}
/** 인쇄 — PDF 를 새 창에서(브라우저 PDF 보기의 인쇄) */
export function printDoc(exam, doc, say) {
  const w = window.open(fileUrl(exam, doc.pdf), "_blank", "noopener");
  if (!w) say?.("새 창이 막혔어요 — 브라우저에서 이 사이트의 팝업을 허용해 주세요");
}

export function MockDoc({ exam, school, docId, say }) {
  const doc = exam.docs.find((d) => d.id === docId) || exam.docs[0];
  const [zi, setZi] = useState(0);
  const [cur, setCur] = useState(0);
  const boxRef = useRef(null);
  const [w, setW] = useState(0);
  useEffect(() => {
    const el = boxRef.current;
    if (!el) return undefined;
    const fit = () => setW(el.clientWidth);
    fit();
    const ro = typeof ResizeObserver !== "undefined" ? new ResizeObserver(fit) : null;
    ro?.observe(el);
    return () => ro?.disconnect();
  }, []);
  useEffect(() => {
    const on = () => {
      const pgs = [...(boxRef.current?.querySelectorAll(".mx-dpg") || [])];
      const mid = window.innerHeight / 2;
      const k = pgs.findIndex((p) => { const r = p.getBoundingClientRect(); return r.top <= mid && r.bottom >= mid; });
      if (k >= 0) setCur(k);
    };
    window.addEventListener("scroll", on, { passive: true });
    return () => window.removeEventListener("scroll", on);
  }, []);
  const goPage = (k) => {
    const el = boxRef.current?.querySelectorAll(".mx-dpg")[k];
    if (el) window.scrollBy({ top: el.getBoundingClientRect().top - 64, behavior: "smooth" });
  };
  const pw = Math.max(280, (w - 4) * ZOOMS[zi]);
  return (
    <div className="cs-paperpage">
      <div className="mx-dtabs">
        {exam.docs.map((d) => (
          <a key={d.id} href={`#/mock/${exam.id}/doc/${d.id}`} className={"cs-chip" + (d.id === doc.id ? " on" : "")}>{d.label}<small> {d.pages.length}쪽</small></a>
        ))}
      </div>
      <div ref={boxRef} className="cs-paperbox mx-dbox">
        <div style={{ width: pw, margin: zi === 0 ? "0 auto" : 0 }}>
          {doc.pages.map((pg, k) => (
            <div key={pg.img} className="mx-dpg" style={{ aspectRatio: `${pg.w} / ${pg.h}` }}>
              <img src={fileUrl(exam, pg.img)} alt={`${doc.label} ${k + 1}쪽`} loading={k < 2 ? "eager" : "lazy"} draggable={false} />
            </div>
          ))}
        </div>
      </div>
      <div className="cs-pbar2" role="toolbar" aria-label="자료 도구">
        <div className="cs-zoom">
          <button type="button" className="cs-tb" disabled={zi === 0} onClick={() => setZi((v) => Math.max(0, v - 1))} aria-label="작게">−</button>
          <button type="button" className="cs-tb cs-zv" onClick={() => setZi(0)} title="폭 맞춤">{zi === 0 ? "맞춤" : `${Math.round(ZOOMS[zi] * 100)}%`}</button>
          <button type="button" className="cs-tb" disabled={zi === ZOOMS.length - 1} onClick={() => setZi((v) => Math.min(ZOOMS.length - 1, v + 1))} aria-label="크게">＋</button>
        </div>
        <div className="cs-zoom">
          <button type="button" className="cs-tb" disabled={cur <= 0} onClick={() => goPage(cur - 1)} aria-label="앞 쪽">‹</button>
          <span className="cs-tb mx-pgn">{cur + 1}/{doc.pages.length}</span>
          <button type="button" className="cs-tb" disabled={cur >= doc.pages.length - 1} onClick={() => goPage(cur + 1)} aria-label="다음 쪽">›</button>
        </div>
        <span className="cs-fill" />
        <button type="button" className="sv-btn sm mx-nw" onClick={() => printDoc(exam, doc, say)} title="인쇄">🖨<span className="lg"> 인쇄</span></button>
        <button type="button" className="sv-btn sm mx-nw" onClick={() => downloadDoc(exam, doc, school?.short, say)} title="받기">⬇<span className="lg"> 받기{doc.bytes ? ` ${fmtBytes(doc.bytes)}` : ""}</span></button>
      </div>
    </div>
  );
}

export function MockKey({ exam, uid }) {
  const paper = useMemo(() => (uid === undefined ? null : readMockPaper(exam.id)), [exam.id, uid]);
  const g = useMemo(() => (paper?.submitted ? gradeMock(exam, paper.answers, paper.sa) : null), [exam, paper]);
  const rowOf = g ? Object.fromEntries(g.rows.map((r) => [r.i, r])) : {};
  const mcs = exam.items.filter((it) => it.kind === "mc"), sas = exam.items.filter((it) => it.kind === "sa");
  const go = (i) => { location.hash = `#/mock/${exam.id}/q/${i}`; };
  return (
    <div className="cs-wrap mx-keypage">
      {g && <div className="mx-keysum">시험지 채점 <b>{g.score}</b>/{g.max} · 선택형 {g.mc.ok}/{g.mc.n} 맞힘 — 표의 ○ ✗는 그 채점이에요</div>}
      <div className="cs-sec">선택형 <small>{mcs.length}문항 · {exam.pts.mc}점</small></div>
      <div className="mx-ktab" role="table" aria-label="선택형 정답">
        <div className="mx-kr head" role="row"><span>번호</span><span>정답</span><span>배점</span><span>단원 · 유형</span>{g && <span>내 답</span>}</div>
        {mcs.map((it) => {
          const r = rowOf[it.i], mine = paper?.answers?.[it.i]?.sel || [];
          const avs = (it.av || []).filter(avKnown);
          return (
            <button key={it.i} type="button" className={"mx-kr" + (r ? " " + r.status : "")} role="row" onClick={() => go(it.i)}>
              <span className="n">{it.label}</span>
              <span className="a">{choiceText(it.ans)}</span>
              <span className="p">{it.pts}</span>
              <span className="u"><Rich text={it.unit} />{avs.length > 0 && <i title={avs.map((k) => avItem(k)?.title).join(" · ")}> 🎬</i>}</span>
              {g && <span className="m">{mine.length ? mine.map((c) => CIRCLED[c]).join("") : "—"} {r?.status === "ok" ? "○" : "✗"}</span>}
            </button>
          );
        })}
      </div>
      <div className="cs-sec">서답형 <small>{sas.length}문항 · {exam.pts.sa}점</small></div>
      {sas.map((it) => {
        const r = rowOf[it.i];
        return (
          <div key={it.i} className="cs-card mx-ksa">
            <div className="mx-ksah"><b>[{it.label}]</b> <span>{it.title}</span><span className="cs-fill" /><b>{it.pts}점</b>{r && r.status !== "pending" && <em className={r.status}>{r.got}점</em>}</div>
            <div className="mx-ans"><span className="iv-lab">답</span><Rich text={it.answer} /></div>
            {it.rubric?.length > 0 && (
              <ul className="mx-krub">{it.rubric.map(([t, p], k) => <li key={k}><Rich text={t} /> <b>({p}점)</b></li>)}</ul>
            )}
            <div className="mx-ksaf"><button type="button" className="sv-btn sm" onClick={() => go(it.i)}>한 문제씩 풀기 ›</button></div>
          </div>
        );
      })}
      {exam.notes?.length > 0 && <p className="cs-dnote">※ {exam.notes.join(" ")}</p>}
    </div>
  );
}
