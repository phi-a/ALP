"""Cross-check the simple frame and Sun formulas against astropy."""
import unittest
from datetime import datetime
from math import acos, degrees

from astropy.coordinates import PrecessedGeocentric, SkyCoord, get_sun
from astropy.time import Time

from darknessalp import (
    galactic_to_radec, gmst, julian_date, radec_to_galactic, sun_direction)

EPOCHS = [datetime(2026, 3, 20, 14, 46), datetime(2027, 1, 1, 0, 0),
          datetime(2027, 7, 15, 9, 30)]


class TestAgainstAstropy(unittest.TestCase):
    def test_sun_direction_within_a_tenth_of_a_degree(self):
        # our ECI is the mean equinox of date, not GCRS: 0.4 deg apart
        for t in EPOCHS:
            ours = sun_direction(julian_date(t))
            frame = PrecessedGeocentric(equinox=Time(t))
            sun = get_sun(Time(t)).transform_to(frame).cartesian.xyz.value
            sun = sun / (sun @ sun) ** 0.5
            sep = degrees(acos(min(1.0, sum(a * b for a, b in zip(ours, sun)))))
            self.assertLess(sep, 0.1)

    def test_gmst_within_an_arcsecond_of_time(self):
        for t in EPOCHS:
            ref = Time(t).sidereal_time("mean", "greenwich").deg
            self.assertAlmostEqual(gmst(julian_date(t)), ref, delta=0.01)

    def test_galactic_round_trip_matches_skycoord(self):
        for l, b in [(0.0, 0.0), (57.0, 22.0), (300.0, -60.0)]:
            ra, dec = galactic_to_radec(l, b)
            ref = SkyCoord(l=l, b=b, unit="deg", frame="galactic").icrs
            self.assertAlmostEqual(ra, ref.ra.deg, places=3)
            self.assertAlmostEqual(dec, ref.dec.deg, places=3)
            l2, b2 = radec_to_galactic(ref.ra.deg, ref.dec.deg)
            self.assertLess(min(abs(l2 - l), 360 - abs(l2 - l)), 1e-3)
            self.assertAlmostEqual(b2, b, places=3)


if __name__ == "__main__":
    unittest.main()
