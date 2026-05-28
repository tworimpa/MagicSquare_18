# Magic Square 4×4 — TDD 연습 프로젝트

4×4 마방진 TDD·Clean Architecture 연습 프로젝트.

## 문서

| 순서 | 파일 | 내용 |
|---|---|---|
| 1 | [docs/01-problem-definition.md](docs/01-problem-definition.md) | STEP 1–5: 관찰, Why, 진짜 문제 정의, Invariant |
| 2 | [docs/02-problem-framing.md](docs/02-problem-framing.md) | STEP 6: 사용자, 성공 기준, 실패 시나리오 |
| 3 | [docs/03-acceptance-criteria.md](docs/03-acceptance-criteria.md) | TDD Acceptance Criteria (Given/When/Then) |
| 4 | [docs/04-dual-track-clean-architecture-design.md](docs/04-dual-track-clean-architecture-design.md) | Dual-Track UI + Logic / Clean Architecture 설계 |

## 구현 계약 (확정)

- **입력:** `int[4][4]` (0=빈칸, 빈칸 2개, 0 또는 1~16, non-zero 중복 금지)
- **출력:** `int[6]` = `[r1,c1,n1,r2,c2,n2]` (1-index; Case A/B 배치 규칙)

## Report · Prompt

| 폴더 | 파일 | 내용 |
|---|---|---|
| [Report/](Report/) | [00-project-progress-report.md](Report/00-project-progress-report.md) | 프로젝트 진행 보고서 |
| [Prompt/](Prompt/) | [00-dialogue-transcript-export.md](Prompt/00-dialogue-transcript-export.md) | 대화형 Transcript Export |
| [Prompt/](Prompt/) | [01-executable-prompts-index.md](Prompt/01-executable-prompts-index.md) | 재실행용 프롬프트 모음 |

## 다음 단계

Domain RED 순서(D-F05 → D-H01)에 따라 `PartialGrid4x4` · `MagicSquareValidator`부터 TDD 시작.
