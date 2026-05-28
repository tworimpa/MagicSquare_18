"""UI Boundary — 입출력 계약·Domain 호출 오케스트레이션."""

from __future__ import annotations

from typing import Protocol

from magicsquare.boundary.error_codes import ErrorCode
from magicsquare.boundary.error_mapper import ErrorMapper
from magicsquare.boundary.input_validator import validate_input_contract
from magicsquare.boundary.output_validator import validate_output_format
from magicsquare.boundary.response_models import (
    ErrorResponse,
    SuccessResponse,
)
from magicsquare.entity.domain_errors import DomainValidationError

Matrix4x4 = list[list[int]]
Solution6 = list[int]
BoundaryResponse = SuccessResponse | ErrorResponse


class PartialMagicSquareSolver(Protocol):
    """Domain SolvePartialMagicSquare 호출 계약."""

    def solve(self, matrix: Matrix4x4) -> Solution6:
        """부분 격자를 완성한다.

        Args:
            matrix: 유효한 4×4 입력 격자.

        Returns:
            ``[r1,c1,n1,r2,c2,n2]`` Solution6.

        Raises:
            DomainValidationError: 해가 없거나 도메인 규칙 위반.
        """


class UIBoundary:
    """외부 Caller와 Domain 사이 입출력 Boundary."""

    def __init__(self, solver: PartialMagicSquareSolver) -> None:
        """UIBoundary를 초기화한다.

        Args:
            solver: SolvePartialMagicSquare Use Case (테스트에서는 Mock).
        """
        self._solver = solver

    def submit(self, matrix: Matrix4x4 | None) -> BoundaryResponse:
        """int[4][4] 입력을 받아 Solve 결과 또는 ErrorResponse를 반환한다.

        Args:
            matrix: Caller 입력 격자.

        Returns:
            SuccessResponse 또는 ErrorResponse.
        """
        input_error = validate_input_contract(matrix)
        if input_error is not None:
            return ErrorMapper.to_error_response(input_error)

        assert matrix is not None
        try:
            result = self._solver.solve(matrix)
        except DomainValidationError:
            return ErrorMapper.to_error_response(ErrorCode.SOLVE_IMPOSSIBLE)
        except Exception:
            return ErrorMapper.to_error_response(ErrorCode.INTERNAL_ERROR)

        if not validate_output_format(result):
            return ErrorMapper.to_error_response(ErrorCode.INTERNAL_ERROR)

        return SuccessResponse(result=result)
