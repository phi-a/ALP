from math import cos, radians, sin


def eci_to_ecef(v, gmst_deg):
    """Return the vector rotated from ECI into Earth-fixed axes."""
    c, s = cos(radians(gmst_deg)), sin(radians(gmst_deg))
    x, y, z = v
    return (c * x + s * y, -s * x + c * y, z)
