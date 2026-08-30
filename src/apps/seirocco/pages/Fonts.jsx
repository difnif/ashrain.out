// 폰트 창고 — 관리자 전용. 시록고는 기록하는 곳: UI 자산 중 서체 수집처를 여기 둔다.
// 실사용 폰트는 리포 public/fonts/ 커밋으로 적용(정적 서빙) — 창고는 수집·후보 보관(추후 Supabase Storage).
import { Page, Card, Row, Chip } from "../../../shared/demo";

export default function Fonts({ isAdmin }) {
  if (!isAdmin) return (
    <Page title="폰트 창고">
      <Card><p className="d-note">관리자 전용 공간이에요.</p></Card>
    </Page>
  );
  return (
    <Page title="폰트 창고" right={<Chip tone="warn">관리자</Chip>}>
      <Card title="적용 중">
        <Row main="EBS 훈민정음 새론체" sub="한글 UI 크롬 · public/fonts/EBSHunminjeongeumSaeronR" right={<Chip tone="ok">적용</Chip>} />
        <Row main="Tangerine" sub="영문 UI 크롬 · Google Fonts CDN" right={<Chip tone="ok">적용</Chip>} />
      </Card>
      <Card title="후보 보관">
        <div className="d-vault" style={{ textAlign: "center", padding: "24px 12px", marginBottom: 10 }}>
          <p className="d-main" style={{ marginBottom: 4 }}>폰트 파일 올리기</p>
          <p className="d-sub">TTF · OTF · WOFF2 — 라이선스 메모와 함께 보관</p>
        </div>
        <Row main="(비어 있음)" sub="후보를 모으고, 채택되면 public/fonts로 승격해요" />
      </Card>
      <p className="d-note">교육 자료는 전부 학생앱 관리자 도구에 — 여긴 UI 자산만. 관리자 화면 피로 분담.</p>
    </Page>
  );
}
