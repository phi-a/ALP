from math import acos, asin, degrees, sqrt

from darknessalp.constants import R_EARTH_KM


def earth_limb_angle(r_eci_km, n_hat):
    """Return degrees from boresight to the limb; negative looks at Earth."""
    x, y, z = r_eci_km
    r = sqrt(x * x + y * y + z * z)
    nadir_cos = -(x * n_hat[0] + y * n_hat[1] + z * n_hat[2]) / r
    nadir_angle = degrees(acos(max(-1.0, min(1.0, nadir_cos))))
    return nadir_angle - degrees(asin(R_EARTH_KM / r))
