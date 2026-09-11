#!/usr/bin/env python3
#
# Helper script to run build_usd.py with all optional features enabled.
#
import os
import sys
import subprocess
from pathlib import Path

FULL_FEATURE_FLAGS = [
    "--alembic",
    "--draco",
    "--materialx",
    "--openimageio",
    "--opencolorio",
    "--openvdb",
    "--ptex",
    "--embree",
    "--vulkan",
]

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: build_usd_full.py <install_dir> [additional options...]")
        print("\nRuns build_usd.py with all optional features enabled:")
        print("  " + " ".join(FULL_FEATURE_FLAGS))
        print("\nPasses any additional arguments directly to build_usd.py.\n")
        if len(sys.argv) < 2:
            sys.exit(1)

    build_usd_script = Path(__file__).resolve().parent / "build_usd.py"

    # Set VULKAN_SDK default if standard paths exist
    if "VULKAN_SDK" not in os.environ:
        if os.path.exists("/usr/include/vulkan") or os.path.exists("/usr/share/vulkan"):
            os.environ["VULKAN_SDK"] = "/usr"

    user_args = sys.argv[1:]
    user_arg_set = set(user_args)

    flags_to_add = []
    for flag in FULL_FEATURE_FLAGS:
        if flag == "--vulkan":
            if "--no-vulkan" in user_arg_set:
                continue
            if "VULKAN_SDK" not in os.environ and "--vulkan" not in user_arg_set:
                print("NOTE: VULKAN_SDK is not set. Omitting --vulkan. (Set VULKAN_SDK to enable Vulkan).")
                continue
        if flag not in user_arg_set:
            flags_to_add.append(flag)

    cmd = [sys.executable, str(build_usd_script)]
    cmd.extend(flags_to_add)
    cmd.extend(user_args)

    try:
        completed = subprocess.run(cmd, env=os.environ)
        sys.exit(completed.returncode)
    except KeyboardInterrupt:
        sys.exit(130)

if __name__ == "__main__":
    main()
