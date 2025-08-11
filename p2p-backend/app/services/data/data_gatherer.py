from typing import List, Dict, Any
import requests
import pandas as pd
import logging
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SwimResult:
    """Data class for storing swim result attributes"""

    place: int
    name: str
    gender: str
    pace: float
    time: int
    age: int
    bib: str
    country: str
    locality: str
    region: str
    overall_rank: int
    gender_rank: int
    race_date: datetime


class ResultsFetcher:
    """Handles fetching and processing of swim results"""

    def __init__(self, base_url: str = "https://results.athlinks.com"):
        self.base_url = base_url
        self.session = requests.Session()

    def fetch_swim_results(self, event_id: str, event_course_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch swim results from the API with proper pagination

        Args:
            event_id: The ID of the event
            event_course_id: The course ID
            limit: Number of results per page

        Returns:
            List of raw result dictionaries
        """
        from_value = 0
        all_results = []

        try:
            while True:
                url = f"{self.base_url}/event/{event_id}"
                params = {"eventCourseId": event_course_id, "from": from_value, "limit": limit}

                response = self.session.get(url, params=params)
                response.raise_for_status()

                data = response.json()
                if not self._validate_response(data):
                    break

                results = data[0]["interval"]["intervalResults"]
                if not results:
                    break

                all_results.extend(results)
                from_value += limit

                logger.info(f"Fetched {len(results)} results. Total: {len(all_results)}")

        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise

        return all_results

    def parse_results(self, raw_results: List[Dict[str, Any]], race_date: datetime) -> pd.DataFrame:
        """
        Parse raw results into a DataFrame efficiently

        Args:
            raw_results: List of raw result dictionaries
            race_date: Date of the race

        Returns:
            Processed DataFrame
        """
        # Process all results at once instead of loop
        processed_data = [
            SwimResult(
                place=result.get("overallRank"),
                name=result.get("displayName", "").lower(),
                gender=result.get("gender"),
                pace=self._calculate_pace(result),
                time=result.get("time", {}).get("timeInMillis"),
                age=result.get("age"),
                bib=result.get("bib"),
                country=result.get("country"),
                locality=result.get("locality"),
                region=result.get("region"),
                overall_rank=result.get("overallRank"),
                gender_rank=result.get("genderRank"),
                race_date=race_date,
            ).__dict__
            for result in raw_results
        ]

        df = pd.DataFrame(processed_data)
        return self._optimize_dtypes(df)

    def _validate_response(self, data: List[Dict[str, Any]]) -> bool:
        """
        Validate the API response structure

        Args:
            data: Response data from API

        Returns:
            bool: True if valid, False otherwise
        """
        return data and isinstance(data, list) and len(data) > 0 and "interval" in data[0] and "intervalResults" in data[0]["interval"]

    @staticmethod
    def _calculate_pace(result: Dict[str, Any]) -> float:
        """Calculate pace in minutes per mile"""
        time = result.get("time", {}).get("timeInMillis", 0)
        if "pace" in result and "time" in result["pace"]:
            return (result["pace"]["time"]["timeInMillis"] if result["pace"]["distance"]["distanceUnit"] != "100m" else time) / (
                2 * 60 * 1000
            )
        return time / (2 * 60 * 1000)

    @staticmethod
    def _optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
        """Optimize DataFrame memory usage"""
        numeric_columns = ["place", "time", "age", "overall_rank", "gender_rank"]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], downcast="integer")

        df["pace"] = df["pace"].astype("float32")
        return df
