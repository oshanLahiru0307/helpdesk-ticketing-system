class AppException(Exception):
    """Base application exception with HTTP status code and message."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


class NotFoundException(AppException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(404, detail)


class BadRequestException(AppException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(400, detail)


class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(401, detail)
