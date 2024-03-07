from wallet.core.errors import bad_request, forbidden, ok, not_found


class CustomError(Exception):
    """Base class for other exceptions"""
    pass


class SomethingBadHappened(CustomError):
    """Raised when something bad happens"""
    pass


class CustomException(Exception):

    def __init__(self, message):
        super().__init__(message)

    def http_response(self):
        raise NotImplementedError


class NotFoundException(CustomException):

    def __init__(self, error_code: str):
        self.message = error_code
        super().__init__(self.message)

    def http_response(self):
        return not_found(self.message)


class BadRequestException(CustomException):

    def __init__(self, error_code: str):
        self.message = error_code
        super().__init__(self.message)

    def http_response(self):
        return bad_request(self.message)


class ForbiddenException(CustomException):
    def __init__(self, error_code: str):
        self.message = error_code
        super().__init__(self.message)

    def http_response(self):
        return forbidden(self.message)
