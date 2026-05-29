"""Golden Master harness — 시나리오 실행·직렬화·approve 비교."""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from pathlib import Path

from magicsquare.boundary.response_models import SuccessResponse
from magicsquare.control.domain_solver import DomainPartialMagicSquareSolver
from magicsquare.control.solve_facade import SolveFacade

Matrix4x4 = list[list[int]]

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
            f"{diff}"
        )

    return expected_doc
