import unittest

from darknessalp import load_igrf


class TestLoadIgrf(unittest.TestCase):
    def test_epoch_values(self):
        self.assertEqual(load_igrf(2025.0)[(1, 0)], (-29350.0, 0.0))
        self.assertEqual(load_igrf(2020.0)[(1, 1)], (-1451.37, 4653.35))

    def test_interpolation_and_extrapolation(self):
        g, _ = load_igrf(2022.5)[(1, 0)]
        self.assertAlmostEqual(g, (-29403.41 - 29350.0) / 2)
        g, _ = load_igrf(2027.0)[(1, 0)]
        self.assertAlmostEqual(g, -29350.0 + 2 * 12.6)

    def test_degree_13_present(self):
        self.assertIn((13, 13), load_igrf(2027.0))

    def test_out_of_range(self):
        with self.assertRaises(ValueError):
            load_igrf(2031.0)


if __name__ == "__main__":
    unittest.main()
