# Magic Square — TDD 문서·체크리스트

> 프로젝트 개요·환경 설정: [루트 README](../README.md)

---

## RED 단계 To-Do 리스트

| # | 작업 | 상태 |
|---|------|------|
| 1 | SSOT 확인 (`docs/03`, `docs/04`, `docs/test_plan.md`) | ✅ |
| 2 | RED skeleton / assert 배선 (`tests/`) | ✅ |
| 3 | pytest RED 확인 후 `src/` 최소 GREEN | ✅ C-00~C-15 |
| 4 | Dual-Track 혼합 금지 (Boundary Mock / Domain 순수) | ✅ |
| 5 | 전체 pytest GREEN (`88 passed`) | ✅ |
| 6 | Golden Master 회귀 안전장치 (아래 GM-01~10) | ✅ |
| 7 | REFACTOR 착수 전 GM PASS 재확인 | 🔲 |

---

### Golden Master 회귀 안전장치

Refactoring 시작 전 구축.  
GREEN 완료 후 즉시 적용.

#### 기준 파일 생성

- [x] **GM-01:** `golden_master_expected.txt` 생성 — `tests/golden_master_expected.txt`
- [x] **GM-02:** 정상/역순/오류 시나리오 추가 — `normal_success`, `reverse_success`, `invalid_blank_count`, `duplicate_number`, `no_valid_solution`
- [x] **GM-03:** `git add tests/golden_master_expected.txt` (버전 관리 포함)

#### 테스트 코드

- [x] **GM-04:** `test_golden_master_magic_square` 작성 — `tests/golden_master/test_golden_master_magic_square.py`
- [x] **GM-05:** approve 패턴 적용 — `GM_APPROVE=1`, `assert_matches_expected`, `assert_section_matches`
- [x] **GM-06:** Golden Master 테스트 PASS 확인 — `pytest -m golden_master -v` → 16 passed

#### 회귀 보호

- [x] **GM-07:** row-major 규칙 보호 — `validate_row_major_coords` (GM-TC-01/02)
- [x] **GM-08:** 1-index 출력 보호 — `validate_solution6_format` (좌표 ∈ [1,4])
- [x] **GM-09:** reverse 조합 fallback 보호 — `validate_case_b_fallback` (GM-TC-02)
- [x] **GM-10:** Error Contract 보호 — `validate_error_contract` + SSOT `ERROR_MESSAGES` (GM-TC-03~05)

**실행**

```powershell
python -m pytest -m golden_master -o addopts="" -v
python scripts/generate_golden_master.py
```

**설계 SSOT:** [golden-master-design.md](golden-master-design.md) · **세션 보고:** [Report/08.golden-master-gm01-gm02_Report.md](../Report/08.golden-master-gm01-gm02_Report.md)

---

## 관련 문서

| 파일 | 내용 |
|------|------|
| [01-problem-definition.md](01-problem-definition.md) | 문제 정의·Invariant |
| [03-acceptance-criteria.md](03-acceptance-criteria.md) | Given/When/Then AC |
| [04-dual-track-clean-architecture-design.md](04-dual-track-clean-architecture-design.md) | Dual-Track 설계 |
| [test_plan.md](test_plan.md) | FR-01 Test Plan |
| [golden-master-design.md](golden-master-design.md) | GM approve·GM-TC 매핑 |
