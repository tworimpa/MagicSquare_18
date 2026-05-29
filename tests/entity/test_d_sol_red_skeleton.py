"""Track B — D-SOL-01~04 (Report/04)."""

from __future__ import annotations

import pytest

from magicsquare.entity.solve_partial_magic_square import (
    UnsolvableDomainError,
    solution,
)

GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

# Case A fails, Case B succeeds — blanks (1,1),(2,3); missing {11,16}
GRID_G2: list[list[int]] = [
    [0, 3, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# Both cases fail → UnsolvableDomainError — blanks (1,1),(1,2); missing {1,2}
GRID_G3: list[list[int]] = [
    [0, 0, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
]


class TestDSol01CaseASuccess:
    """D-SOL-01 — G1 valid Solution6 (Case B when Case A invalid)."""

    def test_d_sol_01_g1_case_a_returns_solution6(self) -> None:
        # Given
        matrix = [row[:] for row in GRID_G1]

        # When
        result = solution(matrix)

        # Then
        assert result == [2, 2, 10, 3, 3, 7]


class TestDSol02CaseBSuccess:
    """D-SOL-02 — G2 Case B after A fails."""

    def test_d_sol_02_g2_case_b_success(self) -> None:
        # Given
        matrix = [row[:] for row in GRID_G2]

        # When
        result = solution(matrix)

        # Then — Case B: larger(16)→first blank, smaller(11)→second
        assert result == [1, 1, 16, 2, 3, 11]


class TestDSol03Unsolvable:
    """D-SOL-03 — G3 both cases fail."""

    def test_d_sol_03_g3_unsolvable_domain_error(self) -> None:
        # Given
        matrix = [row[:] for row in GRID_G3]

        # When / Then
        with pytest.raises(UnsolvableDomainError):
            solution(matrix)


class TestDSol04OutputFormat:
    """D-SOL-04 — len 6 and 1-index coords."""

    def test_d_sol_04_solution_length_and_one_index(self) -> None:
        # Given
        matrix = [row[:] for row in GRID_G1]

        # When
        result = solution(matrix)

        # Then
        assert len(result) == 6
        r1, c1, _, r2, c2, _ = result
        assert all(1 <= coord <= 4 for coord in (r1, c1, r2, c2))
