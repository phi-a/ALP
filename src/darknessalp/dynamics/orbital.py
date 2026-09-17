"""Orbital accelerations, km/s^2, for (N, 3) positions in km."""
import numpy as np

from darknessalp.constants import J2, MU_EARTH_KM3_S2, R_EQUATOR_KM


def two_body(r):
    """Return the point-mass acceleration."""
    r = np.atleast_2d(r)
    return -MU_EARTH_KM3_S2 * r / np.linalg.norm(r, axis=1, keepdims=True)**3


def j2_acceleration(r):
    """Return the J2 oblateness acceleration."""
    r = np.atleast_2d(r)
    x, y, z = r.T
    rr = np.linalg.norm(r, axis=1)
    k = 1.5 * J2 * MU_EARTH_KM3_S2 * R_EQUATOR_KM**2 / rr**5
    zz = 5 * z**2 / rr**2
    return (k * np.stack([x * (zz - 1), y * (zz - 1), z * (zz - 3)])).T


def two_body_j2(r):
    """Return two-body plus J2 acceleration."""
    return two_body(r) + j2_acceleration(r)
