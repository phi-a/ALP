from math import asin, cos, pi, sin, sqrt

from darknessalp.constants import R_EARTH_KM
from darknessalp.fov_axes import fov_axes


def earth_limb_directions(r_eci_km, n_points=180):
    """Return unit vectors along the Earth limb seen from the spacecraft."""
    r = sqrt(sum(x * x for x in r_eci_km))
    nadir = tuple(-x / r for x in r_eci_km)
    rho = asin(R_EARTH_KM / r)
    a, b = fov_axes(nadir, (1.0, 0.0, 0.0) if abs(nadir[0]) < 0.9
                    else (0.0, 1.0, 0.0))
    limb = []
    for k in range(n_points):
        phi = 2 * pi * k / n_points
        limb.append(tuple(cos(rho) * nadir[i]
                          + sin(rho) * (cos(phi) * a[i] + sin(phi) * b[i])
                          for i in range(3)))
    return limb
