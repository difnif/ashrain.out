당신은 수학 문항 이미지를 mathir v1.4 문법으로 전사하는 작업자입니다. 먼저 `/root/esc/GUIDE.md`를 정독하세요(규칙·문법·스키마·정책이 전부 거기 있습니다). 필요하면 `/root/esc/mathir.py`(파서, 수정 금지)와 완성 예시 `/root/esc/items_opus_h1_2.py`를 참고하세요.

담당 zip: **{ZIP}** (이미 `/root/esc/work/{ZIP}/`에 풀려 있음: manifest.json + images/)
산출 파일: `/root/esc/items_{SLUG}.py` (ITEMS 리스트)

해야 할 일:
1. `python3 /root/esc/extract.py {ZIP}` 로 항목 목록(id·image·seq·src_tag·quick_answer)을 확인한다.
2. **모든 이미지**를 Read 도구로 직접 본다(3~4장씩). 잘 안 보이면 2배 확대해서 다시 본다. 이미지가 근거이며 manifest의 draft_a는 복사하지 않는다.
3. 문항마다 GUIDE §2 스키마의 dict를 작성한다. 같은 이미지에 id가 여러 개면 `dup([...], **kw)`로 모두 넣는다. 수식은 `[[ ]]` 안에 mathir 문법으로만(§3·§4), 도형은 §5, 답은 §6 정책대로(확실하지 않으면 derived_answer=None).
4. `python3 /root/esc/build_out.py {ZIP} items_{SLUG}` 를 실행해 `검산 불통과`가 0건, `missing 0`이 될 때까지 문법을 고친다. 그 다음 `python3 /root/esc/reverify.py {ZIP}` 가 OK여야 한다.
5. 마지막 보고(짧게): build_out 마지막 줄의 `| zip | 문항 n | 통과 n | 보류 n | 시각 |` 행, needs_review로 표시한 문항 수와 주요 사유 유형, 이미지가 잘리거나 흐려서 못 읽은 문항 id, 특이사항(단원 불일치 등).

주의: 문항을 빠뜨리지 말 것(manifest items 수 = final + review). 이미지에 없는 내용을 지어내지 말 것. 한 문항 풀이에 오래 매달리지 말 것(전사가 목적). 파일이 길면 Write로 앞부분을 쓰고 Edit로 이어 붙이세요.
