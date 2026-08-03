// ashrain.out — 홈 대시보드 (v1.0)
// 시간대별 히어로 인사 + 활동 대시보드(현재 데모 데이터) + 교육철학 카드
// 개념 트리는 #/learn (개념 학습)으로 분리
import { useEffect, useState } from "react";
import { supabase } from "../supabaseClient";

const CSS = `
.hd-root { min-height: 100vh; padding: 16px 14px 60px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.hd-root * { box-sizing: border-box; }
.hd-light { background:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0D9488; --in:#F4F6F8; }
.hd-dark  { background:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#5EEAD4; --in:#101116; }
.hd-wrap { max-width: 680px; margin: 0 auto; }
.hd-btns { display: flex; gap: 7px; flex-wrap: wrap; margin-bottom: 14px; align-items: center; }
.hd-logo { height: 30px; margin-right: 2px; }
.hd-btn { background: var(--card); border: 1px solid var(--bd); border-radius: 999px; color: var(--ink);
  font-size: 12px; font-weight: 700; padding: 8px 12px; cursor: pointer; }
.hd-hero { position: relative; border-radius: 20px; padding: 26px 22px 22px; color: #fff;
  overflow: hidden; margin-bottom: 14px; box-shadow: 0 6px 22px rgba(0,0,0,.14); }
.hd-hero-hi { font-size: 14px; opacity: .92; margin: 0; font-weight: 600; }
.hd-hero-nick { font-size: 26px; font-weight: 800; margin: 4px 0 10px; }
.hd-hero-greet { font-size: 16.5px; font-weight: 700; margin: 0; line-height: 1.55; }
.hd-hero-time { position: absolute; right: 18px; bottom: 14px; font-size: 11.5px; opacity: .8; }
.hd-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
@media (max-width: 480px) { .hd-grid { grid-template-columns: 1fr; } }
.hd-card { background: var(--card); border: 1px solid var(--bd); border-radius: 14px; padding: 14px 15px;
  position: relative; }
.hd-card.wide { grid-column: 1 / -1; }
.hd-t { font-size: 12px; font-weight: 800; color: var(--mut); letter-spacing: .5px; margin: 0 0 8px; }
.hd-big { font-size: 20px; font-weight: 800; color: var(--ink); margin: 0; }
.hd-sub { font-size: 12px; color: var(--mut); margin: 4px 0 0; line-height: 1.6; }
.hd-bar { height: 8px; background: var(--in); border-radius: 999px; overflow: hidden; margin: 10px 0 6px; }
.hd-bar > div { height: 100%; background: var(--ac); border-radius: 999px; }
.hd-go { display: inline-block; margin-top: 10px; background: transparent; border: 1.5px solid var(--ac);
  border-radius: 999px; color: var(--ac); font-size: 12px; font-weight: 800; padding: 7px 13px; cursor: pointer; }
.hd-demo { position: absolute; top: 10px; right: 12px; font-size: 9.5px; font-weight: 800;
  color: var(--mut); border: 1px solid var(--bd); border-radius: 5px; padding: 1px 5px; opacity: .8; }
.hd-week { display: flex; align-items: flex-end; gap: 6px; height: 64px; margin-top: 8px; }
.hd-wcol { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.hd-wbar { width: 100%; background: var(--ac); border-radius: 5px 5px 2px 2px; opacity: .85; }
.hd-wlab { font-size: 10px; color: var(--mut); }
.hd-philo { grid-column: 1 / -1; position: relative; border-radius: 16px; overflow: hidden; cursor: pointer;
  background: linear-gradient(120deg, #14343B 0%, #0D9488 130%); color: #fff; padding: 20px 130px 20px 20px;
  min-height: 108px; border: none; text-align: left; }
.hd-philo-eyebrow { font-size: 10.5px; letter-spacing: 2.5px; opacity: .85; margin: 0 0 6px; font-weight: 800; }
.hd-philo-t { font-size: 17px; font-weight: 800; margin: 0 0 6px; }
.hd-philo-d { font-size: 12px; opacity: .9; margin: 0; line-height: 1.6; }
.hd-philo-img { position: absolute; right: -6px; top: 0; bottom: 0; width: 120px; object-fit: cover;
  object-position: center top; opacity: .9; mask-image: linear-gradient(to right, transparent, #000 30%);
  -webkit-mask-image: linear-gradient(to right, transparent, #000 30%); }
.hd-philo-arrow { position: absolute; right: 12px; bottom: 10px; font-size: 16px; }
.hd-note { text-align: center; color: var(--mut); font-size: 11px; margin-top: 16px; line-height: 1.7; }
`;

const GREETS = [
  "저는 안녕 안 해요 😌", "복습은 하셨나요?", "오답노트, 열어봤나요?", "어제 배운 거 한 줄로 말해볼래요?",
  "오늘도 반가워요!", "어서 오세요 😊", "수학할 준비 됐나요?", "차근차근 가 봅시다",
  "꾸준함이 재능을 이겨요", "한 문제만 풀고 가도 성공!", "오늘의 공부, 시작해볼까요?", "숙제 먼저, 딴짓은 나중에!",
  "돌아온 걸 환영해요", "개념이 무기예요 🗡️", "궁금하면 물음표를 눌러요", "틀린 문제가 진짜 선생님이에요",
  "딱 5분만 집중해볼까요?", "어려우면 천천히 — 대신 멈추진 말기", "오늘 컨디션은 어때요?", "수학은 눈으로 말고 손으로!",
  "공식보다 '이유'를 기억해요", "지난 시험 오답, 다시 봤나요?", "작은 성공을 쌓는 중이에요", "포기만 안 하면 이기는 게임",
  "머리 말고 엉덩이로 공부하는 거예요", "오늘도 한 칸 성장 🌱", "모르는 건 부끄러운 게 아니에요", "쉬는 것도 공부의 일부예요",
  "계산 실수, 오늘은 꼭 잡아봅시다", "시작이 반 — 접속했으니 벌써 4분의 1!",
];

const skyOf = (h) =>
  h < 6  ? ["linear-gradient(135deg,#1b2440 0%,#3b2f63 100%)", "고요한 새벽이에요"] :
  h < 11 ? ["linear-gradient(135deg,#2193b0 0%,#6dd5ed 100%)", "좋은 아침이에요"] :
  h < 17 ? ["linear-gradient(135deg,#0d9488 0%,#34d399 100%)", "활기찬 오후예요"] :
  h < 20 ? ["linear-gradient(135deg,#ee9ca7 0%,#b06ab3 100%)", "노을 지는 저녁이에요"] :
           ["linear-gradient(135deg,#141e30 0%,#243b55 100%)", "차분한 밤이에요"];

export default function HomeDash({ theme = "light", onToggleTheme }) {
  const [nick, setNick] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const [greet] = useState(() => GREETS[Math.floor(Math.random() * GREETS.length)]);
  const now = new Date();
  const [sky, hi] = skyOf(now.getHours());

  useEffect(() => {
    supabase.auth.getUser().then(async ({ data }) => {
      const u = data?.user; if (!u) return;
      const { data: p } = await supabase.from("profiles").select("username, role").eq("id", u.id).maybeSingle();
      setNick(p?.username || ""); setIsAdmin(p?.role === "admin");
    });
  }, []);

  const week = [35, 55, 20, 70, 45, 85, 30]; // 데모: 요일별 학습(분)
  const days = ["월", "화", "수", "목", "금", "토", "일"];

  return (
    <div className={`hd-root hd-${theme}`}>
      <style>{CSS}</style>
      <div className="hd-wrap">
        <div className="hd-btns">
          <img className="hd-logo" src="/brand/ashrain_logo.png" alt="ashrain" />
          {isAdmin && <button className="hd-btn" onClick={() => (location.hash = "#/admin/concepts")}>📚 개념 등록</button>}
          {isAdmin && <button className="hd-btn" onClick={() => (location.hash = "#/admin/qna")}>💬 질문 검토</button>}
          {isAdmin && <button className="hd-btn" onClick={() => (location.hash = "#/admin/chats")}>🗂 질문대화</button>}
          {isAdmin && <button className="hd-btn" onClick={() => (location.hash = "#/admin/images")}>🖼 이미지 현황</button>}
          <button className="hd-btn" onClick={() => (location.hash = "#/board")}>📋 질문게시판</button>
          <button className="hd-btn" onClick={() => (location.hash = "#/me")}>👤 마이페이지</button>
          {onToggleTheme && <button className="hd-btn" onClick={onToggleTheme}>{theme === "dark" ? "☀️" : "🌙"}</button>}
          <a className="hd-btn" style={{ textDecoration: "none", display: "flex", alignItems: "center", gap: 5 }}
            href="https://www.instagram.com/ashrain.out" target="_blank" rel="noreferrer" title="앱 문의 (인스타그램 DM)">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="18" height="18" rx="5.2" /><circle cx="12" cy="12" r="4.2" />
              <circle cx="17.3" cy="6.7" r="1.15" fill="currentColor" stroke="none" />
            </svg> 문의
          </a>
        </div>

        <div className="hd-hero" style={{ background: sky }}>
          <p className="hd-hero-hi">{hi}</p>
          <p className="hd-hero-nick">{nick || "친구"}님</p>
          <p className="hd-hero-greet">“{greet}”</p>
          <span className="hd-hero-time">{now.getMonth() + 1}월 {now.getDate()}일 · {days[(now.getDay() + 6) % 7]}요일</span>
        </div>

        <div className="hd-grid">
          <div className="hd-card wide">
            <span className="hd-demo">DEMO</span>
            <p className="hd-t">▶ 이어서 학습</p>
            <p className="hd-big">A01 · 소수와 합성수</p>
            <div className="hd-bar"><div style={{ width: "60%" }} /></div>
            <p className="hd-sub">단락 3/5 읽음 · 어제 저녁에 보다 멈췄어요</p>
            <button className="hd-go" onClick={() => (location.hash = "#/c/m1-1-01")}>이어보기 →</button>
          </div>

          <div className="hd-card">
            <span className="hd-demo">DEMO</span>
            <p className="hd-t">🔥 연속 출석</p>
            <p className="hd-big">12일째</p>
            <p className="hd-sub">이번 주 5일 접속 — 최고 기록까지 3일!</p>
          </div>

          <div className="hd-card">
            <span className="hd-demo">DEMO</span>
            <p className="hd-t">📕 오답노트</p>
            <p className="hd-big">미복습 4문제</p>
            <p className="hd-sub">정수와 유리수 2 · 소인수분해 2</p>
          </div>

          <div className="hd-card wide">
            <span className="hd-demo">DEMO</span>
            <p className="hd-t">📈 이번 주 학습 시간 <span style={{ fontWeight: 600 }}>· 합계 5시간 40분</span></p>
            <div className="hd-week">
              {week.map((v, i) => (
                <div key={i} className="hd-wcol">
                  <div className="hd-wbar" style={{ height: `${v}%`, opacity: i === (now.getDay() + 6) % 7 ? 1 : 0.5 }} />
                  <span className="hd-wlab">{days[i]}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="hd-card">
            <span className="hd-demo">DEMO</span>
            <p className="hd-t">⚡ 연산 스피드</p>
            <p className="hd-big">92점 · 4분 12초</p>
            <p className="hd-sub">지난 기록보다 38초 빨라졌어요</p>
          </div>

          <div className="hd-card">
            <span className="hd-demo">DEMO</span>
            <p className="hd-t">💬 내 질문</p>
            <p className="hd-big">답변 완료 1건</p>
            <p className="hd-sub">A01-1 약수 질문에 답이 달렸어요</p>
            <button className="hd-go" onClick={() => (location.hash = "#/board")}>보러 가기 →</button>
          </div>

          <div className="hd-card wide" style={{ padding: 0, border: "none", background: "transparent" }}>
            <button className="hd-btn" style={{ width: "100%", padding: "16px 0", fontSize: 15, fontWeight: 800, borderRadius: 14 }}
              onClick={() => (location.hash = "#/learn")}>
              📚 개념 학습 목록 열기
            </button>
          </div>

          <button className="hd-philo" onClick={() => (location.hash = "#/philosophy")}>
            <p className="hd-philo-eyebrow">ASHRAIN PHILOSOPHY</p>
            <p className="hd-philo-t">우리가 이렇게 가르치는 이유</p>
            <p className="hd-philo-d">유클리드에서 프로이덴탈까지 —<br />아쉬레인 설명 방식의 뿌리를 소개합니다</p>
            <img className="hd-philo-img" alt=""
              src="https://upload.wikimedia.org/wikipedia/commons/7/73/Frans_Hals_-_Portret_van_Ren%C3%A9_Descartes.jpg"
              onError={(e) => { e.currentTarget.style.display = "none"; }} />
            <span className="hd-philo-arrow">→</span>
          </button>
        </div>

        <p className="hd-note">대시보드 수치는 데모예요 — 활동 기록 기능이 연결되면 실제 데이터로 채워집니다.</p>
      </div>
    </div>
  );
}
