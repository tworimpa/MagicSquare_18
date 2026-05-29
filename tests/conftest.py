"""pytest 공통 설정 — Golden Master fixtures."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from golden_master.harness import DEFAULT_EXPECTED_PATH


def pytest_configure(config: pytest.Config) -> None:
    """pytest 마커 golden_master 등록."""
    config.addinivalue_line(
        "markers",
        "golden_master: GM-1/GM-2 Approval/Golden Master 회귀 테스트",
    )


@pytest.fixture(scope="session")
def golden_master_path() -> Path:
    """Golden Master baseline 파일 경로."""
    return DEFAULT_EXPECTED_PATH


@pytest.fixture(scope="session")
def approve_mode() -> bool:
    """GM_APPROVE=1 이면 baseline 갱신."""
    return os.environ.get("GM_APPROVE", "").lower() in {"1", "true", "yes"}
