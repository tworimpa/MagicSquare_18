"""완성 4×4 마방진 판정."""

from __future__ import annotations

from magicsquare.entity.constants import (
    EMPTY_CELL_VALUE,
    GRID_SIZE,
    MAGIC_CONSTANT,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
)

Matrix4x4 = list[list[int]]


def _col_sums(matrix: Matrix4x4) -> list[int]:
    return [
        sum(matrix[row][col] for row in range(GRID_SIZE))
        for col in range(GRID_SIZE)
    ]


def _anti_diagonal_sum(matrix: Matrix4x4) -> int:
    return sum(matrix[row][GRID_SIZE - 1 - row] for row in range(GRID_SIZE))


def is_magic_square(matrix: Matrix4x4) -> bool:
    """완성 격자가 행·열·대각 합과 순열을 만족하는지 판정한다 (D-VAL-01/03).

    Args:
        matrix: 4×4 완성 격자 (0 없음, 1~16 순열).

    Returns:
        마방진이면 ``True``.
    """
    flat = [cell for row in matrix for cell in row]
    if EMPTY_CELL_VALUE in flat:
        return False
    if len(set(flat)) != GRID_SIZE * GRID_SIZE:
        return False
    if set(flat) != set(range(MIN_CELL_VALUE, MAX_CELL_VALUE + 1)):
        return False
    if any(sum(row) != MAGIC_CONSTANT for row in matrix):
        return False
    if any(total != MAGIC_CONSTANT for total in _col_sums(matrix)):
        return False
    if sum(matrix[row][row] for row in range(GRID_SIZE)) != MAGIC_CONSTANT:
        return False
    if _anti_diagonal_sum(matrix) != MAGIC_CONSTANT:
        return False
    return True
