import pandas as pd


def load_data(competitive=True):
    file_path = (
        "./data/competitive-swim_results.csv"
        if competitive
        else "./data/non-competitive-swim_results.csv"
    )
    df = pd.read_csv(file_path)
    df["RaceDate"] = pd.to_datetime(df["RaceDate"])
    df["Year"] = df["RaceDate"].dt.year
    df["Time (min)"] = df["Time (ms)"] / 60000

    # Define age groups
    bins = [0, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, float("inf")]
    labels = [
        "13-19",
        "20-24",
        "25-29",
        "30-34",
        "35-39",
        "40-44",
        "45-49",
        "50-54",
        "55-59",
        "60-64",
        "65-69",
        "70+",
    ]
    df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)

    return df
