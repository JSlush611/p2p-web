from __future__ import annotations
from pathlib import Path
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# ---- Config ----
AGE_BINS = [0, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, float("inf")]
AGE_LABELS = ["13-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70+"]

USECOLS = ["Name", "RaceDate", "Age", "Gender", "Region", "Time (ms)"]
DTYPES = {
    "Name": "string",
    "Age": "Int64",
    "Gender": "category",
    "Region": "category",
    "Time (ms)": "Int64",
}


class SwimDataService:
    """
    Loads both CSVs once at startup and keeps them in memory.
    """

    def __init__(self, data_dir: str = "./data"):
        self._data_dir = Path(data_dir)
        logger.info("Loading swim competition datasets…")
        self._competitive = self._load("competitive-swim_results.csv")
        self._non_competitive = self._load("non-competitive-swim_results.csv")
        logger.info("Datasets loaded successfully")

    def _load(self, filename: str) -> pd.DataFrame:
        fp = self._data_dir / filename
        df = pd.read_csv(fp, usecols=USECOLS, dtype=DTYPES, parse_dates=["RaceDate"]).copy()

        # Derive once at load time
        df["Year"] = df["RaceDate"].dt.year
        df["Time (min)"] = df["Time (ms)"] / 60000.0
        df["AgeGroup"] = pd.cut(df["Age"].astype("float"), bins=AGE_BINS, labels=AGE_LABELS, right=False).astype("category")
        return df

    def get_data(self, competitive: bool = True) -> pd.DataFrame:
        # Shallow copy prevents accidental in-place edits from leaking back
        return (self._competitive if competitive else self._non_competitive).copy(deep=False)


# Global instance
_service = SwimDataService()


def load_data(competitive: bool = True, force_reload: bool = False) -> pd.DataFrame:
    # force_reload kept for API compatibility
    return _service.get_data(competitive)
