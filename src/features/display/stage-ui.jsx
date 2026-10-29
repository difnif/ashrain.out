// ashrain.out — 교실 모니터 무대 공용 부품 (stage-ui.jsx)
// 교실 모니터(AdminDisplay)와 컨셉 문제 해설 영상(pages/sets/SetVideo)이 같은 무대 · 조작 막대 · 단추 모양을 쓴다.
//   DSP_CSS — 16:9 무대 · 조작 막대(움직이면 뜨고 스스로 숨는다) · 목록 · 액자 카드
//   Btn · Ic · FrameIc — 조작 막대 단추와 아이콘

export function Btn({ title, on, onClick, disabled, children }) {
  return (
    <button type="button" className={"dsp-btn" + (on ? " on" : "")} title={title} aria-label={title} disabled={disabled}
      aria-pressed={on === undefined ? undefined : !!on} onClick={onClick}>{children}</button>
  );
}
/** 액자 모양(못에 걸린 그림틀 · 산과 해) */
export function FrameIc() {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth={1.9}
      strokeLinecap="round" strokeLinejoin="round">
      <path d="M8.6 7.2 12 3.6l3.4 3.6" />
      <circle cx="12" cy="3.4" r="0.9" fill="currentColor" stroke="none" />
      <rect x="3.2" y="7.2" width="17.6" height="13.4" rx="1.6" />
      <path d="M6.2 17.6l3.6-4.4 2.6 2.7 1.9-1.9 3.5 3.6" />
      <circle cx="15.6" cy="11" r="1.35" />
    </svg>
  );
}
export function Ic({ d, fill }) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" aria-hidden="true">
      <path d={d} fill={fill ? "currentColor" : "none"} stroke="currentColor" strokeWidth={fill ? 0 : 2.2}
        strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

const NOISE = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E\")";
export const DSP_CSS = `
@font-face { font-family: "EBS Hunminjeongeum Saeron"; font-weight: 400; font-display: swap;
  src: url("/fonts/EBSHunminjeongeumSaeronR.woff2") format("woff2"), url("/fonts/EBSHunminjeongeumSaeronR.ttf") format("truetype"); }
.dsp-root { position: fixed; inset: 0; z-index: 200; display: flex; align-items: center; justify-content: center;
  overflow: hidden; -webkit-user-select: none; user-select: none; touch-action: manipulation;
  font-family: 'Pretendard Variable', Pretendard, system-ui, sans-serif; }
.dsp-dark { background: #121a33; --ink: #F2E8D0; --soft: #B8B0A0; --chip: rgba(10,15,32,.62); --chipbd: rgba(242,232,208,.22);
  --e: #F2877B; --m: #6BD3C3; --gold: #F4C65A; --card: #1c2647; }
.dsp-light { background: #e9dec3; --ink: #3B3021; --soft: #7B6C55; --chip: rgba(255,251,241,.78); --chipbd: rgba(59,48,33,.22);
  --e: #C34E3E; --m: #13877A; --gold: #B37A0E; --card: #f6efdf; }
.dsp-idle { cursor: none; }
.dsp-frame { position: relative; width: min(100vw, calc(100vh * 16 / 9)); aspect-ratio: 16 / 9; container-type: inline-size; }
.dsp-paper { position: absolute; inset: -40vmax; pointer-events: none; }
.dsp-dark .dsp-paper { background: radial-gradient(70% 70% at 50% 40%, #2a3762 0%, #1c2647 55%, #121a33 100%); }
.dsp-light .dsp-paper { background: radial-gradient(70% 70% at 50% 35%, #fcf8ee 0%, #f3ead6 55%, #e6d9bb 100%); }
.dsp-paper::after { content: ""; position: absolute; inset: 0; opacity: .06; mix-blend-mode: overlay; background-image: ${NOISE}; }
.dsp-svg { position: absolute; inset: 0; width: 100%; height: 100%; display: block; overflow: visible; }
.dsp-svg text { font-kerning: normal; }

/* 오른쪽 위: 액자 단추 + 학년 토글 */
.dsp-tr { position: absolute; right: 2.6cqw; top: 2.4cqw; display: flex; align-items: center; gap: .9cqw; z-index: 5; }
.dsp-fbtn { width: 4.3cqw; height: 4.3cqw; padding: 0; border-radius: 999px; border: 1px solid var(--chipbd); background: var(--chip);
  color: var(--ink); display: grid; place-items: center; font-size: 2.15cqw; cursor: pointer; -webkit-tap-highlight-color: transparent;
  transition: color .25s, border-color .25s; }
.dsp-fbtn:hover { color: var(--gold); border-color: var(--gold); }

/* 학년 토글 */
.dsp-mode { position: relative; display: flex; background: var(--chip);
  border: 1px solid var(--chipbd); border-radius: 999px; padding: .35cqw; }
.dsp-mode button { position: relative; z-index: 1; border: 0; background: none; color: var(--soft); cursor: pointer;
  font: inherit; font-size: 1.62cqw; font-weight: 800; letter-spacing: .04em; padding: .62cqw 1.75cqw; border-radius: 999px;
  -webkit-tap-highlight-color: transparent; transition: color .35s; min-width: 7.2cqw; }
.dsp-mode button[aria-checked="true"] { color: #fff; }
.dsp-light .dsp-mode button[aria-checked="true"] { color: #fffdf6; }
.dsp-knob { position: absolute; top: .35cqw; bottom: .35cqw; left: .35cqw; width: calc(50% - .35cqw); border-radius: 999px;
  background: var(--e); transition: transform .45s cubic-bezier(.65,0,.35,1), background .45s; }
.dsp-mode.on-m .dsp-knob { transform: translateX(100%); background: var(--m); }

/* 조작 막대 */
.dsp-ctl { position: absolute; left: 50%; top: 2.4cqw; transform: translate(-50%, -.6cqw); display: flex; align-items: center;
  gap: .5cqw; padding: .45cqw .7cqw; border-radius: 999px; background: var(--chip); border: 1px solid var(--chipbd);
  opacity: 0; pointer-events: none; transition: opacity .3s, transform .3s; z-index: 6; }
.dsp-ctl.show { opacity: 1; pointer-events: auto; transform: translate(-50%, 0); }
.dsp-btn { width: 3.5cqw; height: 3.5cqw; border-radius: 999px; border: 0; background: none; color: var(--ink);
  font-size: 1.65cqw; display: grid; place-items: center; cursor: pointer; -webkit-tap-highlight-color: transparent; }
.dsp-btn:hover { background: rgba(127,127,127,.16); }
.dsp-btn.on { color: var(--gold); background: rgba(127,127,127,.14); }
.dsp-btn:disabled { opacity: .28; cursor: default; background: none; }
.dsp-sep { width: 1px; height: 2.2cqw; background: var(--chipbd); margin: 0 .3cqw; }

/* 액자 조작: 원판 수 · 빠르기 · 걸리는 시간 */
.dsp-num { display: inline-flex; flex-direction: column; align-items: center; min-width: 3.3cqw; line-height: 1; color: var(--ink); }
.dsp-num b { font-size: 1.9cqw; font-weight: 800; font-variant-numeric: tabular-nums; }
.dsp-num small { font-size: .8cqw; color: var(--soft); font-weight: 700; margin-top: .28cqw; }
.dsp-seg { display: flex; border: 1px solid var(--chipbd); border-radius: 999px; padding: .25cqw; gap: .2cqw; }
.dsp-seg button { border: 0; background: none; color: var(--soft); font: inherit; font-size: 1.2cqw; font-weight: 800; cursor: pointer; white-space: nowrap;
  padding: .55cqw 1.1cqw; border-radius: 999px; -webkit-tap-highlight-color: transparent; transition: background .25s, color .25s; }
.dsp-seg button[aria-checked="true"] { background: var(--gold); color: #1c2647; }
.dsp-light .dsp-seg button[aria-checked="true"] { color: #fffdf6; }
.dsp-hint { position: absolute; left: 50%; top: 7.5cqw; transform: translate(-50%, -.5cqw); z-index: 6; white-space: nowrap;
  font-size: 1.08cqw; font-weight: 600; color: var(--soft); background: var(--chip); border: 1px solid var(--chipbd);
  border-radius: 999px; padding: .42cqw 1.25cqw; opacity: 0; pointer-events: none; transition: opacity .3s, transform .3s; }
.dsp-hint.show { opacity: 1; transform: translate(-50%, 0); }
.dsp-hint b { color: var(--ink); font-weight: 800; }
.dsp-hint b.on { color: var(--gold); }

/* 장면 설정 칩 — 조작 막대 아래 */
.dsp-pctl { position: absolute; left: 50%; top: 7.5cqw; transform: translate(-50%, -.5cqw); display: flex; align-items: center;
  gap: .4cqw; padding: .35cqw .8cqw; border-radius: 999px; background: var(--chip); border: 1px solid var(--chipbd);
  opacity: 0; pointer-events: none; transition: opacity .3s, transform .3s; z-index: 6; white-space: nowrap; }
.dsp-pctl.show { opacity: 1; pointer-events: auto; transform: translate(-50%, 0); }
.dsp-pc { display: flex; align-items: center; gap: .35cqw; }
.dsp-pc .lb { font-size: 1.1cqw; font-weight: 800; color: var(--soft); margin: 0 .3cqw 0 .2cqw; }
.dsp-pctl .dsp-num { min-width: 4.6cqw; }

/* 진행 */
.dsp-dots { position: absolute; right: 2.8cqw; bottom: 1.6cqw; display: flex; gap: .55cqw; opacity: .55; }
.dsp-dots i { width: .5cqw; height: .5cqw; border-radius: 999px; background: var(--soft); }
.dsp-dots i.on { background: var(--gold); width: 1.4cqw; }
.dsp-prog { position: absolute; left: 0; right: 0; bottom: 0; height: .22cqw; opacity: .45; }
.dsp-prog i { display: block; height: 100%; background: var(--gold); transform-origin: 0 50%; }
.dsp-paused { position: absolute; left: 50%; bottom: 7.4cqw; transform: translateX(-50%); font-size: 1.25cqw; font-weight: 800;
  color: var(--ink); background: var(--chip); border: 1px solid var(--chipbd); border-radius: 999px; padding: .3cqw 1.1cqw; }
.dsp-paused.fr { left: 3.4cqw; top: 3cqw; bottom: auto; transform: none; }   /* 액자: 받침 글자를 가리지 않게 왼쪽 위 */
.dsp-paused.lab { left: auto; right: 2.8cqw; bottom: 2.6cqw; transform: none; }   /* 실험 액자: 기록·자막을 가리지 않게 오른쪽 아래 */

/* 장면 목록 */
.dsp-list { position: absolute; inset: 0; z-index: 8; display: grid; place-items: center; background: rgba(0,0,0,.35);
  backdrop-filter: blur(3px); -webkit-backdrop-filter: blur(3px); }
.dsp-list-in { width: 78cqw; max-height: 86%; overflow: auto; background: var(--card); color: var(--ink); border-radius: 1.6cqw;
  border: 1px solid var(--chipbd); padding: 1.6cqw 1.8cqw; box-shadow: 0 2cqw 5cqw rgba(0,0,0,.35); }
.dsp-list-h { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.2cqw; font-size: 1.7cqw; }
.dsp-list-h button { border: 0; background: none; color: var(--soft); font-size: 1.7cqw; cursor: pointer; }
.dsp-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: .9cqw; }
.dsp-chips { display: flex; align-items: center; gap: .6cqw; margin-bottom: 1.1cqw; flex-wrap: wrap; }
.dsp-chips .lb { font-size: 1.2cqw; color: var(--soft); font-weight: 700; margin-right: .4cqw; }
.dsp-chip { border: 1px solid var(--chipbd); background: transparent; color: var(--ink); border-radius: 999px; cursor: pointer;
  font: inherit; font-size: 1.25cqw; font-weight: 700; padding: .45cqw 1.1cqw; -webkit-tap-highlight-color: transparent; }
.dsp-chip small { font-size: .95cqw; color: var(--soft); margin-left: .45cqw; font-weight: 600; }
.dsp-chip.on { border-color: var(--gold); color: var(--gold); box-shadow: inset 0 0 0 1px var(--gold); }
.dsp-chip.on small { color: var(--gold); }
.dsp-sec { margin-top: 1.1cqw; transition: opacity .25s; }
.dsp-sec.off { opacity: .42; }
.dsp-sec-h { font-size: 1.15cqw; font-weight: 800; color: var(--soft); margin: 0 0 .6cqw .2cqw; letter-spacing: .02em; }
.dsp-card { text-align: left; border: 1px solid var(--chipbd); border-radius: 1cqw; background: transparent; color: var(--ink);
  padding: .9cqw 1.1cqw; cursor: pointer; display: grid; grid-template-columns: auto 1fr; column-gap: .9cqw; row-gap: .15cqw;
  font: inherit; -webkit-tap-highlight-color: transparent; }
.dsp-card.on { border-color: var(--gold); box-shadow: inset 0 0 0 1px var(--gold); }
.dsp-card .n { grid-row: span 2; font-size: 1.5cqw; font-weight: 800; color: var(--gold); align-self: center; }
.dsp-card .e { font-size: 1.25cqw; font-weight: 700; color: var(--e); }
.dsp-card .m { font-size: 1.25cqw; font-weight: 700; color: var(--m); }

/* 액자 목록 */
.dsp-gal-in { width: 84cqw; max-height: 94%; padding-bottom: 1.2cqw; }
.dsp-gal-sub { margin: -.4cqw 0 1.2cqw .1cqw; font-size: 1.15cqw; color: var(--soft); }
.dsp-gal { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.1cqw; }
.dsp-fcard { text-align: left; border: 1px solid var(--chipbd); border-radius: 1.2cqw; background: transparent; color: var(--ink);
  padding: 0 0 1.1cqw; cursor: pointer; overflow: hidden; display: flex; flex-direction: column; gap: .4cqw; font: inherit;
  -webkit-tap-highlight-color: transparent; transition: border-color .25s, box-shadow .25s; }
.dsp-fcard svg { width: 100%; aspect-ratio: 1600 / 700; display: block; background: rgba(127,127,127,.09); border-bottom: 1px solid var(--chipbd); }
.dsp-fcard .t { padding: .6cqw 1.1cqw 0; font-size: 1.4cqw; font-weight: 800; display: flex; align-items: baseline; flex-wrap: wrap; column-gap: .7cqw; }
.dsp-fcard .t small { font-size: .9cqw; color: var(--gold); font-weight: 700; }
.dsp-fcard .d { padding: 0 1.1cqw; font-size: 1.02cqw; color: var(--soft); line-height: 1.45;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.dsp-fcard .k { margin: 0 1.1cqw; align-self: flex-start; font-size: .82cqw; font-weight: 800; letter-spacing: .04em; color: var(--soft);
  border: 1px solid var(--chipbd); border-radius: 999px; padding: .12cqw .6cqw; }
.dsp-fcard:hover, .dsp-fcard.on { border-color: var(--gold); box-shadow: inset 0 0 0 1px var(--gold); }
.dsp-gal-foot { margin-top: 1.2cqw; display: flex; justify-content: flex-end; }
`;
