from http import HTTPStatus


class CustomException(Exception):
    code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.message = message


class NoCustomerExistanceException(CustomException):
    code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    message = HTTPStatus.FORBIDDEN.description


class NoEventException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description


class NoDoubleEventException(CustomException):
    code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = HTTPStatus.BAD_REQUEST.description


class TicketNotAvailableException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description
