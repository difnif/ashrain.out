// 서무 2 — 문제 표시 습관 (표시 연습 기획 채팅 합의 반영)
// M코드 레지스트리 v0: 기호는 스킨, 데이터는 의미 코드. 템플릿 토큰 앵커링 · 구간형/지점형 구분.
// v1 입력은 탭 기반(분절→선택→팔레트) — 자유 드로잉은 상위 버전. 미결 3: 매핑 확정·입력 방식·채점 관대함.
import { Card, Row, Chip } from "../../../shared/demo";

const M = [
  ["M-01", "동그라미", "구하는 것", "구간"],
  ["M-02", "네모", "주어진 대상·값", "구간"],
  ["M-03", "밑줄", "조건", "구간"],
  ["M-04", "겹밑줄", "놓치면 틀리는 핵심 조건", "구간"],
  ["M-05", "물결", "함정 어휘 (서로 다른·자연수·이상/초과)", "구간"],
  ["M-06", "빗금", "단서 경계 · 흐름 전환점", "지점"],
];

export default function Marking() {
  return (
    <>
      <Card title="표시 미리보기 — 내 관습이 곧 레지스트리">
        <p style={{ fontSize: 14, lineHeight: 2.1, margin: 0 }}>
          <span style={{ textDecoration: "underline wavy var(--down)" }}>서로 다른</span>{" "}
          <span style={{ border: "1.5px solid var(--ac2)", borderRadius: 4, padding: "0 3px" }}>두 자연수 x, y</span>
          에 대하여 <span style={{ borderBottom: "2px solid var(--ink)" }}>x + y = 10</span> 일 때,
          <span style={{ color: "var(--mut)", fontWeight: 800 }}> ╱ </span>
          <span style={{ border: "1.5px solid var(--ac)", borderRadius: 999, padding: "0 6px" }}>xy의 최댓값</span>을 구하시오.
        </p>
      </Card>
      <Card title="M코드 레지스트리 v0">
        {M.map(([c, n, m, k]) => (
          <Row key={c} main={c + " " + n} sub={m} right={<Chip tone={k === "지점" ? "warn" : ""}>{k}형</Chip>} />
        ))}
      </Card>
      <p className="d-note">여기 남는 내 표시가 곧 시범 표시의 원판이 돼요 — 학생 연습 모드(시범/연습 오버레이 디프)는 학생앱 몫. G코드(도형)와 한 언어의 두 방언.</p>
    </>
  );
}
