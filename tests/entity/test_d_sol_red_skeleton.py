"""Track B RED Skeleton — D-SOL-01~04 (Report/04).

Domain Mock forbidden. solution() alias → SolvePartialMagicSquare / TwoCellSolver.
"""

from __future__ import annotations

import pytest

# from magicsquare.entity.solve_partial_magic_square import solution


class TestDSol01CaseASuccess:
    """D-SOL-01 — G1 Case A → [2,2,7,3,3,10] (I8)."""

    def test_d_sol_01_g1_case_a_returns_solution6(self) -> None:
        # Given — G1
        # When — solution(matrix)
        pytest.fail("RED: D-SOL-01 — G1 Case A → [2,2,7,3,3,10]")


class TestDSol02CaseBSuccess:
    """D-SOL-02 — G2 Case B after A fails (I9)."""

    def test_d_sol_02_g2_case_b_success(self) -> None:
        # Given — G2 (TBD)
        pytest.fail("RED: D-SOL-02 — G2 TBD; Case B success after A fails")


class TestDSol03Unsolvable:
    """D-SOL-03 — G3 both cases fail → UnsolvableDomainError (I10)."""

    def test_d_sol_03_g3_unsolvable_domain_error(self) -> None:
        # Given — G3 (TBD)
        # When — solution(matrix)
        pytest.fail("RED: D-SOL-03 — G3 TBD; UnsolvableDomainError")


class TestDSol04OutputFormat:
    """D-SOL-04 — len 6 and 1-index coords (with I8/I9)."""

    def test_d_sol_04_solution_length_and_one_index(self) -> None:
        # Given — G1
        # When — solution(matrix)
        pytest.fail("RED: D-SOL-04 — len==6; r,c in [1,4]")
