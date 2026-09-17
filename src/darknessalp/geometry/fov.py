"""Field-of-view frame: offsets around a boresight and cone quadrature."""
import numpy as np


def fov_axes(n_hat, up_hint=(0.0, 0.0, 1.0)):
    """Return (x_hat, y_hat) across the boresight; y_hat toward up_hint."""
    n = np.asarray(n_hat, float)
    up = np.asarray(up_hint, float)
    if abs(np.dot(up, n)) > 0.999:   # boresight along the hint: use x
        up = np.array([1.0, 0.0, 0.0])
    y = up - np.dot(up, n) * n
    y = y / np.linalg.norm(y)
    return np.cross(y, n), y


def project(v, n_hat, x_hat, y_hat):
    """Return (x_deg, y_deg) offsets; radius is the true angle from centre."""
    v = np.atleast_2d(v)
    theta = np.degrees(np.arccos(np.clip(v @ n_hat, -1, 1)))
    px, py = v @ x_hat, v @ y_hat
    norm = np.hypot(px, py)
    norm = np.where(norm == 0, 1.0, norm)
    return theta * px / norm, theta * py / norm


def direction(x_deg, y_deg, n_hat, x_hat, y_hat):
    """Return unit vectors at angular offsets (x, y) from the boresight."""
    x, y = np.broadcast_arrays(np.asarray(x_deg, float),
                               np.asarray(y_deg, float))
    theta = np.radians(np.hypot(x, y))
    norm = np.where(theta == 0, 1.0, np.hypot(x, y))
    cx, cy = (x / norm)[..., None], (y / norm)[..., None]
    return (np.cos(theta)[..., None] * n_hat
            + np.sin(theta)[..., None] * (cx * x_hat + cy * y_hat))


def cone_directions(n_hat, half_angle_deg=10.0, rings=3):
    """Return (M, 3) directions and equal-area weights sampling the cone."""
    x_hat, y_hat = fov_axes(n_hat)
    edges = half_angle_deg * np.sqrt(np.arange(rings + 1) / rings)
    xs, ys, ws = [0.0], [0.0], [edges[1] ** 2]
    for k in range(1, rings):
        r_mid = 0.5 * (edges[k] + edges[k + 1])
        count = 6 * k
        phi = 2 * np.pi * np.arange(count) / count
        xs += list(r_mid * np.cos(phi))
        ys += list(r_mid * np.sin(phi))
        ws += [(edges[k + 1] ** 2 - edges[k] ** 2) / count] * count
    dirs = direction(np.array(xs), np.array(ys), n_hat, x_hat, y_hat)
    weights = np.array(ws) / sum(ws)
    return dirs, weights
