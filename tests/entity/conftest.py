"""Entity RED skeleton — G0~G3 격자 placeholder (Report/04 §3.2).

Fixtures are commented until Domain VO/services exist.
Uncomment when implementing Track B GREEN phase.
"""

from __future__ import annotations

# import pytest

# G0 — Example Grid A (complete magic square, M=34)
# GRID_G0: list[list[int]] = [
#     [16, 3, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]

# G1 — blanks (2,2) and (3,3) 1-index; missing {7, 10}
# GRID_G1: list[list[int]] = [
#     [16, 3, 2, 13],
#     [5, 0, 11, 8],
#     [9, 6, 0, 12],
#     [4, 15, 14, 1],
# ]

# G2 — Case A fail, Case B success; blanks (1,1),(2,3); missing {11,16}
GRID_G2: list[list[int]] = [
    [0, 3, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# G3 — both Case A/B fail; blanks (1,1),(1,2); missing {1,2}
GRID_G3: list[list[int]] = [
    [0, 0, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
]

# @pytest.fixture
# def grid_g0() -> list[list[int]]:
#     """D-VAL-01 — complete grid."""
#     return [row[:] for row in GRID_G0]

# @pytest.fixture
# def grid_g1() -> list[list[int]]:
#     """D-LOC-01, D-MIS-01, D-SOL-01."""
#     return [row[:] for row in GRID_G1]
