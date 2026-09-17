from math import cos, radians, sin


def sun_direction(jd):
    """Return the ECI unit vector toward the Sun (Almanac low precision)."""
    n = jd - 2451545.0
    mean_lon = radians((280.460 + 0.9856474 * n) % 360)
    anomaly = radians((357.528 + 0.9856003 * n) % 360)
    lon = mean_lon + radians(1.915 * sin(anomaly) + 0.020 * sin(2 * anomaly))
    obliquity = radians(23.439 - 0.0000004 * n)
    return (cos(lon), cos(obliquity) * sin(lon), sin(obliquity) * sin(lon))
