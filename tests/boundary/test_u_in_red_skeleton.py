"""Track A — U-IN-04~08 (Report/04).

U-IN-01~03: `test_ac_fr_01_01_red.py` — duplicate forbidden.
U-IN-04~08: GREEN (C-01~03).
"""

from __future__ import annotations

from magicsquare.boundary.error_codes import ErrorCode
from magicsquare.boundary.input_validator import validate_input_contract

# G0 — Example Grid A (complete, 0 empty cells)
GRID_G0: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# G1 — blanks (2,2) and (3,3) 1-index; missing {7, 10}
GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


class TestUIn04FourByThree:
    """U-IN-04 — 4×3 → INPUT_COL_COUNT (Test Plan BV-05)."""

    def test_u_in_04_four_by_three_returns_e001(self) -> None:
        # Given — 4 rows × 3 cols
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]

        # When
        result = validate_input_contract(matrix)

        # Then
        assert result is ErrorCode.INPUT_COL_COUNT


class TestUIn05FiveByFive:
    """U-IN-05 — 5×5 → INPUT_ROW_COUNT (Test Plan BV-06)."""

    def test_u_in_05_five_by_five_returns_e001(self) -> None:
        # Given
        matrix = [[1, 2, 3, 4, 5] for _ in range(5)]

        # When
        result = validate_input_contract(matrix)

        # Then
        assert result is ErrorCode.INPUT_ROW_COUNT


class TestUIn06ZeroEmptyCells:
    """U-IN-06 — 0 empty cells (G0) → INPUT_EMPTY_COUNT."""

    def test_u_in_06_zero_empty_cells_returns_e002(self) -> None:
        # Given — G0 complete grid (no zeros)
        matrix = [row[:] for row in GRID_G0]

        # When
        result = validate_input_contract(matrix)

        # Then
        assert result is ErrorCode.INPUT_EMPTY_COUNT


class TestUIn07ThreeEmptyCells:
    """U-IN-07 — 3 empty cells → INPUT_EMPTY_COUNT."""

    def test_u_in_07_three_empty_cells_returns_e002(self) -> None:
        # Given — G1 with additional 0 (3 blanks total)
        matrix = [row[:] for row in GRID_G1]
        matrix[0][0] = 0

        # When
        result = validate_input_contract(matrix)

        # Then
        assert result is ErrorCode.INPUT_EMPTY_COUNT


class TestUIn08NegativeCell:
    """U-IN-08 — cell -1 with exactly 2 zeros → INPUT_VALUE_RANGE."""

    def test_u_in_08_negative_cell_returns_e004(self) -> None:
        # Given — 4×4, 2 zeros, one cell -1
        matrix = [
            [0, 3, 2, 13],
            [5, 10, -1, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 0],
        ]

        # When
        result = validate_input_contract(matrix)

        # Then
        assert result is ErrorCode.INPUT_VALUE_RANGE


class TestUIn09DuplicateNonZero:
    """U-IN-09 — duplicate non-zero with 2 zeros → INPUT_DUPLICATE."""

    def test_u_in_09_duplicate_non_zero_returns_e005(self) -> None:
        # Given — 4×4, 2 zeros, duplicate 5
        matrix = [
            [16, 3, 2, 0],
            [5, 10, 5, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 0],
        ]

        # When
        result = validate_input_contract(matrix)

        # Then
        assert result is ErrorCode.INPUT_DUPLICATE


class TestUIn10SeventeenCell:
    """U-IN-10 — cell 17 with 2 zeros → INPUT_VALUE_RANGE."""

    def test_u_in_10_seventeen_cell_returns_e004(self) -> None:
        # Given — 4×4, 2 zeros, one cell 17
        matrix = [
            [16, 3, 2, 13],
            [5, 10, 17, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 0],
        ]

        # When
        result = validate_input_contract(matrix)

        # Then
        assert result is ErrorCode.INPUT_VALUE_RANGE


class TestUIn09DuplicateNonZero:
    """U-IN-09 — duplicate non-zero with 2 zeros → INPUT_DUPLICATE."""

    def test_u_in_09_duplicate_non_zero_returns_e005(self) -> None:
        # Given — 4×4, 2 zeros, duplicate 5
        matrix = [
            [16, 3, 2, 0],
            [5, 10, 5, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 0],
        ]

        # When
        result = validate_input_contract(matrix)

        # Then
        assert result is ErrorCode.INPUT_DUPLICATE


class TestUIn10SeventeenCell:
    """U-IN-10 — cell 17 with 2 zeros → INPUT_VALUE_RANGE."""

    def test_u_in_10_seventeen_cell_returns_e004(self) -> None:
        # Given — 4×4, 2 zeros, one cell 17
        matrix = [
            [16, 3, 2, 13],
            [5, 10, 17, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 0],
        ]

        # When
        result = validate_input_contract(matrix)

        # Then
        assert result is ErrorCode.INPUT_VALUE_RANGE
