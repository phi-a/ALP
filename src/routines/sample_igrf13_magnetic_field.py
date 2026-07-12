from forms.bricks.models.mag import geomagnetic_field, load_igrf_model


class SampleIGRF13MagneticFieldRoutine:
    """Per-step IGRF-13 magnetic-field routine that holds the FORMS handle."""

    def __init__(self, forms, *, lmax=13, record=True, samples=None):
        self.forms = forms
        self.lmax = lmax
        self.record = record
        self.samples = samples
        self._igrf13_model = None

    def step(self):
        """Evaluate the magnetic field at the current state and publish it."""
        if self._igrf13_model is None:
            self._igrf13_model = load_igrf_model()

        position = self.forms.satellite.get_position().to_list()
        field = geomagnetic_field(
            position,
            self.forms.time.epoch,
            model="igrf13",
            lmax=self.lmax,
            loaded_model=self._igrf13_model,
            return_cartesian="gcrs",
        )
        bx, by, bz = (float(value) for value in field)

        field_variable = self.forms.get_variable("B_IGRF13_GCRS")
        if field_variable is None:
            field_variable = self.forms.types.vector(
                "B_IGRF13_GCRS",
                overwrite=False,
            )

        magnitude_variable = self.forms.get_variable("B_IGRF13_MAG")
        if magnitude_variable is None:
            magnitude_variable = self.forms.types.scalar(
                "B_IGRF13_MAG",
                unit="T",
                overwrite=False,
            )

        field_variable.set(x=bx, y=by, z=bz)
        magnitude = field_variable.magnitude()
        magnitude_variable.set(magnitude)
        if self.record:
            field_variable.mark()
            magnitude_variable.mark()

        if self.samples is None:
            return

        elapsed = (self.forms.time.epoch - self.forms.time.epoch0) * 86400.0
        sample = {
            "time_s": elapsed,
            "position_km": position,
            "field_gcrs_t": [bx, by, bz],
            "magnitude_t": magnitude,
        }
        if self.samples and abs(self.samples[-1]["time_s"] - elapsed) < 1.0e-6:
            self.samples[-1] = sample
            return

        self.samples.append(sample)

    __call__ = step
