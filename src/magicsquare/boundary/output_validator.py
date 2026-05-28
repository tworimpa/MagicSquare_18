"""출력 포맷 검증 — int[6] Solution6 계약."""

from __future__ import annotations

from magicsquare.entity.constants import (
    GRID_SIZE,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
    SOLUTION_LENGTH,
)

Solution6 = list[int]


def validate_output_format(result: Solution6) -> bool:
    """Domain ``int[6]`` 출력 형식을 검증한다.

    Args:
        result: ``[r1,c1,n1,r2,c2,n2]`` (1-index).

    Returns:
        형식이 유효하면 True.
    """
    if len(result) != SOLUTION_LENGTH:
        return False

    coords = (result[0], result[1], result[3], result[4])
    values = (result[2], result[5])

    if not all(MIN_CELL_VALUE <= coord <= GRID_SIZE for coord in coords):
        return False
    if not all(MIN_CELL_VALUE <= value <= MAX_CELL_VALUE for value in values):
        return False
    if values[0] == values[1]:
        return False
    return True
