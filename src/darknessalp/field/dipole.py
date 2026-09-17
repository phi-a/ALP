"""Tilted centred dipole from the IGRF degree-1 coefficients."""
import numpy as np

from darknessalp.constants import R_EARTH_KM


def dipole_moment(coeffs):
    """Return the degree-1 coefficient vector (g11, h11, g10) in nT."""
    g, h = coeffs
    return np.array([g[1, 1], h[1, 1], g[1, 0]])


def dipole_axis(coeffs):
    """Return the unit vector of the dipole axis toward magnetic north."""
    m = -dipole_moment(coeffs)
    return m / np.linalg.norm(m)


def dipole_field(r_ecef, coeffs):
    """Return the dipole field in tesla, ECEF axes, for (N, 3) points."""
    r = np.atleast_2d(r_ecef)
    gvec = dipole_moment(coeffs)
    r2 = np.sum(r * r, axis=1, keepdims=True)
    dot = np.sum(r * gvec, axis=1, keepdims=True) / r2
    scale = (R_EARTH_KM**2 / r2) ** 1.5 * 1e-9
    return scale * (3 * dot * r - gvec)
