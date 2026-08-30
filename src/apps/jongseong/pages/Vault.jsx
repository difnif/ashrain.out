// 녹음 창고 — 관리자 전용(추후). 상담·안내 녹음 같은 음성 자산 보관처를 종성에 둔다.
import { Page, Card, Row, Chip } from "../../../shared/demo";

export default function Vault({ isAdmin }) {
  if (!isAdmin) return (
    <Page title="녹음 창고">
      <Card><p className="d-note">관리자 전용 공간이에요.</p></Card>
    </Page>
  );
  return (
    <Page title="녹음 창고" right={<Chip tone="warn">관리자</Chip>}>
      <Card title="올리기">
        <div className="d-vault" style={{ textAlign: "center", padding: "24px 12px" }}>
          <p className="d-main" style={{ marginBottom: 4 }}>녹음 파일 올리기</p>
          <p className="d-sub">MP3 · M4A — 태그(상담·안내·행사)와 함께 보관</p>
        </div>
      </Card>
      <Card title="보관 중">
        <Row main="(비어 있음)" sub="업로드 연결은 추후 — Supabase Storage 버킷 예정" />
      </Card>
    </Page>
  );
}
