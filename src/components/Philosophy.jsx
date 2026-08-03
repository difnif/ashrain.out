// ashrain.out — 교육철학 (v1.0)
// 애쉬레인의 수학 교습 방식이 어떤 학문적 전통 위에 서 있는지 — 학자·사상·문헌.
// 초상: 위키미디어 공용(퍼블릭 도메인) 링크, 로드 실패 시 이니셜로 대체.
import { useState } from "react";

const CSS = `
.ph-root { min-height: 100vh; padding: 26px 14px 70px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.ph-light { background:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0D9488; --in:#F4F6F8; }
.ph-dark  { background:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#5EEAD4; --in:#101116; }
.ph-wrap { max-width: 680px; margin: 0 auto; }
.ph-eyebrow { font-size: 11px; letter-spacing: 3px; color: var(--ac); font-weight: 800; margin: 0 0 6px; text-align: center; }
.ph-h1 { color: var(--ink); font-size: 24px; font-weight: 800; margin: 0 0 10px; text-align: center; }
.ph-intro { color: var(--ink); font-size: 14.5px; line-height: 1.8; margin: 0 0 8px; }
.ph-pillars { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 16px 0 30px; }
@media (max-width: 480px) { .ph-pillars { grid-template-columns: 1fr; } }
.ph-pillar { background: var(--card); border: 1px solid var(--bd); border-radius: 12px; padding: 12px 13px; }
.ph-pillar b { display: block; color: var(--ac); font-size: 13px; margin-bottom: 4px; }
.ph-pillar span { color: var(--ink); font-size: 12.5px; line-height: 1.6; }
.ph-sec { font-size: 12px; letter-spacing: 2px; color: var(--mut); font-weight: 800; margin: 34px 0 14px; text-align: center; }
.ph-card { background: var(--card); border: 1px solid var(--bd); border-radius: 16px; padding: 18px; margin-bottom: 16px; }
.ph-top { display: flex; gap: 14px; align-items: center; margin-bottom: 12px; }
.ph-ava { position: relative; width: 74px; height: 74px; border-radius: 14px; overflow: hidden; flex-shrink: 0;
  background: var(--in); border: 1px solid var(--bd); display: flex; align-items: center; justify-content: center; }
.ph-ava span { font-size: 26px; font-weight: 800; color: var(--mut); font-family: Georgia, serif; }
.ph-ava img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.ph-name { color: var(--ink); font-size: 17px; font-weight: 800; margin: 0; }
.ph-years { color: var(--mut); font-size: 12px; margin: 2px 0 0; }
.ph-tag { color: var(--ac); font-size: 12.5px; font-weight: 700; margin: 4px 0 0; }
.ph-p { color: var(--ink); font-size: 13.5px; line-height: 1.85; margin: 0 0 10px; }
.ph-ash { background: var(--in); border-left: 3px solid var(--ac); border-radius: 8px;
  padding: 10px 12px; margin: 12px 0 10px; }
.ph-ash b { color: var(--ac); font-size: 12px; letter-spacing: 1px; display: block; margin-bottom: 4px; }
.ph-ash p { color: var(--ink); font-size: 13px; line-height: 1.75; margin: 0; }
.ph-refs { border-top: 1px dashed var(--bd); padding-top: 8px; margin-top: 4px; }
.ph-refs p { color: var(--mut); font-size: 11.5px; line-height: 1.7; margin: 0; }
.ph-book { background: var(--card); border: 1px solid var(--bd); border-radius: 12px; padding: 13px 15px; margin-bottom: 10px; }
.ph-book b { color: var(--ink); font-size: 13.5px; }
.ph-book p { color: var(--mut); font-size: 12.5px; line-height: 1.7; margin: 4px 0 0; }
.ph-foot { color: var(--mut); font-size: 12px; text-align: center; margin-top: 30px; line-height: 1.8; }
.ph-back { display: block; margin: 26px auto 0; background: var(--ac); border: none; border-radius: 999px;
  color: #fff; font-size: 13.5px; font-weight: 800; padding: 11px 26px; cursor: pointer; }
.ph-dark .ph-back { color: #0B0C0F; }
`;

const W = "https://upload.wikimedia.org/wikipedia/commons/";
const SCHOLARS = [
  {
    id: "euclid", name: "유클리드 (Euclid)", years: "기원전 300년경 · 알렉산드리아",
    initial: "E", img: W + "3/3a/Euklid-von-Alexandria_1.jpg",
    tag: "기하는 '거리'에서 시작된다 — 자취(locus)의 관점",
    body: [
      "유클리드의 『원론(Elements)』은 2,300년 동안 수학 교과서의 원형이었어요. 그 출발점은 소박합니다 — 점, 선, 그리고 \"두 점 사이의 가장 짧은 길\"이라는 거리 감각. 원은 처음부터 '한 점에서 같은 거리에 있는 점들의 모임'으로 정의됩니다. 도형이 먼저 있고 성질을 찾는 게 아니라, 조건(거리)이 먼저 있고 도형이 그 결과로 태어나는 거예요.",
      "이 '조건이 만드는 도형' — 자취(locus)의 관점은 아폴로니우스의 원뿔곡선으로 이어집니다. 두 점까지 거리의 합이 일정하면 타원, 차가 일정하면 쌍곡선. 외심이 '세 꼭짓점에서 같은 거리인 점'인 것도 정확히 같은 문법이죠.",
    ],
    ash: "애쉬레인이 외심·내심을 '거리가 일정한 점'으로, 원과 타원을 '등거리 조건의 형제'로 잇고, 기하 개념마다 \"이 조건이 어떤 도형을 낳는가\"를 묻는 이유가 여기에 있습니다. 중2 외심이 고등 원의 방정식·이차곡선으로 이어지는 예습 포인트의 뼈대예요.",
    refs: "유클리드, 『원론』 (Thomas Heath 영역 The Thirteen Books of Euclid's Elements; 국내: 이무현 역 『기하학 원론』, 교우사)",
  },
  {
    id: "descartes", name: "르네 데카르트 (René Descartes)", years: "1596–1650 · 프랑스",
    initial: "D", img: W + "7/73/Frans_Hals_-_Portret_van_Ren%C3%A9_Descartes.jpg",
    tag: "기하를 대수로, 대수를 기하로 — 두 세계의 번역",
    body: [
      "1637년 『방법서설』의 부록 「기하학(La Géométrie)」에서 데카르트는 좌표라는 다리를 놓았습니다. 점은 수의 쌍이 되고, 곡선은 방정식이 되고, 도형 문제는 계산 문제가 됩니다 — 해석기하학의 탄생이에요.",
      "이 번역은 양방향입니다. 방정식을 그림으로 '보고', 그림을 식으로 '계산'하는 것. 점·선·면이 상수항·1차·2차와 짝을 이루고, 연립방정식의 해가 두 직선의 교점으로 보이는 순간 — 대수와 기하는 한 언어의 두 방언이 됩니다.",
    ],
    ash: "복습 포인트 III(기하↔대수 다리)가 바로 데카르트 프로그램입니다. 1학기 대수를 2학기 기하로 다시 읽고, 기하 조건을 식으로 번역하는 훈련 — 좌표평면(중1)이 함수(중2)로, 함수가 도형의 방정식(고등)으로 이어지는 서사의 설계자예요.",
    refs: "R. Descartes, La Géométrie (1637); 국내: 『방법서설·정신지도규칙』(문예출판사 등) — 기하학 부록 해설은 수학사 개론서 참조",
  },
  {
    id: "hankel", name: "헤르만 한켈 (Hermann Hankel)", years: "1839–1873 · 독일",
    initial: "H", img: W + "9/9c/Hermann_Hankel.jpg",
    tag: "음수 × 음수 = 양수인 진짜 이유 — 형식 불역의 원리",
    body: [
      "\"음수 곱하기 음수는 왜 양수인가\"에 수학이 내놓은 공식 답변이 한켈의 형식 불역의 원리(1867)입니다. 새로운 수(음수)를 들여올 때, 기존 수에서 성립하던 계산 법칙(분배법칙 등)이 그대로 유지되도록 규칙을 정한다 — 그러면 (-1)×(-1)=+1은 선택이 아니라 필연이 됩니다.",
      "기하적으로 보면 더 선명해요. ×(-1)은 수직선에서 방향을 180° 뒤집는 일이고, 두 번 뒤집으면 제자리 — '반대의 반대'죠. 이 회전 해석은 아르강과 가우스의 복소평면에서 완성되어, i가 90° 회전이라는 놀라운 그림으로 이어집니다.",
    ],
    ash: "애쉬레인이 +·-를 '크기'가 아니라 방향으로 가르치는 근거입니다. 양수는 굳이 +가 필요 없는 자연스러운 세기의 수, -는 시계 반대 방향 같은 '반대 방향' 표시. 음×음=양은 외울 규칙이 아니라 반대의 반대라는 당연한 사건이 됩니다.",
    refs: "H. Hankel, Theorie der complexen Zahlensysteme (1867); A. Martínez, Negative Math (Princeton, 2005) — 음수 규칙의 역사와 대안 탐구",
  },
  {
    id: "klein", name: "펠릭스 클라인 (Felix Klein)", years: "1849–1925 · 독일",
    initial: "K", img: W + "0/06/Felix_Klein.jpeg",
    tag: "수학은 '변환'의 학문 — 에를랑겐 프로그램",
    body: [
      "1872년, 23세의 클라인은 에를랑겐 대학 취임 강연에서 선언합니다 — 기하학이란 어떤 변환을 해도 변하지 않는 성질을 연구하는 학문이다. 평행이동·회전·확대 같은 변환의 무리를 정하면, 그때마다 하나의 기하학이 태어난다는 것. 수학을 '대상'이 아니라 '움직임'으로 보는 혁명이었어요.",
      "클라인은 교육자로서도 거인입니다. 『고급 관점에서 본 초등수학』에서 그는 대학 수학의 눈으로 학교 수학을 다시 비추면, 학교에서 배우는 규칙들의 '진짜 이유'가 보인다고 역설했습니다 — 이 책의 정신이 곧 '근본 설명'입니다.",
    ],
    ash: "부등식에서 상수항을 더하면 범위가 수평이동하고, 계수를 곱하면 범위가 늘어난다 — 경계값의 이동과 거리로 부등식을 읽는 애쉬레인의 방식이 정확히 변환의 관점입니다. 이 감각이 함수의 평행이동으로, 다시 벡터로 이어지도록 복습·예습 포인트를 설계합니다. '대학 수준이다 싶을 만큼 자세한 설명'의 원전이 바로 클라인이에요.",
    refs: "F. Klein, Elementarmathematik vom höheren Standpunkte aus (1908) — 국내: 『고급 관점에서 본 초등수학』; 에를랑겐 프로그램(1872) 해설: 수학사 개론서",
  },
  {
    id: "freudenthal", name: "한스 프로이덴탈 (Hans Freudenthal)", years: "1905–1990 · 네덜란드",
    initial: "F", img: W + "2/2d/Hans_Freudenthal.jpg",
    tag: "개념이 태어난 자리에서 가르치기 — 교수학적 현상학",
    body: [
      "프로이덴탈은 \"수학은 완성된 체계가 아니라 인간의 활동\"이라고 선언한 수학교육학의 아버지입니다. 그의 교수학적 현상학은 묻습니다 — 이 개념은 어떤 현상을 정리하려고 태어났는가? 그 발생의 자리에서 출발할 때 학생은 개념을 '재발명'하며 배웁니다.",
      "그가 세운 현실주의 수학교육(RME)은 네덜란드를 넘어 세계 교육과정에 스며들었습니다. 핵심은 '현실'이 꼭 일상 소재라는 뜻이 아니라, 학생에게 실감 나는 맥락이라는 것 — 용어의 어원, 이름이 붙은 이유, 기호가 그렇게 생긴 사연도 훌륭한 현실입니다.",
    ],
    ash: "약수(約數)를 '실로 묶어 줄이는' 그림에서 시작하고, 소수(素數)를 '물들이기 전 흰 실'로 만나고, '왜 이 이름일까' 패널을 모든 개념에 붙이는 것 — 애쉬레인의 용어 분해 교습이 프로이덴탈의 노선입니다. 개념의 탄생 설화를 알면, 공식은 암기가 아니라 재발견이 됩니다.",
    refs: "H. Freudenthal, Didactical Phenomenology of Mathematical Structures (1983); Mathematics as an Educational Task (1973)",
  },
  {
    id: "skemp", name: "리처드 스켐프 (Richard Skemp)", years: "1919–1995 · 영국",
    initial: "S", img: null,
    tag: "'어떻게'가 아니라 '왜' — 관계적 이해",
    body: [
      "스켐프는 이해를 두 종류로 갈랐습니다. 도구적 이해 — 규칙을 알고 쓸 줄 아는 것('음수끼리 곱하면 양수'). 관계적 이해 — 왜 그런지, 다른 개념과 어떻게 이어지는지 아는 것. 도구적 이해는 빠르지만 부서지기 쉽고, 관계적 이해는 느리지만 새로운 문제 앞에서 스스로 길을 냅니다.",
      "그의 통찰 중 뼈아픈 대목 — 시험은 도구적 이해만으로도 통과할 수 있어서, 학교는 종종 빠른 길을 택한다는 것. 하지만 하위권 학생일수록 '왜'가 빠진 규칙 더미에 먼저 깔립니다. 관계의 그물이 있어야 규칙이 걸릴 자리가 생겨요.",
    ],
    ash: "\"수학적으로 오류만 아니라면 근본 설명을 최대한 자세히 — 빼는 건 쉽다\"는 애쉬레인의 원칙이 스켐프의 답입니다. 1이 소수가 아닌 진짜 이유(유일성 보호), 계수가 '개수'가 아닌 이유까지 내려가는 설명은 사치가 아니라, 하위권 학생에게 더 필요한 안전망입니다.",
    refs: "R. Skemp, \"Relational Understanding and Instrumental Understanding\" (Mathematics Teaching 77, 1976); 『수학학습심리학』(The Psychology of Learning Mathematics, 국내 번역본)",
  },
];

const BOOKS = [
  ["폴 록하트, 『Measurement』 (Harvard, 2012)", "자·컴퍼스가 아니라 '측정과 거리'라는 물음에서 기하 전체를 다시 짓는 책. 애쉬레인의 '거리에서 출발하는 기하' 서사와 가장 가까운 현대 저작."],
  ["알베르토 마르티네스, 『Negative Math』 (Princeton, 2005)", "음수 규칙이 하늘에서 떨어진 게 아니라 역사 속 선택이었음을 보여주는 책 — '방향으로서의 음수'를 더 깊이 파고들 때."],
  ["펠릭스 클라인, 『고급 관점에서 본 초등수학』", "학교 수학의 모든 규칙 뒤에 있는 대학 수학의 풍경. '너무 자세하다 싶은 설명'의 교과서."],
  ["대한수학회 수학용어집 (온라인)", "우리말 수학 용어의 공식 표준. 용어의 유래를 추적할 때의 출발점 — 상당수가 메이지 시대 일본 번역어를 거쳐 정착했습니다."],
];

export default function Philosophy({ theme = "light" }) {
  return (
    <div className={`ph-root ph-${theme}`}>
      <style>{CSS}</style>
      <div className="ph-wrap">
        <p className="ph-eyebrow">ASHRAIN.OUT</p>
        <h1 className="ph-h1">교육철학 — 왜 이렇게 가르치는가</h1>
        <p className="ph-intro">
          애쉬레인의 설명 방식은 취향이 아니라 전통 위에 서 있습니다. 용어를 글자까지 뜯어보고,
          부호를 방향으로 읽고, 부등식을 경계값의 이동으로 보고, 기하를 거리에서 다시 짓는 것 —
          아래 학자들이 먼저 걸어간 길입니다. 우리는 그 길을 하위권 학생의 보폭에 맞게 다시 놓을 뿐입니다.
        </p>
        <div className="ph-pillars">
          <div className="ph-pillar"><b>① 용어의 뿌리</b><span>한자 파자와 영어 어원에서 개념의 정체를 만난다</span></div>
          <div className="ph-pillar"><b>② 방향과 변환</b><span>부호는 방향, 식의 변화는 이동과 늘림으로 읽는다</span></div>
          <div className="ph-pillar"><b>③ 경계값과 검산</b><span>경계를 대입해 스스로 확인하는 습관을 심는다</span></div>
          <div className="ph-pillar"><b>④ 거리의 기하</b><span>도형은 조건(거리)이 낳은 자취로 이해한다</span></div>
        </div>

        <p className="ph-sec">— 이 길을 먼저 걸은 사람들 —</p>
        {SCHOLARS.map((s) => (
          <div key={s.id} className="ph-card">
            <div className="ph-top">
              <div className="ph-ava">
                <span>{s.initial}</span>
                {s.img && <img src={s.img} alt={s.name} loading="lazy"
                  onError={(e) => { e.currentTarget.style.display = "none"; }} />}
              </div>
              <div>
                <p className="ph-name">{s.name}</p>
                <p className="ph-years">{s.years}</p>
                <p className="ph-tag">{s.tag}</p>
              </div>
            </div>
            {s.body.map((p, i) => <p key={i} className="ph-p">{p}</p>)}
            <div className="ph-ash"><b>애쉬레인에서는</b><p>{s.ash}</p></div>
            <div className="ph-refs"><p>📚 {s.refs}</p></div>
          </div>
        ))}

        <p className="ph-sec">— 더 읽어볼 문헌 —</p>
        {BOOKS.map(([t, d], i) => (
          <div key={i} className="ph-book"><b>{t}</b><p>{d}</p></div>
        ))}

        <p className="ph-foot">
          이 페이지는 계속 자랍니다 — 복습과 시험 훈련 편이 더해질 예정이에요.<br />
          학자 초상: Wikimedia Commons (퍼블릭 도메인).
        </p>
        <button className="ph-back" onClick={() => (location.hash = "")}>홈으로 돌아가기</button>
      </div>
    </div>
  );
}
