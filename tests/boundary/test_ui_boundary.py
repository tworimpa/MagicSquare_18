"""UIBoundary 계약 테스트 — Test ID U-C01, U-C10~U-C12."""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from magicsquare.boundary.error_codes import ERROR_MESSAGES, ErrorCode
from magicsquare.boundary.response_models import ErrorResponse, SuccessResponse
from magicsquare.boundary.ui_boundary import UIBoundary
from magicsquare.entity.domain_errors import DomainValidationError
from tests.boundary.conftest import MOCK_SOLUTION, VALID_PARTIAL_GRID


@dataclass
class MockSolver:
    """Domain Mock — Boundary 계약 테스트 전용."""

    result: list[int] = field(default_factory=lambda: MOCK_SOLUTION.copy())
    should_fail: bool = False
    calls: list[list[list[int]]] = field(default_factory=list)

    def solve(self, matrix: list[list[int]]) -> list[int]:
        """Mock solve — 호출 기록 후 결과 또는 예외."""
        self.calls.append([row[:] for row in matrix])
        if self.should_fail:
            raise DomainValidationError(
                code="SOLVE_IMPOSSIBLE",
                message=ERROR_MESSAGES[ErrorCode.SOLVE_IMPOSSIBLE],
            )
        return self.result.copy()


class TestUIBoundarySuccessPath:
    """U-C01, U-C11, U-C12: 성공 경로."""

    def test_valid_input_returns_ok_with_six_element_result(
        self,
        valid_partial_grid: list[list[int]],
    ) -> None:
        # Arrange — U-C01
        solver = MockSolver()
        boundary = UIBoundary(solver)

        # Act
        response = boundary.submit(valid_partial_grid)

        # Assert
        assert isinstance(response, SuccessResponse)
        assert response.status == "OK"
        assert len(response.result) == 6
        assert response.result == MOCK_SOLUTION

    def test_success_result_coordinates_and_values_in_range(
        self,
        valid_partial_grid: list[list[int]],
    ) -> None:
        # Arrange — U-C11
        solver = MockSolver()
        boundary = UIBoundary(solver)

        # Act
        response = boundary.submit(valid_partial_grid)

        # Assert
        assert isinstance(response, SuccessResponse)
        r1, c1, n1, r2, c2, n2 = response.result
        assert all(1 <= coord <= 4 for coord in (r1, c1, r2, c2))
        assert all(1 <= value <= 16 for value in (n1, n2))
        assert n1 != n2

    def test_domain_solver_called_once_with_same_input(
        self,
        valid_partial_grid: list[list[int]],
    ) -> None:
        # Arrange — U-C12
        solver = MockSolver()
        boundary = UIBoundary(solver)

        # Act
        boundary.submit(valid_partial_grid)

        # Assert
        assert len(solver.calls) == 1
        assert solver.calls[0] == valid_partial_grid


class TestUIBoundaryFailurePath:
    """U-C10: Domain 실패."""

    def test_domain_failure_returns_solve_impossible(
        self,
        valid_partial_grid: list[list[int]],
    ) -> None:
        # Arrange — U-C10
        solver = MockSolver(should_fail=True)
        boundary = UIBoundary(solver)

        # Act
        response = boundary.submit(valid_partial_grid)

        # Assert
        assert isinstance(response, ErrorResponse)
        assert response.code is ErrorCode.SOLVE_IMPOSSIBLE
        assert response.message == ERROR_MESSAGES[ErrorCode.SOLVE_IMPOSSIBLE]
        assert response.result is None
