from abc import ABC, abstractmethod

from .exceptions import InvalidBoundsError


class AbstractValidator(ABC):
    @abstractmethod
    def validate(self):
        pass


class LassoValidator(AbstractValidator):
    def __init__(self):
        self.errors = []

    def get_error_message(self):
        return "\n".join([e.message for e in self.errors])

    def validate(self, lasso_grid):
        try:
            self.validate_xbounds(lasso_grid.xmin, lasso_grid.xmax)
        except InvalidBoundsError as e:
            self.errors.append(e)

        try:
            self.validate_ybounds(lasso_grid.ymin, lasso_grid.ymax)
        except InvalidBoundsError as e:
            self.errors.append(e)

    @staticmethod
    def validate_xbounds(xmin: int | float, xmax: int | float):
        if xmin >= xmax:
            raise InvalidBoundsError(
                f"Invalid bounds with xmin >= xmax, {xmin=}, {xmax=}"
            )

    @staticmethod
    def validate_ybounds(ymin: int | float, ymax: int | float):
        if ymin >= ymax:
            raise InvalidBoundsError(
                f"Invalid bounds with ymin >= ymax, {ymin=}, {ymax=}"
            )
