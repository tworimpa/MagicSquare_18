"""UX 표현 레이어 — 성공·입력 상태 사용자 친화 포맷."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from magicsquare.boundary.error_codes import ErrorCode
from magicsquare.boundary.error_mapper import ErrorMapper
from magicsquare.boundary.input_validator import count_empty_cells
from magicsquare.boundary.response_models import ErrorResponse, SuccessResponse
from magicsquare.entity.constants import EMPTY_CELL_VALUE, REQUIRED_EMPTY_CELL_COUNT

Matrix4x4 = list[list[int]]
Solution6 = list[int]


@dataclass(frozen=True, slots=True)
class UXSuccessPresentation:
    """성공 결과 UX 표현."""

    result: Solution6
    summary_ko: str
    preview_grid: Matrix4x4

    def to_dict(self) -> dict[str, Any]:
        """UI 렌더링용 dict를 반환한다."""
        return {
            "result": self.result,
            "summary_ko": self.summary_ko,
            "preview_grid": self.preview_grid,
        }


@dataclass(frozen=True, slots=True)
class UXGridStatus:
    """격자 입력 상태 — live counter·접근성 레이블."""

    empty_count: int
    required_empty_count: int
    empty_status_label: str
    aria_label: str

    def to_dict(self) -> dict[str, Any]:
        """UI 렌더링용 dict를 반환한다."""
        return {
            "empty_count": self.empty_count,
            "required_empty_count": self.required_empty_count,
            "empty_status_label": self.empty_status_label,
            "aria_label": self.aria_label,
        }


class UXPresentation:
    """Boundary 응답을 사용자 친화 표현으로 변환한다."""

    @staticmethod
    def format_solution_summary(result: Solution6) -> str:
        """Solution6를 한글 요약 문장으로 변환한다."""
        r1, c1, n1, r2, c2, n2 = result
        return f"({r1},{c1})에 {n1}, ({r2},{c2})에 {n2}을 넣으세요."

    @staticmethod
    def build_preview_grid(matrix: Matrix4x4, result: Solution6) -> Matrix4x4:
        """완성 미리보기 격자를 생성한다."""
        preview = [row[:] for row in matrix]
        preview[result[0] - 1][result[1] - 1] = result[2]
        preview[result[3] - 1][result[4] - 1] = result[5]
        return preview

    @staticmethod
    def from_success(
        matrix: Matrix4x4,
        response: SuccessResponse,
    ) -> UXSuccessPresentation:
        """SuccessResponse를 UX 성공 표현으로 변환한다."""
        return UXSuccessPresentation(
            result=response.result,
            summary_ko=UXPresentation.format_solution_summary(response.result),
            preview_grid=UXPresentation.build_preview_grid(matrix, response.result),
        )

    @staticmethod
    def from_error(
        response: ErrorResponse,
        *,
        matrix: Matrix4x4 | None = None,
    ) -> dict[str, Any]:
        """ErrorResponse를 UX 에러 표현 dict로 변환한다."""
        context: dict[str, Any] = {}
        if matrix is not None:
            empty_count = count_empty_cells(matrix)
            context["empty_count"] = empty_count
            context["required_empty_count"] = REQUIRED_EMPTY_CELL_COUNT
            if response.code is ErrorCode.INPUT_EMPTY_COUNT:
                context["empty_status_label"] = (
                    f"빈칸 {empty_count}/{REQUIRED_EMPTY_CELL_COUNT}"
                )
        presentation = ErrorMapper.from_error_response(response, context=context)
        return presentation.to_dict()

    @staticmethod
    def grid_status(matrix: Matrix4x4) -> UXGridStatus:
        """격자 입력 live counter·aria 레이블을 생성한다."""
        empty_count = count_empty_cells(matrix)
        return UXGridStatus(
            empty_count=empty_count,
            required_empty_count=REQUIRED_EMPTY_CELL_COUNT,
            empty_status_label=(
                f"빈칸 {empty_count}/{REQUIRED_EMPTY_CELL_COUNT}"
            ),
            aria_label=(
                f"4 by 4 magic square grid, "
                f"{empty_count} empty cells of "
                f"{REQUIRED_EMPTY_CELL_COUNT} required"
            ),
        )

    @staticmethod
    def cell_aria_label(row: int, col: int, value: int) -> str:
        """셀 단위 접근성 레이블을 생성한다 (1-index)."""
        if value == EMPTY_CELL_VALUE:
            return f"Row {row} column {col}, empty cell"
        return f"Row {row} column {col}, value {value}"
