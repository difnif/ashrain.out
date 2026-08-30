// 내 학생 — 계약 상태별 목록 (3층: 활성 계약 관계만 열람)
import { Page, Card, Row, Chip } from "../../../shared/demo";

const LIST = [
  { id: 1, name: "김하늘", g: "중2", sub: "오답 3건 새로 등록 · 어제", st: ["활성", "ok"] },
  { id: 2, name: "이도윤", g: "중1", sub: "스피드 연산 정답률 78% · 오늘", st: ["활성", "ok"] },
  { id: 3, name: "박서준", g: "고1", sub: "계약 제안 승인 대기", st: ["제안 중", "warn"] },
  { id: 4, name: "최유나", g: "중3", sub: "계약 종료 — 열람 차단됨", st: ["종료", ""] },
];

export default function Students() {
  return (
    <Page title="내 학생">
      <Card>
        {LIST.map((s) => (
          <Row key={s.id} main={s.name + " · " + s.g} sub={s.sub}
            right={<Chip tone={s.st[1]}>{s.st[0]}</Chip>}
            onClick={() => (location.hash = "#/students/" + s.id)} />
        ))}
      </Card>
      <p className="d-note">열람 권한은 신분이 아니라 관계에 붙어요 — 활성 계약이 있는 학생만 여기 보여요.</p>
    </Page>
  );
}
