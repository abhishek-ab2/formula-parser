__all__ = ['ERRORS', 'CustomException', 'get_error_desc', 'get_custom_error']

import traceback


class CustomException(Exception):
    default_message = 'Error in {field}: {message}'
    base_type: type[Exception] = Exception

    def __init__(self, message: str, field: str = '', description: str = ''):
        self.message = message or self.default_message
        self.field = field
        self.description = description

    def get_message(self):
        return self.message.format(
                message=self.message,
                field=self.field
        )


class Syntax(CustomException):
    default_message = 'Syntax Error in {field}: {message}'
    base_type = SyntaxError


class Undefined(CustomException):
    default_message = 'Undefined variable/function in {field}: {message}'
    base_type = NameError


class ZeroDivision(CustomException):
    default_message = 'ZeroDivision in {field}: {message}'
    base_type = ZeroDivisionError


class Type(CustomException):
    default_message = 'TypeError in {field}: {message}'
    base_type = TypeError


def get_error_desc(error: Exception):
    traceback_lines = tuple(reversed(traceback.format_exception(type(error), error, error.__traceback__)))

    desc = ''
    for i, line in enumerate(traceback_lines):
        if '^' in line:
            desc = '\n'.join((traceback_lines[i+1], traceback_lines[i]))
            break

    return desc


def get_custom_error(exc: Exception):
    return ERRORS.get(type(exc), CustomException)


ERRORS = {
    error.base_type: error
    for error in (Syntax, Undefined, ZeroDivision, Type, CustomException)
}
