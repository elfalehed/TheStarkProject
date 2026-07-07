#!/usr/bin/env python3
"""Discover deployable services from the workspace for CI/CD matrixing."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".go",
    ".rs",
    ".java",
    ".cs",
    ".cpp",
    ".cc",
    ".c",
    ".h",
    ".hpp",
    ".swift",
    ".kt",
    ".scala",
    ".rb",
    ".php",
    ".lua",
}
SOURCE_DIR_NAMES = (
    "src",
    "app",
    "lib",
    "bin",
    "public",
    "firmware",
    "ros2_ws",
    "sim",
    "missions",
    "launch",
    "safety",
    "ik",
    "model",
    "visualizer",
    "components",
    "hooks",
    "widgets",
    "overlays",
    "dashboard",
    "scanners",
    "planner",
    "coordinator",
    "llm",
    "memory",
    "plugins",
    "cli",
    "core",
    "inference",
    "training",
    "models",
    "agents",
)


def _has_meaningful_content(candidate: Path) -> bool:
    if (candidate / "Dockerfile").exists():
        return True
    if (candidate / "tests").exists():
        return True
    for name in SOURCE_DIR_NAMES:
        source_dir = candidate / name
        if source_dir.exists() and any(path.is_file() for path in source_dir.rglob("*")):
            return True
    return any(path.is_file() and path.suffix.lower() in SOURCE_EXTENSIONS for path in candidate.rglob("*"))


def discover_services(root: Path | None = None) -> list[dict[str, Any]]:
    base_root = root or ROOT
    services: list[dict[str, Any]] = []
    service_roots = [base_root / "modules", base_root / "shared", base_root / "examples"]
    for base_dir in service_roots:
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
            if not _has_meaningful_content(candidate):
                continue
            service_type = "node" if has_manifest else "python" if has_python else "container" if has_docker else "generic"
            services.append(
                {
                    "name": candidate.name,
                    "path": str(candidate.relative_to(base_root)).replace("\\", "/"),
                    "type": service_type,
                    "has_tests": (candidate / "tests").exists(),
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
