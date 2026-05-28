# 실행용 프롬프트 모음 (Executable Prompts Index)

> Turn 2·3에서 생성된 **재실행 가능** 프롬프트. Cursor 채팅에 복사·붙여넣기하여 사용.

---

## Prompt-A — TDD 설계 문서 생성 (Meta-Prompt)

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

**출처:** Turn 9 (현재)

```markdown
1. Report/ 폴더에 프로젝트 진행 보고서 생성
2. Prompt/ 폴더에 대화형 transcript export
   - Turn별 User/Assistant
   - 실행용 프롬프트 index
   - 보안 정보(토큰) 제외
```

---

## 프롬프트 체인 (권장 순서)

```
Prompt-C (문제정의)
  → Prompt-D (문서화)
  → Prompt-B (Clean Architecture)
  → Prompt-A (TDD 설계 문서 — 선택)
  → Prompt-E (Report Export)
  → [구현 단계] Domain RED TDD
```

---

## 관련 파일

| 파일 | 설명 |
|---|---|
| [00-dialogue-transcript-export.md](00-dialogue-transcript-export.md) | Turn별 대화 전체 |
| [../Report/00-project-progress-report.md](../Report/00-project-progress-report.md) | 진행 보고서 |
| [../docs/](../docs/) | 설계 산출물 |
