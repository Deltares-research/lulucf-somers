import numba
import numpy as np
from numba.experimental import jitclass

from lulucf.geometry import predicates


@jitclass([("idx", numba.int64[:]), ("values", numba.float64[:, :])])
class PolygonCoordinates:
    def __init__(self, idx, values):
        self.idx = idx
        self.values = values

    def select_index(self, index):
        return self.idx[self.idx == index]

    def select_coordinates(self, index):
        return self.values[self.idx == index]


@jitclass(
    [
        ("xmin", numba.float64),
        ("ymin", numba.float64),
        ("xmax", numba.float64),
        ("ymax", numba.float64),
    ]
)
class Cell:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def get_cell_segments(self):
        return np.array(
            [
                [self.xmin, self.ymin],
                [self.xmax, self.ymin],
                [self.xmax, self.ymax],
                [self.xmin, self.ymax],
                [self.xmin, self.ymin],
            ]
        )

    def contains_point(self, x, y):
        return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax


@numba.njit
def polygon_area(polygon_coords):
    area = 0
    for i in range(len(polygon_coords) - 1):
        x1, y1 = polygon_coords[i]
        x2, y2 = polygon_coords[i + 1]
        area += x1 * y2 - x2 * y1
    return 0.5 * area


@numba.njit
def orientation(polygon_coords):
    area = polygon_area(polygon_coords)
    if area > 0:
        return "ccw"
    elif area < 0:
        return "cw"
    else:
        raise ValueError("Polygon is not valid.")


@numba.njit
def line_intersection(p1, p2, q1, q2):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = q1
    x4, y4 = q2

    # Caluclate determinant
    det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if det == 0:
        return np.array([np.nan, np.nan])  # No intersection (lines are parallel)

    # Calculate intersection coördinates
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / det
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / det

    # Check if intersection is on the line segment
    if 0 <= t <= 1 and 0 <= u <= 1:
        ix = x1 + t * (x2 - x1)
        iy = y1 + t * (y2 - y1)
        return np.array([ix, iy])
    return np.array([np.nan, np.nan])


@numba.njit
def clip_polygon(coords, cell):
    clipped_points = np.full_like(coords, np.nan)
    intersects = np.full(len(coords), 0.0)

    cell_segments = cell.get_cell_segments()

    counter = 0
    for i in range(len(coords) - 1):
        if counter >= len(clipped_points):
            new_clipped_points = np.full((counter * 2, 2), np.nan)
            new_intersects = np.full(counter * 2, 0.0)
            new_clipped_points[:counter] = clipped_points
            new_intersects[:counter] = intersects
            clipped_points = new_clipped_points
            intersects = new_intersects

        p1 = coords[i]
        p2 = coords[i + 1]

        p1_in_cell = cell.contains_point(p1[0], p1[1])
        p2_in_cell = cell.contains_point(p2[0], p2[1])

        for j in range(len(cell_segments) - 1):
            c1 = cell_segments[j]
            c2 = cell_segments[j + 1]

            intersection = line_intersection(p1, p2, c1, c2)
            has_intersection = np.all(~np.isnan(intersection))

            if not (p1_in_cell or p2_in_cell or has_intersection):
                continue
            elif p1_in_cell and p2_in_cell and not has_intersection:
                pass  # Hele segment toevoegen
            elif p2_in_cell and has_intersection and not p1_in_cell:
                pass  # Voeg intersection, p2 toe
            elif p1_in_cell and has_intersection and not p2_in_cell:
                pass  # Voeg p1, intersection toe
            elif not (p1_in_cell or p2_in_cell) and has_intersection:
                pass  # Voeg intersections toe
            else:
                pass  # Kijken of er nog een optie is.

    return clipped_points
