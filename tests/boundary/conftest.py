"""Boundary 레이어 공통 fixture."""

from __future__ import annotations

import pytest

VALID_PARTIAL_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 0],
]

MOCK_SOLUTION: list[int] = [2, 3, 11, 4, 4, 1]


@pytest.fixture
def valid_partial_grid() -> list[list[int]]:
    """U-C01 등에서 사용하는 유효 4×4 partial grid."""
    return [row[:] for row in VALID_PARTIAL_GRID]
