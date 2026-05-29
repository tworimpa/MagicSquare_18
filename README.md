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
| 6 | `docs/05-tdd-design.md` (권장) | TDD 설계 12섹션 — Turn 11 채팅 산출, 파일 저장 대기 |

## 구현 계약 (확정)

- **입력:** `int[4][4]` (0=빈칸, 빈칸 2개, 0 또는 1~16, non-zero 중복 금지)
- **출력:** `int[6]` = `[r1,c1,n1,r2,c2,n2]` (1-index; Case A/B 배치 규칙)

## Report · Prompt

| 폴더 | 파일 | 내용 |
|---|---|---|
| [Report/](Report/) | [00-project-progress-report.md](Report/00-project-progress-report.md) | 프로젝트 진행 보고서 |
| [Report/](Report/) | [03.qa-defect-list-ac-fr-01-01_Report.md](Report/03.qa-defect-list-ac-fr-01-01_Report.md) | QA 결함 분석·defect_list 세션 보고 |
| [Report/](Report/) | [04.dual-track-red-design-fr01-05_Report.md](Report/04.dual-track-red-design-fr01-05_Report.md) | FR-01~FR-05 Dual-Track RED 설계표 세션 |
| [Report/](Report/) | [05.red-skeleton-pytest-cov_Report.md](Report/05.red-skeleton-pytest-cov_Report.md) | RED Skeleton 25건·pytest-cov 세션 |
| [Prompt/](Prompt/) | [00-dialogue-transcript-export.md](Prompt/00-dialogue-transcript-export.md) | 대화형 Transcript Export |
| [Prompt/](Prompt/) | [03.qa-defect-list-ac-fr-01-01_Prompt.md](Prompt/03.qa-defect-list-ac-fr-01-01_Prompt.md) | 세션 03 Transcript Export |
| [Prompt/](Prompt/) | [04.dual-track-red-design-fr01-05_Prompt.md](Prompt/04.dual-track-red-design-fr01-05_Prompt.md) | 세션 04 Transcript Export |
| [Prompt/](Prompt/) | [05.red-skeleton-pytest-cov_Prompt.md](Prompt/05.red-skeleton-pytest-cov_Prompt.md) | 세션 05 Transcript Export |
| [Prompt/](Prompt/) | [01-executable-prompts-index.md](Prompt/01-executable-prompts-index.md) | 재실행용 프롬프트 모음 |

## RED 단계 To-Do 리스트

> 이 체크리스트는 [docs/test_plan.md](docs/test_plan.md) 기반으로 생성되었습니다.
> 각 항목은 RED(실패 테스트 작성) 완료 시 체크합니다.

### Track A — UI / Boundary 테스트
- [ ] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [ ] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [ ] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [ ] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [ ] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [ ] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [ ] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증

### Track B — Domain / Logic 테스트
- [ ] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [ ] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [ ] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [ ] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인

### 커버리지 목표
- [ ] Domain Logic: 95%+ (pip install pytest-cov)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결
- [x] [defect_list.md](defect_list.md) 생성 및 발견 결함 기록 (DEF-001~007, Open 5건)
- [ ] 모든 결함 수정 후 회귀 테스트 통과 확인

## 다음 단계

Domain RED 순서(D-F05 → D-H01)에 따라 `PartialGrid4x4` · `MagicSquareValidator`부터 TDD 시작.
