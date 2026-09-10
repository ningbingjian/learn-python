import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
broken = subprocess.run(
    [sys.executable, "-c", "import cli"],
    cwd=root / "broken",
    text=True,
    capture_output=True,
    check=False,
    timeout=5,
)
assert broken.returncode != 0
assert "ImportError: cannot import name 'success_message' from 'cli'" in broken.stderr
assert "operations.py" in broken.stderr and "cli.py" in broken.stderr
print("broken: ImportError from partial initialization")
fixed = subprocess.run(
    [sys.executable, "-c", "import cli; print(cli.run())"],
    cwd=root / "fixed",
    text=True,
    capture_output=True,
    check=False,
    timeout=5,
)
assert fixed.returncode == 0 and fixed.stderr == ""
assert fixed.stdout == "Added Read\n"
print("fixed:", fixed.stdout.strip())
