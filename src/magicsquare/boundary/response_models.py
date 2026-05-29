"""Boundary 응답 DTO — Success/Error 스키마."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from magicsquare.boundary.error_codes import ERROR_MESSAGES, ErrorCode


@dataclass(frozen=True, slots=True)
class ErrorResponse:
    """에러 응답 — docs/04 §2.2 Error Schema."""

    code: ErrorCode
    message: str
    status: str = "ERROR"
    result: None = None

    def to_dict(self) -> dict[str, Any]:
        """JSON 직렬화용 dict를 반환한다."""
        return {
            "status": self.status,
            "code": self.code.value,
            "message": self.message,
            "result": self.result,
        }


@dataclass(frozen=True, slots=True)
class SuccessResponse:
    """성공 응답 — docs/04 §2.2 Output Schema."""

    result: list[int]
    status: str = "OK"

    def to_dict(self) -> dict[str, Any]:
        """JSON 직렬화용 dict를 반환한다."""
        return {
            "status": self.status,
            "result": self.result,
        }


def build_error_response(code: ErrorCode) -> ErrorResponse:
    """ErrorCode에 대응하는 ErrorResponse를 생성한다.

    Args:
        code: Boundary Error Code.

    Returns:
        message가 SSOT와 완전 일치하는 ErrorResponse.
    """
    return ErrorResponse(code=code, message=ERROR_MESSAGES[code])
