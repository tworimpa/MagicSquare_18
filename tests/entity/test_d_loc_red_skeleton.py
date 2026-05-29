"""Track B — D-LOC-01 (Report/04)."""

from __future__ import annotations

from magicsquare.entity.partial_grid_4x4 import find_blank_coords

GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


class TestDLoc01BlankCoordinates:
    """D-LOC-01 — G1 row-major blanks (2,2) and (3,3) 1-index."""

    def test_d_loc_01_g1_blank_coords_row_major(self) -> None:
        # Given
        matrix = [row[:] for row in GRID_G1]

        # When
        first, second = find_blank_coords(matrix)

        # Then
        assert first == (2, 2)
        assert second == (3, 3)
