from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "ci" / "discover_services.py"
SPEC = importlib.util.spec_from_file_location("discover_services", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
DISCOVER_SERVICES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DISCOVER_SERVICES)


def test_discover_services_skips_empty_modules(tmp_path: Path) -> None:
    root = tmp_path
    (root / "modules" / "empty-module").mkdir(parents=True)
    (root / "modules" / "empty-module" / "requirements.txt").write_text("requests\n", encoding="utf-8")

    (root / "modules" / "empty-src-module" / "src").mkdir(parents=True)
    (root / "modules" / "empty-src-module" / "package.json").write_text("{}\n", encoding="utf-8")

    (root / "modules" / "real-module" / "src").mkdir(parents=True)
    (root / "modules" / "real-module" / "src" / "main.py").write_text("print('hello')\n", encoding="utf-8")

    services = DISCOVER_SERVICES.discover_services(root=root)

    assert [service["name"] for service in services] == ["real-module"]
