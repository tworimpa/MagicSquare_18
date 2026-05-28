# TDD Acceptance Criteria — 4×4 Magic Square

> **목적:** 생성 + 검증  
> **형식:** Given / When / Then (테스트 **명세**; 구현 코드·assert·프레임워크 문법 없음)  
> **불변 조건:** [01-problem-definition.md](01-problem-definition.md) INV-1~5  
> **Framing:** [02-problem-framing.md](02-problem-framing.md) SC-* / FS-*

---

## 참조: 알려진 유효 4×4 예시

아래 **Example Grid A**는 AC-V01, AC-G01, AC-G03에서 공통 사용한다.

| | c1 | c2 | c3 | c4 |
|---|---|---|---|---|
| **r1** | 16 | 3 | 2 | 13 |
| **r2** | 5 | 10 | 11 | 8 |
| **r3** | 9 | 6 | 7 | 12 |
| **r4** | 4 | 15 | 14 | 1 |

- 행·열·주대각·부대각 합 = **34**
- 값 {1,…,16} 순열

---

## 1. Validate — Happy Path

### AC-V01 — 알려진 유효 마방진

| | |
|---|---|
| **Given** | Example Grid A (완성 4×4, INV-1~2 만족) |
| **When** | Validate 실행 |
| **Then** | `valid: true` |
| **Invariant** | INV-3, INV-4, INV-5 (전체) |

### AC-V02 — magic sum 파생값 (선택 출력)

| | |
|---|---|
| **Given** | Example Grid A |
| **When** | Validate 실행 (magicSum 반환 옵션 활성) |
| **Then** | `valid: true` **且** `magicSum: 34` |
| **Invariant** | INV-3~5 파생 |

---

## 2. Validate — 마방진 규칙 위반 (FS-C*)

### AC-V03 — 한 행 합 불일치

| | |
|---|---|
| **Given** | Example Grid A에서 (1,1) 값 16 → 15로 변경 (나머지 동일) |
| **When** | Validate 실행 |
| **Then** | `valid: false`; violations에 **행 합** 규칙 포함 |
| **Invariant** | INV-3 위반 |

### AC-V04 — 한 열 합 불일치

| | |
|---|---|
| **Given** | Example Grid A에서 (1,2) 값 3 → 4로 변경 |
| **When** | Validate 실행 |
| **Then** | `valid: false`; violations에 **열 합** 규칙 포함 |
| **Invariant** | INV-4 위반 |

### AC-V05 — 주대각 합 불일치

| | |
|---|---|
| **Given** | Example Grid A에서 (2,2) 값 10 → 9로 변경 (행·열은 우연히 맞을 수 있으나 대각 깨짐) |
| **When** | Validate 실행 |
| **Then** | `valid: false`; violations에 **주대각** 규칙 포함 |
| **Invariant** | INV-5 (주대각) |

### AC-V06 — 부대각 합 불일치

| | |
|---|---|
| **Given** | Example Grid A에서 (1,4) 값 13 → 12로 변경 |
| **When** | Validate 실행 |
| **Then** | `valid: false`; violations에 **부대각** 규칙 포함 |
| **Invariant** | INV-5 (부대각) |

### AC-V07 — 부분 성공 착시 (행·열만 34)

| | |
|---|---|
| **Given** | 모든 행·열 합 = 34이나 주대각 합 ≠ 34인 4×4 배치 (反例 직접 구성) |
| **When** | Validate 실행 |
| **Then** | `valid: false` (부분 만족으로 true 금지) |
| **Invariant** | INV-5; STEP 2 "부분 성공 착시" 대응 |

---

## 3. Validate — 입력 구조·값 오류 (FS-A*, FS-B*)

### AC-V08 — 격자 크기 오류

| | |
|---|---|
| **Given** | 3×4 정수 배열 |
| **When** | Validate 실행 |
| **Then** | `valid: false` 또는 `INVALID_GRID_SIZE`; 마방진 규칙 검사 **수행 전** 거부 |
| **Invariant** | INV-1 |

### AC-V09 — 값 범위 오류

| | |
|---|---|
| **Given** | 4×4 배열, 한 셀 값 = 0 |
| **When** | Validate 실행 |
| **Then** | `INVALID_VALUE_RANGE` (완성 격자 전제 위반) |
| **Invariant** | INV-2 |

### AC-V10 — 중복

| | |
|---|---|
| **Given** | 4×4 배열, (1,1)과 (2,2) 모두 값 5, 나머지 1~16에서 5 제외 14개 |
| **When** | Validate 실행 |
| **Then** | `INVALID_DUPLICATE` |
| **Invariant** | INV-2 |

### AC-V11 — 누락 숫자

| | |
|---|---|
| **Given** | 4×4 배열, 1~15만 사용 (16 없음), 중복 없음 |
| **When** | Validate 실행 |
| **Then** | `INVALID_MISSING_VALUE` |
| **Invariant** | INV-2 |

### AC-V12 — null 입력

| | |
|---|---|
| **Given** | 입력 null |
| **When** | Validate 실행 |
| **Then** | `INPUT_NULL` |
| **Invariant** | — |

---

## 4. Generate — Happy Path

### AC-G01 — 생성 결과는 항상 유효

| | |
|---|---|
| **Given** | (입력 없음) |
| **When** | Generate 실행 → 결과 grid G |
| **Then** | Validate(G) → `valid: true` |
| **Invariant** | INV-1~5 전체 |

### AC-G02 — 결정적 생성 (seed 고정)

| | |
|---|---|
| **Given** | `seed = 42` |
| **When** | Generate(seed) 두 번 실행 |
| **Then** | 두 결과 grid **완전 동일** |
| **Invariant** | 재현성 (STEP 3) |

### AC-G03 — 생성 ≠ Example Grid A (다양성, 선택)

| | |
|---|---|
| **Given** | `seed = 1` |
| **When** | Generate(seed) |
| **Then** | Validate 통과 **且** 결과 ≠ Example Grid A (동일 배치만 반복하지 않음) |
| **Invariant** | Secondary capability "제시" |

---

## 5. Generate — Failure (계약 유지)

### AC-G04 — 생성 실패 코드 (방어)

| | |
|---|---|
| **Given** | (4×4 도메인: 항상 생성 가능) |
| **When** | Generate 내부 오류 시뮬레이션 (테스트 double) |
| **Then** | `GENERATION_FAILED`; Validate 호출 **없음** |
| **Invariant** | SC-03 보호 |

---

## 6. Traceability Matrix

| Invariant | Framing (FS/SC) | Acceptance Criteria |
|---|---|---|
| INV-1 4×4 | FS-A01,A02; SC-05 | AC-V08 |
| INV-2 순열 1~16 | FS-B01~03; SC-05 | AC-V09,V10,V11 |
| INV-3 행 합 | FS-C01; SC-02 | AC-V03, AC-V07 |
| INV-4 열 합 | FS-C02; SC-02 | AC-V04 |
| INV-5 대각 합 | FS-C03~05; SC-02 | AC-V05,V06,V07 |
| 전체 valid | SC-01 | AC-V01,V02 |
| Generate→Validate | SC-03,04; FS-D01 | AC-G01,G02,G03,G04 |
| null 입력 | FS-A03 | AC-V12 |

---

## 7. RED 우선 구현 순서 (TDD Roadmap)

| 순서 | AC ID | RED에서 기대 | 이유 |
|---|---|---|---|
| 1 | AC-V08, AC-V12 | 구조/null 거부 | 가장 바깥 계약 |
| 2 | AC-V09, AC-V10, AC-V11 | 값·집합 거부 | INV-2 |
| 3 | AC-V01 | Example Grid A → true | Validator happy path |
| 4 | AC-V03~V07 | 규칙 위반 → false | INV-3~5 분리 |
| 5 | AC-G01 | Generate → Validate pass | Secondary capability |
| 6 | AC-G02, AC-G03 | seed·다양성 | 재현성·데모 |
| 7 | AC-V02, AC-G04 | 선택·방어 | 부가 계약 |

---

## 8. 자기 검수 체크리스트

| 항목 | 상태 |
|---|---|
| INV-1~5 각각 ≥1 AC 연결 | ✓ |
| Happy path ≥1 (Validate) | ✓ AC-V01 |
| Failure path ≥6 (Validate) | ✓ AC-V03~V12 (10개) |
| Generate AC 존재 | ✓ AC-G01~G04 |
| Given/When/Then 형식 | ✓ |
| 구현 코드·테스트 코드 없음 | ✓ |
| Example Grid A 명시 | ✓ |

---

## 9. 후속 단계 (본 문서 범위 외)

- Dual-Track UI Boundary 계약 (입력 스키마·에러 메시지 고정)
- Domain / UI / Data 레이어 분리 설계
- 실제 테스트 코드 작성 (Red 단계)
