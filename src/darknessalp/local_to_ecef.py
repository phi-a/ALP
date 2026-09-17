from math import cos, sin


def local_to_ecef(b_local, theta_rad, phi_rad):
    """Return a (B_r, B_theta, B_phi) vector in Earth-fixed x, y, z."""
    b_r, b_t, b_p = b_local
    ct, st = cos(theta_rad), sin(theta_rad)
    cp, sp = cos(phi_rad), sin(phi_rad)
    return (b_r * st * cp + b_t * ct * cp - b_p * sp,
            b_r * st * sp + b_t * ct * sp + b_p * cp,
            b_r * ct - b_t * st)
