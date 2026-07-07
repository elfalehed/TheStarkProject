#!/usr/bin/env python3
"""Discover deployable services from the workspace for CI/CD matrixing."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SERVICE_ROOTS = [ROOT / "modules", ROOT / "shared", ROOT / "examples"]


def discover_services() -> list[dict[str, Any]]:
    services: list[dict[str, Any]] = []
    for base_dir in SERVICE_ROOTS:
        if not base_dir.exists():
            continue
        for candidate in sorted(base_dir.iterdir()):
            if not candidate.is_dir():
                continue
            if candidate.name.startswith(".") or candidate.name == "__pycache__":
                continue
            has_manifest = (candidate / "package.json").exists()
            has_python = (candidate / "pyproject.toml").exists() or (candidate / "requirements.txt").exists()
            has_docker = (candidate / "Dockerfile").exists()
            has_tests = (candidate / "tests").exists()
            if not any([has_manifest, has_python, has_docker, has_tests]):
                continue
            service_type = "node" if has_manifest else "python" if has_python else "container" if has_docker else "generic"
            services.append(
                {
                    "name": candidate.name,
                    "path": str(candidate.relative_to(ROOT)).replace("\\", "/"),
                    "type": service_type,
                    "has_tests": has_tests,
                }
            )
    return services


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=["json", "github"], default="json")
    args = parser.parse_args()

    services = discover_services()
    if args.format == "json":
        print(json.dumps({"services": services}, indent=2))
    else:
        names = [service["name"] for service in services]
        print(json.dumps(names))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
