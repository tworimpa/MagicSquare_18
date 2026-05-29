"""부분 마방진 완성 Use Case."""

from __future__ import annotations

from magicsquare.entity.completion_strategy import try_case_a, try_case_b
from magicsquare.entity.domain_errors import DomainValidationError
from magicsquare.entity.partial_grid_4x4 import (
    Matrix4x4,
    find_blank_coords,
    find_not_exist_nums,
)

Solution6 = list[int]


class UnsolvableDomainError(DomainValidationError):
    """Case A·B 모두 실패 시 도메인 오류."""


def solution(matrix: Matrix4x4) -> Solution6:
    """부분 격자를 완성하여 Solution6를 반환한다.

    Args:
        matrix: 빈칸 2개인 4×4 격자.

    Returns:
        ``[r1,c1,n1,r2,c2,n2]`` (1-index).

    Raises:
        UnsolvableDomainError: 유효한 완성이 없을 때.
    """
    first, second = find_blank_coords(matrix)
    missing = find_not_exist_nums(matrix)
    smaller, larger = missing[0], missing[1]

    case_a = try_case_a(matrix, first, second, smaller, larger)
    if case_a is not None:
        return case_a

    case_b = try_case_b(matrix, first, second, smaller, larger)
    if case_b is not None:
        return case_b

    raise UnsolvableDomainError(
        code="SOLVE_IMPOSSIBLE",
        message="No valid magic square completion exists for the given grid.",
    )
