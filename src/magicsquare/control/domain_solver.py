"""Domain solver adapter — Control → Entity bridge."""

from __future__ import annotations

from magicsquare.entity.solve_partial_magic_square import solution

Matrix4x4 = list[list[int]]
Solution6 = list[int]


class DomainPartialMagicSquareSolver:
    """PartialMagicSquareSolver Protocol 구현 — Entity solution() 위임."""

    def solve(self, matrix: Matrix4x4) -> Solution6:
        """부분 격자를 완성한다.

        Args:
            matrix: 유효한 4×4 입력 격자.

        Returns:
            ``[r1,c1,n1,r2,c2,n2]`` Solution6.

        Raises:
            UnsolvableDomainError: 해가 없을 때.
        """
        return solution(matrix)
