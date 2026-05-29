# Defect List — Magic Square 4×4

| 항목 | 내용 |
|---|---|
| **Document ID** | DL-MSQ-001 |
| **Version** | 0.1 |
| **Status** | Open (5 open / 0 closed) |
| **Last verified** | 2026-05-29 |
| **Verification** | `python -m pytest -q` → **5 failed, 39 passed** |
| **SSOT** | `docs/test_plan.md`, `docs/04-dual-track-clean-architecture-design.md` §13, `src/magicsquare/boundary/error_codes.py` |

> **요약:** 현재 실패 5건은 **production 결함이 아님**. `tests/boundary/test_ac_fr_01_01_red.py`가 존재하지 않는 `INVALID_SIZE` 계약을 기대함. Boundary·InputValidator는 SSOT(`INPUT_NULL` / `INPUT_ROW_COUNT` / `INPUT_COL_COUNT`)대로 동작하며, Domain 0-call·`ErrorResponse` 반환은 정상.

---

## 결함 목록

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|---|---|---|---|---|---|---|---|
| DEF-001 | Major | AC-FR-01-01 | `UIBoundary.submit(None)` 호출 후 `test_none_grid_returns_invalid_size_error_response` 실행 | `code="INVALID_SIZE"`, `ErrorResponse` | `code="INPUT_NULL"`, `ErrorResponse` (예외 없음) | RED 테스트가 프롬프트 예시 `INVALID_SIZE` 사용; PRD §13·Test Plan BV-01은 `INPUT_NULL` | `test_ac_fr_01_01_red.py` assertion을 `ErrorCode.INPUT_NULL` + `ERROR_MESSAGES`로 정렬 |
| DEF-002 | Major | AC-FR-01-01 | 동일 입력으로 `test_none_grid_message_exact_match_prd_section_8_1` 실행 | `message="Grid must be 4x4."` | `message="Input matrix must not be null."` | §13 message SSOT와 RED 테스트 기대 불일치 | DEF-001과 동일 파일에서 `ERROR_MESSAGES[ErrorCode.INPUT_NULL]` assert |
| DEF-003 | Major | AC-FR-01-02 | `UIBoundary.submit([])` 후 `test_empty_list_grid_returns_invalid_size_error` 실행 | `INVALID_SIZE` + `"Grid must be 4x4."` | `INPUT_ROW_COUNT` + `"Matrix must have exactly 4 rows."` | 크기 오류를 단일 `INVALID_SIZE`로 통합 기대; SSOT는 행/열 분리 코드 | `ErrorCode.INPUT_ROW_COUNT` + 해당 message assert |
| DEF-004 | Major | AC-FR-01-03 | `UIBoundary.submit([[]]*4)` 후 `test_four_rows_zero_cols_grid_returns_invalid_size_error` 실행 | `INVALID_SIZE` + `"Grid must be 4x4."` | `INPUT_COL_COUNT` + `"Each row must have exactly 4 columns."` | 열 수 불일치를 `INVALID_SIZE`로 기대; Test Plan BV-03은 `INPUT_COL_COUNT` | `ErrorCode.INPUT_COL_COUNT` + 해당 message assert |
| DEF-005 | Major | AC-FR-01-02 | `UIBoundary.submit(3×4 grid)` 후 `test_three_by_four_grid_returns_invalid_size_error` 실행 | `INVALID_SIZE` + `"Grid must be 4x4."` | `INPUT_ROW_COUNT` + `"Matrix must have exactly 4 rows."` | 3×4를 `INVALID_SIZE`로 기대; Test Plan BV-04는 `INPUT_ROW_COUNT` | `ErrorCode.INPUT_ROW_COUNT` + 해당 message assert |
| DEF-006 | Info | — | `README.md` RED 체크리스트 TC-A-02·TC-A-03 검토 | SSOT Error Code 8종 (`INPUT_*`) | `"INVALID_SIZE"`, `"Grid must be 4x4."` 문구 | README가 구 프롬프트 예시를 반영; `docs/test_plan.md`와 불일치 | README TC-A-02~03·TC-A-07을 Test Plan BV 표준으로 갱신 |
| DEF-007 | Info | — | `test_ac_fr_01_01_red.py` 모듈 docstring·클래스 docstring 검토 | PRD §13 / Test Plan BV 참조 | `"PRD §8.1 INVALID_SIZE"` (PRD에 §8.1·`INVALID_SIZE` 미정의) | 잘못된 PRD 섹션·코드명 인용 | docstring을 `docs/test_plan.md` BV-01~06, AC-FR-01-01로 수정 |

---

## 검증됨 — 결함 아님 (Negative findings)

| 항목 | AC ID | 재현 | 결과 | 비고 |
|---|---|---|---|---|
| None 입력 크래시 | AC-FR-01-01 | `grid=None` → `boundary.submit` | `ErrorResponse` 반환, **AttributeError 없음** | Critical 해당 없음 |
| Domain 미호출 (BR-05) | AC-FR-01-01 | `grid=None` + Mock/spy | `solve.call_count == 0` (**3 tests PASS**) | `ui_boundary.py:59-61` early return 정상 |
| InputValidator SSOT | AC-FR-01-01~03 | `tests/boundary/test_input_validator.py` | **16/16 PASS** | `input_validator.py:36-46` SSOT 일치 |
| 스코프 제한 | AC-FR-01-01 | `test_module_scope_excludes_ac_fr_01_02_to_05_cases` | **PASS** | AC-FR-01-02~05 케이스 미포함 |

---

## 수정 우선순위

| 순위 | ID | 담당 레이어 | 예상 작업 |
|---|---|---|---|
| 1 | DEF-001 ~ DEF-005 | Test (Track A) | `test_ac_fr_01_01_red.py` SSOT 정렬 — **production 변경 0줄** |
| 2 | DEF-006, DEF-007 | Docs / Test | README·docstring SSOT 동기화 |

---

## GREEN 확인 절차 (결함 수정 후)

```powershell
cd "c:\Users\usejen_id\CursorAI\dev\MagicSquare _1004"
python -m pytest tests/boundary/test_ac_fr_01_01_red.py -v --tb=short
python -m pytest -v --tb=short
```

**Definition of Done (결함 클로즈):** 위 명령 **44 passed, 0 failed** + 본 문서 Status를 Closed로 갱신.

---

## 변경 이력

| 날짜 | 버전 | 변경 |
|---|---|---|
| 2026-05-29 | 0.1 | 최초 작성 — pytest 5 failed (AC-FR-01-01 RED 테스트 명세 결함) |
