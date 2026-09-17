from math import sqrt


def fov_axes(n_hat, up_hint=(0.0, 0.0, 1.0)):
    """Return (x_hat, y_hat) across the boresight; y_hat toward up_hint."""
    dot = sum(u * n for u, n in zip(up_hint, n_hat))
    y = [u - dot * n for u, n in zip(up_hint, n_hat)]
    norm = sqrt(sum(v * v for v in y))
    y = tuple(v / norm for v in y)
    x = (y[1] * n_hat[2] - y[2] * n_hat[1],
         y[2] * n_hat[0] - y[0] * n_hat[2],
         y[0] * n_hat[1] - y[1] * n_hat[0])
    return x, y
