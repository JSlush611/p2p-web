import pandas as pd

DATA_CACHE = {}

def load_data(competitive=True, force_reload=False):
    """
    Load dataset into memory and cache it to avoid reloading on every request.
    
    Parameters:
        competitive (bool): Whether to load competitive dataset.
        force_reload (bool): If True, reloads the dataset from file.
    
    Returns:
        pd.DataFrame: The loaded dataset.
    """
    key = "competitive" if competitive else "non-competitive"
    
    # Load from cache if available and not forcing reload
    if key in DATA_CACHE and not force_reload:
        return DATA_CACHE[key]
    
    # Otherwise, load from file
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
        "13-19", "20-24", "25-29", "30-34", "35-39", "40-44",
        "45-49", "50-54", "55-59", "60-64", "65-69", "70+"
    ]
    df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)

    DATA_CACHE[key] = df
    return df