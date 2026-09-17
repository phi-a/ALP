"""
yamamoto.py
------------
Key equations from Yamamoto et al. (2020) JCAP 02 (2020) 011
"A search for a contribution from axion-like particles to the X-ray diffuse background utilizing the Earth's magnetic field"

Zen-styled version: minimal underscores, variable names close to physics.

Author: Phoenix Alpine (2025)
"""

import numpy as np

# -----------------------------
# 1. Dark matter decay into ALPs
# -----------------------------

def emissivity(rhoDM, GammaDecay, mDM):
    """
    Eq (2.1): ALP emissivity from DM decay.
    """
    return 2 * rhoDM * GammaDecay / mDM


def intensity_line(columnDM, GammaDecay, mDM):
    """
    Eq (2.2): ALP intensity along line of sight.
    """
    return columnDM * GammaDecay / (2 * np.pi * mDM)


def column_density(rhoDMofr, r):
    """
    Eq (2.3): Column density integral of DM profile.
    """
    return np.trapz(rhoDMofr(r), r)


# -----------------------------
# 2. Cosmological ALP spectrum
# -----------------------------

def fcosmo(x, OmegaM=0.315, OmegaL=0.685):
    """
    Eq (2.6): Cosmological function f(x).
    """
    return (OmegaM + (1 - OmegaM - OmegaL) / x - OmegaL / x**3) ** -0.5


def spectrum(Ea, mDM, GammaDecay, rhoDM0, H0=67.8, c=3e5):
    """
    Eq (2.5): Cosmological continuum ALP spectrum.
    Ea in keV, mDM in keV, rhoDM0 in keV cm^-3.
    """
    x = mDM / (2 * Ea)
    pref = np.sqrt(2) * c * GammaDecay * rhoDM0 / (np.pi * H0 * mDM**2.5)
    return pref * Ea**0.5 * fcosmo(x)


# -----------------------------
# 3. ALP-photon conversion
# -----------------------------

def Pgeneral(gCoupling, Bperpofx, xmax, ma, Ea, steps=1000):
    """
    Eq (2.7): General conversion with varying Bperp(x).
    """
    Ea_eV = Ea * 1e3
    q = ma**2 / (2 * Ea_eV)
    xs = np.linspace(0, xmax, steps)
    integrand = Bperpofx(xs) * np.exp(-1j * q * xs)
    integral = np.trapz(integrand, xs)
    return np.abs((gCoupling / 2) * integral)**2


def Puniform(gCoupling, Bperp, Lcoh, ma, Ea):
    """
    Eq (2.10): Conversion probability in uniform field.
    """
    Ea_eV = Ea * 1e3
    q = ma**2 / (2 * Ea_eV)
    num = 2 * Lcoh**2 * (1 - np.cos(q * Lcoh))
    den = (q * Lcoh)**2 if q != 0 else 1
    return ((gCoupling * Bperp / 2)**2) * num / den


def Plight(gCoupling, Bperp, Lcoh):
    """
    Eq (2.11): Light ALP limit qL << 1.
    """
    return (gCoupling * Bperp * Lcoh / 2)**2


def Pscale(gCoupling, BperpL):
    """
    Eq (2.13): Numerical scaling form.
    """
    return 2.45e-21 * (gCoupling / 1e-10)**2 * (BperpL)**2


# -----------------------------
# 4. Coupling constraint
# -----------------------------

def gconstraint(mDM, tauDM, BperpL, rhoDM, H0=67.8, f=1.92):
    """
    Eq (4.1): Upper bound on gCoupling.
    """
    return (3.3e-7
            * (mDM / 10.0)**1.25
            * (tauDM / 4.32e17)**0.5
            * (BperpL / 100.0)**-1
            * (rhoDM / 1.25)**-0.5
            * (H0 / 67.8)**-0.5
            * (f / 1.92)**-0.5)
