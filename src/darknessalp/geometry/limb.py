"""Earth limb geometry seen from the spacecraft."""
import numpy as np

from darknessalp.constants import R_EARTH_KM
from darknessalp.geometry.fov import fov_axes


def earth_angular_radius_deg(r_eci):
    """Return the angular radius of the Earth disk from the spacecraft."""
    return np.degrees(np.arcsin(R_EARTH_KM / np.linalg.norm(r_eci)))


def limb_angle(r_eci, n_hats):
    """Return degrees from boresight(s) to the limb; negative = at Earth."""
    n = np.atleast_2d(n_hats)
    nadir = -r_eci / np.linalg.norm(r_eci)
    nadir_angle = np.degrees(np.arccos(np.clip(n @ nadir, -1, 1)))
    return nadir_angle - earth_angular_radius_deg(r_eci)


def limb_directions(r_eci, n_points=180):
    """Return (n_points, 3) unit vectors along the limb ring."""
    nadir = -r_eci / np.linalg.norm(r_eci)
    rho = np.radians(earth_angular_radius_deg(r_eci))
    hint = (1.0, 0.0, 0.0) if abs(nadir[0]) < 0.9 else (0.0, 1.0, 0.0)
    a, b = fov_axes(nadir, hint)
    phi = np.linspace(0, 2 * np.pi, n_points, endpoint=False)[:, None]
    return (np.cos(rho) * nadir
            + np.sin(rho) * (np.cos(phi) * a + np.sin(phi) * b))
