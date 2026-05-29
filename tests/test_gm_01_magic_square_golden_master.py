"""GM-01/GM-2 — Magic Square Solver Golden Master 회귀 테스트.

실행:
    python -m pytest tests/test_gm_01_magic_square_golden_master.py -v
    python -m pytest -m golden_master -v

baseline 갱신:
    $env:GM_APPROVE="1"
    python -m pytest tests/test_gm_01_magic_square_golden_master.py -v
"""

from __future__ import annotations

import io
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from golden_master.harness import (
    GM_TC_ORDER,
    GM_TC_SCENARIOS,
    SCENARIO_GRIDS,
    assert_matches_expected,
    assert_section_matches,
    assert_text_equals,
    capture_scenario_body,
    capture_stdout_scenario,
    parse_document,
    parse_error_contract,
    parse_solution6,
    read_expected_text,
    validate_case_a_placement,
    validate_case_b_fallback,
    validate_error_contract,
    validate_row_major_coords,
    validate_solution6_format,
)

pytestmark = pytest.mark.golden_master


class TestGoldenMasterApprove:
    """[TAG][GoldenMaster] — 전체 baseline approve 패턴."""

    def test_gm2_full_baseline_file_compare(
        self,
        golden_master_path: Path,
        approve_mode: bool,
    ) -> None:
        """전체 golden_master_expected.txt — 없으면 생성, 있으면 비교."""
        assert_matches_expected(golden_master_path, approve=approve_mode)


class TestGoldenMasterApiSerialization:
    """API Result DTO 직렬화 vs baseline 섹션 비교."""

    @pytest.mark.parametrize("tc_id", GM_TC_ORDER)
    def test_gm2_api_result_matches_baseline_section(
        self,
        tc_id: str,
        golden_master_path: Path,
        approve_mode: bool,
    ) -> None:
        """GM-TC-0X — capture_scenario_body vs expected section."""
        section = GM_TC_SCENARIOS[tc_id]
        assert_section_matches(
            golden_master_path,
            section,
            approve=approve_mode,
        )


class TestGoldenMasterStdoutCapture:
    """stdout capture — CLI 스타일 출력 vs baseline."""

    @pytest.mark.parametrize("tc_id", GM_TC_ORDER)
    def test_gm2_stdout_capture_matches_baseline(
        self,
        tc_id: str,
        golden_master_path: Path,
        approve_mode: bool,
    ) -> None:
        """stdout redirect 후 섹션 텍스트 비교."""
        section = GM_TC_SCENARIOS[tc_id]
        matrix = SCENARIO_GRIDS[section]

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            print(capture_stdout_scenario(section, matrix), end="")
        actual_stdout = buffer.getvalue()

        if approve_mode or not golden_master_path.is_file():
            assert_section_matches(golden_master_path, section, approve=True)
            return

        document = parse_document(read_expected_text(golden_master_path))
        expected_stdout = f"[{section}]\n{document.sections[section]}"
        assert_text_equals(expected_stdout, actual_stdout, f"{tc_id}/stdout")


class TestGoldenMasterContracts:
    """Golden Master 통과 후 도메인·에러 계약 검증."""

    def test_gm_tc_01_normal_success_case_a_contract(
        self,
        golden_master_path: Path,
    ) -> None:
        """GM-TC-01 — 정상 조합(Case A) int[6]·row-major·1-index."""
        section = GM_TC_SCENARIOS["GM-TC-01"]
        matrix = SCENARIO_GRIDS[section]
        body = capture_scenario_body(section, matrix)
        if golden_master_path.is_file():
            baseline = parse_document(read_expected_text(golden_master_path))
            assert_text_equals(baseline.sections[section], body, section)

        result = parse_solution6(body)
        validate_solution6_format(result)
        validate_row_major_coords(matrix, result)
        validate_case_a_placement(matrix, result)

    def test_gm_tc_02_reverse_success_case_b_contract(
        self,
        golden_master_path: Path,
    ) -> None:
        """GM-TC-02 — reverse fallback(Case B) after Case A fails."""
        section = GM_TC_SCENARIOS["GM-TC-02"]
        matrix = SCENARIO_GRIDS[section]
        body = capture_scenario_body(section, matrix)
        if golden_master_path.is_file():
            baseline = parse_document(read_expected_text(golden_master_path))
            assert_text_equals(baseline.sections[section], body, section)

        result = parse_solution6(body)
        validate_solution6_format(result)
        validate_row_major_coords(matrix, result)
        validate_case_b_fallback(matrix, result)

    def test_gm_tc_03_invalid_blank_count_error_contract(
        self,
        golden_master_path: Path,
    ) -> None:
        """GM-TC-03 — 빈칸 수 위반 (SSOT: INPUT_EMPTY_COUNT)."""
        section = GM_TC_SCENARIOS["GM-TC-03"]
        body = capture_scenario_body(section, SCENARIO_GRIDS[section])
        if golden_master_path.is_file():
            baseline = parse_document(read_expected_text(golden_master_path))
            assert_text_equals(baseline.sections[section], body, section)

        code, message = parse_error_contract(body)
        assert code.value == "INPUT_EMPTY_COUNT"
        validate_error_contract(code, message)

    def test_gm_tc_04_duplicate_number_error_contract(
        self,
        golden_master_path: Path,
    ) -> None:
        """GM-TC-04 — DUPLICATE_NUMBER (SSOT: INPUT_DUPLICATE)."""
        section = GM_TC_SCENARIOS["GM-TC-04"]
        body = capture_scenario_body(section, SCENARIO_GRIDS[section])
        if golden_master_path.is_file():
            baseline = parse_document(read_expected_text(golden_master_path))
            assert_text_equals(baseline.sections[section], body, section)

        code, message = parse_error_contract(body)
        assert code.value == "INPUT_DUPLICATE"
        validate_error_contract(code, message)

    def test_gm_tc_05_no_valid_magic_square_error_contract(
        self,
        golden_master_path: Path,
    ) -> None:
        """GM-TC-05 — NO_VALID_MAGIC_SQUARE (SSOT: SOLVE_IMPOSSIBLE)."""
        section = GM_TC_SCENARIOS["GM-TC-05"]
        body = capture_scenario_body(section, SCENARIO_GRIDS[section])
        if golden_master_path.is_file():
            baseline = parse_document(read_expected_text(golden_master_path))
            assert_text_equals(baseline.sections[section], body, section)

        code, message = parse_error_contract(body)
        assert code.value == "SOLVE_IMPOSSIBLE"
        validate_error_contract(code, message)
