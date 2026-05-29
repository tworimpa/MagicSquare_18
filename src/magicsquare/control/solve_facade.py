"""Solve Use Case Facade — Boundary와 Domain 연결."""

from __future__ import annotations

from magicsquare.boundary.ui_boundary import (
    BoundaryResponse,
    PartialMagicSquareSolver,
    UIBoundary,
)

Matrix4x4 = list[list[int]]


class SolveFacade:
    """SolvePartialMagicSquare Use Case 진입점."""

    def __init__(self, solver: PartialMagicSquareSolver) -> None:
        """SolveFacade를 초기화한다.

        Args:
            solver: Domain solver 구현 또는 Mock.
        """
        self._ui_boundary = UIBoundary(solver)

    def solve(self, matrix: Matrix4x4 | None) -> BoundaryResponse:
        """부분 마방진 Solve Use Case를 실행한다.

        Args:
            matrix: 4×4 입력 격자.

        Returns:
            SuccessResponse 또는 ErrorResponse.
        """
        return self._ui_boundary.submit(matrix)
