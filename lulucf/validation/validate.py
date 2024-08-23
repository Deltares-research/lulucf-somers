import sys
from functools import wraps

from .exceptions import InvalidLassoError
from .validators import LassoValidator


def validate_lasso(f):
    @wraps(f)
    def wrapper(*args):
        validator = LassoValidator()
        lasso = f(*args)

        validator.validate(lasso)
        if validator.errors:
            message = validator.get_error_message()

            input_ = ", ".join([str(a) for a in args])
            raise InvalidLassoError(
                f"\nInvalid LassoGrid call with: LassoGrid({input_})\n\n{message}"
            )
        return lasso

    return wrapper
