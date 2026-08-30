// 백돌길 — 햇빛에 반사돼 반짝이는 길: 학생앱에서 파생된 것들이 떠오르는 공간
// 무엇이 올라올지는 미정 — 지금은 공간과 '전달·출제' 동작만.
import { Page, Card, Row, Chip } from "../../../shared/demo";

const ITEMS = [
  { t: "오늘 많이 풀린 문제", s: "일차함수 그래프 해석 · 학생 214명이 풀었어요", k: "문제" },
  { t: "이번 주 인기 개념 카드", s: "m2-2-05 연립방정식의 활용", k: "개념" },
  { t: "학생 신문에서 반짝인 글", s: "‘시험 전날의 마음가짐’ · 익명", k: "글" },
];

export default function Baekdol() {
  return (
    <Page title="백돌길">
      <p className="d-note">흰 돌길에 볕이 튀듯, 아이들 사이에서 반짝인 것들이 떠올라요. 마음에 드는 걸 자녀에게 건네보세요.</p>
      <Card>
        {ITEMS.map((it, i) => (
          <Row key={i} main={it.t} sub={it.s} right={
            <span style={{ display: "flex", gap: 6 }}>
              <Chip>{it.k}</Chip>
              <button className="d-btn" style={{ padding: "5px 9px" }}>전달</button>
              {it.k === "문제" && <button className="d-btn" style={{ padding: "5px 9px" }}>출제</button>}
            </span>} />
        ))}
      </Card>
    </Page>
  );
}
