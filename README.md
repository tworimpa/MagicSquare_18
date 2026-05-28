# Magic Square 4×4 — TDD 연습 프로젝트

4×4 마방진 **생성 + 검증**을 TDD·명세 우선 방식으로 다루기 위한 문제 정의 문서 모음.

## 문서

| 순서 | 파일 | 내용 |
|---|---|---|
| 1 | [docs/01-problem-definition.md](docs/01-problem-definition.md) | STEP 1–5: 관찰, Why, 진짜 문제 정의, Invariant |
| 2 | [docs/02-problem-framing.md](docs/02-problem-framing.md) | STEP 6: 사용자, 성공 기준, 실패 시나리오 |
| 3 | [docs/03-acceptance-criteria.md](docs/03-acceptance-criteria.md) | TDD Acceptance Criteria (Given/When/Then) |

## 확정된 목적

- **Primary:** 마방진 **자동 판정** (Validate)
- **Secondary:** 유효한 배치 **생성·제시** (Generate)
- **Non-goal:** 사용자 퍼즐 UI, n×n 일반화, 최적화

## 다음 단계

구현 전: Acceptance Criteria RED 순서(§7)에 따라 Domain Validate부터 TDD 시작.
