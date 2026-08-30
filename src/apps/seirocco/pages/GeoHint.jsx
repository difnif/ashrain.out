// 서무 3 — 도형 힌트 표시 습관 (도형 힌트 인수인계 v1.0 반영)
// 원칙: 힌트 = 해설지의 파생 뷰 · 무검토 · 침묵(4게이트) · 만족 대역 [10,50] · h2에서 절단.
// 입도 규칙: 병목이 '찾기'면 가리키고(G-01), '보기'면 주장하라(G-02/03).
import { Card, Row, Chip } from "../../../shared/demo";

const G = [
  ["G-01", "주목", "여길 봐", ""],
  ["G-02", "동일", "이 둘은 같다", ""],
  ["G-03", "관계", "한 규칙으로 묶인다", ""],
  ["G-04", "보조", "이걸 그어라 (고스트)", ""],
  ["G-05", "발췌", "부분 도형만 떼어 봐", "v2"],
  ["G-06", "추적", "이 순서로 따라가", "예약"],
];

export default function GeoHint() {
  return (
    <>
      <Card title="G코드 레지스트리 v0 — 도형의 의미 언어">
        {G.map(([c, n, m, v]) => (
          <Row key={c} main={c + " " + n} sub={m} right={v ? <Chip>{v}</Chip> : <Chip tone="ac">v1</Chip>} />
        ))}
      </Card>
      <Card title="내 표시 습관 → 구성 문법">
        <Row main="원주각 배치" sub="호를 먼저, 두 각을 결속 — 주장 수준(G-03)" right={<Chip tone="ok">문법화</Chip>} />
        <Row main="닮음 찾기 배치" sub="대응변을 그어주면 연습이 증발 — 가리킴 상한(G-01)" right={<Chip tone="ok">문법화</Chip>} />
        <Row main="입법 대기" sub="블랙리스트 v0 · claim 레지스트리 · 구성 문법 배치(회당 5~10) · p_target" right={<Chip tone="warn">Park</Chip>} />
      </Card>
      <p className="d-note">시선의 구조를 코드로 응고시키는 방 — 구성 라이브러리가 이 기능의 진짜 자산이에요. 학생 쪽 선예측 탭·오답 히트맵이 이 문법을 데이터로 되먹여요.</p>
    </>
  );
}
