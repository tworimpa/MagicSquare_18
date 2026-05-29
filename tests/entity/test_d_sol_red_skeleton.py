"""Track B — D-SOL-01~04 (Report/04)."""

from __future__ import annotations

import pytest

from magicsquare.entity.solve_partial_magic_square import solution

GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
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
    """D-SOL-02 — G2 Case B after A fails (TBD)."""

    @pytest.mark.skip(reason="G2 grid not fixed — Report/04 placeholder")
    def test_d_sol_02_g2_case_b_success(self) -> None:
        pytest.fail("RED: D-SOL-02 — G2 TBD; Case B success after A fails")


class TestDSol03Unsolvable:
    """D-SOL-03 — G3 both cases fail (TBD)."""

    @pytest.mark.skip(reason="G3 grid not fixed — Report/04 placeholder")
    def test_d_sol_03_g3_unsolvable_domain_error(self) -> None:
        pytest.fail("RED: D-SOL-03 — G3 TBD; UnsolvableDomainError")


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
