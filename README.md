# Magic Square 4×4 — TDD 연습 프로젝트

4×4 마방진 TDD·Clean Architecture 연습 프로젝트.

## 문서

| 순서 | 파일 | 내용 |
|---|---|---|
| 1 | [docs/01-problem-definition.md](docs/01-problem-definition.md) | STEP 1–5: 관찰, Why, 진짜 문제 정의, Invariant |
| 2 | [docs/02-problem-framing.md](docs/02-problem-framing.md) | STEP 6: 사용자, 성공 기준, 실패 시나리오 |
| 3 | [docs/03-acceptance-criteria.md](docs/03-acceptance-criteria.md) | TDD Acceptance Criteria (Given/When/Then) |
| 4 | [docs/04-dual-track-clean-architecture-design.md](docs/04-dual-track-clean-architecture-design.md) | Dual-Track UI + Logic / Clean Architecture 설계 |
| 5 | [docs/test_plan.md](docs/test_plan.md) | FR-01 Input Verification Test Plan (AC-FR01-01 앵커) |
| 6 | [docs/README.md](docs/README.md) | RED To-Do · Golden Master GM-01~10 체크리스트 |
| 7 | `docs/05-tdd-design.md` (권장) | TDD 설계 12섹션 — Turn 11 채팅 산출, 파일 저장 대기 |

## 구현 계약 (확정)

- **입력:** `int[4][4]` (0=빈칸, 빈칸 2개, 0 또는 1~16, non-zero 중복 금지)
- **출력:** `int[6]` = `[r1,c1,n1,r2,c2,n2]` (1-index; Case A/B 배치 규칙)
- **에러 코드 SSOT:** `src/magicsquare/boundary/error_codes.py` — `INPUT_NULL`, `INPUT_ROW_COUNT`, `INPUT_COL_COUNT` 등 8종 (`INVALID_SIZE`는 PRD에 없음)

## 개발 환경 · pytest

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

`pytest` 기본 실행 시 HTML 리포트가 자동 생성된다 (`pyproject.toml` `addopts`).

| 산출물 | 경로 | 내용 |
|---|---|---|
| 테스트 결과 | `reports/pytest-report.html` | 통과/실패·traceback |
| 커버리지 | `htmlcov/index.html` | 라인·브랜치 커버리지 |

```powershell
python -m pytest
Start-Process reports\pytest-report.html
Start-Process htmlcov\index.html
```

커버리지·HTML 리포트 없이 실행: `python -m pytest --no-cov --override-ini="addopts=-v"`

## Report · Prompt

| 폴더 | 파일 | 내용 |
|---|---|---|
| [Report/](Report/) | [00-project-progress-report.md](Report/00-project-progress-report.md) | 프로젝트 진행 보고서 |
| [Report/](Report/) | [03.qa-defect-list-ac-fr-01-01_Report.md](Report/03.qa-defect-list-ac-fr-01-01_Report.md) | QA 결함 분석·defect_list 세션 보고 |
| [Report/](Report/) | [04.dual-track-red-design-fr01-05_Report.md](Report/04.dual-track-red-design-fr01-05_Report.md) | FR-01~FR-05 Dual-Track RED 설계표 세션 |
| [Report/](Report/) | [05.red-skeleton-pytest-cov_Report.md](Report/05.red-skeleton-pytest-cov_Report.md) | RED Skeleton 25건·pytest-cov 세션 |
| [Report/](Report/) | [06.ac-fr-01-01-green-null-grid_Report.md](Report/06.ac-fr-01-01-green-null-grid_Report.md) | AC-FR-01-01 GREEN (grid=None) 세션 |
| [Report/](Report/) | [07.pytest-html-reports_Report.md](Report/07.pytest-html-reports_Report.md) | pytest HTML 테스트·커버리지 리포트 자동 생성 |
| [Report/](Report/) | [08.golden-master-gm01-gm02_Report.md](Report/08.golden-master-gm01-gm02_Report.md) | Golden Master GM-1 baseline·GM-2 회귀 테스트 |
| [Prompt/](Prompt/) | [00-dialogue-transcript-export.md](Prompt/00-dialogue-transcript-export.md) | 대화형 Transcript Export |
| [Prompt/](Prompt/) | [03.qa-defect-list-ac-fr-01-01_Prompt.md](Prompt/03.qa-defect-list-ac-fr-01-01_Prompt.md) | 세션 03 Transcript Export |
| [Prompt/](Prompt/) | [04.dual-track-red-design-fr01-05_Prompt.md](Prompt/04.dual-track-red-design-fr01-05_Prompt.md) | 세션 04 Transcript Export |
| [Prompt/](Prompt/) | [05.red-skeleton-pytest-cov_Prompt.md](Prompt/05.red-skeleton-pytest-cov_Prompt.md) | 세션 05 Transcript Export |
| [Prompt/](Prompt/) | [06.ac-fr-01-01-green-null-grid_Prompt.md](Prompt/06.ac-fr-01-01-green-null-grid_Prompt.md) | 세션 06 Transcript Export |
| [Prompt/](Prompt/) | [07.pytest-html-reports_Prompt.md](Prompt/07.pytest-html-reports_Prompt.md) | 세션 07 Transcript Export |
| [Prompt/](Prompt/) | [08.golden-master-gm01-gm02_Prompt.md](Prompt/08.golden-master-gm01-gm02_Prompt.md) | 세션 08 Transcript Export (GM-1·GM-2) |
| [Prompt/](Prompt/) | [01-executable-prompts-index.md](Prompt/01-executable-prompts-index.md) | 재실행용 프롬프트 모음 |

## GREEN 진행 (Track A — FR-01)

> SSOT: [docs/test_plan.md](docs/test_plan.md) BV-01~06 · 커밋 묶음 **C-00** 완료 (`green(C-00): align ac_fr tests to INPUT_* SSOT`)

| Commit | Test ID | 상태 |
|---|---|---|
| **C-00** | U-C02, U-IN-01~03 (null·size) | ✅ GREEN — `test_ac_fr_01_01_red.py` 9건, `test_input_validator` U-C02 |
| **C-01** | U-IN-04, U-IN-05 | ✅ GREEN — 4×3 `INPUT_COL_COUNT`, 5×5 `INPUT_ROW_COUNT` |
| **C-02** | U-IN-06, U-IN-07 | ✅ GREEN — G0/G1 empty count → `INPUT_EMPTY_COUNT` |
| **C-03** | U-IN-08 | ✅ GREEN — `input_validator` value range (검증만, src 무변경) |
| **C-04** | U-FLOW-02a/b | ✅ GREEN — null·size zero-call (검증만) |
| **C-05** | U-FLOW-02c-e | ✅ GREEN — empty·value·dup zero-call (검증만) |
| **C-06** | U-OUT-01~03 | ✅ GREEN — output contract (검증만) |
| **C-07** | D-LOC-01 | ✅ GREEN — `find_blank_coords` |
| **C-08** | D-MIS-01 | ✅ GREEN — `find_not_exist_nums` |
| **C-09** | D-VAL-02/04 | ✅ GREEN — row·주대각 |
| **C-10** | D-VAL-01/03 | ✅ GREEN — G0 true·열 합 |
| **C-11** | D-VAL-05/06 | ✅ GREEN — 0 셀 거부 |
| **C-12** | D-SOL-01/04 | ✅ GREEN — G1 Case B |
| **C-13** | D-SOL-02/03 | ✅ GREEN — G2 Case B, G3 unsolvable (src 검증만) |
| **C-14** | U-IN-09/10 | ✅ GREEN — duplicate·17 (src 검증만) |
| **C-15** | IT-OK01 | ✅ GREEN — `DomainPartialMagicSquareSolver` |
| **GM-1** | Golden Master | ✅ `tests/golden_master_expected.txt` (5 scenarios) |
| **GM-2** | Golden Master tests | ✅ `tests/test_gm_01_magic_square_golden_master.py` (16건) |
| **GM-3** | docs README | ✅ [docs/README.md](docs/README.md) GM-01~10 체크리스트 |

**최근 pytest:** `88 passed` · `python -m pytest tests/test_gm_01_magic_square_golden_master.py -v`

> **TDD 분리:** `red(C-03~C-12)` = tests/ 배선만 · `green(C-0X)` = src/ 최소 구현만

## AC-FR-01-01 체크리스트 (Test Plan BV 기준)

> [docs/test_plan.md](docs/test_plan.md) BV-01~06 · `tests/boundary/test_ac_fr_01_01_red.py`

### Track A — UI / Boundary
- [x] TC-A-01: `grid=None` → `ErrorResponse` 반환 (BV-01)
- [x] TC-A-02: `code`가 `INPUT_NULL` (SSOT `ErrorCode`)
- [x] TC-A-03: `message`가 `ERROR_MESSAGES[INPUT_NULL]`과 문자 단위 동일
- [x] TC-A-04: `grid=None` 시 Domain `solve` 0회 호출 (spy/mock)
- [x] TC-A-05: `grid=[]` → `INPUT_ROW_COUNT` (BV-02)
- [x] TC-A-06: `grid=3×4` → `INPUT_ROW_COUNT` (BV-04)
- [x] TC-A-07: 반환 타입 `ErrorResponse`, 행 0열 `[[]]*4` → `INPUT_COL_COUNT` (BV-03)

### Track B — Domain 격리 (AC-FR-01-01 범위)
- [x] TC-B-01: Boundary가 `None` 분기 처리 — Domain에 `None` 미전달
- [x] TC-B-02: `grid=None` 후 `solve` 미호출
- [x] TC-B-03: `solve` 호출 시 테스트 실패 처리
- [x] TC-B-04: AC-FR-01-02~05 전용 케이스 모듈 미포함

### 커버리지 목표
- [ ] Domain Logic: 95%+ (현재 ~89%, `htmlcov/index.html`)
- [x] Boundary Layer: 85%+ (현재 ~90%+, `htmlcov/index.html` 참고)
- [x] 전체 TOTAL: 90%+ (현재 ~92%)

### 결함 목록
- [x] [defect_list.md](defect_list.md) 생성 (DEF-001~007)
- [x] DEF-001~005: 테스트 SSOT 정렬 (C-00)
- [x] DEF-006: README `INPUT_*` 반영 (본 갱신)
- [x] DEF-007: `test_ac_fr_01_01_red.py` docstring SSOT 정렬 (C-00)
- [x] RED skeleton 27건 GREEN 완료 — 전체 `72 passed`

## 다음 단계

1. Domain 커버리지 95%+ (anti-diagonal·Case A 경로)
2. IT-F01/02 — `SOLVE_IMPOSSIBLE`·Repository (Post-MVP)
3. REFACTOR — `solve_facade` vs `domain_solver` 정리
