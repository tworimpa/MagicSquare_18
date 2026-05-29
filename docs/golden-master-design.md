# Golden Master (GM-1 / GM-2) — Magic Square Solver

> **Test ID:** GM-1 (baseline) · GM-2 (pytest)  
> **대상:** `SolveFacade` + `DomainPartialMagicSquareSolver`  
> **기준 파일:** `tests/golden_master_expected.txt` (버전 관리 필수)

---

## 1. 목적

Solver의 **관찰 가능한 출력**(Success `result` / Error `code`+`message`)이 의도치 않게 바뀌면  
pytest가 `--- expected` / `+++ actual` unified diff와 함께 FAIL 한다.

---

## 2. GM-2 Test Case 매핑

| Test Case | Baseline 섹션 | 검증 |
|-----------|---------------|------|
| **GM-TC-01** | `normal_success` | Case A · int[6] · row-major · 1-index |
| **GM-TC-02** | `reverse_success` | Case B fallback · A 실패 후 B |
| **GM-TC-03** | `invalid_blank_count` | Error `INPUT_EMPTY_COUNT` (레거시 INVALID_BLANK_COUNT 대응) |
| **GM-TC-04** | `duplicate_number` | Error `INPUT_DUPLICATE` |
| **GM-TC-05** | `no_valid_solution` | Error `SOLVE_IMPOSSIBLE` |

---

## 3. 시나리오 (baseline 섹션)

| 섹션 | 의미 | 입력 요약 | 기대 결과 |
|------|------|-----------|-----------|
| `normal_success` | Case A 성공 | blanks (1,3),(2,2) | `[1, 3, 2, 2, 2, 10]` |
| `reverse_success` | Case B 성공 | blanks (3,3),(4,4) | `[3, 3, 6, 4, 4, 1]` |
| `invalid_blank_count` | 빈칸 수 위반 | 0 blanks (G0) | `INPUT_EMPTY_COUNT` |
| `duplicate_number` | non-zero 중복 | duplicate 5 | `INPUT_DUPLICATE` |
| `no_valid_solution` | Domain 해 없음 | G3 격자 | `SOLVE_IMPOSSIBLE` |

에러 코드는 SSOT `ErrorCode` enum 값을 사용한다.

---

## 4. Approve 패턴

| 조건 | 동작 |
|------|------|
| `golden_master_expected.txt` **없음** | 현재 출력으로 자동 생성 |
| **있음** | `open(path).read()` vs actual 문자열 비교 |
| **불일치** | `--- expected` / `+++ actual` / `@@` unified diff 후 FAIL |
| `GM_APPROVE=1` | baseline 덮어쓰기 (승인) |

---

## 5. GM-2 구현 구성

| 파일 | 역할 |
|------|------|
| `tests/golden_master_expected.txt` | Golden Master baseline |
| `tests/golden_master/harness.py` | 캡처·파싱·contract·diff |
| `tests/golden_master/test_golden_master_magic_square.py` | **GM-2** `@pytest.mark.golden_master` |
| `tests/golden_master/conftest.py` | 마커 등록 |
| `scripts/generate_golden_master.py` | baseline 생성 CLI |

**캡처 방식 (이중):**

1. **API Result serialization** — `capture_scenario_body()` (DTO → 텍스트)
2. **stdout capture** — `capture_stdout_scenario()` + `redirect_stdout`

---

## 6. 실행 예시

```powershell
# GM-2만 실행 (16건)
python -m pytest -m golden_master -o addopts="" -v

# 파일 지정
python -m pytest tests/golden_master/test_golden_master_magic_square.py -o addopts="" -v

# baseline 갱신
$env:GM_APPROVE="1"
python -m pytest -m golden_master -o addopts="" -v

# baseline 생성 스크립트
python scripts/generate_golden_master.py
```

**실행 결과 예시:**

```text
collected 88 items / 72 deselected / 16 selected
tests/golden_master/test_golden_master_magic_square.py::TestGoldenMasterApprove::test_gm2_full_baseline_file_compare PASSED
...
====================== 16 passed, 72 deselected in 0.22s ======================
```

**실패 시 출력 예시:**

```text
AssertionError: Golden Master [normal_success] mismatch
--- expected
Input:
16 3 0 13
...
+++ actual
Input:
...
@@ -5,6 +5,7 @@
```

---

## 7. Contract 검증 (GM-2)

| 규칙 | GM-TC | 검증 함수 |
|------|-------|-----------|
| int[6] 형식 | 01, 02 | `validate_solution6_format` |
| row-major 빈칸 순서 | 01, 02 | `validate_row_major_coords` |
| 1-index 좌표 ∈ [1,4] | 01, 02 | `validate_solution6_format` |
| 작은 수 우선 (Case A) | 01 | `validate_case_a_placement` |
| reverse fallback (Case B) | 02 | `validate_case_b_fallback` |
| Error Contract (SSOT message) | 03~05 | `validate_error_contract` |

---

## 8. 운영 규칙

1. 의도적 출력 변경 → `GM_APPROVE=1` → `git add tests/golden_master_expected.txt`
2. 테스트 약화·baseline 삭제 금지 (RG-01)
3. Domain 알고리즘 변경 시 GM-TC-01/02 반드시 재검토

---

**End of Golden Master Design**
