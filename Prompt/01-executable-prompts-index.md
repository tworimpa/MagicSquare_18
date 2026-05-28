# 실행용 프롬프트 모음 (Executable Prompts Index)

> Turn 2·10·11에서 생성된 **재실행 가능** 프롬프트. Cursor 채팅에 복사·붙여넣기하여 사용.  
> **권장:** TDD 설계 문서 생성은 **Prompt-F** (= Prompt-A′ 전체 실행) 사용.

---

## Prompt-F — TDD 설계 문서 실행 (권장, = A′ 전체)

**출처:** Turn 11  
**목적:** `docs/05-tdd-design.md` 본문 1회 생성 (채팅 또는 파일 저장)  
**선행:** `@docs/01` ~ `@docs/04`, `@README.md` 컨텍스트 첨부  
**금지:** 구현, 테스트 코드, (지시 시) 파일 수정

> **전문:** Turn 11 User 메시지와 동일. 아래 **Prompt-A′** 블록 전체를 붙여넣으면 된다.

---

## Prompt-A′ — TDD 설계 Meta-Prompt (강화판)

**출처:** Turn 10  
**목적:** 01~04·README와 정합된 12섹션 TDD 설계 문서 생성 지시  
**대비 Prompt-A:** 전역 Solve 계약, AC-V/G·D-* 매핑, RED-1~8, 반例, 4방향 추적

```markdown
# 역할
너는 **4×4 Magic Square TDD 설계 문서**를 작성하는 **시스템 설계·명세·TDD 전략 전문가**다.
목표는 “코드를 짜는 것”이 아니라, **Red → Green → Refactor**를 시작하기 전에 팀이 합의할 **테스트 가능한 설계 명세**를 한 문서로 고정하는 것이다.

# 지금 하지 말 것 (엄격)
- 소스 코드, 테스트 코드, 의사코드, 알고리즘 구현
- 파일 생성·수정·삭제 (이번 턴에서는 **채팅 응답으로 문서 본문만** 출력)
- UI 구현, DB, API, 배포, 성능 최적화 논의
- “나중에 정하자”식 모호 표현

# 반드시 읽고 정합시킬 기존 산출물
| 파일 | 활용 |
|---|---|
| `docs/01-problem-definition.md` | INV-1~5, 목적(생성+검증) |
| `docs/02-problem-framing.md` | SC-*, FS-* |
| `docs/03-acceptance-criteria.md` | AC-* |
| `docs/04-dual-track-clean-architecture-design.md` | 레이어·도메인·전역 계약 |
| `README.md` | 입출력 계약, Domain RED |

**전역 계약(고정):** 입력 `int[4][4]`(0×2), 출력 `int[6]` 1-index Case A/B/C, magic sum 34, 검증 Primary + Solve Secondary.

# 산출물: `docs/05-tdd-design.md` 권장, 한국어 Markdown, mermaid 1개

# 문서 필수 구조 (12섹션)
1. 문서 개요  2. 문제 정의 요약  3. 시스템 경계
4. 기능 단위 (ValidateMagicSquare, SolvePartialMagicSquare, Generate)
5. TDD 설계 원칙  6. AC 매핑 + 반例≥3
7. RED 로드맵 (PartialGrid4x4→Validator→Analyzer→Strategy→Solve)
8. 데이터·계약 모델  9. 실패 처리  10. TDD 사이클 + mermaid
11. Out of Scope≥8  12. 구현 착수 체크리스트

# 작성 품질: 검증 가능 Then, 4방향 추적 표, 용어 통일, 모호 금지
# 말미 자기 검수 Y/N 체크리스트 8항목
# 출력: 섹션 1~12 + 자기 검수를 단일 응답으로 완료
```

> **전체 실행판:** 위 요약을 확장한 **Turn 11 전문**은 [00-dialogue-transcript-export.md](00-dialogue-transcript-export.md) Turn 11 참조. 재실행 시 Turn 11 User 블록 또는 본 세션에서 붙여넣은 **Prompt-F 전문** 사용.

---

## Prompt-A — TDD 설계 문서 생성 (Meta-Prompt, 초안)

**출처:** Turn 2  
**목적:** 4×4 Magic Square **TDD 설계 문서** 1회 생성  
**금지:** 구현, 파일 수정, 테스트 코드

```markdown
# 역할
너는 **4×4 Magic Square TDD 설계 문서**를 작성하는 **시스템 설계·명세 전문가**다.

# 지금 하지 말 것
- 구현·알고리즘·의사코드·파일 생성/수정·테스트 코드

# 프로젝트 전제
- 목적: **생성 + 검증** (유효 배치 제시 + 자동 판정)
- Invariant: 4×4, 1~16 순열, 행·열·주대각·부대각 합 동일 (magic sum 34)

# 산출물 구조 (12섹션)
1. 문서 개요
2. 문제 정의 요약
3. 시스템 경계
4. 기능 단위 분해 (ValidateMagicSquare, GenerateMagicSquare)
5. TDD 설계 원칙
6. Acceptance Criteria (Given/When/Then, 코드 X)
7. RED 로드맵
8. 데이터·계약 모델 (개념만)
9. 실패 처리
10. TDD 사이클 연결
11. Out of Scope
12. 구현 착수 전 체크리스트

# 작성 규칙
- 한국어, Markdown, mermaid 1개, 모호 표현 금지
- 말미 자기 검수 체크리스트 포함

위 구조대로 설계 문서 전체를 작성하라.
```

---

## Prompt-B — Dual-Track Clean Architecture 설계

**출처:** Turn 3, 8  
**목적:** Domain/UI/Data/Integration **설계 문서** (구현 X)

```markdown
당신은 Dual-Track UI + Logic TDD 및 Clean Architecture 설계 전문가입니다.

프로젝트: Magic Square (4x4) — TDD 연습용
목적: 레이어 분리 + 계약 기반 테스트 + 리팩토링 훈련

제약:
- 구현 코드 X
- UI = Boundary, Data = save/load 인터페이스

입력: 4x4 int[][] (0=빈칸×2, 0|1~16, non-zero 중복 금지)
출력: int[6]=[r1,c1,n1,r2,c2,n2] (1-index, Case A/B)

필수 출력 구조:
# 1) Logic Layer — 1.1~1.5
# 2) Screen Layer — 2.1~2.4 (에러 메시지 8종 완전 일치)
# 3) Data Layer — 3.1~3.4 (InMemory 추천)
# 4) Integration — 4.1~4.5 (Traceability Matrix)

추가: 모호 표현 금지, 검증 가능, 표/체크리스트 적극 사용
```

---

## Prompt-C — 문제 정의 STEP 1–5

**출처:** Turn 1, 4

```markdown
당신은 문제 정의 전문가입니다.
4x4 Magic Square — STEP 1(관찰) ~ STEP 5(진짜 문제 정의)를 작성하라.

제약: 구현·코드·알고리즘 금지, Markdown

STEP 5 포함:
- 표면/개선 문제 정의
- Invariant 5개
- 훈련 사고 능력 6종
```

---

## Prompt-D — Plan → 문서 파일 생성

**출처:** Turn 4

```markdown
Implement the plan: STEP 1–5 문제 정의 + STEP 6 Framing + Acceptance Criteria.
Do NOT edit the plan file.

생성:
- docs/01-problem-definition.md
- docs/02-problem-framing.md
- docs/03-acceptance-criteria.md
- README.md 업데이트

To-do: confirm-purpose, step6-framing, acceptance-criteria
```

---

## Prompt-E — Report & Transcript Export

**출처:** Turn 9, Turn 12, Turn 19, Turn 22  
**목적:** 진행 보고서 + 대화 transcript + 프롬프트 인덱스 일괄 갱신

```markdown
다음 순서로 실행해줘.
1. Report/ 폴더에 프로젝트 진행 보고서 생성 (또는 갱신)
2. Prompt/ 폴더에 현재까지 프롬프트 전체를 대화형 transcript로 Export
   - Turn별 User/Assistant 요약
   - 실행용 프롬프트 index 반영
   - GitHub PAT 등 보안 정보 제외
```

**단축형 (Turn 22):**

```markdown
보고서 내보내주는 것과 프롬프트 저장
```

---

## 프롬프트 체인 (권장 순서)

```
Prompt-C (문제정의)
  → Prompt-D (문서화 docs/01~03)
  → Prompt-B (Clean Architecture docs/04)
  → Prompt-A′ / Prompt-F (TDD 설계 docs/05)
  → Cursor Rules (.cursorrules → .cursor/rules/*.mdc)
  → Prompt-E (Report + Transcript Export)
  → [구현] Domain RED (D-F05 → D-H01)
```

---

## 관련 파일

| 파일 | 설명 |
|---|---|
| [00-dialogue-transcript-export.md](00-dialogue-transcript-export.md) | Turn 1~22 대화 전체 |
| [../Report/00-project-progress-report.md](../Report/00-project-progress-report.md) | 진행 보고서 |
| [../docs/](../docs/) | 설계 산출물 |
