# tests/test_data_service.py

import pytest
from app.services.data_service import load_data
import pandas as pd
from unittest.mock import patch

def test_load_data_competitive():
    sample_data = pd.DataFrame({
        'RaceDate': ['2021-08-07', '2021-08-07'],
        'Time (ms)': [1830000, 1722000],
        'Age': [25, 30]
    })
    with patch('pandas.read_csv', return_value=sample_data):
        df = load_data(competitive=True)
        assert 'Year' in df.columns
        assert df['Year'].iloc[0] == 2021
        assert df['Time (min)'].iloc[0] == 30.5  # 1830000 ms to minutes
        assert df['AgeGroup'].iloc[0] == '25-29'

def test_load_data_non_competitive():
    sample_data = pd.DataFrame({
        'RaceDate': ['2021-08-07', '2021-08-07'],
        'Time (ms)': [2000000, 2100000],
        'Age': [35, 40]
    })
    with patch('pandas.read_csv', return_value=sample_data):
        df = load_data(competitive=False)
        assert 'Year' in df.columns
        assert df['Year'].iloc[0] == 2021
        assert df['Time (min)'].iloc[0] == pytest.approx(33.3333, 0.0001)
        assert df['AgeGroup'].iloc[1] == '40-44'

def test_load_data_age_group_assignment():
    sample_data = pd.DataFrame({
        'Age': [18, 22, 27, 33, 38, 43, 48, 53, 58, 63, 68, 75],
        'Time (ms)': [0]*12,
        'RaceDate': ['2021-08-07']*12
    })
    with patch('pandas.read_csv', return_value=sample_data):
        df = load_data()
        expected_age_groups = ['13-19', '20-24', '25-29', '30-34', '35-39', '40-44',
                               '45-49', '50-54', '55-59', '60-64', '65-69', '70+']
        assert list(df['AgeGroup']) == expected_age_groups

def test_load_data_race_date_parsing():
    sample_data = pd.DataFrame({
        'RaceDate': ['2021-08-07', 'invalid-date'],
        'Time (ms)': [1830000, 1722000],
        'Age': [25, 30]
    })
    with patch('pandas.read_csv', return_value=sample_data):
        with pytest.raises(Exception):
            load_data()
