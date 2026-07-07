#!/usr/bin/env python3
"""Install module dependencies in a developer-friendly way."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULES_ROOT = ROOT / "modules"


def discover_requirements() -> list[Path]:
    requirements_files: list[Path] = []
    for module_dir in sorted(MODULES_ROOT.iterdir()):
        if not module_dir.is_dir():
            continue
        requirement_path = module_dir / "requirements.txt"
        if requirement_path.exists():
            requirements_files.append(requirement_path)
    return requirements_files


def install_requirements(requirements_files: list[Path], dry_run: bool = False) -> int:
    for requirements_path in requirements_files:
        module_name = requirements_path.parent.name
        print(f"[{module_name}] {'Would install' if dry_run else 'Installing'} {requirements_path.name}")
        if dry_run:
            continue
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)],
            check=True,
            cwd=str(ROOT),
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Show modules that would be installed")
    args = parser.parse_args()

    requirements_files = discover_requirements()
    if not requirements_files:
        print("No module requirements.txt files were found.")
        return 0
    return install_requirements(requirements_files, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
