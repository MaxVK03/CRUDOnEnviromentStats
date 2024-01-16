from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

import dataManagement.models
from main import app

# client = TestClient(app)

'''
def test_get_temperature_change_by_continent_valid_no_year():
    with patch('services.continent_service.get_temperature_change_by_continent') as mock_service:
        mock_service.return_value = {'data': 'some data'}
        response = client.get("/continent/temperatureChange?continent=Europe")
        assert response.status_code == 200
        assert response.json() == {'data': 'some data'}


def test_get_temperature_change_by_continent_valid_with_year():
    with patch('services.continent_service.get_temperature_change_by_continent') as mock_service:
        mock_service.return_value = {'data': 'some data'}
        response = client.get("/continent/temperatureChange?continent=Europe&year=2020")
        assert response.status_code == 200
        assert response.json() == {'data': 'some data'}


def test_get_temperature_change_by_continent_valid_with_year_in_csv():
    with patch('services.continent_service.get_temperature_change_by_continent') as mock_service:
        mock_service.return_value = [{"data": "some data", "population": 1000}]
        response = client.get("/continent/temperatureChange?continent=Europe&inCSV=True")
        assert response.status_code == 200
        assert response.text == "data,population\r\nsome data,1000\r\n"


def test_get_temperature_change_by_continent_no_year_in_csv():
    with patch('services.continent_service.get_temperature_change_by_continent') as mock_service:
        mock_service.return_value = [{"data": "some data", "year": 2020}]
        response = client.get("/continent/temperatureChange?continent=Europe&year=2020&inCSV=True")
        assert response.status_code == 200
        assert response.text == "data,year\r\nsome data,2020\r\n"


def test_get_temperature_change_by_continent_invalid_continent():
    response = client.get("/continent/temperatureChange?continent=Unknown")
    assert response.status_code == 400
'''