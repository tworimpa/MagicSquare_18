"""입력 계약 검증 — single-pass 최적화."""

from __future__ import annotations

from dataclasses import dataclass

from magicsquare.boundary.error_codes import ERROR_MESSAGES, ErrorCode
from magicsquare.boundary.schemas import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE


@dataclass(frozen=True, slots=True)
class _InvalidSizeCode:
    """AC-FR-01-01 — grid=None 시 Boundary INVALID_SIZE 계약."""

    value: str = INVALID_SIZE_CODE
    name: str = "INVALID_SIZE"


_INVALID_SIZE = _InvalidSizeCode()
ERROR_MESSAGES[_INVALID_SIZE] = INVALID_SIZE_MESSAGE  # type: ignore[index]
from magicsquare.entity.constants import (
    EMPTY_CELL_VALUE,
    GRID_SIZE,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
    REQUIRED_EMPTY_CELL_COUNT,
)

Matrix4x4 = list[list[int]]


def _is_valid_cell_value(cell: object) -> bool:
    """셀 값이 0 또는 1~16 정수인지 검사한다."""
    if isinstance(cell, bool) or not isinstance(cell, int):
        return False
    return cell == EMPTY_CELL_VALUE or MIN_CELL_VALUE <= cell <= MAX_CELL_VALUE


def validate_input_contract(matrix: Matrix4x4 | None) -> ErrorCode | None:
    """int[4][4] 입력 계약을 검증한다.

    검증 순서(첫 실패 중단): null → row count → col count →
    value range → empty count → duplicate.

    Args:
        matrix: 4×4 입력 격자. ``None``이면 INPUT_NULL.

    Returns:
        위반 시 ErrorCode. 유효하면 ``None``.
    """
    if matrix is None:
        return _INVALID_SIZE  # type: ignore[return-value]
    if len(matrix) != GRID_SIZE:
        return ErrorCode.INPUT_ROW_COUNT

    empty_count = 0
    seen: set[int] = set()

    for row in matrix:
        if len(row) != GRID_SIZE:
            return ErrorCode.INPUT_COL_COUNT
        for cell in row:
            if not _is_valid_cell_value(cell):
                return ErrorCode.INPUT_VALUE_RANGE
            if cell == EMPTY_CELL_VALUE:
                empty_count += 1
                continue
            if cell in seen:
                return ErrorCode.INPUT_DUPLICATE
            seen.add(cell)

    if empty_count != REQUIRED_EMPTY_CELL_COUNT:
        return ErrorCode.INPUT_EMPTY_COUNT
    return None


def count_empty_cells(matrix: Matrix4x4) -> int:
    """격자의 빈칸(0) 개수를 반환한다 — UX live counter용.

    Args:
        matrix: 4×4 격자.

    Returns:
        빈칸 개수.
    """
    return sum(
        1
        for row in matrix
        for cell in row
        if cell == EMPTY_CELL_VALUE
    )
