"""Boundary 에러 매핑 — API message와 UX 보조 문구 분리."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from magicsquare.boundary.error_codes import ERROR_MESSAGES, ErrorCode
from magicsquare.boundary.response_models import ErrorResponse, build_error_response


UX_HINTS_KO: dict[ErrorCode, str] = {
    ErrorCode.INPUT_NULL: "격자 데이터가 없습니다. 다시 입력해 주세요.",
    ErrorCode.INPUT_ROW_COUNT: "행은 4개여야 합니다.",
    ErrorCode.INPUT_COL_COUNT: "모든 행은 4열이어야 합니다.",
    ErrorCode.INPUT_VALUE_RANGE: (
        "각 칸은 0(빈칸) 또는 1~16 정수만 입력할 수 있습니다."
    ),
    ErrorCode.INPUT_EMPTY_COUNT: "빈칸(0)은 정확히 2개여야 합니다.",
    ErrorCode.INPUT_DUPLICATE: "1~16 숫자는 중복될 수 없습니다.",
    ErrorCode.SOLVE_IMPOSSIBLE: (
        "이 배치로는 마방진을 완성할 수 없습니다. 숫자를 수정해 보세요."
    ),
    ErrorCode.INTERNAL_ERROR: "일시적 오류입니다. 다시 시도해 주세요.",
}


@dataclass(frozen=True, slots=True)
class UXErrorPresentation:
    """UX 표현 레이어 — API message는 불변, hint만 보조."""

    code: str
    message: str
    hint_ko: str
    context: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """UI 렌더링용 dict를 반환한다."""
        return {
            "code": self.code,
            "message": self.message,
            "hint_ko": self.hint_ko,
            "context": self.context,
        }


class ErrorMapper:
    """Domain/Boundary 오류를 ErrorResponse·UX 표현으로 매핑한다."""

    @staticmethod
    def to_error_response(code: ErrorCode) -> ErrorResponse:
        """ErrorCode를 ErrorResponse로 변환한다."""
        return build_error_response(code)

    @staticmethod
    def to_ux_presentation(
        code: ErrorCode,
        *,
        context: dict[str, Any] | None = None,
    ) -> UXErrorPresentation:
        """ErrorCode를 UX 친화적 표현으로 변환한다.

        API ``message`` 문자열은 SSOT와 완전 일치를 유지한다.
        """
        return UXErrorPresentation(
            code=code.value,
            message=ERROR_MESSAGES[code],
            hint_ko=UX_HINTS_KO[code],
            context=context or {},
        )

    @staticmethod
    def from_error_response(
        response: ErrorResponse,
        *,
        context: dict[str, Any] | None = None,
    ) -> UXErrorPresentation:
        """ErrorResponse를 UX 표현으로 변환한다."""
        return ErrorMapper.to_ux_presentation(
            response.code,
            context=context,
        )
