from math import asin, degrees, sqrt


def magnetic_latitude(r_ecef_km, coeffs):
    """Return centred-dipole magnetic latitude in degrees."""
    gx, gy = coeffs[(1, 1)]
    gz = coeffs[(1, 0)][0]
    x, y, z = r_ecef_km
    g = sqrt(gx * gx + gy * gy + gz * gz)
    r = sqrt(x * x + y * y + z * z)

    # the dipole axis points opposite to the n=1 coefficient vector
    return degrees(asin(-(gx * x + gy * y + gz * z) / (g * r)))
