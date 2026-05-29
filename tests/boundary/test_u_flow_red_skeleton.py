"""Track A RED Skeleton — U-FLOW-02 extended (Report/04).

invalid input → SolvePartialMagicSquare.execute call_count == 0.
U-IN-01~03 flow cases: Report/08 — do not duplicate.
"""

from __future__ import annotations

import pytest

# from magicsquare.boundary.ui_boundary import UIBoundary

# Spy/mock: SolvePartialMagicSquare.execute or PartialMagicSquareSolver.solve


class TestUFlow02ExecuteZeroOnInvalid:
    """U-FLOW-02 — Domain 0-call on each invalid class."""

    def test_u_flow_02a_null_execute_call_count_zero(self) -> None:
        # Given — matrix = None; execute spy
        # When — UIBoundary.submit(None)
        pytest.fail("RED: U-FLOW-02a — null → execute.call_count==0")

    def test_u_flow_02b_invalid_size_execute_call_count_zero(self) -> None:
        # Given — matrix = []; execute spy
        # When — UIBoundary.submit([])
        pytest.fail("RED: U-FLOW-02b — invalid size → execute.call_count==0")

    def test_u_flow_02c_invalid_empty_count_execute_call_count_zero(self) -> None:
        # Given — G0 (0 blanks); execute spy
        # When — UIBoundary.submit(G0)
        pytest.fail("RED: U-FLOW-02c — empty count fail → execute.call_count==0")

    def test_u_flow_02d_invalid_value_range_execute_call_count_zero(self) -> None:
        # Given — 4×4, 2 zeros, -1; execute spy
        # When — UIBoundary.submit(matrix)
        pytest.fail("RED: U-FLOW-02d — value range fail → execute.call_count==0")

    def test_u_flow_02e_invalid_duplicate_execute_call_count_zero(self) -> None:
        # Given — 4×4, 2 zeros, duplicate non-zero; execute spy
        # When — UIBoundary.submit(matrix)
        pytest.fail("RED: U-FLOW-02e — duplicate fail → execute.call_count==0")
