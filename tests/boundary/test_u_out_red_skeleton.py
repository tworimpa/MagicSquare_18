"""Track A RED Skeleton — U-OUT-01~03 (Report/04).

TDD phase: RED (Skeleton) — pytest.fail only; Domain Mock for UIBoundary only (comments).
"""

from __future__ import annotations

import pytest

# from magicsquare.boundary.ui_boundary import UIBoundary

# G1 + Mock execute returning [2, 2, 7, 3, 3, 10] — see Report/04 §3.2


class TestUOut01ResultLength:
    """U-OUT-01 — success result length 6."""

    def test_u_out_01_success_result_length_six(self) -> None:
        # Given — G1 contract-valid partial grid
        # Arrange — PartialMagicSquareSolver mock → [2, 2, 7, 3, 3, 10]
        # When — UIBoundary.submit(matrix) or solve(matrix)
        pytest.fail("RED: U-OUT-01 — OK result len(result)==6")


class TestUOut02OneIndexCoordinates:
    """U-OUT-02 — r,c ∈ [1,4] 1-index; G1 → (2,2),(3,3)."""

    def test_u_out_02_coordinates_one_indexed(self) -> None:
        # Given — G1 + mock [2, 2, 7, 3, 3, 10]
        # When — UIBoundary.submit(G1)
        pytest.fail("RED: U-OUT-02 — 1-index coords (2,2) and (3,3)")


class TestUOut03ValidInputExecuteOnce:
    """U-OUT-03 — valid G1 → execute/solve exactly once (U-FLOW-03)."""

    def test_u_out_03_valid_g1_execute_called_once(self) -> None:
        # Given — G1; SolvePartialMagicSquare.execute spy/mock
        # When — UIBoundary.submit(G1)
        # Then (future) — execute.call_count == 1; arg deep-equal G1
        pytest.fail("RED: U-OUT-03 — valid input → execute.call_count==1")
