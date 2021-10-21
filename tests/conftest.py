from pathlib import Path

import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def datadir() -> Path:
    return Path(__file__).parent / "data"


@pytest.fixture
def yaml_not_found(mocker: MockerFixture):
    # make appear as if yaml (package) is not installed
    mocker.patch("compile_dcm2bids_config.yaml", None)
    yield
