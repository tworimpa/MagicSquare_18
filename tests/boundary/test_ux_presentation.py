"""UX 표현 레이어 테스트 — 사용자 친화 피드백."""

from magicsquare.boundary.error_codes import ERROR_MESSAGES, ErrorCode
from magicsquare.boundary.error_mapper import ErrorMapper
from magicsquare.boundary.response_models import ErrorResponse, SuccessResponse
from magicsquare.boundary.ux_presentation import UXPresentation
from tests.boundary.conftest import MOCK_SOLUTION, VALID_PARTIAL_GRID


class TestUXPresentation:
    """UX 디자이너 개선 — message 불변 + 보조 문구·접근성."""

    def test_success_summary_uses_one_index_coordinates(self) -> None:
        # Arrange
        response = SuccessResponse(result=MOCK_SOLUTION)

        # Act
        presentation = UXPresentation.from_success(VALID_PARTIAL_GRID, response)

        # Assert
        assert presentation.summary_ko == "(2,3)에 11, (4,4)에 1을 넣으세요."

    def test_success_preview_grid_fills_empty_cells(self) -> None:
        # Arrange
        response = SuccessResponse(result=MOCK_SOLUTION)

        # Act
        presentation = UXPresentation.from_success(VALID_PARTIAL_GRID, response)

        # Assert
        assert presentation.preview_grid[1][2] == 11
        assert presentation.preview_grid[3][3] == 1

    def test_error_presentation_keeps_exact_api_message(self) -> None:
        # Arrange
        response = ErrorMapper.to_error_response(ErrorCode.INPUT_DUPLICATE)

        # Act
        ux = UXPresentation.from_error(response)

        # Assert
        assert ux["message"] == ERROR_MESSAGES[ErrorCode.INPUT_DUPLICATE]
        assert ux["hint_ko"]
        assert ux["message"] != ux["hint_ko"]

    def test_empty_count_context_for_empty_cell_error(self) -> None:
        # Arrange
        matrix = [row[:] for row in VALID_PARTIAL_GRID]
        matrix[0][0] = 0
        response = ErrorMapper.to_error_response(ErrorCode.INPUT_EMPTY_COUNT)

        # Act
        ux = UXPresentation.from_error(response, matrix=matrix)

        # Assert
        assert ux["context"]["empty_count"] == 3
        assert ux["context"]["empty_status_label"] == "빈칸 3/2"

    def test_grid_status_provides_aria_label(self) -> None:
        # Arrange & Act
        status = UXPresentation.grid_status(VALID_PARTIAL_GRID)

        # Assert
        assert status.empty_count == 2
        assert status.empty_status_label == "빈칸 2/2"
        assert "empty cells" in status.aria_label

    def test_cell_aria_label_distinguishes_empty_and_value(self) -> None:
        # Arrange & Act
        empty_label = UXPresentation.cell_aria_label(2, 3, 0)
        value_label = UXPresentation.cell_aria_label(1, 1, 16)

        # Assert
        assert "empty cell" in empty_label
        assert "value 16" in value_label
