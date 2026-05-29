"""Track A — U-FLOW-02 (Report/04)."""

from __future__ import annotations

from dataclasses import dataclass, field

from magicsquare.boundary.ui_boundary import UIBoundary
from tests.boundary.test_u_in_red_skeleton import GRID_G0


@dataclass
class SolveSpy:
    """PartialMagicSquareSolver spy."""

    calls: list[list[list[int]]] = field(default_factory=list)

    def solve(self, matrix: list[list[int]]) -> list[int]:
        """Record call and return stub."""
        self.calls.append([row[:] for row in matrix])
        return [1, 1, 1, 1, 1, 1]


class TestUFlow02ExecuteZeroOnInvalid:
    """U-FLOW-02 — Domain 0-call on each invalid class."""

    def test_u_flow_02a_null_execute_call_count_zero(self) -> None:
        # Given
        spy = SolveSpy()
        boundary = UIBoundary(spy)

        # When
        boundary.submit(None)

        # Then
        assert len(spy.calls) == 0

    def test_u_flow_02b_invalid_size_execute_call_count_zero(self) -> None:
        # Given
        spy = SolveSpy()
        boundary = UIBoundary(spy)

        # When
        boundary.submit([])

        # Then
        assert len(spy.calls) == 0

    def test_u_flow_02c_invalid_empty_count_execute_call_count_zero(self) -> None:
        # Given — G0 (0 blanks)
        spy = SolveSpy()
        boundary = UIBoundary(spy)
        matrix = [row[:] for row in GRID_G0]

        # When
        boundary.submit(matrix)

        # Then
        assert len(spy.calls) == 0

    def test_u_flow_02d_invalid_value_range_execute_call_count_zero(self) -> None:
        # Given — 4×4, 2 zeros, -1
        spy = SolveSpy()
        boundary = UIBoundary(spy)
        matrix = [
            [0, 3, 2, 13],
            [5, 10, -1, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 0],
        ]

        # When
        boundary.submit(matrix)

        # Then
        assert len(spy.calls) == 0

    def test_u_flow_02e_invalid_duplicate_execute_call_count_zero(self) -> None:
        # Given — 4×4, 2 zeros, duplicate non-zero
        spy = SolveSpy()
        boundary = UIBoundary(spy)
        matrix = [
            [16, 3, 2, 0],
            [5, 10, 5, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 0],
        ]

        # When
        boundary.submit(matrix)

        # Then
        assert len(spy.calls) == 0
