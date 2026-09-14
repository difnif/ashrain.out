// 문항 본문(읽기 전용) — 번호 · 문제 · 도형 · 보기.  풀이·해설 UI 는 ItemView 가 이 위에 얹는다.
// props
//   item        test_items 행
//   index       0부터 — 번호 배지 (null 이면 배지 없음)
//   selected    고른 보기 번호 (0~4) — 표시만
//   reveal      true 면 정답 보기를 초록, 고른 오답을 빨강으로
//   onSelect    (idx) => void — 있으면 보기가 버튼이 된다 (reveal 이면 잠금)
//   showChoices 기본 true
//   compact     목록·인쇄용 작은 글씨
//   print       인쇄용(보기 테두리 없음)
//   meta        true 면 난이도·유형 칩
import { CIRCLED, correctChoiceIndex, kindOf } from "../lib/answers";
import MathText from "./MathText";
import ItemFigure from "./ItemFigure";
import "./item.css";

const DIFF = { 1: "쉬움", 2: "보통", 3: "표준", 4: "심화", 5: "도전" };
const KIND = { choice: "객관식", short: "단답", ox: "OX", essay: "서술" };

export default function ItemQuestion({ item, index = null, selected = null, reveal = false, onSelect, showChoices = true, compact = false, print = false, meta = false, figWidth = 320, children }) {
  if (!item) return null;
  const kind = kindOf(item);
  const correct = reveal && kind === "choice" ? correctChoiceIndex(item) : -1;
  const cls = "iq" + (compact ? " iq-compact" : "") + (print ? " iq-print" : "");
  return (
    <div className={cls}>
      {(index != null || meta) && (
        <div className="iq-head">
          {index != null && <span className="iq-no">{index + 1}</span>}
          {meta && (
            <span className="iq-meta">
              <span className="iq-tag">{KIND[kind] || kind}</span>
              {item.difficulty ? <span className="iq-tag">{DIFF[item.difficulty] || `난이도 ${item.difficulty}`}</span> : null}
              {item.points ? <span className="iq-tag">{item.points}점</span> : null}
            </span>
          )}
        </div>
      )}
      <MathText as="div" className="iq-q" text={item.question} />
      <ItemFigure figure={item.figure} width={figWidth} />
      {showChoices && kind === "choice" && Array.isArray(item.choices) && (
        <div className="iq-choices">
          {item.choices.map((c, i) => {
            let st = "";
            if (reveal) {
              if (i === correct) st = " ok";
              else if (i === selected) st = " bad";
              else st = " dim";
            } else if (i === selected) st = " sel";
            const Tag = onSelect ? "button" : "div";
            return (
              <Tag key={i} type={onSelect ? "button" : undefined} className={"iq-choice" + st}
                disabled={onSelect && reveal ? true : undefined}
                onClick={onSelect && !reveal ? () => onSelect(i) : undefined}>
                <span className="iq-circ">{CIRCLED[i] || i + 1}</span>
                <MathText text={c} />
              </Tag>
            );
          })}
        </div>
      )}
      {children}
    </div>
  );
}
