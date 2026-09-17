from math import atan2, cos, sin, sqrt

from darknessalp.constants import R_EARTH_KM
from darknessalp.local_to_ecef import local_to_ecef
from darknessalp.schmidt_legendre import schmidt_legendre


def igrf_field(r_ecef_km, coeffs, lmax=13):
    """Return the IGRF field in tesla, Earth-fixed axes, at an ECEF point."""
    x, y, z = r_ecef_km
    rho = sqrt(x * x + y * y)
    r = sqrt(rho**2 + z * z)
    theta, phi = atan2(rho, z), atan2(y, x)
    p, dp = schmidt_legendre(lmax, theta)

    b_r = b_theta = b_phi = 0.0
    for n in range(1, lmax + 1):
        scale = (R_EARTH_KM / r) ** (n + 2)
        for m in range(n + 1):
            g, h = coeffs[(n, m)]
            cm, sm = cos(m * phi), sin(m * phi)
            b_r += (n + 1) * scale * (g * cm + h * sm) * p[n][m]
            b_theta -= scale * (g * cm + h * sm) * dp[n][m]
            b_phi += scale * m * (g * sm - h * cm) * p[n][m]

    st = sin(theta)
    b_phi = b_phi / st if st > 1e-12 else 0.0
    return local_to_ecef((b_r * 1e-9, b_theta * 1e-9, b_phi * 1e-9),
                         theta, phi)
