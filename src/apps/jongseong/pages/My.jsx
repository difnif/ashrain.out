// 종성 마이페이지 — 계정 · 인연(자녀 등록 = 혈연)
import { Page, Card, Row, Chip } from "../../../shared/demo";
import Ties from "../../../shared/Ties";

export default function My() {
  return (
    <Page title="마이페이지">
      <Card title="계정">
        <Row main="박재우" sub="학부모" right={<Chip>학부모</Chip>} />
      </Card>
      <Ties emphasizeChild />
    </Page>
  );
}
