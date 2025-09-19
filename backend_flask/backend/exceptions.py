class APIException(Exception):
    status_code = 400
    message = 'Something went wrong'

    def __init__(self, message: str | None = None, status_code: int | None = None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)


class NotFound(APIException):
    status_code = 404
    message = 'Resource not found'


class AlreadyExists(APIException):
    status_code = 409
    message = 'Resource already exists'


class PermissionDenied(APIException):
    status_code = 403
    message = 'Permission denied'


class ValidationError(APIException):
    status_code = 422
    message = 'Validation failed'