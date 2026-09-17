from math import hypot

from darknessalp.angular_separation import angular_separation


def project_to_fov(v, n_hat, x_hat, y_hat):
    """Return (x_deg, y_deg) offsets of a unit vector from the boresight."""
    theta = angular_separation(v, n_hat)
    px = sum(a * b for a, b in zip(v, x_hat))
    py = sum(a * b for a, b in zip(v, y_hat))
    norm = hypot(px, py)
    if norm == 0.0:
        return 0.0, 0.0

    # angular-offset projection: radius is the true angle from centre
    return theta * px / norm, theta * py / norm
