import subprocess
import sys
import unittest
from pathlib import Path


class ChecklistTests(unittest.TestCase):
    def run_cli(self, transcript):
        result = subprocess.run(
            [sys.executable, "reference.py"],
            cwd=Path(__file__).resolve().parents[1],
            input=transcript,
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertIn("Bye.", result.stdout)
        return result.stdout

    def test_empty(self):
        self.assertIn("Empty.", self.run_cli("list\nquit\n"))

    def test_invalid_name_does_not_consume_id(self):
        output = self.run_cli("add\n \nadd\nBook\nlist\nquit\n")
        self.assertIn("Error: name cannot be empty.", output)
        self.assertIn("#1 [ ] Book", output)
        self.assertNotIn("Added #2.", output)

    def test_order(self):
        output = self.run_cli("add\nBook\nadd\nCoat\nlist\nquit\n")
        self.assertLess(output.index("#1 [ ] Book"), output.index("#2 [ ] Coat"))

    def test_repeat_pack_and_session_continues(self):
        output = self.run_cli("add\nBook\npack\n1\npack\n1\nadd\nCoat\nlist\nquit\n")
        self.assertEqual(output.count("Packed #1."), 1)
        self.assertIn("Already packed.", output)
        self.assertIn("#1 [x] Book", output)
        self.assertIn("#2 [ ] Coat", output)

    def test_bad_and_missing_id(self):
        output = self.run_cli("pack\nabc\npack\n99\nlist\nquit\n")
        self.assertIn("Error: id must be an integer.", output)
        self.assertIn("Error: item #99 does not exist.", output)
        self.assertIn("Empty.", output)

    def test_commands_recover(self):
        output = self.run_cli("\nunknown\n QUIT \n")
        self.assertIn("Enter a command.", output)
        self.assertIn("Unknown command: unknown", output)


if __name__ == "__main__":
    unittest.main()
