import unittest

from darknessalp import in_umbra


class TestInUmbra(unittest.TestCase):
    def test_behind_earth(self):
        self.assertTrue(in_umbra((-7000.0, 0.0, 0.0), (1.0, 0.0, 0.0)))

    def test_sunward(self):
        self.assertFalse(in_umbra((7000.0, 0.0, 0.0), (1.0, 0.0, 0.0)))

    def test_beside_shadow(self):
        self.assertFalse(in_umbra((-7000.0, 6500.0, 0.0), (1.0, 0.0, 0.0)))


if __name__ == "__main__":
    unittest.main()
