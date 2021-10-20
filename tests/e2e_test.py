import subprocess
from pathlib import Path

import pytest


@pytest.mark.e2e
def test_cli(datadir: Path):
    config1 = datadir / "config1.json"
    config2 = datadir / "config2.json"
    expected = datadir / "merged_config1_config2.json"

    res = subprocess.run(
        ("compile-dcm2bids-config", config1, config2),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        encoding="utf8",
    )

    assert res.returncode == 0
    assert res.stderr == ""
    assert res.stdout == expected.read_text()


@pytest.mark.e2e
def test_cli_with_json_and_yaml_input_configs(datadir: Path):
    config1 = datadir / "config1.json"
    config3 = datadir / "config3.yaml"
    expected = datadir / "merged_config1_config3.json"

    res = subprocess.run(
        ("compile-dcm2bids-config", config1, config3),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        encoding="utf8",
    )

    assert res.returncode == 0
    assert res.stderr == ""
    assert res.stdout == expected.read_text()


@pytest.mark.e2e
def test_cli_yaml_output(datadir: Path):
    config1 = datadir / "config1.json"
    config3 = datadir / "config3.yaml"
    expected = datadir / "merged_config1_config3.yaml"

    res = subprocess.run(
        ("compile-dcm2bids-config", "--to-yaml", config1, config3),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        encoding="utf8",
    )

    assert res.returncode == 0
    assert res.stderr == ""
    assert res.stdout == expected.read_text()
