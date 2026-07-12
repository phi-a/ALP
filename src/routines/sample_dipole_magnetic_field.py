import numpy as np


class SampleDipoleMagneticFieldRoutine:
    """Per-step aligned-dipole magnetic-field routine that holds the FORMS handle."""

    def __init__(
        self,
        forms,
        *,
        earth_radius_km,
        equatorial_surface_field_nt,
        dipole_axis_gcrs,
        samples=None,
    ):
        self.forms = forms
        self.earth_radius_km = float(earth_radius_km)
        self.equatorial_surface_field_nt = float(equatorial_surface_field_nt)
        self.dipole_axis_gcrs = np.array(dipole_axis_gcrs, dtype=float)
        self.samples = samples

    def step(self):
        """Evaluate the aligned dipole field at the current state and publish it."""
        position_km = np.array(self.forms.satellite.get_position().to_list(), dtype=float)
        radius_km = np.linalg.norm(position_km)
        radial_hat = position_km / radius_km
        dipole_hat = self.dipole_axis_gcrs

        scale_nt = self.equatorial_surface_field_nt * (
            self.earth_radius_km / radius_km
        ) ** 3
        field_nt = scale_nt * (
            3.0 * np.dot(dipole_hat, radial_hat) * radial_hat - dipole_hat
        )
        magnitude_nt = float(np.linalg.norm(field_nt))

        field_variable = self.forms.get_variable("B_CUSTOM_GCRS")
        if field_variable is None:
            field_variable = self.forms.types.vector(
                "B_CUSTOM_GCRS",
                overwrite=False,
            )

        magnitude_variable = self.forms.get_variable("B_CUSTOM_MAG")
        if magnitude_variable is None:
            magnitude_variable = self.forms.types.scalar(
                "B_CUSTOM_MAG",
                unit="nT",
                overwrite=False,
            )

        field_variable.set(
            x=float(field_nt[0]),
            y=float(field_nt[1]),
            z=float(field_nt[2]),
        )
        magnitude_variable.set(magnitude_nt)
        field_variable.mark()
        magnitude_variable.mark()

        if self.samples is None:
            return

        elapsed_s = (self.forms.time.epoch - self.forms.time.epoch0) * 86400.0
        sample = {
            "time_s": float(elapsed_s),
            "position_km": position_km.copy(),
            "field_nt": field_nt.copy(),
            "magnitude_nt": magnitude_nt,
        }
        if self.samples and abs(self.samples[-1]["time_s"] - elapsed_s) < 1.0e-6:
            self.samples[-1] = sample
            return

        self.samples.append(sample)

    __call__ = step
