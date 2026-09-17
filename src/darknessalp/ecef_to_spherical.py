from math import atan2, degrees, sqrt


def ecef_to_spherical(r_ecef_km):
    """Return geocentric (lat_deg, lon_deg, r_km) of an Earth-fixed point."""
    x, y, z = r_ecef_km
    rho = sqrt(x * x + y * y)
    return degrees(atan2(z, rho)), degrees(atan2(y, x)), sqrt(rho**2 + z * z)
