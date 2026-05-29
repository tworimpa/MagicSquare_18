"""AC-FR-01-01 — grid=None 선행 입력 검증 (Track A).

SSOT: docs/test_plan.md BV-01~06, error_codes.py §13 INPUT_*.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from unittest.mock import MagicMock, create_autospec

import pytest

from magicsquare.boundary.error_codes import ERROR_MESSAGES, ErrorCode
from magicsquare.boundary.response_models import ErrorResponse
from magicsquare.boundary.ui_boundary import PartialMagicSquareSolver, UIBoundary

FORBIDDEN_TEST_KEYWORDS = (
    "duplicate",
    "empty_count",
    "value_range",
    "solve_impossible",
    "case_a",
    "case_b",
    "missing_number",
    "magic_square",
    "blank_finder",
)


@dataclass
class ResolveSpy:
    """Domain resolve() 진입점 spy — 호출 횟수 기록."""

    calls: list[list[list[int]] | None] = field(default_factory=list)

    def resolve(self, grid: list[list[int]] | None) -> list[int]:
        """Domain resolver stub."""
        self.calls.append(
            [row[:] for row in grid] if grid is not None else None
        )
        return [1, 1, 1, 1, 1, 1]


class ResolveSolverAdapter:
    """UIBoundary PartialMagicSquareSolver — resolve() spy 래핑."""

    def __init__(self, spy: ResolveSpy) -> None:
        self._spy = spy

    def solve(self, matrix: list[list[int]]) -> list[int]:
        """resolve() spy에 위임."""
        return self._spy.resolve(matrix)


class TestAcFr0101NullGridFailure:
    """AC-FR-01-01 / BV-01 — matrix is null → INPUT_NULL."""

    def test_none_grid_returns_invalid_size_error_response(self) -> None:
        """AC-FR-01-01, BV-01 — ErrorResponse code INPUT_NULL."""
        # Given — AC-FR-01-01
        spy = ResolveSpy()
        boundary = UIBoundary(ResolveSolverAdapter(spy))
        grid = None

        # When
        response = boundary.submit(grid)

        # Then
        assert isinstance(response, ErrorResponse)
        assert response.status == "ERROR"
        assert response.result is None
        assert response.code == ErrorCode.INPUT_NULL
        assert response.to_dict()["code"] == ErrorCode.INPUT_NULL.value

    def test_none_grid_message_exact_match_prd_section_8_1(self) -> None:
        """AC-FR-01-01, BV-01 — message SSOT (ERROR_MESSAGES)."""
        # Given — AC-FR-01-01
        spy = ResolveSpy()
        boundary = UIBoundary(ResolveSolverAdapter(spy))
        grid = None

        # When
        response = boundary.submit(grid)

        # Then
        assert response.message == ERROR_MESSAGES[ErrorCode.INPUT_NULL]


class TestAcFr0101BoundaryGrids:
    """AC-FR-01-02~03 / BV-02~05 — size envelope → INPUT_ROW/COL_COUNT."""

    def test_empty_list_grid_returns_invalid_size_error(self) -> None:
        """AC-FR-01-02, BV-02 — [] → INPUT_ROW_COUNT."""
        # Given — AC-FR-01-02
        spy = ResolveSpy()
        boundary = UIBoundary(ResolveSolverAdapter(spy))
        grid: list[list[int]] = []

        # When
        response = boundary.submit(grid)

        # Then
        assert isinstance(response, ErrorResponse)
        assert response.code == ErrorCode.INPUT_ROW_COUNT
        assert response.to_dict()["code"] == ErrorCode.INPUT_ROW_COUNT.value
        assert response.message == ERROR_MESSAGES[ErrorCode.INPUT_ROW_COUNT]

    def test_four_rows_zero_cols_grid_returns_invalid_size_error(self) -> None:
        """AC-FR-01-03, BV-03 — [[]]*4 → INPUT_COL_COUNT."""
        # Given — AC-FR-01-03
        spy = ResolveSpy()
        boundary = UIBoundary(ResolveSolverAdapter(spy))
        grid = [[]] * 4

        # When
        response = boundary.submit(grid)

        # Then
        assert isinstance(response, ErrorResponse)
        assert response.code == ErrorCode.INPUT_COL_COUNT
        assert response.to_dict()["code"] == ErrorCode.INPUT_COL_COUNT.value
        assert response.message == ERROR_MESSAGES[ErrorCode.INPUT_COL_COUNT]

    def test_three_by_four_grid_returns_invalid_size_error(self) -> None:
        """AC-FR-01-02, BV-04 — 3×4 → INPUT_ROW_COUNT."""
        # Given — AC-FR-01-02
        spy = ResolveSpy()
        boundary = UIBoundary(ResolveSolverAdapter(spy))
        grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

        # When
        response = boundary.submit(grid)

        # Then
        assert isinstance(response, ErrorResponse)
        assert response.code == ErrorCode.INPUT_ROW_COUNT
        assert response.to_dict()["code"] == ErrorCode.INPUT_ROW_COUNT.value
        assert response.message == ERROR_MESSAGES[ErrorCode.INPUT_ROW_COUNT]


class TestAcFr0101DomainIsolation:
    """AC-FR-01-01, BR-05 — Domain resolve() 격리."""

    def test_none_grid_resolve_zero_calls_spy(self) -> None:
        """AC-FR-01-01 — grid=None 시 solve 0회."""
        # Given — AC-FR-01-01
        spy = ResolveSpy()
        boundary = UIBoundary(ResolveSolverAdapter(spy))
        grid = None

        # When
        boundary.submit(grid)

        # Then
        assert len(spy.calls) == 0

    def test_none_grid_resolve_zero_calls_unittest_mock(self) -> None:
        """AC-FR-01-01 — grid=None 시 mock solve 미호출."""
        # Given — AC-FR-01-01
        solver = create_autospec(PartialMagicSquareSolver, instance=True)
        boundary = UIBoundary(solver)
        grid = None

        # When
        boundary.submit(grid)

        # Then
        solver.solve.assert_not_called()

    def test_none_grid_resolve_mock_call_count_fails_if_invoked(self) -> None:
        """AC-FR-01-01 — resolve() 호출 시 RED 실패."""
        # Given — AC-FR-01-01
        solver = MagicMock(spec=PartialMagicSquareSolver)
        solver.solve.return_value = [1, 1, 1, 1, 1, 1]
        boundary = UIBoundary(solver)
        grid = None

        # When
        boundary.submit(grid)

        # Then — 호출됐을 경우 pytest.fail
        if solver.solve.call_count > 0:
            pytest.fail(
                "resolve()/solve() must not be called when grid is None "
                f"(call_count={solver.solve.call_count})"
            )


class TestAcFr0101ScopeLimit:
    """AC-FR-01-01 — AC-FR-01-02~05 / FR-02~05 미포함."""

    def test_module_scope_excludes_ac_fr_01_02_to_05_cases(self) -> None:
        """AC-FR-01-01 — 모듈 스코프 제한."""
        # Given — AC-FR-01-01
        import tests.boundary.test_ac_fr_01_01_red as target_module

        test_names = [
            name
            for name, obj in inspect.getmembers(target_module)
            if name.startswith("test_") and callable(obj)
        ]

        # When — FR-01-02~05 / FR-02~05 전용 키워드 포함 여부
        out_of_scope = [
            name
            for name in test_names
            if any(keyword in name for keyword in FORBIDDEN_TEST_KEYWORDS)
        ]

        # Then
        assert out_of_scope == [], (
            "AC-FR-01-02~05 / FR-02~05 cases must not appear in this module: "
            f"{out_of_scope}"
        )
