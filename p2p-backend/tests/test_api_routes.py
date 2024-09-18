import pytest
from unittest.mock import patch
import pandas as pd

@pytest.fixture
def sample_data():
    data = {
        'Year': [2020, 2021, 2021],
        'Name': ['alice', 'bob', 'charlie'],
        'Time (min)': [30.5, 28.7, 35.2],
        'AgeGroup': ['25-29', '30-34', '25-29'],
        'Gender': ['F', 'M', 'M'],
        'Age': [27, 32, 28],
        'Region': ['Region1', 'Region2', 'Region1'],
        'Time (ms)': [1830000, 1722000, 2112000],
        'RaceDate': pd.to_datetime(['2020-08-01', '2021-08-07', '2021-08-07'])
    }
    return pd.DataFrame(data)

def test_test_api(client):
    response = client.get('/api/test')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'

@patch('app.services.data_service.load_data')
def test_participation_by_year_api(mock_load_data, client, sample_data):
    mock_load_data.return_value = sample_data
    response = client.get('/api/participation-by-year')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'graph' in json_data

def test_user_time_by_year_api(client, sample_data):
    with patch('app.services.data_service.load_data', return_value=sample_data):
        response = client.get('/api/user-time-by-year', query_string={'name': 'Jonathan Schluesche'})
        assert response.status_code == 200
        json_data = response.get_json()
        assert 'graph' in json_data

        # Test with missing name parameter
        response = client.get('/api/user-time-by-year')
        assert response.status_code == 400
        json_data = response.get_json()
        assert 'error' in json_data

        # Test with non-existent user
        response = client.get('/api/user-time-by-year', query_string={'name': 'nonexistent'})
        assert response.status_code == 404
        json_data = response.get_json()
        assert 'error' in json_data

def test_user_position_in_year_api(client, sample_data):
    with patch('app.services.data_service.load_data', return_value=sample_data):
        response = client.get('/api/user-position-in-year', query_string={'name': 'alice', 'year': '2020'})
        assert response.status_code == 200
        json_data = response.get_json()
        assert 'name' in json_data
        assert json_data['name'] == 'alice'

        # Test with missing parameters
        response = client.get('/api/user-position-in-year', query_string={'name': 'alice'})
        assert response.status_code == 400
        json_data = response.get_json()
        assert 'error' in json_data

        # Test with non-existent user
        response = client.get('/api/user-position-in-year', query_string={'name': 'nonexistent', 'year': '2020'})
        assert response.status_code == 404
        json_data = response.get_json()
        assert 'error' in json_data

def test_average_time_by_gender_age_group_and_year_api(client, sample_data):
    with patch('app.services.data_service.load_data', return_value=sample_data):
        response = client.get('/api/user-average-time-gender-age-group-and-year', query_string={
            'gender': 'F',
            'age_group': '25-29',
            'name': 'alice',
            'overlay': 'true',
            'overlay_user_time': 'true'
        })
        assert response.status_code == 200
        json_data = response.get_json()
        assert 'graph' in json_data

        # Test with missing parameters
        response = client.get('/api/user-average-time-gender-age-group-and-year', query_string={
            'gender': 'F'
        })
        assert response.status_code == 400
        json_data = response.get_json()
        assert 'error' in json_data
