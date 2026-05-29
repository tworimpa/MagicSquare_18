"""Case A/B 완성 전략."""

from __future__ import annotations

from magicsquare.entity.magic_square_validator import is_magic_square
from magicsquare.entity.partial_grid_4x4 import BlankCoord, Matrix4x4

Solution6 = list[int]


def _filled_grid(
    matrix: Matrix4x4,
    first: BlankCoord,
    second: BlankCoord,
    first_value: int,
    second_value: int,
) -> Matrix4x4:
    """빈칸에 숫자를 채운 복사 격자를 반환한다."""
    filled = [row[:] for row in matrix]
    r1, c1 = first
    r2, c2 = second
    filled[r1 - 1][c1 - 1] = first_value
    filled[r2 - 1][c2 - 1] = second_value
    return filled


def try_case_a(
    matrix: Matrix4x4,
    first: BlankCoord,
    second: BlankCoord,
    smaller: int,
    larger: int,
) -> Solution6 | None:
    """Case A: smaller→first, larger→second."""
    filled = _filled_grid(matrix, first, second, smaller, larger)
    if not is_magic_square(filled):
        return None
    r1, c1 = first
    r2, c2 = second
    return [r1, c1, smaller, r2, c2, larger]


def try_case_b(
    matrix: Matrix4x4,
    first: BlankCoord,
    second: BlankCoord,
    smaller: int,
    larger: int,
) -> Solution6 | None:
    """Case B: larger→first, smaller→second."""
    filled = _filled_grid(matrix, first, second, larger, smaller)
    if not is_magic_square(filled):
        return None
    r1, c1 = first
    r2, c2 = second
    return [r1, c1, larger, r2, c2, smaller]
