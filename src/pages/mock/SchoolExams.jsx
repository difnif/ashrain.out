// ashrain.out — 공부하기 › 시험 보기 › 학교별 모의고사 (#/study/exam/school[/<학교>[/<판>]])
//   학교 찾기(이름 · 줄임 · 지역 · 초성) → 학교 → 판(융합 · 기본 · 기출 분석 …) → 회차(시기별로 묶음) → 시험 화면(#/mock/<id>)
//   회차는 컨셉 문제 세트처럼 아이콘 칸(번호 · 판 아이콘 · 회차 · 푼 만큼 막대 · 채점 점수) — ExamTiles 는 시청각 학습 › 학교별 모의고사도 쓴다.
//   목록은 공개 버킷 mock-exams 의 index.json(lib/mockexams.js) — 학교 · 시험이 늘어도 앱을 고칠 일이 없다.
import { useMemo, useState } from "react";
import { searchSchools, editionsOf, examGroups, readRecentSchools, pushRecentSchool, readMockRecord, readMockPaper, edInfo } from "../../lib/mockexams";
import { useMockIndex, useMockUser } from "./parts";
import "./mock.css";

const crumbGo = (h) => () => { location.hash = h; };

export default function SchoolExams({ path = [] }) {
  const { index, err } = useMockIndex();
  const [schoolId, edRaw] = path;
  const ed = edRaw ? decodeURIComponent(edRaw) : "";
  if (err) return <><Crumb /><div className="st-empty">목록을 불러오지 못했어요 — 연결을 확인해 주세요. ({err})</div></>;
  if (!index) return <><Crumb /><div className="st-empty">불러오는 중…</div></>;
  if (!schoolId) return <SchoolList index={index} />;
  const school = index.schools.find((s) => s.id === schoolId);
  if (!school) return <><Crumb /><div className="st-empty">없는 학교예요. <button type="button" className="mx-linkb" onClick={crumbGo("#/study/exam/school")}>학교 찾기</button></div></>;
  if (!ed) return <SchoolHome index={index} school={school} />;
  return <EdList index={index} school={school} ed={ed} />;
}

function Crumb({ school, ed }) {
  return (
    <div className="st-crumb mx-crumb">
      <button type="button" onClick={crumbGo("#/study/exam")}>시험 보기</button><span aria-hidden="true">›</span>
      {school ? <button type="button" onClick={crumbGo("#/study/exam/school")}>학교별 모의고사</button> : <b>학교별 모의고사</b>}
      {school && <><span aria-hidden="true">›</span>{ed ? <button type="button" onClick={crumbGo(`#/study/exam/school/${school.id}`)}>{school.short || school.name}</button> : <b>{school.short || school.name}</b>}</>}
      {ed && <><span aria-hidden="true">›</span><b>{edInfo(ed).title}</b></>}
    </div>
  );
}

/* ── 학교 찾기 ── */
function SchoolList({ index }) {
  const [q, setQ] = useState("");
  const recent = useMemo(() => readRecentSchools().map((id) => index.schools.find((s) => s.id === id)).filter(Boolean), [index]);
  const found = useMemo(() => searchSchools(index.schools, q), [index, q]);
  const open = (s) => { pushRecentSchool(s.id); location.hash = `#/study/exam/school/${s.id}`; };
  const examsOf = (s) => index.exams.filter((e) => e.school === s.id);
  return (
    <>
      <Crumb />
      <p className="st-cdesc">우리 학교 시험지와 같은 양식 · 범위로 만든 실전 모의고사예요. 학교를 고르면 융합 · 기본으로 나눠 골라 풀어요.</p>
      <input className="sv-search mx-search" type="search" value={q} onChange={(e) => setQ(e.target.value)} enterKeyHint="search"
        placeholder="학교 찾기 — 문정중, 송파, ㅁㅈ …" aria-label="학교 찾기" />
      {!q && recent.length > 0 && (
        <div className="mx-recent">
          <span>최근</span>
          {recent.map((s) => <button key={s.id} type="button" className="cs-chip" onClick={() => open(s)}>{s.short || s.name}</button>)}
        </div>
      )}
      {index.empty ? (
        <div className="st-empty">학교별 모의고사를 올리는 중이에요 — 조금만 기다려 주세요.</div>
      ) : found.length === 0 ? (
        <div className="st-empty">「{q.trim()}」에 맞는 학교가 아직 없어요.<br />학교 이름을 줄여서(예: 문정) 찾거나, 선생님께 우리 학교 모의고사를 부탁해 보세요.</div>
      ) : (
        <div className="st-list mx-schools">
          {found.map((s) => {
            const ex = examsOf(s);
            const eds = editionsOf(index, s.id).filter((e) => e.n > 0);
            return (
              <button key={s.id} type="button" className="st-folder" onClick={() => open(s)}>
                <span className="fi mx-sfi" aria-hidden="true">{(s.short || s.name).slice(0, 2)}</span>
                <span className="nm"><b>{s.name}</b>
                  <small>{[s.region, ex.length ? `모의고사 ${ex.length}회` : "준비 중"].filter(Boolean).join(" · ")}{eds.length ? ` · ${eds.map((e) => `${e.title} ${e.n}`).join(" · ")}` : ""}</small></span>
                <span className="go" aria-hidden="true">›</span>
              </button>
            );
          })}
        </div>
      )}
      {!index.empty && <p className="st-sec" style={{ fontWeight: 600 }}>학교는 계속 늘어나요 — 이름 · 지역 · 초성(ㅁㅈ)으로 찾아요.</p>}
    </>
  );
}

/* ── 학교 → 판 고르기 ── */
function SchoolHome({ index, school }) {
  const eds = editionsOf(index, school.id);
  return (
    <>
      <Crumb school={school} />
      <div className="mx-shero">
        <span className="mx-sfi big" aria-hidden="true">{(school.short || school.name).slice(0, 2)}</span>
        <div><b>{school.name}</b><small>{[school.region, school.level].filter(Boolean).join(" · ")}</small></div>
      </div>
      <p className="st-cdesc">어떤 판으로 풀까요?</p>
      <div className="mx-eds">
        {eds.map((e) => (
          <button key={e.id} type="button" className={"mx-ed" + (e.n ? "" : " off")} disabled={!e.n}
            onClick={() => (location.hash = `#/study/exam/school/${school.id}/${encodeURIComponent(e.id)}`)}>
            <span className="ic" aria-hidden="true">{e.icon}</span>
            <b>{e.title}</b>
            <span className="ds">{e.desc}</span>
            <span className="n">{e.n ? `${e.n}회` : "준비 중"}</span>
          </button>
        ))}
      </div>
    </>
  );
}

/* ── 판 → 회차 목록 ── */
function EdList({ index, school, ed }) {
  const uid = useMockUser();
  const eds = editionsOf(index, school.id);
  const groups = examGroups(index, school.id, ed);
  const info = edInfo(ed);
  return (
    <>
      <Crumb school={school} ed={ed} />
      <div className="st-lv mx-edtabs" role="tablist" aria-label="판">
        {eds.map((e) => (
          <button key={e.id} type="button" role="tab" aria-selected={e.id === ed} className={e.id === ed ? "on" : ""} disabled={!e.n && e.id !== ed}
            onClick={() => (location.hash = `#/study/exam/school/${school.id}/${encodeURIComponent(e.id)}`)}>{e.icon} {e.title}<small>{e.n || "—"}</small></button>
        ))}
      </div>
      {info.desc && <p className="st-cdesc">{info.desc}</p>}
      {groups.length === 0 ? (
        <div className="st-empty">{school.short || school.name} {info.title} 모의고사는 준비 중이에요.</div>
      ) : groups.map((gr) => (
        <div key={gr.key}>
          <p className="st-sec">{gr.title}</p>
          {gr.exams[0]?.range && <p className="mx-grange">범위 · {gr.exams[0].range.replace(/\[\[|\]\]|[{}]/g, "")} · 선택형 {gr.exams[0].n?.mc} · 서답형 {gr.exams[0].n?.sa} · {gr.exams[0].minutes}분</p>}
          <ExamTiles exams={gr.exams} uid={uid} />
        </div>
      ))}
    </>
  );
}

/** 회차 아이콘 칸 — 컨셉 문제 세트 칸과 같은 틀. href(e) 로 여는 곳을 바꾼다(시청각 학습은 해설 영상으로) */
export function ExamTiles({ exams, uid, href = (e) => `#/mock/${e.id}`, icon }) {
  return (
    <div className="st-icons mx-eicons">
      {exams.map((e) => <ExamTile key={e.id} e={e} uid={uid} href={href(e)} icon={icon} />)}
    </div>
  );
}

function ExamTile({ e, uid, href, icon }) {
  const rec = uid === undefined ? null : readMockRecord(e.id);
  const paper = uid === undefined ? null : readMockPaper(e.id);
  const last = rec?.results?.[0];
  const n = (e.n?.mc || 0) + (e.n?.sa || 0);
  const done = Math.max(rec ? Object.keys(rec.items || {}).length : 0, paper ? Object.keys(paper.answers || {}).length : 0);
  const pct = last ? 100 : n ? Math.min(100, Math.round((done / n) * 100)) : 0;
  return (
    <button type="button" className={"st-ic mx-eic" + (last ? " done" : "")} title={`${e.title}${e.sub ? ` · ${e.sub}` : ""} · ${e.ed}`}
      onClick={() => (location.hash = href)}>
      <span className="no">{String(e.no).padStart(2, "0")}</span>
      <span className="em" aria-hidden="true">{icon || edInfo(e.ed).icon}</span>
      <span className="nm">{e.no}회{last ? <small className="sc">{last.score}점</small> : done ? <small>{done}/{n}</small> : null}</span>
      <span className="pg" aria-label={last ? `채점 ${last.score}/${last.max}` : `${done}/${n}`}><i style={{ width: `${pct}%` }} /></span>
    </button>
  );
}
