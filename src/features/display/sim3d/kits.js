// ashrain.out — 교실 모니터 「3D 축구」: 팀 옷 색 (sim3d/kits.js)
// 주인공 팀은 2D 장면과 같은 색 계열(맨시티 하늘 · 맨유 빨강 · 첼시 파랑), 상대는 회색 모형(2D 의 회색 선수와 같다).
export const KITS = {
  city: { shirt: "#8DC3EE", shorts: "#F3F5F7", socks: "#8DC3EE" },
  united: { shirt: "#D6302A", shorts: "#F3F5F7", socks: "#22252B" },
  chelsea: { shirt: "#2253C4", shorts: "#2253C4", socks: "#F3F5F7" },
  cityKeeper: { shirt: "#E7E05A", shorts: "#2B2F36", socks: "#E7E05A", gloves: true },
  unitedKeeper: { shirt: "#3E9F5A", shorts: "#2B2F36", socks: "#3E9F5A", gloves: true },
  chelseaKeeper: { shirt: "#F08A2C", shorts: "#2B2F36", socks: "#F08A2C", gloves: true },
  rival: { shirt: "#A3ABB4", shorts: "#6F767F", socks: "#A3ABB4", skin: "#B8B3AB", hair: "#5b5754" },
  rivalKeeper: { shirt: "#5F6670", shorts: "#474C54", socks: "#5F6670", skin: "#B8B3AB", hair: "#4a4744", gloves: true },
};
/** 이름표의 번호 동그라미 색 */
export const KIT_INK = Object.fromEntries(Object.entries(KITS).map(([k, v]) => [k, v.shirt]));
