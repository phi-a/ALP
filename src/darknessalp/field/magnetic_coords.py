"""Centred-dipole magnetic coordinates and the Stormer cut-off."""
import numpy as np

from darknessalp.constants import R_EARTH_KM
from darknessalp.field.dipole import dipole_axis


def magnetic_latitude(r_ecef, coeffs):
    """Return dipole magnetic latitude in degrees for (N, 3) ECEF points."""
    r = np.atleast_2d(r_ecef)
    cos_colat = r @ dipole_axis(coeffs) / np.linalg.norm(r, axis=1)
    return np.degrees(np.arcsin(np.clip(cos_colat, -1, 1)))


def l_shell(mag_lat_deg, r_km):
    """Return the dipole L-shell of a point."""
    return (r_km / R_EARTH_KM) / np.cos(np.radians(mag_lat_deg)) ** 2


def cutoff_rigidity(mag_lat_deg, r_km):
    """Return the Stormer vertical cut-off rigidity in GV."""
    cos4 = np.cos(np.radians(mag_lat_deg)) ** 4
    return 14.9 * cos4 / (r_km / R_EARTH_KM) ** 2
