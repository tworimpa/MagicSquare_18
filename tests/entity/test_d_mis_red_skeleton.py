"""Track B — D-MIS-01 (Report/04)."""

from __future__ import annotations

from magicsquare.entity.partial_grid_4x4 import find_not_exist_nums

GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


class TestDMis01MissingNumbers:
    """D-MIS-01 — G1 missing {7, 10} ascending."""

    def test_d_mis_01_g1_missing_seven_and_ten(self) -> None:
        # Given
        matrix = [row[:] for row in GRID_G1]

        # When
        missing = find_not_exist_nums(matrix)

        # Then
        assert missing == [7, 10]
