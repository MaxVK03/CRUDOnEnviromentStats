from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

client = TestClient(app)

def test_get_country_data_name_year():
    with patch('services.country_service.get_country_data_with_timeFrame') as mock_service:
        mock_service.return_value = {'data': 'some data'}
        response = client.get("/country/data?countryName=Belgium&countryIsocode=&yearid=2020&inCSV=false")
        assert response.status_code == 200
        assert response.json() == {'data': 'some data'}

def test_get_country_data_iso_year_timeFrame_inCSV():
    with patch('services.country_service.get_country_data_with_timeFrame') as mock_service:
        mock_service.return_value = [{'data': 'some data'}]
        response = client.get("/country/data?countryName=&countryIsocode=GER&yearid=2020&timeFrame=before&inCSV=True")
        assert response.status_code == 200
        assert response.text == "data\r\nsome data\r\n"

def test_get_country_data_countryName():
    with patch('services.country_service.get_country_data_without_timeFrame') as mock_service:
        mock_service.return_value = {"data": "some data"}
        response = client.get("/country/data?countryName=Belgium&countryIsocode=&inCSV=false")
        assert response.status_code == 200
        assert response.json() == {"data": "some data"}

def test_get_country_invalid_input():
    response = client.get("/country/data?countryName=&countryIsocode=&yearid=2020&inCSV=false")
    assert response.status_code == 400

# TODO: test post ?
# def test_post_country():

# def test_put_country_name_year():
#     with patch('services.country_service.update_country') as mock_service:
#         mock_service.return_value = {'data': 'some data'}
#         respone = client.put("/country/


'''
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
