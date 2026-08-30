// src/shared/spaces/Haso.jsx — 하소 (공통 공간 · 자유+상담 게시판)
// 세 앱이 공유하는 광장 1. 익명끼리 고민을 나눈다.
// 경제: 글 올리기 = '연'을 날려 보내는 것(연 소모). 마음 맞으면 전서구로 채팅을 연다(30일 후 자동 소멸).
import { Page, Card, Row, Chip } from "../demo";

const POSTS = [
  { t: "중2 아이, 요즘 말수가 줄었어요", s: "익명 · 연 12개 받음 · 어제", gate: "기본", tone: "" },
  { t: "시험 전날 뭐라고 말해주는 게 좋을까요", s: "익명 · 연 31개 받음 · 2일 전", gate: "2급 이상", tone: "warn" },
  { t: "혼자 공부 시간, 어디까지 믿고 둬야 하나", s: "익명 · 연 8개 받음 · 3일 전", gate: "기본", tone: "" },
];

export default function Haso() {
  return (
    <Page title="하소">
      <Card title="연 날리기">
        <p className="d-note" style={{ marginBottom: 10 }}>고민을 적어 연에 실어 보내요 — 글 한 편에 연 1개가 들어요. 연은 '글 읽는 소리'에서 글을 쓰면 쌓여요.</p>
        <textarea className="d-in" placeholder="익명으로 날아가요. 아이 실명·학교명은 적지 말아주세요." />
        <div style={{ display: "flex", gap: 8, marginTop: 8, alignItems: "center" }}>
          <Chip tone="ac">보유 연 3</Chip><span className="d-sp" />
          <button className="d-btn pri">연 날리기 (연 1 소모)</button>
        </div>
      </Card>
      <Card title="날아든 연">
        {POSTS.map((p, i) => (
          <Row key={i} main={p.t} sub={p.s}
            right={<span style={{ display: "flex", gap: 6 }}>
              <Chip tone={p.tone}>{p.gate}</Chip>
              <button className="d-btn" style={{ padding: "5px 9px" }}>전서구</button>
            </span>} />
        ))}
      </Card>
      <p className="d-note">전서구 칩은 그 유저가 받는 최소 등급이에요 — 과한 상담 요청을 막는 문턱. 열린 대화방은 30일 뒤 스스로 사라져요.</p>
    </Page>
  );
}
