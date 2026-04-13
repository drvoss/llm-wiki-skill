# llm-wiki 운영 가이드

**언어:** [English](OPERATIONS.md) | [한국어](OPERATIONS.ko.md) | [简体中文](OPERATIONS.zh-CN.md)

이 문서는 첫 사용 이후의 운영 흐름을 다룹니다. 중복 정리, 배치 ingest,
lint 습관, archive 기준 같은 day-2 작업을 정리합니다.

---

## 1. 운영 모델

- `raw/` 는 바꾸지 않는 원문 레이어
- `entities/`, `concepts/`, `comparisons/`, `queries/` 는 정제된 요약 레이어
- `SCHEMA.md` 는 규칙 계약
- `index.md`, `log.md` 는 탐색의 뼈대

기본 리듬:

1. 관련 소스 몇 개를 ingest
2. 관련 페이지를 한 번에 정리
3. `wiki-lint.py` 실행
4. taxonomy / navigation drift를 바로 수정

---

## 2. 중복 페이지 정리

다음 기준을 권장합니다.

- 같은 엔티티/개념을 다루면 **merge**
- 범위가 다르면 **분리 유지**
- 완전히 대체되었으면 **archive**

정리 순서:

1. 남길 페이지 결정
2. 유효한 내용 병합
3. 중요한 링크 갱신
4. `index.md` 에서 이전 페이지 제거
5. `log.md` 에 기록

---

## 3. Schema Drift 대응

보통 이런 형태로 나타납니다.

- 비슷한 태그가 여러 개 생김
- 페이지 범위가 섞임
- 파일명 규칙이 흔들림

대응 순서:

1. `SCHEMA.md` 의 taxonomy를 먼저 정리
2. 페이지 태그를 새 taxonomy에 맞게 수정
3. 제목/파일명을 점검
4. `wiki-lint.py --strict` 실행

---

## 4. Batch Ingest 전략

관련 소스가 여러 개면 하나씩 따로 처리하지 마세요.

권장 순서:

1. 관련 소스를 모두 읽기
2. 반복되는 entity / concept 목록화
3. 기존 위키를 한 번에 검색
4. 페이지를 한 번에 생성/수정
5. `index.md` 한 번 갱신
6. `log.md` 한 번 기록

---

## 5. Query 파일링 기준

`queries/`에는 다시 만들기 귀찮은 답만 남기는 편이 좋습니다.

좋은 후보:

- 여러 페이지를 종합한 답
- 다시 물어볼 가능성이 높은 답
- 반복 의사결정을 돕는 답

나쁜 후보:

- 단순 lookup
- 한 줄짜리 사실 확인
- 다시 만들기 쉬운 답

---

## 6. Stale 페이지 점검

stale 페이지가 항상 나쁜 것은 아닙니다.

- 여전히 정확하고 유용하면 유지
- 일부만 낡았으면 업데이트
- 완전히 대체되었으면 archive

불필요한 churn보다 품질 개선에 집중하는 것이 좋습니다.

---

## 7. Archive 절차

권장 절차:

1. 페이지를 `_archive/` 로 이동
2. `index.md` 에서 제거
3. 중요한 wikilink 정리
4. 무엇으로 대체되었는지 `log.md` 에 기록

raw source는 archive 대상이 아니라 provenance 레이어라는 점을 유지하세요.

---

## 8. Lint 운영

```bash
python3 scripts/wiki-lint.py ~/wiki/my-domain
python3 scripts/wiki-lint.py --strict ~/wiki/my-domain
python3 scripts/wiki-lint.py --json ~/wiki/my-domain
python3 scripts/wiki-lint.py --fix ~/wiki/my-domain
```

- 일상 점검: 기본 lint
- 공유 저장소/CI: `--strict`
- 자동화: `--json`
- 안전한 메타데이터 수정: `--fix`

---

## 9. Stats 운영

빠른 현황 요약이 필요할 때는 `wiki-stats.py`를 사용하세요.

```bash
python3 scripts/wiki-stats.py ~/wiki/my-domain
python3 scripts/wiki-stats.py --json ~/wiki/my-domain
```

좋은 사용 예:

- 위키가 실제로 자라고 있는지 확인
- 페이지 타입 비중 확인
- raw source와 curated page가 같이 늘고 있는지 확인

---

## 10. 유지보수 주기

### 의미 있는 ingest 후

- 관련 페이지 업데이트
- index/log 갱신
- lint 실행

### 여러 소스 배치 처리 후

- 이름/태그 정리
- 필요하면 durable query 1-2개 파일링

### 주기적으로

- stale 페이지 검토
- 태그 정리
- archive 정리

이 정도면 과한 절차 없이도 위키 품질을 유지할 수 있습니다.
