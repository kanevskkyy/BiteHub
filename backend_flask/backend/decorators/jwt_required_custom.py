from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import (
    NoAuthorizationError,
    RevokedTokenError,
    FreshTokenRequired,
    CSRFError,
    JWTDecodeError,
    JWTExtendedException,
    UserLookupError
)
from jwt import ExpiredSignatureError, InvalidTokenError, DecodeError

def jwt_required_custom(optional=False, fresh=False, refresh=False, locations=None, verify_type=True):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request(
                    optional=optional,
                    fresh=fresh,
                    refresh=refresh,
                    locations=locations,
                    verify_type=verify_type
                )
                return f(*args, **kwargs)

            except ExpiredSignatureError:
                return {
                    'error': 'token_expired',
                    'message': 'The token has expired. Please log in again or refresh the token.'
                }, 401

            except RevokedTokenError:
                return {
                    'error': 'revoked_token',
                    'message': 'This token has been revoked.'
                }, 401

            except FreshTokenRequired:
                return {
                    'error': 'fresh_token_required',
                    'message': 'This action requires a fresh token.'
                }, 401

            except CSRFError:
                return {
                    'error': 'csrf_error',
                    'message': 'CSRF check failed.'
                }, 401

            except (InvalidTokenError, DecodeError, JWTDecodeError):
                return {
                    'error': 'invalid_token',
                    'message': 'The token is invalid or malformed.'
                }, 422

            except NoAuthorizationError:
                return {
                    'error': 'authorization_required',
                    'message': 'Authorization token is required.'
                }, 401

            except UserLookupError:
                return {
                    'error': 'user_lookup_failed',
                    'message': 'The user associated with this token was not found.'
                }, 404

            except JWTExtendedException as e:
                return {
                    'error': 'jwt_error',
                    'message': str(e)
                }, 400

        return decorated_function
    return decorator