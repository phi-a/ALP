from math import cos, sin, sqrt


def schmidt_legendre(nmax, theta_rad):
    """Return Schmidt semi-normalised P[n][m] and dP/dtheta[n][m]."""
    ct, st = cos(theta_rad), sin(theta_rad)
    p = [[0.0] * (nmax + 1) for _ in range(nmax + 1)]
    dp = [[0.0] * (nmax + 1) for _ in range(nmax + 1)]
    p[0][0] = 1.0

    for n in range(1, nmax + 1):
        # sectoral term from the previous diagonal
        k = sqrt((2 * n - 1) / (2 * n)) if n > 1 else 1.0
        p[n][n] = k * st * p[n - 1][n - 1]
        dp[n][n] = k * (st * dp[n - 1][n - 1] + ct * p[n - 1][n - 1])

        # remaining orders by recurrence in n
        for m in range(n):
            c1 = (2 * n - 1) / sqrt(n * n - m * m)
            c2 = sqrt((n - 1) ** 2 - m * m) / sqrt(n * n - m * m)
            p2 = p[n - 2][m] if n > 1 else 0.0
            dp2 = dp[n - 2][m] if n > 1 else 0.0
            p[n][m] = c1 * ct * p[n - 1][m] - c2 * p2
            dp[n][m] = c1 * (ct * dp[n - 1][m] - st * p[n - 1][m]) - c2 * dp2
    return p, dp
