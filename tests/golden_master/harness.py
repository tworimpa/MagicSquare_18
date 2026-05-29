"""Golden Master harness — 시나리오 실행·직렬화·approve 비교."""

from __future__ import annotations

import ast
import difflib
import re
from dataclasses import dataclass
from pathlib import Path

from magicsquare.boundary.error_codes import ERROR_MESSAGES, ErrorCode
from magicsquare.boundary.response_models import SuccessResponse
from magicsquare.control.domain_solver import DomainPartialMagicSquareSolver
from magicsquare.control.solve_facade import SolveFacade
from magicsquare.entity.completion_strategy import try_case_a, try_case_b
from magicsquare.entity.partial_grid_4x4 import find_blank_coords, find_not_exist_nums

Matrix4x4 = list[list[int]]
Solution6 = list[int]

DEFAULT_EXPECTED_PATH = Path(__file__).resolve().parent.parent / "golden_master_expected.txt"

# Case A 성공 — blanks (1,3),(2,2); missing {2,10}
GRID_NORMAL_SUCCESS: Matrix4x4 = [
    [16, 3, 0, 13],
    [5, 0, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# Case B 성공 — blanks (3,3),(4,4); missing {1,6}
GRID_REVERSE_SUCCESS: Matrix4x4 = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

# 0 blanks (complete grid)
GRID_INVALID_BLANK_COUNT: Matrix4x4 = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# duplicate non-zero 5
GRID_DUPLICATE_NUMBER: Matrix4x4 = [
    [16, 3, 2, 0],
    [5, 10, 5, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 0],
]

# both Case A/B fail
GRID_NO_VALID_SOLUTION: Matrix4x4 = [
    [0, 0, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
]

SCENARIO_GRIDS: dict[str, Matrix4x4] = {
    "normal_success": GRID_NORMAL_SUCCESS,
    "reverse_success": GRID_REVERSE_SUCCESS,
    "invalid_blank_count": GRID_INVALID_BLANK_COUNT,
    "duplicate_number": GRID_DUPLICATE_NUMBER,
    "no_valid_solution": GRID_NO_VALID_SOLUTION,
}

SCENARIO_ORDER: tuple[str, ...] = (
    "normal_success",
    "reverse_success",
    "invalid_blank_count",
    "duplicate_number",
    "no_valid_solution",
)

# GM-2 Test Case ID → baseline section (docs/golden-master-design.md)
GM_TC_SCENARIOS: dict[str, str] = {
    "GM-TC-01": "normal_success",
    "GM-TC-02": "reverse_success",
    "GM-TC-03": "invalid_blank_count",
    "GM-TC-04": "duplicate_number",
    "GM-TC-05": "no_valid_solution",
}

GM_TC_ORDER: tuple[str, ...] = tuple(GM_TC_SCENARIOS.keys())

_SECTION_HEADER = re.compile(r"^\[[a-z][a-z0-9_]*\]$")


@dataclass(frozen=True, slots=True)
class GoldenMasterDocument:
    """파싱된 Golden Master 기준 문서."""

    sections: dict[str, str]

    def serialize(self) -> str:
        """섹션 순서를 유지한 텍스트 표현을 반환한다."""
        blocks: list[str] = []
        for name in SCENARIO_ORDER:
            if name not in self.sections:
                continue
            blocks.append(f"[{name}]")
            blocks.append(self.sections[name].rstrip())
            blocks.append("")
        return "\n".join(blocks).rstrip() + "\n"


def format_grid(matrix: Matrix4x4) -> str:
    """4×4 격자를 공백 구분 행 텍스트로 포맷한다."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in matrix)


def format_matrix_inline(matrix: Matrix4x4) -> list[list[int]]:
    """격자 복사본을 반환한다."""
    return [row[:] for row in matrix]


def _solve_facade() -> SolveFacade:
    return SolveFacade(DomainPartialMagicSquareSolver())


def capture_scenario_body(name: str, matrix: Matrix4x4) -> str:
    """단일 시나리오의 Golden Master 본문( Input/Output 또는 Error )을 생성한다."""
    response = _solve_facade().solve(format_matrix_inline(matrix))
    lines = ["Input:", format_grid(matrix)]

    if isinstance(response, SuccessResponse):
        lines.extend(["Output:", str(response.result)])
        return "\n".join(lines)

    lines.extend(
        [
            "Error:",
            response.code.value,
            "Message:",
            response.message,
        ]
    )
    return "\n".join(lines)


def capture_stdout_scenario(name: str, matrix: Matrix4x4) -> str:
    """CLI 스타일 stdout 캡처용 — 섹션 헤더 + 본문."""
    return f"[{name}]\n{capture_scenario_body(name, matrix)}"


def read_expected_text(path: Path) -> str:
    """기준 파일 전체 텍스트를 읽는다."""
    return path.read_text(encoding="utf-8")


def assert_text_equals(expected: str, actual: str, label: str) -> None:
    """open(expected).read() vs actual 비교 — 불일치 시 diff 출력."""
    if expected == actual:
        return
    diff = unified_diff(expected, actual, label)
    raise AssertionError(
        f"Golden Master [{label}] mismatch — set GM_APPROVE=1 to update baseline\n"
        f"--- expected\n{expected}\n+++ actual\n{actual}\n{diff}"
    )


def assert_section_matches(
    path: Path,
    section_name: str,
    *,
    approve: bool = False,
) -> str:
    """단일 섹션 approve 패턴 — 없으면 전체 파일 생성."""
    matrix = SCENARIO_GRIDS[section_name]
    actual_body = capture_scenario_body(section_name, matrix)

    if approve or not path.is_file():
        write_expected_file(path)
        return actual_body

    document = parse_document(read_expected_text(path))
    expected_body = document.sections.get(section_name)
    if expected_body is None:
        write_expected_file(path)
        return actual_body

    assert_text_equals(expected_body, actual_body, section_name)
    return actual_body


def parse_solution6(body: str) -> Solution6:
    """섹션 본문에서 Output Solution6를 파싱한다."""
    lines = body.splitlines()
    try:
        output_idx = lines.index("Output:")
    except ValueError as exc:
        raise ValueError("Output: block not found") from exc
    return ast.literal_eval(lines[output_idx + 1].strip())


def parse_error_contract(body: str) -> tuple[ErrorCode, str]:
    """섹션 본문에서 Error 계약을 파싱한다."""
    lines = body.splitlines()
    error_idx = lines.index("Error:")
    message_idx = lines.index("Message:")
    code = ErrorCode(lines[error_idx + 1].strip())
    message = lines[message_idx + 1].strip()
    return code, message


def validate_solution6_format(result: Solution6) -> None:
    """int[6] 형식·1-index·값 범위 불변조건."""
    assert len(result) == 6
    r1, c1, n1, r2, c2, n2 = result
    for coord in (r1, c1, r2, c2):
        assert 1 <= coord <= 4
    for value in (n1, n2):
        assert 1 <= value <= 16
    assert n1 != n2


def validate_row_major_coords(matrix: Matrix4x4, result: Solution6) -> None:
    """row-major 빈칸 순서와 Solution6 좌표 일치."""
    first, second = find_blank_coords(matrix)
    r1, c1, _, r2, c2, _ = result
    assert (r1, c1) == first
    assert (r2, c2) == second


def validate_case_a_placement(matrix: Matrix4x4, result: Solution6) -> None:
    """작은 수 우선(Case A) — smaller→first, larger→second."""
    first, second = find_blank_coords(matrix)
    smaller, larger = find_not_exist_nums(matrix)
    case_a = try_case_a(matrix, first, second, smaller, larger)
    assert case_a is not None
    assert result == case_a
    r1, c1, n1, r2, c2, n2 = result
    assert n1 == smaller and n2 == larger


def validate_case_b_fallback(matrix: Matrix4x4, result: Solution6) -> None:
    """reverse fallback(Case B) — Case A 실패 후 larger→first."""
    first, second = find_blank_coords(matrix)
    smaller, larger = find_not_exist_nums(matrix)
    assert try_case_a(matrix, first, second, smaller, larger) is None
    case_b = try_case_b(matrix, first, second, smaller, larger)
    assert case_b is not None
    assert result == case_b
    r1, c1, n1, r2, c2, n2 = result
    assert n1 == larger and n2 == smaller


def validate_error_contract(code: ErrorCode, message: str) -> None:
    """Error Contract — SSOT ERROR_MESSAGES 완전 일치."""
    assert message == ERROR_MESSAGES[code]


def generate_document() -> GoldenMasterDocument:
    """모든 시나리오를 실행해 Golden Master 문서를 생성한다."""
    sections = {
        name: capture_scenario_body(name, grid)
        for name, grid in SCENARIO_GRIDS.items()
    }
    return GoldenMasterDocument(sections=sections)


def parse_document(text: str) -> GoldenMasterDocument:
    """Golden Master 텍스트 파일을 파싱한다."""
    sections: dict[str, str] = {}
    current_name: str | None = None
    current_lines: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if _SECTION_HEADER.match(line):
            if current_name is not None:
                sections[current_name] = "\n".join(current_lines).strip()
            current_name = line[1:-1]
            current_lines = []
            continue
        if current_name is not None:
            current_lines.append(line)

    if current_name is not None:
        sections[current_name] = "\n".join(current_lines).strip()

    return GoldenMasterDocument(sections=sections)


def write_expected_file(path: Path, document: GoldenMasterDocument | None = None) -> Path:
    """기준 파일을 디스크에 기록한다."""
    doc = document or generate_document()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc.serialize(), encoding="utf-8")
    return path


def unified_diff(expected: str, actual: str, label: str) -> str:
    """두 문서의 unified diff를 반환한다."""
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile=f"{label} (expected)",
            tofile=f"{label} (actual)",
        )
    )


def assert_matches_expected(
    path: Path,
    *,
    approve: bool = False,
) -> GoldenMasterDocument:
    """approve 패턴 — 없으면 생성, 있으면 비교.

    Args:
        path: 기준 파일 경로.
        approve: True면 현재 출력으로 기준 파일을 갱신한다.

    Returns:
        기대 문서.

    Raises:
        AssertionError: 불일치 시 unified diff와 함께 실패.
    """
    actual_doc = generate_document()

    if approve or not path.is_file():
        write_expected_file(path, actual_doc)
        return actual_doc

    expected_doc = parse_document(path.read_text(encoding="utf-8"))
    expected_text = expected_doc.serialize()
    actual_text = actual_doc.serialize()

    if expected_text != actual_text:
        diff = unified_diff(expected_text, actual_text, path.name)
        raise AssertionError(
            "Golden Master mismatch — run with GM_APPROVE=1 to update baseline:\n"
            f"--- expected\n{expected_text}+++ actual\n{actual_text}{diff}"
        )

    return expected_doc
