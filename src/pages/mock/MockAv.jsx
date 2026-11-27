// ashrain.out — 공부하기 › 시청각 학습 › 학교별 모의고사 (#/study/av/mock)
//   학교마다 판(융합 · 기본 …) 탭 → 시기별 회차 칸(컨셉 문제 세트 칸과 같은 틀) → 그 시험의 해설 영상(#/mock/<id>/video?from=av)
//   해설 영상: 문항마다 문제 → 풀이(보관함 해설그림)를 교실 모니터처럼 넘겨 본다 — 나가기는 이 목록으로.
import { useState } from "react";
import { editionsOf, examGroups } from "../../lib/mockexams";
import { useMockIndex, useMockUser } from "./parts";
import { ExamTiles } from "./SchoolExams";
import "./mock.css";

const KEY = "ash.study.av.mocked";
const readEd = () => { try { const v = JSON.parse(localStorage.getItem(KEY) || "{}"); return v && typeof v === "object" ? v : {}; } catch { return {}; } };

export default function MockAv() {
  const { index, err } = useMockIndex();
  const uid = useMockUser();
  const [edBy, setEdBy] = useState(readEd);
  if (err) return <div className="st-empty">목록을 불러오지 못했어요 — 연결을 확인해 주세요. ({err})</div>;
  if (!index) return <div className="st-empty">불러오는 중…</div>;
  const schools = index.schools.filter((s) => index.exams.some((e) => e.school === s.id));
  if (!schools.length) return <div className="st-empty">학교별 모의고사를 올리는 중이에요 — 조금만 기다려 주세요.</div>;
  return (
    <>
      {schools.map((s) => {
        const eds = editionsOf(index, s.id).filter((e) => e.n > 0);
        const ed = eds.some((e) => e.id === edBy[s.id]) ? edBy[s.id] : eds[0]?.id;
        const pick = (v) => {
          const n = { ...edBy, [s.id]: v };
          setEdBy(n);
          try { localStorage.setItem(KEY, JSON.stringify(n)); } catch { /* 사생활 모드 등 */ }
        };
        const groups = examGroups(index, s.id, ed);
        return (
          <section key={s.id} className="mx-avsch">
            <div className="mx-shero">
              <span className="mx-sfi big" aria-hidden="true">{(s.short || s.name).slice(0, 2)}</span>
              <div><b>{s.name}</b><small>{[s.region, `모의고사 ${index.exams.filter((e) => e.school === s.id).length}회`].filter(Boolean).join(" · ")}</small></div>
            </div>
            {eds.length > 1 && (
              <div className="st-lv mx-edtabs" role="tablist" aria-label="판">
                {eds.map((e) => (
                  <button key={e.id} type="button" role="tab" aria-selected={e.id === ed} className={e.id === ed ? "on" : ""} onClick={() => pick(e.id)}>
                    {e.icon} {e.title}<small>{e.n}</small>
                  </button>
                ))}
              </div>
            )}
            {groups.map((gr) => (
              <div key={gr.key}>
                <p className="st-sec">{gr.title}</p>
                <ExamTiles exams={gr.exams} uid={uid} href={(e) => `#/mock/${e.id}/video?from=av`} />
              </div>
            ))}
          </section>
        );
      })}
      <p className="st-sec" style={{ fontWeight: 600 }}>시험 화면의 「🎬 해설 영상」과 같아요 — 문제를 풀어 보려면 공부하기 › 시험 보기 › 학교별 모의고사에서 열어요.</p>
    </>
  );
}
