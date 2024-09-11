import numba


@numba.njit
def bbox_overlaps_cell(xmin, ymin, xmax, ymax, bounds):
    overlaps = (
        ((bounds[:, 0] <= xmin) & (bounds[:, 2] >= xmin))
        | ((bounds[:, 0] <= xmax) & (bounds[:, 2] >= xmax))
    ) & (
        ((bounds[:, 1] <= ymin) & (bounds[:, 3] >= ymin))
        | ((bounds[:, 1] <= ymax) & (bounds[:, 3] >= ymax))
    )
    return overlaps


@numba.njit
def bbox_contains_cell(xmin, ymin, xmax, ymax, bounds):
    contains = (
        (xmin >= bounds[:, 0])
        & (xmax <= bounds[:, 2])
        & (ymin >= bounds[:, 1])
        & (ymax <= bounds[:, 3])
    )
    return contains


@numba.njit
def bbox_within_cell(xmin, ymin, xmax, ymax, bounds):
    within = (
        (xmin <= bounds[:, 0])
        & (xmax >= bounds[:, 2])
        & (ymin <= bounds[:, 1])
        & (ymax >= bounds[:, 3])
    )
    return within


@numba.njit
def get_overlapping_polygons(xmin, ymin, xmax, ymax, bounds):
    return (
        bbox_overlaps_cell(xmin, ymin, xmax, ymax, bounds)
        | bbox_contains_cell(xmin, ymin, xmax, ymax, bounds)
        | bbox_within_cell(xmin, ymin, xmax, ymax, bounds)
    )
