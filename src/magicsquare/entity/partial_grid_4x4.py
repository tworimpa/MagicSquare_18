"""부분 4×4 격자 분석 — 빈칸 좌표."""

from __future__ import annotations

from magicsquare.entity.constants import EMPTY_CELL_VALUE

Matrix4x4 = list[list[int]]
BlankCoord = tuple[int, int]


def find_blank_coords(matrix: Matrix4x4) -> tuple[BlankCoord, BlankCoord]:
    """row-major 순으로 빈칸 2개 좌표를 1-index로 반환한다.

    Args:
        matrix: 4×4 격자.

    Returns:
        첫·둘째 빈칸 ``(row, col)`` (1-index).
    """
    blanks: list[BlankCoord] = []
    for row_idx, row in enumerate(matrix):
        for col_idx, cell in enumerate(row):
            if cell == EMPTY_CELL_VALUE:
                blanks.append((row_idx + 1, col_idx + 1))
    first, second = blanks[0], blanks[1]
    return first, second
