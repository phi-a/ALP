from math import acos, degrees


def angular_separation(u, v):
    """Return the angle in degrees between two unit vectors."""
    dot = u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
    return degrees(acos(max(-1.0, min(1.0, dot))))
