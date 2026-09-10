"""Author-side verification; run with Python 3.14 from any working directory."""

import ast
import doctest
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
STATES = [
    "01-first-useful-python-program/03-trust-user-input/01-interactive-script",
    "02-collections-and-mutable-state/03-shared-mutable-state/02-collection-model",
    "03-control-flow/03-compose-interactive-cli/03-control-flow-cli",
    "04-functions-and-contracts/03-state-and-scope/04-function-oriented",
    "05-modules-and-packages/03-break-circular-dependencies/05-package-structured",
    "06-classes-and-object-collaboration/03-compose-task-collaborators/06-object-model",
    "07-integration-and-stage-project/02-complete-and-verify-task-tracker/07-complete-task-tracker",
]
SOLUTION = "07-integration-and-stage-project/03-closed-book-transfer/reference-solution"
LABS = [
    "01-first-useful-python-program/03-trust-user-input/float-precision-lab/float_precision.py",
    "02-collections-and-mutable-state/03-shared-mutable-state/shared-mutable-state-lab/shared_mutable_state.py",
    "04-functions-and-contracts/03-state-and-scope/mutable-default-argument-lab/demo.py",
    "04-functions-and-contracts/03-state-and-scope/scope-and-rebinding-lab/demo.py",
    "05-modules-and-packages/03-break-circular-dependencies/circular-import-lab/verify.py",
]


def run(args, cwd):
    result = subprocess.run(
        [sys.executable, *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    if result.returncode:
        raise AssertionError(f"{cwd}:\n{result.stdout}\n{result.stderr}")
    return result


def check_structure():
    modules = sorted(
        path
        for path in ROOT.iterdir()
        if path.is_dir() and re.match(r"0[1-7]-", path.name)
    )
    assert len(modules) == 7, modules
    units = []
    for module in modules:
        current = sorted(
            path
            for path in module.iterdir()
            if path.is_dir() and re.match(r"0[1-3]-", path.name)
        )
        assert len(current) == 3, module
        units.extend(current)
        for unit in current:
            assert (unit / "README.md").is_file(), unit
            assert "BUILT" in (unit / "README.md").read_text(encoding="utf-8"), unit
    print(
        f"structure: {len(modules)} modules, {len(units)} built units, {len(STATES)} milestones"
    )


def check_links():
    count = 0
    for document in ROOT.rglob("*.md"):
        source = re.sub(
            r"```.*?```", "", document.read_text(encoding="utf-8"), flags=re.DOTALL
        )
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", source):
            parsed = urlsplit(target)
            if parsed.scheme or not parsed.path:
                continue
            path = document.parent / unquote(parsed.path)
            assert path.exists(), f"broken link: {document}: {target}"
            count += 1
    print(f"local link targets: {count} (anchors reviewed separately)")


def check_python():
    files = list(ROOT.rglob("*.py"))
    for path in files:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    print(f"Python syntax: {len(files)} files")


def check_transcripts():
    count = 0
    for document in sorted(ROOT.rglob("*.md")):
        source = document.read_text(encoding="utf-8")
        blocks = re.findall(r"```pycon\n(.*?)\n```", source, re.DOTALL)
        if not blocks:
            continue
        parser = doctest.DocTestParser()
        test = parser.get_doctest(
            "\n\n".join(blocks), {}, str(document), str(document), 0
        )
        runner = doctest.DocTestRunner(optionflags=doctest.ELLIPSIS)
        runner.run(test)
        summary = runner.summarize()
        assert summary.failed == 0, document
        count += summary.attempted
    print(f"executable pycon examples: {count}")


def check_branch_examples():
    document = ROOT / "03-control-flow/01-readable-business-branches/README.md"
    pairs = re.findall(
        r"```python\n(.*?)\n```\s*```text\n(.*?)\n```",
        document.read_text(encoding="utf-8"),
        re.DOTALL,
    )
    assert len(pairs) == 17, "Review expected snippet coverage when editing this Unit."
    for code, expected in pairs:
        result = run(["-c", code], ROOT)
        assert result.stdout.strip() == expected.strip(), (code, result.stdout)
        assert not result.stderr, result.stderr
    print(f"preserved branch chapter: {len(pairs)} independent output examples")


def main():
    if sys.version_info[:2] != (3, 14):
        raise SystemExit("Use Python 3.14; this is the course verification baseline.")
    check_structure()
    check_links()
    check_python()
    check_transcripts()
    check_branch_examples()
    total = 0
    for state in [
        *STATES,
        SOLUTION,
        "03-control-flow/03-compose-interactive-cli/exercises",
    ]:
        result = run(["-m", "unittest", "discover", "-s", "tests", "-v"], ROOT / state)
        match = re.search(r"Ran (\d+) tests?", result.stderr)
        assert match and int(match[1]) > 0, state
        total += int(match[1])
        print(f"{Path(state).name}: {match[1]} tests passed")
    for lab in LABS:
        path = ROOT / lab
        result = run([path.name], path.parent)
        expected = re.findall(
            r"```text\n(.*?)\n```",
            (path.parent / "README.md").read_text(encoding="utf-8"),
            re.DOTALL,
        )
        assert expected, path
        assert result.stdout.strip() in [block.strip() for block in expected], (
            path,
            result.stdout,
        )
        assert not result.stderr, (path, result.stderr)
        print(f"{path.parent.name}: expected output passed")
    print(
        f"PASS: {total} behavior tests, {len(LABS)} labs; learning validation not claimed."
    )


if __name__ == "__main__":
    main()
