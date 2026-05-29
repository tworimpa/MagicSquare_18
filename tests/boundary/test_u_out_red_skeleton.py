"""Track A — U-OUT-01~03 (Report/04)."""

from __future__ import annotations

from dataclasses import dataclass, field

from magicsquare.boundary.response_models import SuccessResponse
from magicsquare.boundary.ui_boundary import UIBoundary
from tests.boundary.test_u_in_red_skeleton import GRID_G1

G1_SOLUTION: list[int] = [2, 2, 7, 3, 3, 10]


@dataclass
class MockSolver:
    """Domain Mock — Boundary U-OUT 계약 전용."""

    result: list[int] = field(default_factory=lambda: G1_SOLUTION.copy())
    calls: list[list[list[int]]] = field(default_factory=list)

    def solve(self, matrix: list[list[int]]) -> list[int]:
        """Mock solve."""
        self.calls.append([row[:] for row in matrix])
        return self.result.copy()


class TestUOut01ResultLength:
    """U-OUT-01 — success result length 6."""

    def test_u_out_01_success_result_length_six(self) -> None:
        # Given
        solver = MockSolver()
        boundary = UIBoundary(solver)
        matrix = [row[:] for row in GRID_G1]

        # When
        response = boundary.submit(matrix)

        # Then
        assert isinstance(response, SuccessResponse)
        assert len(response.result) == 6


class TestUOut02OneIndexCoordinates:
    """U-OUT-02 — r,c ∈ [1,4] 1-index; G1 → (2,2),(3,3)."""

    def test_u_out_02_coordinates_one_indexed(self) -> None:
        # Given
        solver = MockSolver()
        boundary = UIBoundary(solver)
        matrix = [row[:] for row in GRID_G1]

        # When
        response = boundary.submit(matrix)

        # Then
        assert isinstance(response, SuccessResponse)
        r1, c1, _, r2, c2, _ = response.result
        assert (r1, c1) == (2, 2)
        assert (r2, c2) == (3, 3)


class TestUOut03ValidInputExecuteOnce:
    """U-OUT-03 — valid G1 → solve exactly once (U-FLOW-03)."""

    def test_u_out_03_valid_g1_execute_called_once(self) -> None:
        # Given
        solver = MockSolver()
        boundary = UIBoundary(solver)
        matrix = [row[:] for row in GRID_G1]

        # When
        boundary.submit(matrix)

        # Then
        assert len(solver.calls) == 1
        assert solver.calls[0] == matrix
