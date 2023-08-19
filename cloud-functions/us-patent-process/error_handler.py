from dataclasses import dataclass, asdict
from enum import Enum
from errors import MethodNotAllowedError


class _ErrorResponseCode(str, Enum):
    INTERNAL_SERVER_ERROR = "internal_server_error"
    INVALID_REQUEST = "invalid_request"
    METHOD_NOT_ALLOWED = "method_not_allowed"


@dataclass
class _ErrorResponse:
    code: _ErrorResponseCode
    message: str


class ErrorHandler:
    @staticmethod
    def handle_error(error: Exception):
        if isinstance(error, MethodNotAllowedError):
            return (
                asdict(
                    _ErrorResponse(_ErrorResponseCode.METHOD_NOT_ALLOWED, str(error))
                ),
                405,
            )
        elif isinstance(error, ValueError):
            return (
                asdict(_ErrorResponse(_ErrorResponseCode.INVALID_REQUEST, str(error))),
                400,
            )
        else:
            return (
                asdict(
                    _ErrorResponse(
                        _ErrorResponseCode.INTERNAL_SERVER_ERROR,
                        _ErrorResponseCode.INTERNAL_SERVER_ERROR,
                    )
                ),
                500,
            )
