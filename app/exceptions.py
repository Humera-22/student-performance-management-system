class AppException(Exception):
    status_code = 400
    message = "Application error"

    def __init__(self, message=None, status_code=None):
        super().__init__(message)
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code

class NotFoundException(AppException):
    status_code = 404
    message = "Resource not found"

class UnauthorizedException(AppException):
    status_code = 401
    message = "Unauthorized"

class ForbiddenException(AppException):
    status_code = 403
    message = "Forbidden"

class BadRequestException(AppException):
    status_code = 400
    message = "Bad request"
