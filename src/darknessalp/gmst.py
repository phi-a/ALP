def gmst(jd):
    """Return Greenwich mean sidereal time in degrees at a UT1 Julian date."""
    t = (jd - 2451545.0) / 36525.0
    seconds = (67310.54841 + (876600.0 * 3600 + 8640184.812866) * t
               + 0.093104 * t**2 - 6.2e-6 * t**3)
    return (seconds / 240.0) % 360.0
