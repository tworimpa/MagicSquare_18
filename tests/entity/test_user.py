"""User 엔티티 단위 테스트 — Test ID U-E01~U-E05."""

import pytest

from magicsquare.entity.constants import DISPLAY_NAME_MAX_LENGTH, USER_ID_MAX_LENGTH
from magicsquare.entity.domain_errors import DomainValidationError
from magicsquare.entity.user import User, UserRole


class TestUserCreateHappyPath:
    """U-E01: 유효한 입력으로 User 생성."""

    def test_create_user_with_valid_fields_returns_user(self) -> None:
        # Arrange
        user_id = "caller-001"
        display_name = "Boundary Client"
        role = UserRole.CALLER

        # Act
        user = User.create(user_id, display_name, role)

        # Assert
        assert user.user_id == "caller-001"
        assert user.display_name == "Boundary Client"
        assert user.role is UserRole.CALLER
        assert user.is_caller() is True

    def test_create_user_strips_whitespace_from_inputs(self) -> None:
        # Arrange
        user_id = "  learner-01  "
        display_name = "  TDD Learner  "

        # Act
        user = User.create(user_id, display_name, UserRole.LEARNER)

        # Assert
        assert user.user_id == "learner-01"
        assert user.display_name == "TDD Learner"


class TestUserCreateFailurePath:
    """U-E02~U-E04: 불변조건 위반 시 DomainValidationError."""

    def test_create_user_with_empty_user_id_raises(self) -> None:
        # Arrange
        user_id = "   "
        display_name = "Valid Name"

        # Act & Assert
        with pytest.raises(DomainValidationError) as exc_info:
            User.create(user_id, display_name, UserRole.REVIEWER)

        assert exc_info.value.code == "INVALID_USER_ID"

    def test_create_user_with_empty_display_name_raises(self) -> None:
        # Arrange
        user_id = "user-001"
        display_name = ""

        # Act & Assert
        with pytest.raises(DomainValidationError) as exc_info:
            User.create(user_id, display_name, UserRole.LEARNER)

        assert exc_info.value.code == "INVALID_DISPLAY_NAME"

    def test_create_user_with_user_id_exceeding_max_length_raises(self) -> None:
        # Arrange
        user_id = "x" * (USER_ID_MAX_LENGTH + 1)
        display_name = "Valid Name"

        # Act & Assert
        with pytest.raises(DomainValidationError) as exc_info:
            User.create(user_id, display_name, UserRole.CALLER)

        assert exc_info.value.code == "INVALID_USER_ID"

    def test_create_user_with_display_name_exceeding_max_length_raises(self) -> None:
        # Arrange
        user_id = "user-001"
        display_name = "n" * (DISPLAY_NAME_MAX_LENGTH + 1)

        # Act & Assert
        with pytest.raises(DomainValidationError) as exc_info:
            User.create(user_id, display_name, UserRole.REVIEWER)

        assert exc_info.value.code == "INVALID_DISPLAY_NAME"


class TestUserEntityIdentity:
    """U-E05: 엔티티 동등성은 user_id(식별자)로만 결정."""

    def test_users_with_same_id_are_equal(self) -> None:
        # Arrange
        user_a = User.create("same-id", "Name A", UserRole.CALLER)
        user_b = User.create("same-id", "Name B", UserRole.REVIEWER)

        # Act & Assert
        assert user_a == user_b
        assert hash(user_a) == hash(user_b)

    def test_users_with_different_id_are_not_equal(self) -> None:
        # Arrange
        user_a = User.create("id-a", "Same Name", UserRole.LEARNER)
        user_b = User.create("id-b", "Same Name", UserRole.LEARNER)

        # Act & Assert
        assert user_a != user_b

    def test_user_is_not_equal_to_non_user(self) -> None:
        # Arrange
        user = User.create("id-a", "Name", UserRole.LEARNER)

        # Act & Assert
        assert user != "id-a"
        assert user.__eq__("id-a") is NotImplemented
