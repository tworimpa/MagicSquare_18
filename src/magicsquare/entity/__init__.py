"""Entity 레이어 — 도메인 데이터 및 규칙."""

from magicsquare.entity.domain_errors import DomainValidationError
from magicsquare.entity.user import User, UserRole

__all__ = ["DomainValidationError", "User", "UserRole"]
