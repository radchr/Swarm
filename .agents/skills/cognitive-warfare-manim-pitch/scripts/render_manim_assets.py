"""Render reproducible Manim CE stills or preview videos for pitch assets."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys


QUALITY_FLAGS = {
    "low": "-ql",
    "medium": "-qm",
    "high": "-qh",
    "fourk": "-qk",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Python file containing Manim scenes")
    parser.add_argument("--scene", action="append", default=[], help="Scene class; repeat as needed")
    parser.add_argument("--mode", choices=("still", "video"), default="still")
    parser.add_argument("--quality", choices=QUALITY_FLAGS, default="high")
    parser.add_argument("--media-dir", type=Path, default=Path("assets/generated"))
    parser.add_argument("--manim", default=os.environ.get("MANIM_CMD", "manim"), help="Path to Manim CE executable")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    if not source.is_file():
        raise SystemExit(f"Scene file not found: {source}")

    executable = shutil.which(args.manim) or (args.manim if Path(args.manim).is_file() else None)
    if executable is None:
        raise SystemExit("Manim CE executable not found. Pass --manim PATH or set MANIM_CMD.")

    command = [str(executable), QUALITY_FLAGS[args.quality]]
    if args.mode == "still":
        command.append("-s")
    command.extend(["--media_dir", str(args.media_dir.resolve())])
    if not args.scene:
        command.append("-a")
    command.append(str(source))
    command.extend(args.scene)

    print("Running:", subprocess.list2cmdline(command))
    completed = subprocess.run(command, check=False)
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())
