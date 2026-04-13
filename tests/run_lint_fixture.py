#!/usr/bin/env python3
"""
Run repository lint fixtures against scripts/wiki-lint.py.
"""

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "broken-wiki"
EXPECTED = FIXTURE / "expected.json"
LINT_SCRIPT = ROOT / "scripts" / "wiki-lint.py"


def main() -> None:
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    result = subprocess.run(
        [sys.executable, str(LINT_SCRIPT), "--json", str(FIXTURE)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    if result.returncode != expected["exit_code"]:
        print(
            f"Unexpected exit code: expected {expected['exit_code']} got {result.returncode}",
            file=sys.stderr,
        )
        sys.exit(1)

    payload = json.loads(result.stdout)

    for fragment in expected["required_error_substrings"]:
        if not any(fragment in item for item in payload["errors"]):
            print(f"Missing expected error fragment: {fragment}", file=sys.stderr)
            sys.exit(1)

    for fragment in expected["required_warning_substrings"]:
        if not any(fragment in item for item in payload["warnings"]):
            print(f"Missing expected warning fragment: {fragment}", file=sys.stderr)
            sys.exit(1)

    print("Lint fixture checks passed.")


if __name__ == "__main__":
    main()
