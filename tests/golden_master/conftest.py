"""pytest Golden Master marker 등록."""

from __future__ import annotations

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """pytest.ini 마커 golden_master 등록."""
    config.addinivalue_line(
        "markers",
        "golden_master: GM-1/GM-2 Approval/Golden Master 회귀 테스트",
    )
