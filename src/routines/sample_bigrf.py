"""BIGRF magnetic-field sampling routine.

Wraps a FORMS handle and collects B-field snapshots at each call.
Uses the handle's BGCRS / BLocal variables, which the derive phase
refreshes from the IGRF-13 model after every propagation step.
"""

import math


class BIGRFSampler:
    """Collect IGRF-13 B-field samples from a running FORMS simulation.

    Parameters
    ----------
    forms_handle : FORMS
        Initialised handle with a loaded orbit and active propagator.

    Usage
    -----
    sampler = BIGRFSampler(f)
    while not done:
        f.satellite.step()
        f.derive()
        sampler.record()
    df = sampler.to_records()
    """

    def __init__(self, forms_handle):
        self._f = forms_handle
        self._rows = []

    # ------------------------------------------------------------------
    def record(self):
        """Snapshot the current B-field and position into the buffer."""
        f = self._f
        prop = f.satellite.propagator

        t_s = prop.tse * 86400.0

        bgcrs = list(f.BGCRS)
        bloc = list(f.BLocal)
        bmag = math.sqrt(sum(x * x for x in bgcrs))

        self._rows.append({
            "t_s": t_s,
            "lat_deg": float(f.lat),
            "lon_deg": float(f.lon),
            "alt_km": float(f.alt),
            "Bx_gcrs_nT": bgcrs[0] * 1e9,
            "By_gcrs_nT": bgcrs[1] * 1e9,
            "Bz_gcrs_nT": bgcrs[2] * 1e9,
            "Br_local_nT": bloc[0] * 1e9,
            "Btheta_local_nT": bloc[1] * 1e9,
            "Bphi_local_nT": bloc[2] * 1e9,
            "Bmag_nT": bmag * 1e9,
        })

    # ------------------------------------------------------------------
    def to_records(self):
        """Return collected samples as a list of dicts."""
        return list(self._rows)

    def reset(self):
        """Clear the sample buffer."""
        self._rows.clear()

    def __len__(self):
        return len(self._rows)
