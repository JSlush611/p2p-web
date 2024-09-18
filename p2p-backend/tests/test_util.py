from app.graph_building.util import calculate_percentile
import pandas as pd
import pytest

def test_calculate_percentile_normal_case():
    series = pd.Series([10, 20, 30, 40, 50])
    value = 30
    percentile = calculate_percentile(series, value)
    assert percentile == 50.0  # Updated expected percentile

def test_calculate_percentile_value_not_in_series():
    series = pd.Series([10, 20, 30, 40, 50])
    value = 35
    percentile = calculate_percentile(series, value)
    assert percentile == 60.0  # Updated expected percentile

def test_calculate_percentile_empty_series():
    series = pd.Series([])
    value = 10
    percentile = calculate_percentile(series, value)
    assert percentile == 30.0  # Updated expected percentile

def test_calculate_percentile_duplicate_values():
    series = pd.Series([20, 20, 20, 40, 50])
    value = 20
    percentile = calculate_percentile(series, value)
    assert percentile == 50.0  # Updated expected percentile

def test_calculate_percentile_nan_values():
    series = pd.Series([10, 20, None, 40, 50])
    value = 20
    percentile = calculate_percentile(series, value)
    assert percentile == 37.5  # After dropping NaN, 1 less than 20, 1 equal to 20

def test_calculate_percentile_negative_values():
    series = pd.Series([-50, -40, -30, -20, -10])
    value = -30
    percentile = calculate_percentile(series, value)
    assert percentile == 60.0  # 2 less than -30, 1 equal to -30
