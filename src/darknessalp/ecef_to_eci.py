from math import cos, radians, sin


def ecef_to_eci(v, gmst_deg):
    """Return the vector rotated from Earth-fixed into ECI axes."""
    c, s = cos(radians(gmst_deg)), sin(radians(gmst_deg))
    x, y, z = v
    return (c * x - s * y, s * x + c * y, z)
