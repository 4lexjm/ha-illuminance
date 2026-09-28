"""Test manifest and metadata validation for ha_illuminance."""

import json
from pathlib import Path


def test_manifest_contents():
    """Verify manifest.json contains valid required keys and domain."""
    manifest_path = (
        Path(__file__).parent.parent / "custom_components" / "ha_illuminance" / "manifest.json"
    )
    assert manifest_path.is_file()

    with open(manifest_path, encoding="utf-8") as f:
        data = json.load(f)

    assert data["domain"] == "ha_illuminance"
    assert data["name"] == "Illuminance"
    assert data["config_flow"] is True
    assert "@4lexjm" in data["codeowners"]
    assert "4lexjm/ha-illuminance" in data["documentation"]
    assert "4lexjm/ha-illuminance" in data["issue_tracker"]
    assert data["version"] == "6.0.0"
    assert data["iot_class"] == "calculated"


def test_hacs_json():
    """Verify hacs.json configuration."""
    hacs_path = Path(__file__).parent.parent / "hacs.json"
    assert hacs_path.is_file()

    with open(hacs_path, encoding="utf-8") as f:
        data = json.load(f)

    assert data["name"] == "Illuminance"
    assert "homeassistant" in data


def test_strings_and_translations():
    """Verify strings.json and translations are valid JSON."""
    comp_dir = Path(__file__).parent.parent / "custom_components" / "ha_illuminance"
    strings_file = comp_dir / "strings.json"
    assert strings_file.is_file()

    with open(strings_file, encoding="utf-8") as f:
        strings_data = json.load(f)
    assert "title" in strings_data
    assert "config" in strings_data
    assert "options" in strings_data

    trans_dir = comp_dir / "translations"
    assert trans_dir.is_dir()
    for trans_file in trans_dir.glob("*.json"):
        with open(trans_file, encoding="utf-8") as f:
            trans_data = json.load(f)
        assert "title" in trans_data
