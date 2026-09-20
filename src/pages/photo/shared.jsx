// 촬영 모듈 공용 조각 — 문항 카드 · 보관 안내 · 신호등 · 단계 표시 · 진행 막대 · 오류 안내 · 빈 상태 그림
import MathText from "../../components/MathText";
import { CIRCLED } from "../../lib/answers";
import { UNIT_NAMES } from "../../lib/items";
import { putSession, newId } from "../../lib/deviceStore";
import { readCurrent } from "../../lib/photoApi";

export const GRADE_LABEL = { S: "표준형", M: "소폭 변형", C: "창작형" };
export const FEATURE_LABEL = { read: "문장 이해하기", mark: "표시 연습", essay: "서술형 채점·첨삭", check: "풀이과정 검사" };
export const FEATURE_ICON = { read: "🔍", mark: "✍️", essay: "📝", check: "🧾" };
export const LIGHT_LABEL = { green: "좋아요", yellow: "주의", red: "고쳐요" };
const LIGHT_GLYPH = { green: "✓", yellow: "!", red: "✕" };      // 색약이어도 알아볼 수 있게 모양+글자를 함께

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

/** 기기 보관소에 세션 저장 (실패해도 흐름은 막지 않는다). 썸네일은 이 기기에만 — 서버로는 절대 가지 않는다. */
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

/** 여러 차례 부르는 일의 진행 막대 — n/N + 지금 하는 단계 문구 */
export function Progress({ now = 0, total = 1, label, foot }) {
  const pct = total > 0 ? Math.min(100, Math.round((now / total) * 100)) : 0;
  return (
    <div className="ph-prog" role="status" aria-live="polite">
      <div className="hd"><span className="sp" /><span className="tx">{label}</span><span className="cnt">{pct}%</span></div>
      <div className="sv-bar"><i style={{ width: `${pct}%` }} /></div>
      {foot && <div className="ft">{foot}</div>}
    </div>
  );
}

/** 하루 한도(429)에 걸린 오류인가 — api/photo 는 "오늘 사용 한도(N회)를 다 썼어요" 로 답한다 */
export const isQuotaError = (m) => /한도|429/.test(String(m || ""));

/**
 * 오류 + 다음에 할 행동. 글상자만 남기지 않는다.
 *   onRetry  같은 일을 다시 (없으면 버튼 안 그림)
 *   onShoot  다시 찍기
 */
export function ErrorNote({ text, onRetry, retryLabel = "다시 해 보기", onShoot, shootLabel = "다시 찍기", home = true, mine = false }) {
  const quota = isQuotaError(text);
  return (
    <div className="ph-oops" role="alert">
      <div className="tt"><span className="ic">{quota ? "🌙" : "⚠"}</span><span>{quota ? "오늘 쓸 수 있는 횟수를 다 썼어요" : String(text || "잘 되지 않았어요")}</span></div>
      <div className="ds">{quota
        ? "내일 다시 이용할 수 있어요. 오늘 받은 결과는 내 기록에 그대로 남아 있어요."
        : "잠시 뒤 다시 해 보거나, 더 밝은 곳에서 가까이 다시 찍어 보세요."}</div>
      <div className="ph-actions">
        {!quota && onShoot && <button className="sv-btn pri" onClick={onShoot}>{shootLabel}</button>}
        {!quota && onRetry && <button className={"sv-btn" + (onShoot ? "" : " pri")} onClick={onRetry}>{retryLabel}</button>}
        {(quota || mine) && <button className="sv-btn" onClick={() => { location.hash = "#/solve/photo/mine"; }}>내 기록 보기</button>}
        {home && <button className={"sv-btn ghost" + (quota ? " " : " wide")} onClick={() => { location.hash = "#/solve/photo"; }}>촬영 모듈 홈으로</button>}
      </div>
    </div>
  );
}

/** 빈 상태 그림 — 인라인 SVG 소품 (외부 이미지 없음) */
export function EmptyArt({ kind = "shot", size = 84 }) {
  const common = { width: size, height: size, viewBox: "0 0 84 84", fill: "none", stroke: "currentColor", strokeWidth: 2.2, strokeLinecap: "round", strokeLinejoin: "round", "aria-hidden": "true", focusable: "false" };
  if (kind === "box") {
    return (
      <svg {...common}>
        <path d="M14 30 L42 20 L70 30 L42 40 Z" />
        <path d="M14 30 v26 l28 10 V40" />
        <path d="M70 30 v26 l-28 10" />
        <path d="M52 16 v-6 M60 22 l5-5 M44 12 l-1-5" opacity=".55" />
      </svg>
    );
  }
  return (
    <svg {...common}>
      <rect x="10" y="24" width="64" height="42" rx="8" />
      <path d="M30 24 l5-8h14l5 8" />
      <circle cx="42" cy="45" r="11" />
      <path d="M37 45 l4 4 7-8" />
      <path d="M64 33 h3" opacity=".6" />
    </svg>
  );
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

/** 다섯 지표 신호등 — 색 + 모양(동그라미·네모·마름모) + 글자 라벨 */
export function Lights({ criteria, compact = false }) {
  return (
    <div className="ph-sigs">
      {CRITERIA.map((k) => {
        const c = criteria?.[k];
        const l = c?.light || null;
        const lab = l ? LIGHT_LABEL[l] : "아직 없음";
        return (
          <div key={k} className={"ph-sig" + (l ? " " + l : " dim")} title={c?.why || ""} aria-label={`${k} ${lab}`}>
            <span className="dot" aria-hidden="true"><span className="gl">{LIGHT_GLYPH[l] || "·"}</span></span>
            <span className="nm">{k}</span>
            {!compact && l && <span className="lb">{lab}</span>}
          </div>
        );
      })}
    </div>
  );
}

export const fmtWhen = (iso) => { try { const d = new Date(iso); return `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`; } catch { return ""; } };
