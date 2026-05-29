"""Track B RED Skeleton — D-LOC-01 (Report/04).

Domain Mock forbidden. TDD phase: RED (Skeleton).
"""

from __future__ import annotations

import pytest

# from magicsquare.entity.blank_finder import find_blank_coords


class TestDLoc01BlankCoordinates:
    """D-LOC-01 — G1 row-major blanks (2,2) and (3,3) 1-index."""

    def test_d_loc_01_g1_blank_coords_row_major(self) -> None:
        # Given — G1 (tests/entity/conftest.py GRID_G1)
        # When — find_blank_coords(matrix)
        pytest.fail("RED: D-LOC-01 — G1 blanks (2,2) and (3,3) 1-index")
