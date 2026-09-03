# tools\ — 재전사 파이프라인 (세션 인계용)

이 폴더는 클라우드 세션 작업공간(`/root/esc`)에서 쓰던 도구를 그대로 옮긴 것입니다. 다른 컴퓨터/새 세션에서 이어갈 때
`tools\`의 파일들을 세션 작업공간 `/root/esc/`에 두고(`mathir.py`도 같은 곳에), zip을 `/mnt/user-data/uploads/esc files/`에 스테이징하면 같은 절차로 진행됩니다.

- `GUIDE.md` — 전사 규칙·mathir 문법 요약·정책(subagent용 SOP). `AGENT_PROMPT.md` — 작업자에게 주는 지시 템플릿.
- `extract.py {zip}` — zip 해제(UTF-8 파일명 보정) + manifest 요약.  `build_out.py {zip} {items모듈}` — 4관문 검산 → out/{zip}.final.json / .review.json.
- `reverify.py {zip}` — 산출물 재검증.  `finish.py {zip} {items모듈}` — 재검증 후 PROGRESS.md에 행 추가.
- `items\items_*.py` — zip별 전사 원본(ITEMS 리스트). 규칙을 바꿔(예: 빠른정답 불일치도 final) 산출물을 다시 만들 때 `build_out.py`만 재실행하면 됩니다.

판정 규칙(build_out.py): 4관문 불통과 → review / quick_answer(=manifest)와 derived_answer 불일치 → review / needs_review 플래그(문법 한계·도형 표현 불가) → review. 그 외 final.

## 규칙 변경(2026-09-03 22:05) — 빠른정답 불일치는 보류 사유에서 제외
`build_out.py`가 세 파일을 만듭니다: `{zip}.final.json`(통과) / `{zip}.final_qamismatch.json`(통과이나 quick_answer와 불일치 — 형식은 final과 같아 그대로 반영 가능, pattern_tags "빠른정답불일치") / `{zip}.review.json`(보류: 도형·문법·검산).

## 로컬(RAM만) 파이프라인 — `local_pipeline.py`
Claude API + mathir.py 검산으로 같은 절차를 노트북에서 돌립니다(GPU 불필요, 메모리 수십 MB). `pip install anthropic pillow`, `ANTHROPIC_API_KEY` 설정 후
`python local_pipeline.py --zip-dir "C:\Users\User\Documents\esc files" --pattern "esc_sonnet_m3-1_*.zip" --resume`

## 규칙 완화(2026-09-04 00:30) — 도형 표현 불가만이 사유인 보류는 통과
`build_out.py`가 네 파일을 만듭니다: `final.json` / `final_qamismatch.json`(빠른정답 불일치 통과분) / `final_figrelax.json`(도형 완화로 소급 통과분, pattern_tags "도형완화") / `review.json`(문법 한계 등).

## mathir v1.5 제안 패치
`mathir_v15.py`(완성본) · `mathir_v15.diff` · `MATHIR_V15_CHANGES.md`(명세 + mathir.js 동형 패치 체크리스트). 적용 전까지 전사는 v1.4 규칙(GUIDE §3~§7), 적용 후 GUIDE §8 표기를 사용.
