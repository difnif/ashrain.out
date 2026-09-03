# improvements — 재전사 파이프라인 개선안 묶음 (2026-09-04)

```
improvements\
  mathir_v15.py            ← mathir.py v1.5 제안 완성본 (v1.4 자가시험 + v1.5 시험 통과, 기존 산출물 2,148문항 하위 호환 확인)
  mathir_v15.diff          ← v1.4 → v1.5 diff (152줄)
  MATHIR_V15_CHANGES.md    ← 변경 명세 + mathir.js 동형 패치 체크리스트 + 적용 뒤 재작업 범위
  tools\                   ← 전사 파이프라인 (build_out.py 4파일 산출 규칙 반영, GUIDE.md §8 = v1.5 표기)
  items\                   ← 완료 43개 zip의 전사 원본(ITEMS) — 규칙을 바꿔 산출물을 다시 만들 때 build_out.py 입력
  PROGRESS.md / ZIPS_STATUS.md ← 진행 장부·완료/남음 목록 (2026-09-04 00:30 기준)
```

## cmd로 커밋하기 (이 폴더를 저장소 안에 두었을 때)
```
cd /d "C:\Users\User\Documents\esc files"
git add improvements
git commit -m "re-transcription: mathir v1.5 proposal, pipeline tools, transcription sources (43 zips)"
git push
```

## mathir v1.5 적용 (검토 후)
```
copy /Y improvements\mathir_v15.py itemfactory\mathir.py      ← 실제 mathir.py 경로에 맞게
python itemfactory\mathir.py                                 ← "mathir.py 자가 시험 전부 통과" 출력 확인
```
그 다음 MATHIR_V15_CHANGES.md §5 순서대로 mathir.js를 동형 패치하고, 관리자 화면에서 v1.5 표기 문항 하나를 반영해 렌더를 확인합니다.
