"""입력 계약 검증 테스트 — Test ID U-C02~U-C09."""

import pytest

from magicsquare.boundary.error_codes import ERROR_MESSAGES, ErrorCode
from magicsquare.boundary.input_validator import validate_input_contract


class TestInputValidatorContract:
    """Boundary 입력 검증 — 첫 실패 중단 순서."""

    def test_null_matrix_returns_input_null(self) -> None:
        # Arrange — U-C02
        matrix = None

        # Act
        result = validate_input_contract(matrix)

        # Assert
        assert result is ErrorCode.INPUT_NULL

    def test_three_rows_returns_input_row_count(self) -> None:
        # Arrange — U-C03
        matrix = [[0] * 4, [0] * 4, [0] * 4]

        # Act
        result = validate_input_contract(matrix)

        # Assert
        assert result is ErrorCode.INPUT_ROW_COUNT

    def test_four_by_three_returns_input_col_count(self) -> None:
        # Arrange — U-C04
        matrix = [[0, 0, 0] for _ in range(4)]

        # Act
        result = validate_input_contract(matrix)

        # Assert
        assert result is ErrorCode.INPUT_COL_COUNT

    def test_one_empty_cell_returns_input_empty_count(self) -> None:
        # Arrange — U-C05
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]

        # Act
        result = validate_input_contract(matrix)

        # Assert
        assert result is ErrorCode.INPUT_EMPTY_COUNT

    def test_three_empty_cells_returns_input_empty_count(
        self,
        valid_partial_grid: list[list[int]],
    ) -> None:
        # Arrange — U-C06
        matrix = [row[:] for row in valid_partial_grid]
        matrix[0][0] = 0

        # Act
        result = validate_input_contract(matrix)

        # Assert
        assert result is ErrorCode.INPUT_EMPTY_COUNT

    def test_negative_value_returns_input_value_range(self) -> None:
        # Arrange — U-C07
        matrix = [
            [16, 3, 2, 13],
            [5, 10, -1, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 0],
        ]

        # Act
        result = validate_input_contract(matrix)

        # Assert
        assert result is ErrorCode.INPUT_VALUE_RANGE

    def test_seventeen_returns_input_value_range(self) -> None:
        # Arrange — U-C08
        matrix = [
            [16, 3, 2, 13],
            [5, 10, 17, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 0],
        ]

        # Act
        result = validate_input_contract(matrix)

        # Assert
        assert result is ErrorCode.INPUT_VALUE_RANGE

    def test_duplicate_non_zero_returns_input_duplicate(self) -> None:
        # Arrange — U-C09
        matrix = [
            [16, 3, 2, 13],
            [5, 10, 5, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 0],
        ]

        # Act
        result = validate_input_contract(matrix)

        # Assert
        assert result is ErrorCode.INPUT_DUPLICATE

    @pytest.mark.parametrize(
        ("code",),
        [(code,) for code in ErrorCode],
    )
    def test_error_messages_match_ssot(self, code: ErrorCode) -> None:
        # Arrange & Act & Assert — RG-03 snapshot
        assert code.value in {
            "INPUT_NULL",
            "INPUT_ROW_COUNT",
            "INPUT_COL_COUNT",
            "INPUT_VALUE_RANGE",
            "INPUT_EMPTY_COUNT",
            "INPUT_DUPLICATE",
            "SOLVE_IMPOSSIBLE",
            "INTERNAL_ERROR",
        }
        assert ERROR_MESSAGES[code]
