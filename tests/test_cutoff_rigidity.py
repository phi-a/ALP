import unittest

from darknessalp import cutoff_rigidity


class TestCutoffRigidity(unittest.TestCase):
    def test_stormer_values(self):
        self.assertAlmostEqual(cutoff_rigidity(0.0, 6371.2), 14.9)
        self.assertAlmostEqual(cutoff_rigidity(45.0, 6371.2), 3.725)
        self.assertAlmostEqual(cutoff_rigidity(90.0, 6371.2), 0.0)
        self.assertAlmostEqual(cutoff_rigidity(0.0, 12742.4), 14.9 / 4)


if __name__ == "__main__":
    unittest.main()
