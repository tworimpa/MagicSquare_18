"""Boundary 에러 코드 — docs/04 §2.4 message 완전 일치."""

from enum import Enum


class ErrorCode(str, Enum):
    """UI Boundary 표준 Error Code."""

    INPUT_NULL = "INPUT_NULL"
    INPUT_ROW_COUNT = "INPUT_ROW_COUNT"
    INPUT_COL_COUNT = "INPUT_COL_COUNT"
    INPUT_VALUE_RANGE = "INPUT_VALUE_RANGE"
    INPUT_EMPTY_COUNT = "INPUT_EMPTY_COUNT"
    INPUT_DUPLICATE = "INPUT_DUPLICATE"
    SOLVE_IMPOSSIBLE = "SOLVE_IMPOSSIBLE"
    INTERNAL_ERROR = "INTERNAL_ERROR"


ERROR_MESSAGES: dict[ErrorCode, str] = {
    ErrorCode.INPUT_NULL: "Input matrix must not be null.",
    ErrorCode.INPUT_ROW_COUNT: "Matrix must have exactly 4 rows.",
    ErrorCode.INPUT_COL_COUNT: "Each row must have exactly 4 columns.",
    ErrorCode.INPUT_VALUE_RANGE: (
        "Each cell must be 0 or an integer from 1 to 16."
    ),
    ErrorCode.INPUT_EMPTY_COUNT: (
        "Matrix must contain exactly 2 empty cells (0)."
    ),
    ErrorCode.INPUT_DUPLICATE: "Non-zero values must not be duplicated.",
    ErrorCode.SOLVE_IMPOSSIBLE: (
        "No valid magic square completion exists for the given grid."
    ),
    ErrorCode.INTERNAL_ERROR: "An unexpected error occurred.",
}
