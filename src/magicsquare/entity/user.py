"""User 엔티티 — 식별자 기반 호출자·학습자 도메인 모델."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from magicsquare.entity.constants import (
    DISPLAY_NAME_MAX_LENGTH,
    DISPLAY_NAME_MIN_LENGTH,
    USER_ID_MAX_LENGTH,
    USER_ID_MIN_LENGTH,
)
from magicsquare.entity.domain_errors import DomainValidationError


class UserRole(str, Enum):
    """MagicSquare 시스템 Actor 역할.

    docs/02-problem-framing.md §6.1 Actors에 대응한다.
    """

    LEARNER = "LEARNER"
    CALLER = "CALLER"
    REVIEWER = "REVIEWER"


@dataclass(frozen=True, slots=True)
class User:
    """식별자(user_id)로 동등성이 결정되는 User 엔티티.

    Attributes:
        user_id: 불변 사용자 식별자.
        display_name: 표시용 이름.
        role: 시스템 내 Actor 역할.
    """

    user_id: str
    display_name: str
    role: UserRole

    @classmethod
    def create(
        cls,
        user_id: str,
        display_name: str,
        role: UserRole,
    ) -> User:
        """불변조건을 검증한 뒤 User 엔티티를 생성한다.

        Args:
            user_id: 사용자 식별자. 공백만으로 구성될 수 없다.
            display_name: 표시용 이름. 공백만으로 구성될 수 없다.
            role: Actor 역할.

        Returns:
            검증을 통과한 User 인스턴스.

        Raises:
            DomainValidationError: INV-U1~U3 위반 시.
        """
        normalized_id = cls._normalize(user_id)
        normalized_name = cls._normalize(display_name)
        cls._validate_user_id(normalized_id)
        cls._validate_display_name(normalized_name)
        cls._validate_role(role)
        return cls(
            user_id=normalized_id,
            display_name=normalized_name,
            role=role,
        )

    def is_caller(self) -> bool:
        """호출자(Boundary Client) 역할인지 반환한다.

        Returns:
            role이 CALLER이면 True.
        """
        return self.role is UserRole.CALLER

    def __eq__(self, other: object) -> bool:
        """동등성은 user_id(식별자)만으로 판단한다.

        Args:
            other: 비교 대상.

        Returns:
            동일 user_id이면 True.
        """
        if not isinstance(other, User):
            return NotImplemented
        return self.user_id == other.user_id

    def __hash__(self) -> int:
        """user_id 기반 해시."""
        return hash(self.user_id)

    @staticmethod
    def _normalize(value: str) -> str:
        """앞뒤 공백을 제거한다."""
        return value.strip()

    @staticmethod
    def _validate_user_id(user_id: str) -> None:
        """INV-U1: user_id는 1~64자 비공백 문자열이어야 한다."""
        if len(user_id) < USER_ID_MIN_LENGTH:
            raise DomainValidationError(
                code="INVALID_USER_ID",
                message="User id must not be empty.",
            )
        if len(user_id) > USER_ID_MAX_LENGTH:
            raise DomainValidationError(
                code="INVALID_USER_ID",
                message=(
                    f"User id must not exceed {USER_ID_MAX_LENGTH} characters."
                ),
            )

    @staticmethod
    def _validate_display_name(display_name: str) -> None:
        """INV-U2: display_name은 1~100자 비공백 문자열이어야 한다."""
        if len(display_name) < DISPLAY_NAME_MIN_LENGTH:
            raise DomainValidationError(
                code="INVALID_DISPLAY_NAME",
                message="Display name must not be empty.",
            )
        if len(display_name) > DISPLAY_NAME_MAX_LENGTH:
            raise DomainValidationError(
                code="INVALID_DISPLAY_NAME",
                message=(
                    "Display name must not exceed "
                    f"{DISPLAY_NAME_MAX_LENGTH} characters."
                ),
            )

    @staticmethod
    def _validate_role(role: UserRole) -> None:
        """INV-U3: role은 UserRole enum이어야 한다."""
        if not isinstance(role, UserRole):
            raise DomainValidationError(
                code="INVALID_USER_ROLE",
                message="Role must be a valid UserRole.",
            )
