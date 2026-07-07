from pathlib import Path


def test_requirements_file_exists_for_installation_and_testing() -> None:
    requirements_path = Path(__file__).resolve().parents[1] / "requirements.txt"
    assert requirements_path.exists(), "Friday Core should ship a requirements.txt for local setup and CI"

    requirements = requirements_path.read_text(encoding="utf-8")
    assert "pytest" in requirements.lower(), "requirements.txt should include pytest for test execution"
