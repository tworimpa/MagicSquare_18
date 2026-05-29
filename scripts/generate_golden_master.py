#!/usr/bin/env python
"""Golden Master 기준 파일 생성 스크립트.

Usage:
    python scripts/generate_golden_master.py
    python scripts/generate_golden_master.py --output tests/golden_master_expected.txt
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from golden_master.harness import (  # noqa: E402
    DEFAULT_EXPECTED_PATH,
    generate_document,
    write_expected_file,
)


def main() -> int:
    """기준 파일을 생성하고 경로를 stdout에 출력한다."""
    parser = argparse.ArgumentParser(
        description="Generate Golden Master expected file from live solver output.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_EXPECTED_PATH,
        help="Output path (default: tests/golden_master_expected.txt)",
    )
    args = parser.parse_args()

    document = generate_document()
    output_path = write_expected_file(args.output, document)
    print(f"Golden Master written: {output_path}")
    print(document.serialize())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
