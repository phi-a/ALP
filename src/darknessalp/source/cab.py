"""Primordial cosmic ALP background (Conlon & Marsh 2013, arXiv:1304.1804)."""
from scipy.special import gamma
from scipy.stats import weibull_min

CAB_MEAN_KEV = 0.238           # eq. 5.13, modulus mass 5e6 GeV
CAB_FLUX_CM2_S = 0.96e6        # fig. 8, N_eff = 3.62 (delta 0.57)
_SHAPE = 1.5                   # eq. 5.18: E^1/2 exp[-(E/E*)^3/2]


def _scale(mean_kev):
    return mean_kev / gamma(1 + 1 / _SHAPE)


def cab_spectrum(e_kev, mean_kev=CAB_MEAN_KEV):
    """Return the unit-normalised CAB spectrum in keV^-1 at e_kev."""
    return weibull_min.pdf(e_kev, _SHAPE, scale=_scale(mean_kev))


def cab_band_fraction(e_lo_kev, e_hi_kev, mean_kev=CAB_MEAN_KEV):
    """Return the fraction of the CAB flux between e_lo_kev and e_hi_kev."""
    w = weibull_min(_SHAPE, scale=_scale(mean_kev))
    return w.cdf(e_hi_kev) - w.cdf(e_lo_kev)


def cab_flux(delta_neff=0.57):
    """Return the isotropic CAB flux in cm^-2 s^-1, linear in delta_neff."""
    return CAB_FLUX_CM2_S * delta_neff / 0.57
