import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

from darknessalp import orbit, pointing, sim


class TestStateTable(unittest.TestCase):
    def test_one_orbit_table(self):
        t = np.arange(0, 5600, 600.0)
        r, _ = orbit.circular_orbit(t, 420.0, 51.6)
        n = pointing.fixed_inertial(pointing.target("gc"), len(t))
        table = sim.state_table("2027-05-01T00:00:00", t, r, n, lmax=1)
        self.assertEqual(len(table["amp_tm"]), len(t))
        self.assertTrue(np.all(table["alt_km"] > 400))
        self.assertTrue(np.all(np.abs(table["lat_deg"]) <= 52))
        self.assertTrue(np.all(table["amp_tm"] >= 0))
        occulted = table["occulted"]
        self.assertTrue(np.all(table["limb_deg"][occulted] < 0))
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.csv"
            sim.to_csv(table, path)
            self.assertEqual(len(path.read_text().splitlines()), len(t) + 1)


if __name__ == "__main__":
    unittest.main()
