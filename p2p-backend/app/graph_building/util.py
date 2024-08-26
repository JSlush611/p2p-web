# Function to calculate the percentile of a value in a series
def calculate_percentile(series, value):
    rank = series.rank(pct=True).loc[series == value]
    if rank.empty:
        return None
    else:
        return rank.values[0] * 100
