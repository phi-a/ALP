"""Skipper-CCD response: window, silicon, resolution, counts per bin."""
import numpy as np
from scipy.stats import norm

# NIST mass attenuation (Hubbell & Seltzer), keV and cm^2/g; K edges split
_E_AL = [1.0, 1.5, 1.5596, 1.5596001, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0,
         15.0, 20.0]
_MU_AL = [1185.0, 402.2, 362.1, 3957.0, 2263.0, 788.0, 360.5, 193.4, 115.3,
          50.33, 26.23, 7.955, 3.441]
_E_SI = [1.0, 1.5, 1.8389, 1.8389001, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0,
         15.0, 20.0]
_MU_SI = [1570.0, 535.5, 309.2, 3192.0, 2777.0, 978.4, 452.9, 245.0, 147.0,
          64.68, 33.89, 10.34, 4.464]
RHO_AL_G_CM3, RHO_SI_G_CM3 = 2.699, 2.330
FWHM_PER_SIGMA = 2 * np.sqrt(2 * np.log(2))


def _mu_cm(e_kev, energies, mu_rho, rho):
    """Return the linear attenuation coefficient in cm^-1, log-log interp."""
    x = np.log(np.asarray(e_kev, float))
    return rho * np.exp(np.interp(x, np.log(energies), np.log(mu_rho)))


def window_transmission(e_kev, al_nm=50.0):
    """Return the fraction passing an aluminium entrance window."""
    return np.exp(-_mu_cm(e_kev, _E_AL, _MU_AL, RHO_AL_G_CM3) * al_nm * 1e-7)


def silicon_absorption(e_kev, thickness_um=500.0, dead_um=0.0):
    """Return the fraction absorbed in the active silicon."""
    mu = _mu_cm(e_kev, _E_SI, _MU_SI, RHO_SI_G_CM3)
    reach = np.exp(-mu * dead_um * 1e-4)
    return reach * (1 - np.exp(-mu * thickness_um * 1e-4))


def quantum_efficiency(e_kev, al_nm=50.0, thickness_um=500.0, dead_um=0.0):
    """Return window transmission times silicon absorption."""
    return (window_transmission(e_kev, al_nm)
            * silicon_absorption(e_kev, thickness_um, dead_um))


def resolution_fwhm_kev(e_kev, noise_fwhm_kev=0.119, fano=0.118, w_ev=3.72):
    """Return FWHM in keV: Fano broadening and readout noise in quadrature."""
    fano_fwhm = FWHM_PER_SIGMA * np.sqrt(fano * w_ev * np.asarray(e_kev)
                                         * 1e3) * 1e-3
    return np.sqrt(fano_fwhm**2 + noise_fwhm_kev**2)


def grasp_cm2sr(area_cm2=12.0, half_angle_deg=10.0):
    """Return geometric area times the cone solid angle."""
    return area_cm2 * 2 * np.pi * (1 - np.cos(np.radians(half_angle_deg)))


def redistribution(e_kev, e_edges_kev, fwhm_kev=None):
    """Return R[E, j]: the fraction of events at E measured in bin j."""
    e = np.atleast_1d(np.asarray(e_kev, float))
    fwhm = resolution_fwhm_kev(e) if fwhm_kev is None else fwhm_kev
    sigma = np.broadcast_to(np.asarray(fwhm) / FWHM_PER_SIGMA, e.shape)
    cdf = norm.cdf((np.asarray(e_edges_kev)[None, :] - e[:, None])
                   / sigma[:, None])
    return np.diff(cdf, axis=1)


def expected_counts(e_kev, intensity, e_edges_kev, prob, dt_s, qe=None,
                    area_cm2=12.0, half_angle_deg=10.0, live=0.5,
                    select=1.0, fwhm_kev=None):
    """Return counts (samples, bins) for an ALP intensity per keV per sr."""
    e = np.asarray(e_kev, float)
    de = np.diff(e)
    weight = np.concatenate([[de[0] / 2], (de[:-1] + de[1:]) / 2,
                             [de[-1] / 2]])                 # trapezoid
    qe = quantum_efficiency(e) if qe is None else qe
    per_kev = weight * np.asarray(intensity) * qe
    per_bin = per_kev @ redistribution(e, e_edges_kev, fwhm_kev)
    scale = grasp_cm2sr(area_cm2, half_angle_deg) * live * select
    return np.outer(np.asarray(prob) * np.asarray(dt_s), per_bin) * scale
