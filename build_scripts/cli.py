import sys
import subprocess
from pathlib import Path

def build_usd_main():
    script = Path(__file__).resolve().parent / "build_usd.py"
    cmd = [sys.executable, str(script)] + sys.argv[1:]
    try:
        sys.exit(subprocess.run(cmd).returncode)
    except KeyboardInterrupt:
        sys.exit(130)

def build_usd_full_main():
    script = Path(__file__).resolve().parent / "build_usd_full.py"
    cmd = [sys.executable, str(script)] + sys.argv[1:]
    try:
        sys.exit(subprocess.run(cmd).returncode)
    except KeyboardInterrupt:
        sys.exit(130)
