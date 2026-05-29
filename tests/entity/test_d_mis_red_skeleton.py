"""Track B RED Skeleton — D-MIS-01 (Report/04).

Domain Mock forbidden.
"""

from __future__ import annotations

import pytest

# from magicsquare.entity.missing_number_finder import find_not_exist_nums


class TestDMis01MissingNumbers:
    """D-MIS-01 — G1 missing {7, 10} ascending."""

    def test_d_mis_01_g1_missing_seven_and_ten(self) -> None:
        # Given — G1
        # When — find_not_exist_nums(matrix)
        pytest.fail("RED: D-MIS-01 — G1 missing {7,10} sorted; 0 excluded")
