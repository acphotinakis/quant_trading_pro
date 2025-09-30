"""
Phase 1 Complete Runner Script
Executes all Phase 1 components in sequence
"""

import subprocess
import sys
from pathlib import Path
import logging


def run_phase1():
    """Execute all Phase 1 components"""
    scripts = [
        "scripts/setup/fetch_universe.py",
        "src/regimes/initial_classification.py",
        "tests/test_configs.py",
    ]

    for script in scripts:
        print(f"\n{'='*50}")
        print(f"Running: {script}")
        print(f"{'='*50}")

        result = subprocess.run(
            [sys.executable, script], capture_output=True, text=True
        )

        if result.returncode != 0:
            print(f"❌ Failed: {script}")
            print(f"Error: {result.stderr}")
            return False
        else:
            print(f"✅ Success: {script}")
            if result.stdout:
                print(result.stdout)

    return True


if __name__ == "__main__":
    if run_phase1():
        print("\n🎉 Phase 1 completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Phase 1 failed!")
        sys.exit(1)
