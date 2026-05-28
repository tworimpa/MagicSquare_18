"""Entity 레이어 공통 도메인 예외."""


class DomainValidationError(Exception):
    """도메인 불변조건 위반 시 발생하는 예외.

    Attributes:
        code: 기계 판독용 오류 코드.
        message: 사람이 읽을 수 있는 오류 메시지.
    """

    def __init__(self, code: str, message: str) -> None:
        """DomainValidationError를 초기화한다.

        Args:
            code: 오류 코드 (예: ``INVALID_USER_ID``).
            message: 오류 설명 메시지.
        """
        self.code = code
        self.message = message
        super().__init__(message)
