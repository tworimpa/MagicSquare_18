"""GM-1 — Magic Square Solver Golden Master 회귀 테스트."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from .harness import (
    DEFAULT_EXPECTED_PATH,
    SCENARIO_GRIDS,
    SCENARIO_ORDER,
    assert_matches_expected,
    capture_scenario_body,
    parse_document,
)

EXPECTED_PATH = DEFAULT_EXPECTED_PATH


def _approve_mode() -> bool:
    return os.environ.get("GM_APPROVE", "").lower() in {"1", "true", "yes"}


@pytest.fixture(scope="session")
def golden_master_path() -> Path:
    """기준 파일 경로 fixture."""
    return EXPECTED_PATH


class TestGoldenMasterSolver:
    """Approve 패턴 — actual vs expected Golden Master."""

    def test_gm1_full_document_matches_expected(
        self,
        golden_master_path: Path,
    ) -> None:
        # When / Then — approve 시 갱신, 아니면 diff 비교
        assert_matches_expected(golden_master_path, approve=_approve_mode())

    @pytest.mark.parametrize("scenario_name", SCENARIO_ORDER)
    def test_gm1_scenario_section_present(
        self,
        golden_master_path: Path,
        scenario_name: str,
    ) -> None:
        # Given
        if not golden_master_path.is_file():
            pytest.skip("Golden Master baseline not generated yet")

        document = parse_document(golden_master_path.read_text(encoding="utf-8"))

        # Then
        assert scenario_name in document.sections
        assert "Input:" in document.sections[scenario_name]

    @pytest.mark.parametrize("scenario_name", SCENARIO_ORDER)
    def test_gm1_live_capture_matches_baseline_section(
        self,
        golden_master_path: Path,
        scenario_name: str,
    ) -> None:
        # Given
        if not golden_master_path.is_file():
            pytest.skip("Golden Master baseline not generated yet")

        document = parse_document(golden_master_path.read_text(encoding="utf-8"))
        expected_body = document.sections[scenario_name]
        actual_body = capture_scenario_body(
            scenario_name,
            SCENARIO_GRIDS[scenario_name],
        )

        # Then
        assert actual_body == expected_body, (
            f"Scenario [{scenario_name}] drift — set GM_APPROVE=1 to refresh baseline"
        )
