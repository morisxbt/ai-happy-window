"""Copy the bundled competition image to the requested output directory."""

import os
import shutil
from pathlib import Path

here = Path(__file__).resolve().parent
output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
if not os.path.isdir(output_dir):
    raise FileNotFoundError(f"Output directory does not exist: {output_dir}")

shutil.copyfile(here / "entry.png", os.path.join(output_dir, "entry.png"))
