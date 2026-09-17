from math import asin, atan2, cos, degrees, radians, sin

RA_POLE, DEC_POLE, L_NCP = 192.85948, 27.12825, 122.93192  # J2000


def galactic_to_radec(l_deg, b_deg):
    """Return J2000 (ra_deg, dec_deg) of Galactic (l, b)."""
    b, dl = radians(b_deg), radians(L_NCP - l_deg)
    dec_pole = radians(DEC_POLE)
    dec = asin(sin(dec_pole) * sin(b) + cos(dec_pole) * cos(b) * cos(dl))
    dra = atan2(cos(b) * sin(dl),
                sin(b) * cos(dec_pole) - cos(b) * sin(dec_pole) * cos(dl))
    return (RA_POLE + degrees(dra)) % 360, degrees(dec)
