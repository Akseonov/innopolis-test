from pathlib import Path

YEAR = 2025
ROWS = 1000
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_PATH = DATA_DIR / f"rfsd_{YEAR}_raw.csv"
SAMPLE_PATH = DATA_DIR / f"rfsd_{YEAR}_sample.csv"
FIGURES_DIR = Path(__file__).resolve().parent.parent / "reports" / "figures"
