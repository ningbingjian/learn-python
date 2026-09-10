import subprocess
import sys
import unittest
from pathlib import Path


class ImportTests(unittest.TestCase):
    def test_imports_have_no_io(self):
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import task_tracker; import task_tracker.cli; "
                "import task_tracker.__main__",
            ],
            cwd=Path(__file__).resolve().parents[1],
            input="",
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
