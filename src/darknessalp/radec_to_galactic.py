from math import asin, atan2, cos, degrees, radians, sin

from darknessalp.galactic_to_radec import DEC_POLE, L_NCP, RA_POLE


def radec_to_galactic(ra_deg, dec_deg):
    """Return Galactic (l_deg, b_deg) of J2000 (ra, dec)."""
    dec, dra = radians(dec_deg), radians(ra_deg - RA_POLE)
    dec_pole = radians(DEC_POLE)
    b = asin(sin(dec_pole) * sin(dec) + cos(dec_pole) * cos(dec) * cos(dra))
    dl = atan2(cos(dec) * sin(dra),
               sin(dec) * cos(dec_pole) - cos(dec) * sin(dec_pole) * cos(dra))
    return (L_NCP - degrees(dl)) % 360, degrees(b)
