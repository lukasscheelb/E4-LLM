"""Run pytest with the active Python interpreter and return its exit code."""

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="*", help="pytest paths or node IDs")
    parser.add_argument("--junitxml", type=Path, help="report path; parent must exist")
    args = parser.parse_args()

    command = [sys.executable, "-m", "pytest", "-q"]
    if args.junitxml is not None:
        command.extend(["--junitxml", str(args.junitxml)])
    command.extend(args.targets)

    print(f"Working directory: {Path.cwd()}", flush=True)
    print(f"Command arguments: {command!r}", flush=True)
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
