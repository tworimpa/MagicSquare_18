"""Track A — U-IN-04~08 (Report/04).

U-IN-01~03: `test_ac_fr_01_01_red.py` — duplicate forbidden.
U-IN-04~05: GREEN (C-01). U-IN-06~08: RED skeleton.
"""

from __future__ import annotations

import pytest

from magicsquare.boundary.error_codes import ErrorCode
from magicsquare.boundary.input_validator import validate_input_contract

# G0 — complete grid (0 empty cells): see tests/entity/conftest.py GRID_G0 comment
# G1 — three empties variant: G1 + one extra 0


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
    """U-IN-06 — 0 empty cells (G0) → E002."""

    def test_u_in_06_zero_empty_cells_returns_e002(self) -> None:
        # Given — G0 complete grid (no zeros)
        # When — validate_input_contract(matrix)
        pytest.fail("RED: U-IN-06 — G0 zero empties → E002 INPUT_EMPTY_COUNT")


class TestUIn07ThreeEmptyCells:
    """U-IN-07 — 3 empty cells → E002."""

    def test_u_in_07_three_empty_cells_returns_e002(self) -> None:
        # Given — G1 with additional 0 (3 blanks total)
        # When — validate_input_contract(matrix)
        pytest.fail("RED: U-IN-07 — 3 empties → E002 INPUT_EMPTY_COUNT")


class TestUIn08NegativeCell:
    """U-IN-08 — cell -1 with exactly 2 zeros → E004."""

    def test_u_in_08_negative_cell_returns_e004(self) -> None:
        # Given — 4×4, 2 zeros, one cell -1
        # When — validate_input_contract(matrix) after size+empty pass
        pytest.fail("RED: U-IN-08 — -1 → E004 INPUT_VALUE_RANGE")
