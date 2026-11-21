"""Command line entry point: python3 run_festreg.py [input_dir] [output_dir]"""
import sys
from pathlib import Path
from festreg.pipeline import run

here = Path(__file__).parent
info = run(sys.argv[1] if len(sys.argv) > 1 else here / "input",
           sys.argv[2] if len(sys.argv) > 2 else here / "output")
print(info)
