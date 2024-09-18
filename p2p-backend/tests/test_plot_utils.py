# tests/test_plot_utils.py

import pytest
import pandas as pd
from app.graph_building import plot_utils

@pytest.fixture
def sample_data():
    # Create a sample DataFrame for testing
    data = {
        'Year': [2020, 2021, 2021],
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Time (min)': [30.5, 28.7, 35.2],
        'AgeGroup': ['25-29', '30-34', '25-29'],
        'Gender': ['F', 'M', 'M'],
        'Age': [27, 32, 28],
        'Region': ['Region1', 'Region2', 'Region1'],
        'Time (ms)': [1830000, 1722000, 2112000],
        'RaceDate': pd.to_datetime(['2020-08-01', '2021-08-07', '2021-08-07'])
    }
    return pd.DataFrame(data)

def test_plot_participation_by_year(app, sample_data):
    with app.app_context():
        response = plot_utils.plot_participation_by_year(sample_data)
        json_data = response.get_json()
        assert 'graph' in json_data
        assert 'table' in json_data
        assert len(json_data['table']) == 2  # Years 2020 and 2021

def test_plot_average_time_by_year(app, sample_data):
    with app.app_context():
        response = plot_utils.plot_average_time_by_year(sample_data)
        json_data = response.get_json()
        assert 'graph' in json_data
        assert 'table' in json_data
        assert len(json_data['table']) == 2  # Average times for 2020 and 2021

def test_plot_participation_by_age_group(app, sample_data):
    with app.app_context():
        response = plot_utils.plot_participation_by_age_group(sample_data)
        json_data = response.get_json()
        assert 'graph' in json_data
        assert 'table' in json_data

def test_plot_participation_by_region(app, sample_data):
    with app.app_context():
        response = plot_utils.plot_participation_by_region(sample_data)
        json_data = response.get_json()
        assert 'graph' in json_data
        assert 'table' in json_data

def test_plot_time_percentiles_by_year(app, sample_data):
    with app.app_context():
        response = plot_utils.plot_time_percentiles_by_year(sample_data)
        json_data = response.get_json()
        assert 'graph' in json_data
        assert 'table' in json_data
        assert len(json_data['table']) == 3  # 25th, 50th, 75th percentiles

def test_plot_gender_distribution_by_year(app, sample_data):
    with app.app_context():
        response = plot_utils.plot_gender_distribution_by_year(sample_data)
        json_data = response.get_json()
        assert 'graph' in json_data
        assert 'table' in json_data

def test_plot_top_10_fastest_swimmers(app, sample_data):
    with app.app_context():
        response = plot_utils.plot_top_10_fastest_swimmers(sample_data)
        json_data = response.get_json()
        assert 'graph' in json_data
        assert 'table' in json_data
        assert len(json_data['table']) <= 10  # Top 10 swimmers

def test_plot_average_time_by_age_group_and_year(app, sample_data):
    with app.app_context():
        response = plot_utils.plot_average_time_by_age_group_and_year(sample_data)
        json_data = response.get_json()
        assert 'graph' in json_data
        # Table is commented out in original function

def test_plot_age_vs_time_distribution(app, sample_data):
    with app.app_context():
        response = plot_utils.plot_age_vs_time_distribution(sample_data)
        json_data = response.get_json()
        assert 'graph' in json_data
        assert 'table' in json_data

def test_plot_median_time_by_year(app, sample_data):
    with app.app_context():
        response = plot_utils.plot_median_time_by_year(sample_data)
        json_data = response.get_json()
        assert 'graph' in json_data
        assert 'table' in json_data

def test_plot_user_time_by_year(app, sample_data):
    with app.app_context():
        response = plot_utils.plot_user_time_by_year(sample_data, 'Alice')
        json_data = response.get_json()
        assert 'graph' in json_data
        assert 'table' in json_data

        # Test for a non-existent user
        response, status_code = plot_utils.plot_user_time_by_year(sample_data, 'Nonexistent')
        json_data = response.get_json()
        assert status_code == 404
        assert 'error' in json_data

def test_plot_user_time_percentile_by_year(app, sample_data):
    with app.app_context():
        response = plot_utils.plot_user_time_percentile_by_year(sample_data, 'Alice')
        json_data = response.get_json()
        assert 'graph' in json_data
        assert 'table' in json_data

        # Test for a non-existent user
        response, status_code = plot_utils.plot_user_time_percentile_by_year(sample_data, 'Nonexistent')
        json_data = response.get_json()
        assert status_code == 404
        assert 'error' in json_data

def test_plot_average_time_by_gender_age_group_and_year(app, sample_data):
    with app.app_context():
        response = plot_utils.plot_average_time_by_gender_age_group_and_year(
            sample_data, gender='F', age_group='25-29', name='Alice', overlay_avg_time=True, overlay_user_time=True
        )
        json_data = response.get_json()
        assert 'graph' in json_data
        assert 'table' in json_data

        # Test with missing parameters
        response = plot_utils.plot_average_time_by_gender_age_group_and_year(
            sample_data, gender='M', age_group='30-34', name='', overlay_avg_time=False, overlay_user_time=False
        )
        json_data = response.get_json()
        assert 'graph' in json_data
        assert 'table' in json_data
