from __future__ import annotations

import subprocess
import sys


COMMANDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("tests", (sys.executable, "-m", "pytest", "-q")),
    ("public boundary", (sys.executable, "scripts/check_release_boundary.py")),
    ("assignment example", (sys.executable, "examples/assignment_demo.py")),
    ("cp-sat example", (sys.executable, "examples/cp_sat_workforce_demo.py")),
)


def main() -> int:
    for label, command in COMMANDS:
        print(f"==> {label}", flush=True)
        result = subprocess.run(command, check=False)
        if result.returncode != 0:
            print(f"QUALITY GATE: FAIL ({label})", flush=True)
            return result.returncode

    print("QUALITY GATE: PASS", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
