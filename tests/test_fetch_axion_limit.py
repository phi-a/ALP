import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from darknessalp import fetch_axion_limit


class TestFetchAxionLimit(unittest.TestCase):
    def test_reads_cached_file(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "AxionPhoton" / "Fake.txt"
            path.parent.mkdir()
            path.write_text("# m g\n1e-6 1e-10\n2e-6 2e-10\n")

            m, g = fetch_axion_limit("Fake.txt", cache_dir=tmp)

        self.assertEqual(m, [1e-6, 2e-6])
        self.assertEqual(g, [1e-10, 2e-10])


if __name__ == "__main__":
    unittest.main()
