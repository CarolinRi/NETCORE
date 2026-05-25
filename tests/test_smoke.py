"""Smoke tests: environment and legacy entry point work."""

import importlib.util
from pathlib import Path

import netcore
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
LEGACY_PATH = REPO_ROOT / "NETCORE.py"


def _load_legacy_module():
    spec = importlib.util.spec_from_file_location("NETCORE", LEGACY_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_package_version():
    assert netcore.__version__ == "1.0.1"


def test_legacy_netcore_importable():
    module = _load_legacy_module()
    assert hasattr(module, "run_NETCORE")


@pytest.mark.skipif(
    not (REPO_ROOT / "tests" / "fixtures" / "datasets" / "Vitamins.csv").exists(),
    reason="Unzip Test_datasets.zip into tests/fixtures/datasets/",
)
def test_legacy_run_on_vitamins():
    module = _load_legacy_module()
    data = pd.read_csv(REPO_ROOT / "tests" / "fixtures" / "datasets" / "Vitamins.csv")
    result = module.run_NETCORE(data, 0.6)
    assert isinstance(result, list)
    assert len(result) > 0
