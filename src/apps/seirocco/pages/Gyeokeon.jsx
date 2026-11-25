// 시록고 — 격언 도우미 (#/gyeok) · 그달 PRZ-1 코드에 맞는 격언 하나와 보고서 문장을 고르고, 격언 1,009개를 찾아본다.
// 데이터: public/gyeokeon/gyeokeon.v2.json(이 화면을 열 때만 받는다) · 고르기: ../gyeokeon/gyPick.js · 코드 읽기: ../gyeokeon/codeline.js
// 원칙(SPEC-격언그림-항목규칙-v2): 아이에게는 다정하게(아이에게 줄 말), 선생님에게는 정확하게(출전 · 원문 · 판본 표기 · 대조 출처).
//   정답률은 어디에도 보이지 않는다(오른 달 덤은 고르는 데만). 같은 코드면 같은 격언 — 이름 씨앗은 코드 머리의 이름.
//   붙여 넣은 코드는 이 화면 안에서만 쓰고 저장하지 않는다. 장면 그림은 아직(부품을 만드는 중).
import { useEffect, useMemo, useState } from "react";
import { pickMonths, fillReport, teacherCard, dominantType } from "../gyeokeon/gyPick";
import { monthsFromCodes } from "../gyeokeon/codeline";
import { koMatch } from "../../../lib/koSearch";

const TY = {
  rush: ["조급", "#C8452D"], shadow: ["그림자", "#CF7F2A"], cross: ["갈림길", "#B8901F"], steady: ["꾸준", "#5E8C4A"],
  stubborn: ["고집", "#2E897D"], cue: ["단서", "#3A7DB0"], evap: ["증발", "#3B4F9A"], shrink: ["위축", "#6C4E9E"],
  auto: ["자동화", "#9A4A8E"], none: ["주 유형 없음", "#6B6157"],
};
const ORDER = ["rush", "shadow", "cross", "steady", "stubborn", "cue", "evap", "shrink", "auto", "none"];
const WHO = { P: "박재우 선생님", O: "다른 선생님", AI: "AI 문장", E: "코멘트 없음" };
const SAMPLE = [
  "PRZ1 하늘·중2 2609#01 │ 3400○30 │ O0 │ ---0·000000 │ 222222222 │ 000000000 │ 000000000 │ Σ006",
  "PRZ1 하늘·중2 2610#02 │ 3312↑40 │ P1 │ 62C0·120000 │ 302150040 │ 000000000 │ 000000000 │ Σ013",
  "PRZ1 하늘·중2 2611#03 │ 4321↑30 │ P1 │ 55C0·110100 │ 100752000 │ 000000000 │ 000000000 │ Σ021",
].join("\n");

let dataP = null;
const loadData = () => {
  dataP ??= fetch("/gyeokeon/gyeokeon.v2.json").then((r) => { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); });
  return dataP.catch((e) => { dataP = null; throw e; });
};

function TypeChip({ k }) {
  const [l, c] = TY[k || "none"];
  return <span className="gk-ty" style={{ background: c }}>{l}</span>;
}

function Copy({ text }) {
  const [msg, setMsg] = useState("");
  return (
    <button className="d-btn" type="button" onClick={async () => {
      try { await navigator.clipboard.writeText(text); setMsg("복사했어요"); }
      catch { setMsg("길게 눌러 직접 복사해 주세요"); }
      setTimeout(() => setMsg(""), 1800);
    }}>{msg || "문장 복사"}</button>
  );
}

/** 항목 하나 — 아이에게 줄 말 · 보고서 문장 · 선생님 카드 */
function Entry({ e, short, cum }) {
  const t = teacherCard(e);
  const report = short ? fillReport(e, short, cum || 0) : e.report.replace("{N}", "○○는").replace("{C}", "1,000");
  return (
    <div className="gk-entry">
      <div className="gk-title"><b>{e.label}</b><span>{e.label_eum}</span><TypeChip k={e.primary} /></div>
      <p className="gk-src">{e.src}{e.label_kind === "후대 줄임" ? " · 표제는 후대의 줄임말" : ""}</p>
      <p className="gk-story">{e.story}</p>
      <p className="d-lbl">아이에게</p>
      <p className="gk-kid">{e.kid}</p>
      <p className="d-lbl">보고서 문장{short ? "" : " (이름 자리 ○○)"}</p>
      <div className="gk-report"><p>{report}</p><Copy text={report} /></div>
      <details className="gk-t">
        <summary>원문 · 출전 (선생님)</summary>
        <p className="gk-han">{e.text}</p>
        <p>{e.eum}</p>
        <p>{e.meaning}</p>
        {t.labelNote && <p className="d-note">{t.labelNote}</p>}
        {t.edition && <p className="d-note">{t.edition}</p>}
        <p className="d-note">{t.checked}</p>
      </details>
    </div>
  );
}

function PickTab({ data }) {
  const [text, setText] = useState("");
  const [open, setOpen] = useState({});
  const parsed = useMemo(() => monthsFromCodes(text), [text]);
  const results = useMemo(() => parsed.students.map((st) => ({ st, picks: pickMonths(st.short, st.months, data.entries) })), [parsed, data]);
  return (
    <>
      <div className="d-card">
        <p className="d-ct">PRZ-1 정식 코드 — 한 줄에 한 달, 한 학생의 첫 달부터</p>
        <textarea className="d-in gk-codes" value={text} onChange={(ev) => setText(ev.target.value)} spellCheck={false}
          placeholder={"PRZ1 이름·학년 YYMM#순번 │ … │ Σ누적\n여러 학생을 섞어 넣어도 이름으로 나눠요."} />
        <div className="gk-acts">
          <button className="d-btn" type="button" onClick={() => setText(SAMPLE)}>예시 넣기</button>
          {text && <button className="d-btn" type="button" onClick={() => { setText(""); setOpen({}); }}>비우기</button>}
          <span className="d-note">붙여 넣은 코드는 이 화면에서만 쓰고 저장하지 않아요.</span>
        </div>
        {parsed.errors.length > 0 && (
          <p className="gk-err">{parsed.errors.slice(0, 5).map((x) => `${x.line}번째 줄: ${x.error}`).join(" · ")}{parsed.errors.length > 5 ? ` 외 ${parsed.errors.length - 5}줄` : ""}</p>
        )}
      </div>
      {results.map(({ st, picks }) => {
        const rows = picks.map((p, i) => ({ p, m: st.months[i] })).reverse();   // 새 달부터
        return (
          <div className="d-card" key={st.short}>
            <p className="d-ct">{st.short} · {st.grade} — {st.months.length}달 ({st.months[0].nth}~{st.months[st.months.length - 1].nth}번째 달)</p>
            {(!st.fromFirst || st.gaps) && (
              <p className="d-note">첫 달부터 빠짐없이 넣으면 2년 안에 같은 격언이 다시 나오지 않고, 첫 달 · 누적 사건 격언도 제 달에 나와요.</p>
            )}
            {rows.map(({ p, m }, j) => {
              const key = st.short + "#" + m.nth, on = open[key] ?? j === 0;
              return (
                <div key={key} className="gk-month">
                  <div className="d-row click" onClick={() => setOpen((o) => ({ ...o, [key]: !on }))}>
                    <div>
                      <div className="d-main">{m.label} · {m.nth}번째 달 <TypeChip k={dominantType(m.S)} /></div>
                      <div className="d-sub">{p.entry.label} {p.entry.label_eum} · 관측 {WHO[m.who]} · 누적 약 {m.cum.toLocaleString("en-US")}문항</div>
                    </div>
                    <span className="d-sp" /><span className="d-chip">{on ? "접기" : "열기"}</span>
                  </div>
                  {on && <Entry e={p.entry} short={st.short} cum={m.cum} />}
                </div>
              );
            })}
          </div>
        );
      })}
      {!text && (
        <p className="d-note gk-pad">코드는 프리즘 코드북의 정식 코드 한 줄(PRZ1 …)이에요. 「예시 넣기」로 모양을 볼 수 있어요.</p>
      )}
    </>
  );
}

function FindTab({ data }) {
  const [q, setQ] = useState("");
  const [ty, setTy] = useState("");
  const [grp, setGrp] = useState("");
  const [lim, setLim] = useState(30);
  const [open, setOpen] = useState(null);
  const groups = useMemo(() => [...new Set(data.books.map((b) => b.group))], [data]);
  const hits = useMemo(() => {
    const cho = /^[ㄱ-ㅎ]+$/.test(q.replace(/\s+/g, ""));   // 초성만 넣으면 표제 음 · 책 이름에서만 찾는다(긴 고사에 아무렇게나 걸리지 않게)
    const rank = (e) => (koMatch(q, e.label, e.label_eum) ? 0 : koMatch(q, e.text, e.eum, e.book_ko, e.src) ? 1 : 2);
    return data.entries
      .filter((e) => (!ty || e.primary === ty) && (!grp || e.book_group === grp)
        && (cho ? koMatch(q, e.label_eum, e.book_ko) : koMatch(q, e.label, e.label_eum, e.text, e.eum, e.book_ko, e.src, e.story, e.meaning)))
      .map((e, i) => [q ? rank(e) : 0, i, e]).sort((a, b) => a[0] - b[0] || a[1] - b[1]).map((x) => x[2]);   // 표제에 걸린 것부터
  }, [data, q, ty, grp]);
  useEffect(() => { setLim(30); setOpen(null); }, [q, ty, grp]);
  return (
    <>
      <div className="d-card">
        <input className="d-in" type="search" value={q} onChange={(ev) => setQ(ev.target.value)}
          placeholder="표제 · 음 · 원문 · 책 · 출전 · 고사 (초성도 돼요: ㅇㄱㅇㅅ)" />
        <div className="d-tabs gk-filter">
          <button className={"d-tab" + (!ty ? " on" : "")} onClick={() => setTy("")}>모든 유형</button>
          {ORDER.map((k) => <button key={k} className={"d-tab" + (ty === k ? " on" : "")} onClick={() => setTy(ty === k ? "" : k)}>{TY[k][0]}</button>)}
        </div>
        <div className="d-tabs gk-filter">
          <button className={"d-tab" + (!grp ? " on" : "")} onClick={() => setGrp("")}>모든 책</button>
          {groups.map((g) => <button key={g} className={"d-tab" + (grp === g ? " on" : "")} onClick={() => setGrp(grp === g ? "" : g)}>{g}</button>)}
        </div>
        <p className="d-note">{hits.length.toLocaleString("en-US")}개</p>
      </div>
      <div className="d-card">
        {hits.slice(0, lim).map((e) => (
          <div key={e.id} className="gk-month">
            <div className="d-row click" onClick={() => setOpen(open === e.id ? null : e.id)}>
              <div><div className="d-main">{e.label} {e.label_eum} <TypeChip k={e.primary} /></div><div className="d-sub">{e.src}</div></div>
              <span className="d-sp" /><span className="d-chip">{open === e.id ? "접기" : "열기"}</span>
            </div>
            {open === e.id && <Entry e={e} />}
          </div>
        ))}
        {hits.length === 0 && <p className="d-note">찾은 격언이 없어요.</p>}
        {hits.length > lim && <button className="d-btn full" onClick={() => setLim(lim + 30)}>더 보기 ({hits.length - lim}개 남음)</button>}
      </div>
    </>
  );
}

function About({ data }) {
  const n = data.entries.length, web = data.entries.filter((e) => e.check.how === "웹 인용 대조").length;
  return (
    <div className="d-card">
      <p className="d-ct">이렇게 골라요</p>
      <ul className="gk-ul">
        <li>그달 코드의 스펙트럼(유형 몫)에 맞는 격언이 먼저예요. 주 유형이 없는 달(동점 · 미분화)은 「주 유형 없음」 격언이 앞서요.</li>
        <li>기복 · 이달 학습량 · 관측자가 맞는 격언에 덤을 줘요. 정답률이 오른 달에만 작은 덤이 있고, 내린 달은 아무것도 하지 않아요.</li>
        <li>첫 달, 누적 1,000 · 3,000 · 5,000 · 10,000문항을 넘는 달, 12 · 24 · 36번째 달에는 그 달의 격언에 큰 덤이 붙어요.</li>
        <li>한 아이에게 같은 격언은 2년 안에 다시 주지 않아요. 같은 코드면 언제나 같은 격언이에요.</li>
      </ul>
      <p className="d-ct" style={{ marginTop: 14 }}>쓸 때 지킬 것</p>
      <ul className="gk-ul">
        <li>아이에게는 다정하게: 표제와 「아이에게」 한두 문장만 건네요.</li>
        <li>선생님에게는 정확하게: 원문 · 출전을 확인하고, 표제가 후대의 줄임말이면 원문 구절과 함께 적어요.</li>
        <li>정답률은 그림 · 문장 어디에도 넣지 않아요.</li>
      </ul>
      <p className="d-note" style={{ marginTop: 12 }}>
        격언 {n.toLocaleString("en-US")}개 · {data.books.length}권 · 원문 대조 {n.toLocaleString("en-US")}개(그중 웹 인용 대조 {web}개).
        사서 · 삼경 · 제자서 · 사서(史書) · 성리학 · 시문 · 몽학서 · 국내 문헌에서 모았어요. 장면 그림은 부품을 만드는 중이에요.
      </p>
    </div>
  );
}

export default function Gyeokeon() {
  const [tab, setTab] = useState("pick");
  const [data, setData] = useState(null);
  const [err, setErr] = useState("");
  const load = () => { setErr(""); loadData().then(setData).catch(() => setErr("격언을 불러오지 못했어요.")); };
  useEffect(load, []);
  return (
    <div className="d-page">
      <style>{CSS}</style>
      <div className="d-head"><h2>격언 도우미</h2><span className="d-sp" /><span className="d-chip ac">새로</span></div>
      <p className="d-note" style={{ margin: "-4px 0 0" }}>그달 코드에 맞는 격언 하나와 보고서 문장을 골라요. 격언 1,009개를 찾아볼 수도 있어요.</p>
      <div className="d-tabs">
        {[["pick", "코드로 고르기"], ["find", "찾아보기"], ["about", "고르는 법"]].map(([k, l]) => (
          <button key={k} className={"d-tab" + (tab === k ? " on" : "")} onClick={() => setTab(k)}>{l}</button>
        ))}
      </div>
      {err ? <div className="d-card"><p className="d-note">{err}</p><button className="d-btn" onClick={load}>다시 불러오기</button></div>
        : !data ? <div className="d-card"><p className="d-note">격언을 불러오는 중…</p></div>
        : tab === "pick" ? <PickTab data={data} /> : tab === "find" ? <FindTab data={data} /> : <About data={data} />}
    </div>
  );
}

const CSS = `
.gk-codes{min-height:120px;font-size:12.5px;line-height:1.6;font-family:ui-monospace,Menlo,Consolas,monospace;white-space:pre}
.gk-acts{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:8px}
.gk-err{color:var(--down);font-size:12.5px;margin:8px 0 0}
.gk-pad{padding:0 4px}
.gk-ty{display:inline-block;color:#fff;font-size:11px;font-weight:800;border-radius:999px;padding:2px 8px;margin-left:4px;vertical-align:1px}
.gk-month+.gk-month{border-top:1px solid var(--bd)}
.gk-month .d-row{border-bottom:0}
.gk-entry{background:var(--in);border-radius:12px;padding:14px;margin:0 0 12px}
.gk-title{display:flex;align-items:baseline;flex-wrap:wrap;gap:8px}
.gk-title b{font-family:var(--font-serif);font-size:26px;line-height:1.2}
.gk-title span:not(.gk-ty){font-size:14px;color:var(--mut)}
.gk-src{font-size:12.5px;color:var(--mut);margin:4px 0 8px}
.gk-story{font-size:14px;line-height:1.75;margin:0 0 10px}
.gk-kid{font-size:15px;line-height:1.7;margin:0 0 10px;font-weight:600}
.gk-report{display:flex;align-items:flex-start;gap:10px;flex-wrap:wrap}
.gk-report p{flex:1 1 260px;margin:0;font-size:14px;line-height:1.75}
.gk-t{margin-top:12px;font-size:13.5px;line-height:1.75}
.gk-t summary{cursor:pointer;font-weight:700;color:var(--ac)}
.gk-t p{margin:6px 0}
.gk-han{font-family:var(--font-serif);font-size:17px;line-height:1.8}
.gk-filter{margin-top:10px}
.gk-ul{margin:0;padding-left:1.2em;font-size:13.5px;line-height:1.8}
`;
