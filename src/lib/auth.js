// 아이디 기반 로그인: 내부적으로 가상 이메일로 변환해 Supabase Auth 사용
export const ID_DOMAIN = "id.ashrain.app";
export const idToEmail = (id) => (id.includes("@") ? id : `${id.trim().toLowerCase()}@${ID_DOMAIN}`);
export const ID_RULE = /^[a-z0-9_]{4,16}$/; // 영문 소문자·숫자·언더바 4~16자
