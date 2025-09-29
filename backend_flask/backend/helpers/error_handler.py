from marshmallow import ValidationError
from backend.exceptions import APIException


class ErrorHandlerConfigurator:
    @staticmethod
    def init(api):
        @api.errorhandler(APIException)
        def handle_api_exception(error: APIException):
            return {
                'error': error.__class__.__name__,
                'message': error.message
            }, error.status_code

        @api.errorhandler(ValidationError)
        def handle_marshmallow_validation_error(error: ValidationError):
            return {
                'error': 'ValidationError',
                'message': error.messages
            }, 422

        @api.errorhandler(Exception)
        def handle_unexpected_error(error: Exception):
            return {
                'error': 'InternalServerError',
                'message': str(error) or 'Something went wrong'
            }, 500