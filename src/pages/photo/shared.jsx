// 촬영 모듈 공용 조각 — 문항 카드 · 보관 안내 · 신호등 · 단계 표시 · 작은 도우미
import MathText from "../../components/MathText";
import { CIRCLED } from "../../lib/answers";
import { UNIT_NAMES } from "../../lib/items";
import { putSession, newId } from "../../lib/deviceStore";
import { readCurrent } from "../../lib/photoApi";

export const GRADE_LABEL = { S: "표준형", M: "소폭 변형", C: "창작형" };
export const FEATURE_LABEL = { read: "문장 이해하기", mark: "표시 연습", essay: "서술형 채점·첨삭", check: "풀이과정 검사" };
export const FEATURE_ICON = { read: "🔍", mark: "✍️", essay: "📝", check: "🧾" };
export const LIGHT_LABEL = { green: "좋아요", yellow: "주의", red: "고쳐요" };

export { stripMarker, titleOf, findSpan, cutText, aggregateLights, CRITERIA } from "../../lib/photoText.js";
import { titleOf, CRITERIA } from "../../lib/photoText.js";

/** 캔버스 → 작은 미리보기(data URL, 긴 변 480) — sessionStorage 에 넣어도 될 크기 */
export function thumbOf(cv, maxSide = 480) {
  try {
    const sc = Math.min(1, maxSide / Math.max(cv.width, cv.height));
    const t = document.createElement("canvas");
    t.width = Math.max(1, Math.round(cv.width * sc)); t.height = Math.max(1, Math.round(cv.height * sc));
    t.getContext("2d").drawImage(cv, 0, 0, t.width, t.height);
    return t.toDataURL("image/jpeg", 0.7);
  } catch { return null; }
}

/** 방금 찍은 문항(다른 화면에서 넘어온 것)이 있으면 돌려준다 */
export function currentProblem() {
  const c = readCurrent();
  return c && typeof c.question === "string" && c.question ? c : null;
}

/** 기기 보관소에 세션 저장 (실패해도 흐름은 막지 않는다) */
export async function saveDevice(rec) {
  try { return await putSession({ id: rec.id || newId(), ...rec, title: rec.title || titleOf(rec.question) }); } catch { return null; }
}

/** 촬영 흐름 단계 표시 */
export function Steps({ list, at }) {
  return (
    <div className="ph-steps">
      {list.map((s, i) => <span key={s} className={i === at ? "on" : i < at ? "done" : ""}>{i + 1}. {s}</span>)}
    </div>
  );
}

export function Busy({ text }) {
  return <div className="ph-busy"><span className="sp" />{text}</div>;
}

/** 전사된 문항 카드 — 미리보기(선택) · 문장 · 선택지 · 그림 메모 · 등급 */
export function ProblemCard({ p, thumb, title = "찍은 문제", children, showGrade = true }) {
  if (!p) return null;
  return (
    <div className="sv-card">
      <div className="sv-sec" style={{ marginTop: 0 }}>{title}</div>
      {thumb && <img className="ph-thumb" src={thumb} alt="" />}
      <MathText as="div" className="ph-q" text={p.question} />
      {Array.isArray(p.choices) && p.choices.length > 0 && (
        <div className="ph-choices">{p.choices.map((c, i) => <div key={i} className="c"><span>{CIRCLED[i] || i + 1}</span><MathText text={c} /></div>)}</div>
      )}
      {p.figure_note && <div className="ph-fig">그림·표: {p.figure_note}</div>}
      <div className="ph-meta">
        {p.unit_guess && UNIT_NAMES[p.unit_guess] && <span className="tag">{UNIT_NAMES[p.unit_guess]}</span>}
        {p.qtype && <span className="tag">{p.qtype === "choice" ? "선택형" : p.qtype === "essay" ? "서술형" : "단답형"}</span>}
        {showGrade && p.std?.item_grade && <span className="tag" title={p.std.reason || ""}>문항 표현 {GRADE_LABEL[p.std.item_grade]}</span>}
        {Array.isArray(p.warnings) && p.warnings.map((w, i) => <span key={i} className="tag" style={{ color: "var(--bad)" }}>⚠ {w}</span>)}
      </div>
      {children}
    </div>
  );
}

/** 보관 위치 안내 — 답안 원문이 어디 남았는지 학생에게 있는 그대로 */
export function KeepNote({ retention }) {
  if (!retention) return null;
  const where = retention.where;
  let text;
  if (where === "central" && retention.central) text = "이 답안은 학습 기록(서버)에도 저장됐어요 — 문항 표현이 표준형이라 답안을 남겨도 괜찮은 경우예요.";
  else if (retention.error) text = "서버 기록 저장은 실패했지만 결과는 이 기기에 남겼어요.";
  else text = "답안 원문은 이 기기에만 저장했어요. 서버에는 점수·유형 같은 라벨만 남아요.";
  return <div className="ph-keep"><span className="ic">🔒</span><span>{text}</span></div>;
}

/** 다섯 지표 신호등 */
export function Lights({ criteria, compact = false }) {
  return (
    <div className="ph-lights">
      {CRITERIA.map((k) => {
        const c = criteria?.[k];
        const l = c?.light || null;
        return (
          <div key={k} className={"ph-light" + (l ? " " + l : " dim")} title={c?.why || ""}>
            <span className="dot" />
            <span>{k}</span>
            {!compact && l && <span style={{ fontSize: 10.5 }}>{LIGHT_LABEL[l]}</span>}
          </div>
        );
      })}
    </div>
  );
}

export const fmtWhen = (iso) => { try { const d = new Date(iso); return `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`; } catch { return ""; } };
