"""Integration — IT-OK01 valid puzzle end-to-end."""

from __future__ import annotations

from magicsquare.boundary.response_models import SuccessResponse
from magicsquare.control.domain_solver import DomainPartialMagicSquareSolver
from magicsquare.control.solve_facade import SolveFacade

GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


class TestItOk01ValidG1Solve:
    """IT-OK01 — SolveFacade + Domain solver returns Solution6 for G1."""

    def test_it_ok01_valid_g1_returns_domain_solution6(self) -> None:
        # Given
        facade = SolveFacade(DomainPartialMagicSquareSolver())
        matrix = [row[:] for row in GRID_G1]

        # When
        response = facade.solve(matrix)

        # Then
        assert isinstance(response, SuccessResponse)
        assert response.result == [2, 2, 10, 3, 3, 7]
