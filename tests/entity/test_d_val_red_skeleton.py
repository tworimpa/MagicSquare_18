"""Track B — D-VAL-01~06 (Report/04)."""

from __future__ import annotations

from magicsquare.entity.magic_square_validator import is_magic_square

GRID_G0: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


class TestDVal01CompleteGridTrue:
    """D-VAL-01 — G0 → true."""

    def test_d_val_01_g0_complete_grid_is_magic(self) -> None:
        # Given
        matrix = [row[:] for row in GRID_G0]

        # When
        result = is_magic_square(matrix)

        # Then
        assert result is True


class TestDVal02RowSumMismatch:
    """D-VAL-02 — row sum ≠ M → false."""

    def test_d_val_02_g0_row_sum_mismatch_false(self) -> None:
        # Given — (1,1): 16→15
        matrix = [row[:] for row in GRID_G0]
        matrix[0][0] = 15

        # When
        result = is_magic_square(matrix)

        # Then
        assert result is False


class TestDVal03ColSumMismatch:
    """D-VAL-03 — col sum ≠ M → false."""

    def test_d_val_03_g0_col_sum_mismatch_false(self) -> None:
        # Given — (1,2): 3→4
        matrix = [row[:] for row in GRID_G0]
        matrix[0][1] = 4

        # When
        result = is_magic_square(matrix)

        # Then
        assert result is False


class TestDVal04DiagonalMismatch:
    """D-VAL-04 — main diagonal ≠ M → false."""

    def test_d_val_04_g0_main_diagonal_mismatch_false(self) -> None:
        # Given — (2,2): 10→9
        matrix = [row[:] for row in GRID_G0]
        matrix[1][1] = 9

        # When
        result = is_magic_square(matrix)

        # Then
        assert result is False


class TestDVal05PermutationViolation:
    """D-VAL-05 — duplicate / missing 1~16 → false."""

    def test_d_val_05_permutation_violation_false(self) -> None:
        # Given — 16 twice, 1 missing
        matrix = [row[:] for row in GRID_G0]
        matrix[3][3] = 16

        # When
        result = is_magic_square(matrix)

        # Then
        assert result is False


class TestDVal06ZeroInCompleteGrid:
    """D-VAL-06 — 0 in complete grid → false."""

    def test_d_val_06_zero_in_complete_grid_false(self) -> None:
        # Given
        matrix = [row[:] for row in GRID_G0]
        matrix[0][0] = 0

        # When
        result = is_magic_square(matrix)

        # Then
        assert result is False
