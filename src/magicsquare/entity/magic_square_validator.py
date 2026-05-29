"""완성 4×4 마방진 판정."""

from __future__ import annotations

from magicsquare.entity.constants import GRID_SIZE, MAGIC_CONSTANT

Matrix4x4 = list[list[int]]


def is_magic_square(matrix: Matrix4x4) -> bool:
    """완성 격자의 행·주대각 합이 Magic Constant인지 판정한다 (D-VAL-02/04).

    Args:
        matrix: 4×4 완성 격자.

    Returns:
        행·주대각 합이 모두 M이면 ``True``.
    """
    if any(sum(row) != MAGIC_CONSTANT for row in matrix):
        return False
    if sum(matrix[row][row] for row in range(GRID_SIZE)) != MAGIC_CONSTANT:
        return False
    return True
