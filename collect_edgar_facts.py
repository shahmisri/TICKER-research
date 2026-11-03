"""Entrypoint for the Legend Investor skill's bundled EDGAR collector."""
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

from lab18_edgar import main


if __name__ == "__main__":
    raise SystemExit(main())
