import pytest

from lulucf.lasso import LassoGrid
from lulucf.validation.exceptions import InvalidLassoError


@pytest.mark.unittest
def test_validation_wrong_xbounds():
    xmin, xmax = 4, 0
    ymin, ymax = 0, 4
    cellsize = 1
    with pytest.raises(InvalidLassoError):
        LassoGrid(xmin, ymin, xmax, ymax, cellsize, cellsize)


@pytest.mark.unittest
def test_validation_wrong_ybounds():
    xmin, xmax = 0, 4
    ymin, ymax = 4, 0
    cellsize = 1
    with pytest.raises(InvalidLassoError):
        LassoGrid(xmin, ymin, xmax, ymax, cellsize, cellsize)


@pytest.mark.unittest
def test_validation_passes():
    xmin, xmax = 0, 4
    ymin, ymax = 0, 4
    cellsize = 1

    try:
        LassoGrid(xmin, ymin, xmax, ymax, cellsize, cellsize)
        validation_passes = True
    except InvalidLassoError as e:
        raise e
    assert validation_passes
