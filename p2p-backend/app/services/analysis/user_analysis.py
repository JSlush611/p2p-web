from flask import jsonify
import pandas as pd


class UserAnalysis:
    @staticmethod
    def get_user_time_by_year(df, name):
        person_data = df[df["Name"] == name]
        if person_data.empty:
            return None, {
                "error": True,
                "message": f"No data found for '{name}'. Please check the spelling or try a different dataset.",
                "suggestion": "Ensure that the name is correctly spelled and that data exists for the selected dataset.",
            }
        return person_data, None

    @staticmethod
    def get_user_time_percentile_by_year(df, name):
        person_data = df[df["Name"] == name]
        if person_data.empty:
            return None, "No percentile data found for '{}'. This may be due to missing participation records.".format(name)

        person_gender = person_data["Gender"].iloc[0]
        percentiles_all = []
        percentiles_gender = []

        for year in person_data["Year"].unique():
            yearly_data = df[df["Year"] == year]
            yearly_data_gender = yearly_data[yearly_data["Gender"] == person_gender]
            time = person_data[person_data["Year"] == year]["Time (min)"].values[0]
            percentiles_all.append((year, UserAnalysis._calculate_percentile(yearly_data["Time (min)"], time)))
            percentiles_gender.append((year, UserAnalysis._calculate_percentile(yearly_data_gender["Time (min)"], time)))

        return (person_data, person_gender, percentiles_all, percentiles_gender), None

    @staticmethod
    def get_average_time_by_gender_age_group_and_year(df, gender, age_group, name=None):
        filtered_df = df[(df["Gender"] == gender) & (df["AgeGroup"] == age_group)]
        if filtered_df.empty:
            return None, {
                "error": True,
                "message": f"No data found for gender '{gender}' in age group '{age_group}'.",
                "suggestion": "Try selecting a different gender or age group.",
            }

        avg_time = filtered_df.groupby("Year")["Time (min)"].mean()
        overall_avg_time = df.groupby("Year")["Time (min)"].mean()

        user_data = None
        if name:
            user_data = df[df["Name"] == name]
            if user_data.empty:
                return None, {
                    "error": True,
                    "message": f"No data found for '{name}' in the selected dataset.",
                    "suggestion": "Ensure the name is correctly spelled and exists in the dataset.",
                }

        return (avg_time, overall_avg_time, user_data), None

    @staticmethod
    def find_user_position_in_year(df, name, year):
        swimmer_data = df[(df["Name"] == name) & (df["Year"] == year)]
        if swimmer_data.empty:
            return None, f"No data found for '{name}' in {year}."

        best_time = swimmer_data["Time (min)"].min()
        overall_rank = int((df[df["Year"] == year]["Time (min)"] < best_time).sum() + 1)

        age_group = str(swimmer_data["AgeGroup"].iloc[0])
        gender = swimmer_data["Gender"].iloc[0]
        total_participants_in_age_group_and_gender = int(
            len(df[(df["Year"] == year) & (df["AgeGroup"] == age_group) & (df["Gender"] == gender)])
        )

        return {
            "name": name,
            "year": int(year),
            "position": overall_rank,
            "total_participants": int(len(df[df["Year"] == year])),
            "age_group": age_group,
            "total_participants_in_age_group": total_participants_in_age_group_and_gender,
        }, None

    @staticmethod
    def _calculate_percentile(series, value):
        # For swimming, lower time is better, so we invert the percentile
        # This way, being the fastest puts you in the 100th percentile
        rank = (series >= value).mean() * 100
        return float(rank)  # Convert numpy types to native Python float
