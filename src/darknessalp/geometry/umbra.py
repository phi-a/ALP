"""Cylindrical Earth-shadow test."""
import numpy as np

from darknessalp.constants import R_EARTH_KM


def in_umbra(r_eci, sun_hats):
    """Return a bool per row: spacecraft inside the cylindrical shadow."""
    r = np.atleast_2d(r_eci)
    s = np.atleast_2d(sun_hats)
    along = np.sum(r * s, axis=1)
    across2 = np.sum(r * r, axis=1) - along**2
    return (along < 0) & (across2 < R_EARTH_KM**2)
