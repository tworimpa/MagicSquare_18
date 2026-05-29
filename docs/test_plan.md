# Test Plan — FR-01 Input Verification (Anchor: AC-FR01-01)

| 항목 | 내용 |
|---|---|
| **Document ID** | TP-MSQ-FR01-001 |
| **Version** | 0.1 |
| **Status** | Draft |
| **Anchor AC** | AC-FR01-01 (`grid = None`) |
| **PRD Reference** | FR-01, §12.1, §13, §15.1, §16.2 |
| **SSOT Contract** | `docs/PRD_MagicSquare.md`, `docs/04-dual-track-clean-architecture-design.md` |
| **Stack** | Python 3.11+, pytest, dataclass Response DTO *(pydantic 선택 적용 가능)*, `unittest.mock` |
| **Track** | Track A (Boundary) — Domain Mock 격리 |

> **코드·메시지 SSOT 정렬**  
> 프롬프트 예시의 `INVALID_SIZE`는 본 프로젝트 PRD §13에 정의되지 않는다.  
> **null** → `INPUT_NULL` · **행 수 불일치** → `INPUT_ROW_COUNT` · **열 수 불일치** → `INPUT_COL_COUNT` 로 분리 검증한다.

---

## 1. 목적 및 범위

### 1.1 목적

FR-01 **Input Verification**의 선행 Acceptance Criteria인 **AC-FR01-01**을 앵커로, Boundary 계층이 **입력 구조·크기 위반 시 Domain resolver를 호출하지 않음(BR-05)** 을 pytest로 검증한다.

### 1.2 In-Scope (본 계획서)

| 범위 | 설명 |
|---|---|
| **Unit — InputValidator** | `validate_input_contract()` 단독: ErrorCode 반환 |
| **Unit — UIBoundary** | `submit()` 오케스트레이션: ErrorResponse 조립 + Domain 0-call |
| **Unit — ErrorMapper** | Code → message §13 완전 일치 (RG-03) |
| **경계값** | null, 빈 리스트, 열 없음, 3×4 / 4×3 / 5×5 |

### 1.3 Out-of-Scope (본 계획서에서 명시적 제외)

| 제외 항목 | 사유 |
|---|---|
| **4×4 정상 입력 (빈칸 2개·값 유효)** | AC-FR01-01 범위 외; U-C01 / AC-FR01-07 별도 Test Plan |
| Domain Solver·Validator 로직 | Track B (D-*) |
| Integration (IT-*) | Post-MVP |
| Generate / Standalone Validate API | PRD §22 Decision Needed |

---

## 2. pytest 단위 테스트 범위 및 우선순위

### 2.1 테스트 파일·레이어 매핑

| 우선순위 | Test ID | 대상 모듈 | 테스트 파일 | 검증 초점 |
|---|---|---|---|---|
| **P0** | U-C02 | `input_validator.validate_input_contract` | `tests/boundary/test_input_validator.py` | `None` → `INPUT_NULL` |
| **P0** | U-C02-ext | 동일 | 동일 | `UIBoundary.submit(None)` → ErrorResponse + solver 0-call |
| **P0** | U-C03 | `input_validator` | 동일 | 행 수 ≠ 4 → `INPUT_ROW_COUNT` |
| **P0** | U-C04 | `input_validator` | 동일 | 열 수 ≠ 4 → `INPUT_COL_COUNT` |
| **P1** | U-C05~U-C09 | `input_validator` | 동일 | empty count / value range / duplicate |
| **P1** | RG-03 | `error_codes`, `ErrorMapper` | `tests/boundary/test_input_validator.py` 등 | message snapshot 8종 |
| **P2** | U-C11~U-C12 | `ui_boundary.UIBoundary` | `tests/boundary/test_ui_boundary.py` | 성공 경로 only (본 계획 범위 외 참조) |

### 2.2 우선순위 정의

| Level | 기준 | 실행 시점 |
|---|---|---|
| **P0** | AC-FR01-01~03 + BR-05 (Domain 0-call) | 매 commit / PR gate |
| **P1** | AC-FR01-04~06 (값·빈칸·중복) | FR-01 완료 전 필수 |
| **P2** | Error message regression, UX presentation | REFACTOR phase |

### 2.3 AAA 패턴 (rules/05)

```text
Arrange  — grid 입력 + MockSolver(또는 MagicMock) 주입
Act      — validate_input_contract(grid) 또는 boundary.submit(grid)
Assert   — ErrorCode / ErrorResponse + message + solver.call_count == 0
```

### 2.4 Dual-Track 규칙 (RG-05)

- Boundary 테스트는 **Domain 알고리즘을 assert하지 않는다** (magic sum, Case A/B 등).
- Domain은 **Mock / Protocol stub** 만 사용; `SolvePartialMagicSquare` 실구현 import 금지.

---

## 3. 경계값 케이스 목록

검증 순서: **null → row=4 → each row col=4 → …** (FR-01 Processing Rules).  
아래 케이스는 **크기·null 선행 검사** 구간에 해당한다.

| # | Case ID | 입력 (`grid`) | 기대 ErrorCode | 기대 message (§13 exact) | AC | Domain call |
|---|---|---|---|---|---|---|
| 1 | **BV-01** | `None` | `INPUT_NULL` | `Input matrix must not be null.` | AC-FR01-01 | **0** |
| 2 | **BV-02** | `[]` | `INPUT_ROW_COUNT` | `Matrix must have exactly 4 rows.` | AC-FR01-02 | **0** |
| 3 | **BV-03** | `[[]] * 4` | `INPUT_COL_COUNT` | `Each row must have exactly 4 columns.` | AC-FR01-03 | **0** |
| 4 | **BV-04** | 3×4 (3행×4열) | `INPUT_ROW_COUNT` | `Matrix must have exactly 4 rows.` | AC-FR01-02 | **0** |
| 5 | **BV-05** | 4×3 (4행×3열) | `INPUT_COL_COUNT` | `Each row must have exactly 4 columns.` | AC-FR01-03 | **0** |
| 6 | **BV-06** | 5×5 (5행×5열) | `INPUT_ROW_COUNT` | `Matrix must have exactly 4 rows.` | AC-FR01-02 | **0** |

### 3.1 입력 예시 (Arrange)

```python
# BV-01 — Anchor
grid = None

# BV-02
grid = []

# BV-03
grid = [[]] * 4

# BV-04
grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

# BV-05
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]

# BV-06
grid = [[1, 2, 3, 4, 5] for _ in range(5)]
```

### 3.2 기대 출력 (Assert — UIBoundary 경로)

Anchor **BV-01** 전체 응답:

```json
{
  "status": "ERROR",
  "code": "INPUT_NULL",
  "message": "Input matrix must not be null.",
  "result": null
}
```

크기 불일치 케이스(BV-02~06)는 동일하게 `status: "ERROR"`, `result: null`, code/message만 위 표와 일치.

### 3.3 명시적 제외

| 입력 | 제외 사유 |
|---|---|
| 4×4 정상 partial grid (빈칸 2, 값 유효) | AC-FR01-07 / U-C01 영역; 본 계획 **포함 금지** |

---

## 4. 예외·특이 케이스 목록

FR-01 크기·null 검사 이후 단계 또는 Boundary 방어 로직용. P1 이후 확장.

| # | Case ID | 입력 / 조건 | 기대 | AC | 비고 |
|---|---|---|---|---|---|
| E-01 | **Ragged row** | `[[1,2,3,4], [1,2,3], [1,2,3,4], [1,2,3,4]]` | `INPUT_COL_COUNT` | AC-FR01-03 | 행별 열 수 불균일 |
| E-02 | **bool 셀** | 4×4, 한 셀 `True` | `INPUT_VALUE_RANGE` | AC-FR01-04 | `isinstance(True, int)` 함정 |
| E-03 | **float 셀** | 4×4, 한 셀 `1.0` | `INPUT_VALUE_RANGE` | AC-FR01-04 | 정수형 아님 |
| E-04 | **행 원소 non-list** | `[1,2,3,4]` × 4 형태 아님, `matrix[0] = None` | `INPUT_COL_COUNT` 또는 예외 | — | Boundary 방어; 구현 정책 문서화 |
| E-05 | **첫 실패 중단** | `None`이 아닌 3×3 + 셀 `-1` | `INPUT_ROW_COUNT` | AC-FR01-02 | value 검사 **미진입** 확인 |
| E-06 | **BV-03 참조 동일성** | `[[]]*4` 후 `grid[0].append(1)` | `INPUT_COL_COUNT` | AC-FR01-03 | Python list alias; col≠4 유지 |
| E-07 | **반복 submit 결정성** | BV-01 동일 입력 2회 | 동일 ErrorResponse | NFR-03 | hash/ equality |
| E-08 | **matrix 불변** | BV-05 submit 전후 grid deep copy 비교 | 원본 unchanged | BR-16 / NFR-04 | Boundary가 in-place 수정 금지 |
| E-09 | **Unhandled exception** | Mock solver가 `RuntimeError` | `INTERNAL_ERROR` | U-C11 | 입력 통과 **후** 경로; FR-01 범위 외 참조 |

---

## 5. Domain 해결 진입점 호출 횟수 검증 전략 (Mock / Spy)

### 5.1 검증 대상

| 진입점 | 레이어 | 본 계획 기대 call_count |
|---|---|---|
| `PartialMagicSquareSolver.solve()` | Domain (Mock) | 입력 실패 시 **0** |
| `SolvePartialMagicSquare.execute()` | Domain (실구현) | Boundary 테스트에서 **호출 금지** |

### 5.2 전략 A — Protocol Mock + 호출 기록 (권장, 현재 코드베이스 패턴)

`tests/boundary/test_ui_boundary.py`의 `MockSolver` 패턴:

```python
@dataclass
class MockSolver:
    calls: list[list[list[int]]] = field(default_factory=list)

    def solve(self, matrix: list[list[int]]) -> list[int]:
        self.calls.append([row[:] for row in matrix])
        return MOCK_SOLUTION.copy()
```

**Assert:**

```python
response = boundary.submit(grid)
assert len(solver.calls) == 0
assert isinstance(response, ErrorResponse)
assert response.code is ErrorCode.INPUT_NULL  # BV-01 예
```

### 5.3 전략 B — `unittest.mock.create_autospec`

```python
from unittest.mock import create_autospec
from magicsquare.boundary.ui_boundary import PartialMagicSquareSolver

solver = create_autospec(PartialMagicSquareSolver, instance=True)
boundary = UIBoundary(solver)

boundary.submit(None)

solver.solve.assert_not_called()
```

### 5.4 전략 C — `MagicMock` spy (call_count)

```python
from unittest.mock import MagicMock

solver = MagicMock()
solver.solve.return_value = [3, 3, 6, 4, 4, 1]
boundary = UIBoundary(solver)

boundary.submit([])

assert solver.solve.call_count == 0
```

### 5.5 검증 매트릭스 (BV-01~06)

| Case | InputValidator 단독 | UIBoundary + Mock | `solve.call_count` |
|---|---|---|---|
| BV-01 | `INPUT_NULL` | ErrorResponse | 0 |
| BV-02 | `INPUT_ROW_COUNT` | ErrorResponse | 0 |
| BV-03 | `INPUT_COL_COUNT` | ErrorResponse | 0 |
| BV-04 | `INPUT_ROW_COUNT` | ErrorResponse | 0 |
| BV-05 | `INPUT_COL_COUNT` | ErrorResponse | 0 |
| BV-06 | `INPUT_ROW_COUNT` | ErrorResponse | 0 |

### 5.6 금지 사항

- Boundary 테스트에서 `SolvePartialMagicSquare` **실구현** 호출
- call_count 검증 없이 ErrorCode만 assert (BR-05 미검증)
- Domain Mock이 입력 실패 시에도 side effect 발생하도록 설정

---

## 6. 커버리지 목표

| 레이어 | 목표 | 측정 대상 패키지 | 근거 |
|---|---|---|---|
| **Domain (Entity)** | **≥ 95%** branch | `src/magicsquare/entity/` | NFR-01, rules/04 REFACTOR |
| **Boundary** | **≥ 85%** branch | `src/magicsquare/boundary/` | NFR-02 |
| **Control** | ≥ 80% branch | `src/magicsquare/control/` | rules/05 (Data tier) |
| **FR-01 본 계획** | InputValidator + UIBoundary submit 실패 경로 **100%** | `input_validator.py`, `ui_boundary.py` (fail branch) | AC-FR01-01~06 |

### 6.1 FR-01 관련 필수 커버 branch

- `validate_input_contract`: L36~39 (`None`, `len(matrix)`, `len(row)`)
- `UIBoundary.submit`: L59~61 (input_error early return — Domain 미호출)

---

## 7. pytest-cov 측정 전략

### 7.1 설치

```bash
pip install pytest-cov
```

### 7.2 전체 측정 (CI / 로컬 회귀)

```bash
pytest --cov=src --cov-report=term-missing
```

### 7.3 레이어별 측정 (목표 추적)

```bash
# Boundary — FR-01 집중
pytest tests/boundary/ \
  --cov=src/magicsquare/boundary \
  --cov-report=term-missing \
  --cov-fail-under=85

# Domain — Track B (별도 실행)
pytest tests/entity/ \
  --cov=src/magicsquare/entity \
  --cov-report=term-missing \
  --cov-fail-under=95
```

### 7.4 FR-01 앵커 전용 (본 계획 스모크)

```bash
pytest tests/boundary/test_input_validator.py::TestInputValidatorContract::test_null_matrix_returns_input_null \
       tests/boundary/ -k "null or row_count or col_count" \
  --cov=src/magicsquare/boundary/input_validator \
  --cov=src/magicsquare/boundary/ui_boundary \
  --cov-report=term-missing
```

### 7.5 리포트 정책

| 산출물 | 용도 |
|---|---|
| `term-missing` | 로컬 RED/GREEN 루프 — 미커버 라인 즉시 확인 |
| `html` *(선택)* | PR 리뷰 — `pytest --cov=src --cov-report=html` |
| `--cov-fail-under` | CI gate — Boundary 85, Entity 95 |

### 7.6 커버리지 해석 주의

- Boundary 테스트가 Domain 코드를 import하면 커버리지 **오염** 가능 → Track A는 Mock으로 Domain 실행 경로 차단.
- `input_validator` fail branch는 **Domain 0-call**과 쌍으로 검증; 커버리지만으로 BR-05 충족 판단 금지.

---

## 8. Traceability

| Business Rule | AC | Test Case | Test ID |
|---|---|---|---|
| BR-01 (4×4) | AC-FR01-02, 03 | BV-02~06 | U-C03, U-C04 |
| BR-05 (Domain 미호출) | AC-FR01-01~06 | BV-01~06 | U-C02~09 + call_count |
| §13 message | AC-FR01-* | 전 케이스 | RG-03 |

---

## 9. Definition of Done (본 Test Plan)

1. BV-01~06 pytest **GREEN**
2. 각 BV 케이스 **UIBoundary + Mock** 에서 `solve.call_count == 0` 확인
3. §13 message **exact match** (RG-03)
4. Boundary `input_validator` fail branch 커버리지 100%
5. 4×4 정상 입력 케이스는 **본 Plan 테스트 suite에 미포함**

---

**End of Test Plan v0.1**
