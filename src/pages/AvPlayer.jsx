// 공부하기 › 시청각 학습 — 한 항목 보기 (#/av/<key>)
// 교실 모니터와 같은 무대(AdminDisplay 의 Stage)를 av 모드로 연다: 관리자 확인 없이, 처음부터 그 액자(또는 그 묶음의 수업 장면)로.
// 시그니처 프린트(#/av/cnt100:sel — sig)는 그 해설 액자를 그 세트로 열고, 본 기록을 프린트 key 로 남긴다(AdminDisplay 의 sigSeen).
// 목록은 lib/av.js · 공부하기 탭의 시청각 학습(Study.jsx AvSub).
import { Stage } from "./AdminDisplay";
import { AV_CATS, avItem } from "../lib/av";

export default function AvPlayer({ hash }) {
  const key = decodeURIComponent(String(hash || "").split("?")[0].replace(/^#\/av\/?/, "").split("/")[0] || "");
  const it = avItem(key);
  if (!it) { location.replace("#/study/av"); return null; }
  const cat = AV_CATS.find((c) => c.id === it.cat);
  return <Stage key={it.key} av={{ key: it.key, cat: it.cat, catTitle: cat?.title, frame: it.frame, grp: it.grp, title: it.title, set: it.set ?? null, level: it.level || null,
    sig: !!it.sig, n: it.n || 0 }} />;
}
