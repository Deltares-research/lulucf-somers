from abc import ABC, abstractmethod

from .exceptions import InvalidBoundsError, InvalidLassoError


class AbstractValidator(ABC):
    @abstractmethod
    def validate(self):
        pass


class LassoValidator(AbstractValidator):
    def validate(self, *args):
        errors = []
        xmin, ymin, xmax, ymax, *cellsize = args

        try:
            self.validate_xbounds(xmin, xmax)
        except InvalidBoundsError as e:
            errors.append(str(e))

        try:
            self.validate_ybounds(ymin, ymax)
        except InvalidBoundsError as e:
            errors.append(str(e))

        if errors:
            raise InvalidLassoError("Invalid LassoGrid with errors:", errors)

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
