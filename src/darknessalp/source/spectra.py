"""ALP spectra from a decaying parent: Milky Way line, cosmic continuum."""
import astropy.units as u
import numpy as np
from astropy.cosmology import Planck18

C_CM_S = 2.99792458e10
C_KM_S = 299792.458
GYR_S = 3.15576e16
SIGMA_V_KMS = 165.0       # halo dispersion, v0 / sqrt 2, Evans+ 2019


def dm_density_kev_cm3(cosmo=Planck18):
    """Return today's mean dark-matter density in keV cm^-3."""
    return (cosmo.Odm0 * cosmo.critical_density0).to_value(
        u.keV / u.cm**3, u.mass_energy())


def line_intensity(d_gevcm2, m_kev, share, tau_gyr):
    """Return the Milky Way chi -> aa line intensity, cm^-2 s^-1 sr^-1."""
    d_kev = np.asarray(d_gevcm2, float) * 1e6
    return share * d_kev / (2 * np.pi * m_kev * tau_gyr * GYR_S)


def line_sigma_kev(m_kev, sigma_v_kms=SIGMA_V_KMS):
    """Return the halo Doppler width (one sigma) of the line at m/2, keV."""
    return m_kev / 2 * sigma_v_kms / C_KM_S


def continuum_intensity(e_kev, m_kev, share, tau_gyr, cosmo=Planck18):
    """Return the redshifted chi -> aa intensity, cm^-2 s^-1 sr^-1 keV^-1."""
    e = np.atleast_1d(np.asarray(e_kev, float))
    e0 = m_kev / 2
    inside = (e > 0) & (e < e0)
    z = np.where(inside, e0 / np.where(inside, e, 1.0) - 1, 0.0)
    h = cosmo.H(z).to_value(1 / u.s)
    t_u = cosmo.age(0).to_value(u.Gyr)
    alive = np.exp((t_u - cosmo.age(z).to_value(u.Gyr)) / tau_gyr)

    rate = share * dm_density_kev_cm3(cosmo) / (m_kev * tau_gyr * GYR_S)
    out = C_CM_S / (4 * np.pi) * 2 * rate * alive / (np.where(inside, e, 1.0)
                                                    * h)
    return np.where(inside, out, 0.0)
