from flask import jsonify
import pandas as pd


class GeneralAnalysis:
    @staticmethod
    def get_participation_by_year(df):
        return df.groupby("Year")["Name"].count()

    @staticmethod
    def get_average_time_by_year(df):
        avg_time = df.groupby("Year")["Time (min)"].mean()
        overall_avg_time = df["Time (min)"].mean()
        return avg_time, overall_avg_time

    @staticmethod
    def get_participation_by_age_group(df):
        return df["AgeGroup"].value_counts(sort=False)

    @staticmethod
    def get_participation_by_region(df):
        return df["Region"].value_counts().head(10)

    @staticmethod
    def get_time_percentiles(df):
        return df["Time (min)"].quantile([0.25, 0.5, 0.75])

    @staticmethod
    def get_gender_distribution_by_year(df):
        df = df[df["Gender"].isin(["M", "F"])]
        return df.groupby("Year")["Gender"].value_counts().unstack().fillna(0)

    @staticmethod
    def get_top_10_fastest_swimmers(df):
        return df.nsmallest(10, "Time (min)")

    @staticmethod
    def get_average_time_by_age_group_and_year(df):
        return df.groupby(["Year", "AgeGroup"])["Time (min)"].mean().unstack()

    @staticmethod
    def get_age_vs_time_distribution(df):
        return df[["Age", "Time (min)"]]

    @staticmethod
    def get_median_time_by_year(df):
        median_time = df.groupby("Year")["Time (min)"].median()
        overall_median_time = df["Time (min)"].median()
        return median_time, overall_median_time
