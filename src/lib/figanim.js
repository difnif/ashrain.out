// ashrain.out — 해설 애니메이션 플레이어 (figanim.js, v1.2)
// 위치: src/lib/figanim.js  — 순수 DOM, 의존성 없음. 검수 HTML(review.mjs)과 앱이 공유.
//
// 원칙 (Park, 2026-09-07)
//   · 도형·상황 도식은 처음부터 다 그려 둔다(보조선·조건 표기 포함). 애니메이션은 **색으로 강조**하며 설명을 따라간다.
//     강조는 선 색 + 은은한 형광펜 번짐(glow) — 눈으로 따라가기 쉬울 만큼만.
//   · 아래 설명 텍스트와 싱크 — 진행 중인 단계가 굵어진다.
//   · 그림 여백 아무 곳이나 클릭 → 일시정지 / 재생. 끝나면 클릭으로 처음부터.
//   · 이동 문제(기차·거속시)만 실제로 움직인다. 나타나는 효과는 최소.
//   · 판서(steps)는 풀이 줄 전체가 처음부터 보이고, 작은 빨간 메모만 그 순간 써지듯 나타난다.
//   · 기본 속도는 느리게(1×). 오른쪽 위 버튼으로 1.5× 전환. 하단 진행바 클릭·드래그로 위치 이동.
//
// 마크업
//   <div class="anim-level" data-anim='[[cue,…],[cue,…]]'>      ← 단계별 큐 배열
//     <div class="fig-stage">…figsvg 출력…</div>
//     … <li data-step="0">…</li> <li data-step="1">…</li> …     ← 또는 <p data-step="0">
//   </div>
//
// 큐 { act, k, dur, keep }
//   hl      k 요소 강조 (다음 단계에서 해제, keep:true 면 유지)
//   show    k 요소 보이기 (유지)          hide   k 요소 숨기기 (유지)
//   move    k 요소 이동 — train(data-dx) · mover(data-x0/x1) · 일반(data-dx) — trail 동반
//   reveal  steps 판서의 line:i 를 짚음(줄 배경 강조). 판서 줄 전체는 처음부터 다 보인다 — 숨겨 두는 것은
//           작은 빨간 메모(hint:i · mark:i-j 의 note)만이고, 그 키를 hl/pulse 하는 순간 왼쪽→오른쪽으로 써지듯 나타난다
//   pulse   잠깐 커졌다 작아짐
//   k 는 문자열 또는 배열. dur 기본 2400ms(단계), move 는 3300ms — 1× 기준. 1.5× 면 그만큼 빨라진다.
//   (시드에 적힌 dur 값은 예전 1.5× 기준이라 1.5 를 곱해 1× 로 환산한다)

const ACCENT = "#d1495b";
const GLOW = "rgba(255, 196, 0, .75)";      // 형광펜 — 노란빛 번짐 (은은하게)
const CSS = `
.anim-level{position:relative}
.anim-level .fig-stage{position:relative;cursor:pointer;-webkit-tap-highlight-color:transparent;padding-bottom:10px}
.anim-level .fig-stage line[data-k].anim-hl,.anim-level .fig-stage path[data-k].anim-hl,.anim-level .fig-stage polygon[data-k].anim-hl,.anim-level .fig-stage circle[data-k].anim-hl,.anim-level .fig-stage rect[data-k].anim-hl,.anim-level .fig-stage ellipse[data-k].anim-hl{stroke:${ACCENT} !important;stroke-width:2.6px;stroke-opacity:1;opacity:1 !important;filter:drop-shadow(0 0 2.2px ${GLOW})}
.anim-level .fig-stage g[data-k].anim-hl line,.anim-level .fig-stage g[data-k].anim-hl path,.anim-level .fig-stage g[data-k].anim-hl rect{stroke:${ACCENT} !important;stroke-width:2.4px;opacity:1}
.anim-level .fig-stage g[data-k].anim-hl{filter:drop-shadow(0 0 2.2px ${GLOW})}
.anim-level .fig-stage g[data-k].anim-hl text{fill:${ACCENT} !important;font-weight:700}
.anim-level .fig-stage text[data-k].anim-hl{fill:${ACCENT} !important;font-weight:700;paint-order:stroke;stroke:rgba(255,222,80,.6) !important;stroke-width:5px;stroke-linejoin:round;filter:none}
.anim-level .fig-stage circle[data-k^="pt:"].anim-hl{fill:${ACCENT} !important;r:4.2}
.anim-level .fig-stage polygon[data-k].anim-hl{fill:${ACCENT};fill-opacity:.2}
.anim-level .fig-stage rect[data-k^="part:"].anim-hl{filter:drop-shadow(0 0 3px ${GLOW});stroke-width:1.8px}
.anim-level .fig-stage .fig-line{transition:background .25s,opacity .3s;border-radius:4px;padding:0 4px;margin:0 -4px}
.anim-level .fig-stage .fig-line.anim-hl{background:rgba(255,222,80,.22)}
.anim-level .fig-stage .fig-line.anim-hidden{opacity:0;height:0;overflow:hidden;margin:0;padding:0}
.anim-level .fig-stage .fig-hint,.anim-level .fig-stage .fig-note-sup{display:inline-block;transition:clip-path .55s ease-out,opacity .3s}
.anim-level .fig-stage .fig-hint{display:block}
.anim-level .fig-stage .anim-ink{clip-path:inset(0 100% 0 0);opacity:0;transition:none}
.anim-level .fig-stage .fig-mk.anim-hl{color:${ACCENT};font-weight:700;text-decoration:underline;text-decoration-thickness:2px;background:rgba(255,222,80,.28);border-radius:2px}
.anim-level .fig-stage .fig-strike{text-decoration:line-through;opacity:.6}
.anim-level .fig-stage .anim-hidden{opacity:0 !important}
.anim-level .fig-stage.anim-instant *{transition:none !important;animation:none !important}
.anim-level [data-step]{transition:color .2s}
.anim-level [data-step].anim-on{font-weight:700;color:${ACCENT}}
.anim-level [data-step].anim-done{opacity:.72}
.anim-level .anim-seek{position:absolute;left:0;right:0;bottom:0;height:14px;cursor:pointer;touch-action:none}
.anim-level .anim-seek .anim-bar{position:absolute;left:0;right:0;bottom:2px;height:4px;background:rgba(0,0,0,.09);border-radius:2px;overflow:hidden;transition:height .15s}
.anim-level .anim-seek:hover .anim-bar,.anim-level .anim-seek.drag .anim-bar{height:7px}
.anim-level .anim-bar>i{display:block;height:100%;width:0;background:${ACCENT}}
.anim-level .anim-seek .anim-tick{position:absolute;bottom:2px;width:1px;height:7px;background:rgba(255,255,255,.95);pointer-events:none}
.anim-level .anim-badge{position:absolute;left:6px;top:6px;font-size:11px;padding:2px 7px;border-radius:10px;background:rgba(0,0,0,.55);color:#fff;opacity:0;transition:opacity .2s;pointer-events:none}
.anim-level .anim-badge.show{opacity:1}
.anim-level .anim-ctl{position:absolute;right:6px;top:6px;display:flex;gap:4px}
.anim-level .anim-ctl button{font:11px/1 system-ui,sans-serif;padding:3px 7px;border-radius:9px;border:1px solid rgba(0,0,0,.18);background:rgba(255,255,255,.85);color:#444;cursor:pointer}
.anim-level .anim-ctl button.on{background:${ACCENT};border-color:${ACCENT};color:#fff}
.anim-level .fig-stage .anim-pulse{animation:animPulse .5s ease-out}
@keyframes animPulse{0%{transform:scale(1)}50%{transform:scale(1.25)}100%{transform:scale(1)}}
`;

function injectCss() {
  if (typeof document === "undefined" || document.getElementById("figanim-css")) return;
  const st = document.createElement("style");
  st.id = "figanim-css"; st.textContent = CSS;
  document.head.appendChild(st);
}

const ease = (t) => (t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t);

export class AnimPlayer {
  constructor(root, cues, opts = {}) {
    this.root = root;
    this.stage = root.querySelector(".fig-stage");
    this.cues = cues;                    // 단계별 큐 배열
    this.baseStep = opts.stepDur || 2400;   // 1× 기준 (이전 1600ms 가 지금의 1.5× 에 해당)
    this.baseMove = opts.moveDur || 3300;
    this.rate = opts.rate || 1;
    this.i = -1; this.playing = false; this.done = false; this.elapsed = 0;
    this.raf = null; this.timer = null; this.moves = []; this.stepDur_ = this.baseStep;
    this.steps = [...root.querySelectorAll("[data-step]")];
    // 진행바(클릭·드래그로 이동) + 단계 눈금
    this.seek = document.createElement("div"); this.seek.className = "anim-seek";
    this.bar = document.createElement("div"); this.bar.className = "anim-bar"; this.bar.innerHTML = "<i></i>";
    this.seek.appendChild(this.bar);
    for (let j = 1; j < cues.length; j++) {
      const t = document.createElement("i"); t.className = "anim-tick"; t.style.left = `${(j / cues.length) * 100}%`;
      this.seek.appendChild(t);
    }
    this.badge = document.createElement("div"); this.badge.className = "anim-badge";
    this.ctl = document.createElement("div"); this.ctl.className = "anim-ctl";
    this.rateBtn = document.createElement("button"); this.rateBtn.type = "button"; this.rateBtn.textContent = "1.5×";
    this.rateBtn.title = "재생 속도 (1× ↔ 1.5×)";
    this.ctl.appendChild(this.rateBtn);
    this.stage.appendChild(this.seek); this.stage.appendChild(this.badge); this.stage.appendChild(this.ctl);
    this.stage.addEventListener("click", () => this.toggle());
    this.ctl.addEventListener("click", (e) => e.stopPropagation());
    this.rateBtn.addEventListener("click", () => this.setRate(this.rate === 1 ? 1.5 : 1));
    // 진행바 — 클릭·드래그
    const posOf = (e) => { const r = this.seek.getBoundingClientRect(); return Math.min(1, Math.max(0, (e.clientX - r.left) / r.width)); };
    this.seek.addEventListener("pointerdown", (e) => {
      e.stopPropagation(); e.preventDefault();
      this.seek.classList.add("drag"); try { this.seek.setPointerCapture(e.pointerId); } catch { /* 무시 */ }
      this._wasPlaying = this.playing || this.i < 0 || this.done;   // 시작 전·끝난 뒤에 짚으면 그 자리부터 재생
      this.seekTo(posOf(e));
    });
    this.seek.addEventListener("pointermove", (e) => { if (this.seek.classList.contains("drag")) this.seekTo(posOf(e)); });
    const up = (e) => {
      if (!this.seek.classList.contains("drag")) return;
      this.seek.classList.remove("drag"); e.stopPropagation();
      if (this._wasPlaying) this.play();
    };
    this.seek.addEventListener("pointerup", up); this.seek.addEventListener("pointercancel", up);
    this.seek.addEventListener("click", (e) => e.stopPropagation());
    if (this.rate !== 1) this.rateBtn.classList.add("on");
    this.prepare();
  }

  q(k) { return [...this.stage.querySelectorAll(`[data-k="${k}"],[data-ka~="${k}"]`)]; }   // data-ka: 별칭(edge:BA, face 회전형)
  each(k, fn) { for (const kk of (Array.isArray(k) ? k : [k])) this.q(kk).forEach(fn); }

  setRate(r) {
    // 진행 중인 단계의 상대 위치를 유지하며 속도만 바꾼다
    const p = this.stepDur_ ? Math.min(1, this.elapsed / this.stepDur_) : 0;
    this.rate = r;
    this.rateBtn.classList.toggle("on", r !== 1);
    this.flash(`${r}×`);
    if (this.i >= 0 && !this.done) {
      this.stepDur_ = this.durOf(this.cues[this.i] || []);
      this.elapsed = p * this.stepDur_;
      if (this.playing) { this.stop(); this.resume(); }
    }
  }

  durOf(step) {
    let dur = this.baseStep;
    for (const c of step) {
      if (c.act === "move") dur = Math.max(dur, c.dur ? c.dur * 1.5 : this.baseMove);   // 시드의 dur 은 옛 1.5× 기준
      else if (c.dur) dur = Math.max(dur, c.dur * 1.5);
    }
    return dur / this.rate;
  }
  moveDurOf(c) { return (c.dur ? c.dur * 1.5 : this.baseMove) / this.rate; }

  prepare() {
    // 판서(steps)는 전체 풀이가 처음부터 다 보인다. 작은 메모(hint·note)만 잉크가 마르기 전처럼 숨겨 두고,
    // 그 줄·표시가 짚어질 때(hl/pulse) 왼쪽→오른쪽으로 써지듯 나타난다.
    this.stage.querySelectorAll(".fig-hint,.fig-note-sup").forEach((el) => el.classList.add("anim-ink"));
    // 처음부터 숨겨 둘 요소
    this.cues.forEach((st) => (st || []).forEach((c) => {
      if (c.act === "show") this.each(c.k, (el) => el.classList.add("anim-hidden"));
    }));
    this.q("trail").forEach((el) => { el.setAttribute("opacity", "0"); el.setAttribute("x2", el.dataset.x0); });
    this.q("train").forEach((el) => { el.style.transform = ""; });
    this.q("mover").forEach((el) => { el.setAttribute("opacity", "0"); el.setAttribute("cx", el.dataset.x0); });
  }

  clearState() {
    this.stage.querySelectorAll(".anim-hl,.anim-pulse").forEach((el) => { el.classList.remove("anim-hl", "anim-pulse"); delete el.dataset.animKeep; });
    this.stage.querySelectorAll(".anim-hidden,.anim-ink").forEach((el) => el.classList.remove("anim-hidden", "anim-ink"));
    this.steps.forEach((el) => el.classList.remove("anim-on", "anim-done"));
    this.prepare();
  }

  reset() {
    this.stop();
    this.clearState();
    this.i = -1; this.done = false; this.elapsed = 0; this.moves = [];
    this.bar.firstChild.style.width = "0";
  }

  toggle() {
    if (this.done) { this.reset(); this.play(); return; }
    if (this.playing) this.pause(); else this.play();
  }

  flash(text) { this.badge.textContent = text; this.badge.classList.add("show"); clearTimeout(this._bt); this._bt = setTimeout(() => this.badge.classList.remove("show"), 900); }

  play() {
    if (this.playing) return;
    if (this.done) this.reset();
    this.playing = true; this.flash("▶");
    if (this.i < 0) this.next(); else this.resume();
  }
  pause() { this.playing = false; this.flash("❚❚"); this.stop(); }
  stop() { if (this.raf) cancelAnimationFrame(this.raf); if (this.timer) clearTimeout(this.timer); this.raf = null; this.timer = null; }

  // ── 단계 진입 (큐 적용) — 타이머 없이 상태만 바꾼다
  enter(i, { instant = false } = {}) {
    const step = this.cues[i] || [];
    // 이전 단계 강조 해제 (keep 제외)
    this.stage.querySelectorAll(".anim-hl").forEach((el) => { if (!el.dataset.animKeep) el.classList.remove("anim-hl"); });
    this.steps.forEach((el, j) => { el.classList.toggle("anim-on", j === i); el.classList.toggle("anim-done", j < i); });
    const ink = (el) => {                          // 메모가 써지듯 나타남 (자신 또는 안쪽의 메모)
      const list = el.classList.contains("anim-ink") ? [el] : [...el.querySelectorAll(".anim-ink")];
      list.forEach((m) => { if (!instant) void m.offsetWidth; m.classList.remove("anim-ink"); });
    };
    const moves = [];
    for (const c of step) {
      const k = c.k;
      if (c.act === "hl") this.each(k, (el) => { el.classList.add("anim-hl"); ink(el); if (c.keep) el.dataset.animKeep = "1"; });
      else if (c.act === "show") this.each(k, (el) => { el.classList.remove("anim-hidden"); ink(el); });
      else if (c.act === "hide") this.each(k, (el) => el.classList.add("anim-hidden"));
      else if (c.act === "reveal") this.each(k, (el) => { el.classList.remove("anim-hidden"); el.classList.add("anim-hl"); });   // 줄만 짚음 — 메모는 hl 로 따로
      else if (c.act === "pulse") this.each(k, (el) => { if (!instant) { el.classList.remove("anim-pulse"); void el.offsetWidth; el.classList.add("anim-pulse"); } el.classList.add("anim-hl"); ink(el); if (c.keep) el.dataset.animKeep = "1"; });
      else if (c.act === "move") moves.push(c);
    }
    this.i = i; this.moves = moves; this.stepDur_ = this.durOf(step);
  }

  next() {
    if (!this.playing) return;
    const i = this.i + 1;
    if (i >= this.cues.length) { this.finish(); return; }
    this.enter(i);
    const target = this.steps[i];
    if (target && target.scrollIntoView && i > 0) target.scrollIntoView({ block: "nearest", behavior: "smooth" });
    this.stepStart = performance.now(); this.elapsed = 0;
    this.tick();
  }

  resume() { this.stepStart = performance.now() - this.elapsed; this.tick(); }

  tick() {
    if (!this.playing) return;
    const now = performance.now();
    this.elapsed = now - this.stepStart;
    const p = Math.min(1, this.elapsed / this.stepDur_);
    for (const m of this.moves) this.applyMove(m, ease(Math.min(1, this.elapsed / this.moveDurOf(m))));
    this.bar.firstChild.style.width = `${((this.i + p) / this.cues.length) * 100}%`;
    if (p < 1) this.raf = requestAnimationFrame(() => this.tick());
    else this.timer = setTimeout(() => this.next(), 120);
  }

  /** 진행바 위치(0~1)로 이동 — 앞 단계는 즉시 적용, 현재 단계는 그 지점까지. 멈춘 상태로 둔다. */
  seekTo(frac) {
    const total = this.cues.length;
    if (!total) return;
    this.stop();
    this.playing = false;
    const pos = Math.min(total - 1e-6, Math.max(0, frac * total));
    const i = Math.floor(pos), p = pos - i;
    this.stage.classList.add("anim-instant");
    this.clearState();
    this.done = false;
    for (let j = 0; j < i; j++) { this.enter(j, { instant: true }); for (const m of this.moves) this.applyMove(m, 1); }
    this.enter(i, { instant: true });
    this.elapsed = p * this.stepDur_;
    for (const m of this.moves) this.applyMove(m, ease(Math.min(1, this.elapsed / this.moveDurOf(m))));
    this.bar.firstChild.style.width = `${((i + p) / total) * 100}%`;
    void this.stage.offsetWidth;
    this.stage.classList.remove("anim-instant");
  }

  applyMove(c, t) {
    this.each(c.k, (el) => {
      if (el.dataset.dx !== undefined && el.tagName.toLowerCase() === "g") {   // train 등 그룹 이동
        el.style.transform = `translate(${(+el.dataset.dx) * t}px, 0)`;
      } else if (el.dataset.x0 !== undefined && el.dataset.x1 !== undefined) {  // mover 점 이동
        el.setAttribute("opacity", "1");
        el.setAttribute("cx", (+el.dataset.x0) + ((+el.dataset.x1) - (+el.dataset.x0)) * t);
      }
    });
    // trail 은 train 과 함께 자란다
    if (c.k === "train" || (Array.isArray(c.k) && c.k.includes("train"))) {
      this.q("trail").forEach((el) => { el.setAttribute("opacity", "1"); el.setAttribute("x2", (+el.dataset.x0) + (+el.dataset.dx) * t); });
    }
  }

  finish() {
    this.playing = false; this.done = true;
    this.steps.forEach((el) => { el.classList.remove("anim-on"); el.classList.add("anim-done"); });
    this.bar.firstChild.style.width = "100%";
    this.flash("↻ 다시 보려면 클릭");
  }
}

/** 문서 안의 .anim-level 을 모두 플레이어로 만들고, 화면에 들어오면 자동 재생한다. */
export function mountAll(root = document, opts = {}) {
  injectCss();
  const players = [];
  root.querySelectorAll(".anim-level[data-anim]").forEach((el) => {
    let cues;
    try { cues = JSON.parse(el.dataset.anim); } catch { return; }
    if (!Array.isArray(cues) || !cues.length || !el.querySelector(".fig-stage")) return;
    const pl = new AnimPlayer(el, cues, opts);
    players.push(pl);
    el.__anim = pl;
  });
  if (opts.autoplay !== false && typeof IntersectionObserver !== "undefined") {
    const io = new IntersectionObserver((ents) => ents.forEach((e) => {
      const pl = e.target.__anim;
      if (!pl) return;
      if (e.isIntersecting && pl.i < 0) pl.play();
      if (!e.isIntersecting && pl.playing) pl.pause();
    }), { threshold: 0.45 });
    players.forEach((pl) => io.observe(pl.root));
  }
  return players;
}

export default { mountAll, AnimPlayer };
