"""Milky Way dark-matter halo: NFW density and its line-of-sight column."""
import numpy as np
from scipy.integrate import quad

R_SUN_KPC = 8.1
R_S_KPC = 20.0
RHO_SUN_GEV_CM3 = 0.4
R_CORE_KPC = 0.1          # softens the cusp on the exact Galactic Centre ray
R_MAX_KPC = 200.0
KPC_CM = 3.0857e21
_X_SUN = R_SUN_KPC / R_S_KPC
RHO_S_GEV_CM3 = RHO_SUN_GEV_CM3 * _X_SUN * (1 + _X_SUN) ** 2


def nfw_density(r_kpc, rho_s=RHO_S_GEV_CM3, r_s_kpc=R_S_KPC,
                r_core_kpc=R_CORE_KPC):
    """Return the NFW density in GeV cm^-3 at Galactocentric radius r_kpc."""
    x = np.maximum(np.asarray(r_kpc, float), r_core_kpc) / r_s_kpc
    return rho_s / (x * (1 + x) ** 2)


def column_density(l_deg, b_deg, r_max_kpc=R_MAX_KPC, **nfw):
    """Return D = int rho ds in GeV cm^-2 toward Galactic (l, b), per row."""
    l, b = np.broadcast_arrays(np.radians(l_deg), np.radians(b_deg))
    cos_psi = np.cos(l) * np.cos(b)              # angle from the GC direction
    out = np.empty(l.shape)
    for i, c in enumerate(cos_psi.ravel()):
        s_near = R_SUN_KPC * c                   # closest approach to the GC

        def rho_along(s):
            r = np.sqrt(s * s + R_SUN_KPC**2 - 2 * s * R_SUN_KPC * c)
            return nfw_density(r, **nfw)

        breaks = [s_near] if 0 < s_near < r_max_kpc else None
        out.flat[i] = quad(rho_along, 0.0, r_max_kpc, points=breaks,
                           limit=200)[0]
    return out * KPC_CM
