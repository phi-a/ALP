from math import cos, radians, sin


def radec_to_eci(ra_deg, dec_deg):
    """Return the ECI unit vector toward (RA, Dec)."""
    ra, dec = radians(ra_deg), radians(dec_deg)
    return (cos(dec) * cos(ra), cos(dec) * sin(ra), sin(dec))
