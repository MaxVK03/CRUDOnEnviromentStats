from sqlite3 import IntegrityError
import pytest
from pydantic import ValidationError
from unittest.mock import patch
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dataManagement.models import CountryDataRequest, CountryData
from services import country_service
from services.country_service import create_country_data, delete_country_data_by_name_and_year, handle_not_found
from testing.test_continent_services import get_test_db


@pytest.fixture(scope="module")
def test_db():
    db_url = "sqlite:///TestDB.db"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session()


def extract_country_data(result):
    return [
        {'year': data.year, 'country': data.country, 'ghg': data.share_of_temperature_change_from_ghg}
        for data in result
    ]


def test_get_country_data_name_with_time_frame_after(test_db):
    result = country_service.get_country_data_with_timeFrame(test_db, 'Canada', None, 2010, "after")
    extracted_values = extract_country_data(result)
    expected_values = [{'year': 2010, 'country': 'Canada', 'ghg': 2.21},
                       {'year': 2011, 'country': 'Canada', 'ghg': 2.198},
                       {'year': 2012, 'country': 'Canada', 'ghg': 2.186}]
    assert extracted_values == expected_values


def test_get_country_data_name_with_time_frame_after_no_data(test_db):
    with pytest.raises(HTTPException) as excinfo:
        country_service.get_country_data_with_timeFrame(test_db, 'Canada', None, 2013, "after")


def test_get_country_data_name_with_time_frame_before(test_db):
    result = country_service.get_country_data_with_timeFrame(test_db, 'Canada', None, 2012, "before")
    extracted_values = extract_country_data(result)
    expected_values = [{'year': 2010, 'country': 'Canada', 'ghg': 2.21},
                       {'year': 2011, 'country': 'Canada', 'ghg': 2.198},
                       {'year': 2012, 'country': 'Canada', 'ghg': 2.186}]
    assert extracted_values == expected_values


def test_get_country_data_name_with_time_frame_before_no_data(test_db):
    with pytest.raises(HTTPException) as excinfo:
        country_service.get_country_data_with_timeFrame(test_db, 'Canada', None, 2009, "before")


def test_get_country_data_invalid_name(test_db):
    with pytest.raises(HTTPException) as excinfo:
        country_service.get_country_data_with_timeFrame(test_db, 'Invalid Country', None, 2010, "after")


def test_get_country_data_name_with_time_frame_equal(test_db):
    result = country_service.get_country_data_with_timeFrame(test_db, 'Canada', None, 2010, "equal")
    extracted_values = extract_country_data(result)
    expected_values = [{'year': 2010, 'country': 'Canada', 'ghg': 2.21}]
    assert extracted_values == expected_values


def test_get_country_data_name_with_time_frame_equal_no_data(test_db):
    result = country_service.get_country_data_with_timeFrame(test_db, 'Canada', None, 2009, "equal")
    extracted_values = extract_country_data(result)
    assert len(extracted_values) == 0


def test_get_country_data_name_with_time_frame_equal_no_data():
    with pytest.raises(HTTPException) as excinfo:
        country_service.get_country_data_with_timeFrame(get_test_db(), 'Canada', None, 2009, "equal")


def test_get_country_data_iso_with_time_frame_after():
    result = country_service.get_country_data_with_timeFrame(get_test_db(), None, "CAN", 2010, "after")

    extracted_values = [{'year': data.year, 'country': data.country, 'ghg': data.share_of_temperature_change_from_ghg}
                        for data in result]
    assert len(extracted_values) == 3

    expected_values = [{'year': 2010, 'country': 'Canada', 'ghg': 2.21},
                       {'year': 2011, 'country': 'Canada', 'ghg': 2.198},
                       {'year': 2012, 'country': 'Canada', 'ghg': 2.186}]
    for expected in expected_values:
        assert expected in extracted_values


def test_get_country_data_iso_with_time_frame_after_no_data():
    with pytest.raises(HTTPException) as excinfo:
        country_service.get_country_data_with_timeFrame(get_test_db(), None, "CAN", 2013, "after")


def test_get_country_data_iso_with_time_frame_before():
    result = country_service.get_country_data_with_timeFrame(get_test_db(), None, "CAN", 2012, "before")

    # Result should contain all the data for 'Africa'
    extracted_values = [{'year': data.year, 'country': data.country, 'ghg': data.share_of_temperature_change_from_ghg}
                        for data in result]
    assert len(extracted_values) == 3

    expected_values = [{'year': 2010, 'country': 'Canada', 'ghg': 2.21},
                       {'year': 2011, 'country': 'Canada', 'ghg': 2.198},
                       {'year': 2012, 'country': 'Canada', 'ghg': 2.186}]
    for expected in expected_values:
        assert expected in extracted_values


def test_get_country_data_iso_with_time_frame_before_no_data():
    with pytest.raises(HTTPException) as excinfo:
        country_service.get_country_data_with_timeFrame(get_test_db(), None, "CAN", 2009, "before")


def test_get_country_data_iso_with_time_frame_equal():
    result = country_service.get_country_data_with_timeFrame(get_test_db(), None, 'CAN', 2010, "equal")

    extracted_values = [{'year': data.year, 'country': data.country, 'ghg': data.share_of_temperature_change_from_ghg}
                        for data in result]
    assert len(extracted_values) == 1

    expected_values = [{'year': 2010, 'country': 'Canada', 'ghg': 2.21}]
    for expected in expected_values:
        assert expected in extracted_values


def test_get_country_data_iso_with_time_frame_equal_no_data():
    with pytest.raises(HTTPException) as excinfo:
        country_service.get_country_data_with_timeFrame(get_test_db(), None, 'CAN', 2009, "equal")


def test_get_country_data_name_no_timeframe():
    result = country_service.get_country_data_without_timeFrame(get_test_db(), 'Canada', None)

    extracted_values = [{'year': data.year, 'country': data.country, 'ghg': data.share_of_temperature_change_from_ghg}
                        for data in result]
    assert len(extracted_values) == 3

    expected_values = [{'year': 2010, 'country': 'Canada', 'ghg': 2.21},
                       {'year': 2011, 'country': 'Canada', 'ghg': 2.198},
                       {'year': 2012, 'country': 'Canada', 'ghg': 2.186}]
    for expected in expected_values:
        assert expected in extracted_values


def test_get_country_data_name_no_timeframe_no_data():
    result = country_service.get_country_data_without_timeFrame(get_test_db(), 'Canada', None)

    # Result should contain all the data for 'Africa'
    extracted_values = [{'year': data.year, 'country': data.country, 'ghg': data.share_of_temperature_change_from_ghg}
                        for data in result]
    assert len(extracted_values) == 3

    expected_values = [{'year': 2010, 'country': 'Canada', 'ghg': 2.21},
                       {'year': 2011, 'country': 'Canada', 'ghg': 2.198},
                       {'year': 2012, 'country': 'Canada', 'ghg': 2.186}]
    for expected in expected_values:
        assert expected in extracted_values


def test_get_country_data_iso_no_timeframe():
    result = country_service.get_country_data_without_timeFrame(get_test_db(), None, 'CAN')

    extracted_values = [{'year': data.year, 'country': data.country, 'ghg': data.share_of_temperature_change_from_ghg}
                        for data in result]
    assert len(extracted_values) == 3

    expected_values = [{'year': 2010, 'country': 'Canada', 'ghg': 2.21},
                       {'year': 2011, 'country': 'Canada', 'ghg': 2.198},
                       {'year': 2012, 'country': 'Canada', 'ghg': 2.186}]
    for expected in expected_values:
        assert expected in extracted_values


def test_get_country_data_iso_no_timeframe_no_data():
    result = country_service.get_country_data_without_timeFrame(get_test_db(), None, 'CAN')

    # Result should contain all the data for 'Africa'
    extracted_values = [{'year': data.year, 'country': data.country, 'ghg': data.share_of_temperature_change_from_ghg}
                        for data in result]
    assert len(extracted_values) == 3

    expected_values = [{'year': 2010, 'country': 'Canada', 'ghg': 2.21},
                       {'year': 2011, 'country': 'Canada', 'ghg': 2.198},
                       {'year': 2012, 'country': 'Canada', 'ghg': 2.186}]
    for expected in expected_values:
        assert expected in extracted_values


def test_get_country_emission_time_frame_before():
    result = country_service.get_country_emission_with_timeframe(get_test_db(), 'Canada', None, 2012, "before")

    extracted_values = [{'year': data.year, 'country': data.country, 'ghg': data.total_ghg} for data in result]
    assert len(extracted_values) > 0


def test_get_country_emission_iso_with_time_frame_after():
    result = country_service.get_country_emission_with_timeframe(get_test_db(), None, 'CAN', 2010, "after")

    extracted_values = [{'year': data.year, 'country': data.country, 'ghg': data.total_ghg} for data in result]
    assert len(extracted_values) > 0


def test_get_country_emission_with_time_frame_no_data():
    with pytest.raises(HTTPException) as excinfo:
        country_service.get_country_emission_with_timeframe(get_test_db(), 'Canada', None, 2009, "before")


def test_get_country_emission_iso_with_time_frame_before_no_data():
    with pytest.raises(HTTPException) as excinfo:
        country_service.get_country_emission_with_timeframe(get_test_db(), None, 'CAN', 2009, "before")


def test_get_country_emissions_by_name_with_data():
    result = country_service.get_country_emissions_by_name(get_test_db(), 'Canada', None)
    assert result is not None


def test_get_country_emissions_by_iso_with_data():
    result = country_service.get_country_emissions_by_name(get_test_db(), None, 'CAN')
    assert result is not None


def test_get_country_emissions_by_name_no_data():
    with pytest.raises(HTTPException) as excinfo:
        result = country_service.get_country_emissions_by_name(get_test_db(), 'NOC', None)


def test_get_country_emissions_by_iso_no_data():
    with pytest.raises(HTTPException) as excinfo:
        result = country_service.get_country_emissions_by_name(get_test_db(), None, 'NOC')


def test_create_country_data_success():
    db = get_test_db()

    country_data_req = CountryDataRequest(
        country="AAATest Country",
        year=2021,
        iso_code="TCY",
        population=1000000,
        gdp=50000.0,
        co2=1.5,
        energy_per_capita=3000.0,
        energy_per_gdp=200.0,
        methane=0.8,
        nitrous_oxide=0.4,
        share_of_temperature_change_from_ghg=0.5,
        temperature_change_from_ch4=0.2,
        temperature_change_from_co2=0.3,
        temperature_change_from_ghg=0.4,
        temperature_change_from_n2o=0.1,
        total_ghg=2.5
    )

    result = create_country_data(db, country_data_req)
    assert result is not None


def test_create_country_data_invalid_data():
    db = get_test_db()
    with pytest.raises(ValidationError):
        CountryDataRequest(
            country="",
            year=2021,
        )


def test_create_country_data_db_exception():
    db = get_test_db()
    country_data_req = CountryDataRequest(
        country="AAATest Country",
        year=2021,
        iso_code="TCY",
        population=1000000,
        gdp=50000.0,
        co2=1.5,
        energy_per_capita=3000.0,
        energy_per_gdp=200.0,
        methane=0.8,
        nitrous_oxide=0.4,
        share_of_temperature_change_from_ghg=0.5,
        temperature_change_from_ch4=0.2,
        temperature_change_from_co2=0.3,
        temperature_change_from_ghg=0.4,
        temperature_change_from_n2o=0.1,
        total_ghg=2.5
    )
    with patch.object(db, 'add', side_effect=IntegrityError('mocked', 'statement', 'params')):
        with pytest.raises(HTTPException) as excinfo:
            create_country_data(db, country_data_req)
        assert excinfo.value.status_code == 500


def test_update_country_success():
    db = get_test_db()

    country_data_req = CountryDataRequest(
        country="AAATest Country2",
        year=2021,
        iso_code="TCY",
        population=1000000,
        gdp=50000.0,
        co2=1.5,
        energy_per_capita=3000.0,
        energy_per_gdp=200.0,
        methane=0.8,
        nitrous_oxide=0.4,
        share_of_temperature_change_from_ghg=0.5,
        temperature_change_from_ch4=0.2,
        temperature_change_from_co2=0.3,
        temperature_change_from_ghg=0.4,
        temperature_change_from_n2o=0.1,
        total_ghg=2.5
    )

    create_country_data(db, country_data_req)

    updated_data = CountryDataRequest(
        population=1000001,
        gdp=60000.0,
    )

    result = country_service.update_country(db, countryName='AAATest Country',
                                            iso=None, year=2021, updated_data=updated_data)

    assert result is not None
    assert result.population == 1000001
    assert result.gdp == 60000.0


def test_update_country_not_found():
    db = get_test_db()

    updated_data = CountryDataRequest(
        population=2000000,
    )

    with pytest.raises(HTTPException) as excinfo:
        country_service.update_country(db, countryName='Nonexistent Country', iso=None, year=2021,
                                       updated_data=updated_data)
    assert excinfo.value.status_code == 404


def test_delete_country_data_by_name_and_year_success():
    db = get_test_db()
    # Assuming you have a way to add a test entry or a fixture for initial data

    country_data_req = CountryDataRequest(
        country="AAATest Country3",
        year=2021,
        iso_code="TCY",
        population=1000000,
        gdp=50000.0,
        co2=1.5,
        energy_per_capita=3000.0,
        energy_per_gdp=200.0,
        methane=0.8,
        nitrous_oxide=0.4,
        share_of_temperature_change_from_ghg=0.5,
        temperature_change_from_ch4=0.2,
        temperature_change_from_co2=0.3,
        temperature_change_from_ghg=0.4,
        temperature_change_from_n2o=0.1,
        total_ghg=2.5
    )

    create_country_data(db, country_data_req)

    response = country_service.delete_country_data_by_name_and_year(db, 'AAATest Country3', 2021)
    assert response == {"detail": "Deleted successfully"}
    # Verify that the data is actually deleted
    assert db.query(CountryData).filter(CountryData.country == 'AAATest Country3',
                                        CountryData.year == 2021).first() is None


def test_delete_country_data_by_name_and_year_not_found():
    db = get_test_db()
    with pytest.raises(HTTPException) as excinfo:
        country_service.delete_country_data_by_name_and_year(db, 'Nonexistent Country', 2021)
    assert excinfo.value.status_code == 404


def test_getClimContYear_valid_bottom():
    db = get_test_db()
    result = country_service.getClimContYear(db, 5, 2021, 'bottom')
    assert isinstance(result, list)
    assert len(result) <= 5


def test_getClimContYear_valid_top():
    db = get_test_db()
    result = country_service.getClimContYear(db, 5, 2021, 'top')
    assert isinstance(result, list)
    assert len(result) <= 5


def test_getClimContYear_invalid_params():
    db = get_test_db()
    result = country_service.getClimContYear(db, -1, 2021, 'bottom')
    assert result == 'Invalid parameters.'


def test_getClimContPast_valid_bottom():
    db = get_test_db()
    result = country_service.getClimContPast(db, 5, 3, 'bottom')
    assert isinstance(result, list)


def test_getClimContPast_invalid_params():
    db = get_test_db()
    result = country_service.getClimContPast(db, 0, 3, 'top')
    assert result == 'Invalid parameters.'


def test_getEnergy_valid():
    db = get_test_db()
    result = country_service.getEnergy(db, 1, 10, 2021)
    assert isinstance(result, list)


def test_getEnergy_default_params():
    db = get_test_db()
    result = country_service.getEnergy(db, None, None, 2021)
    assert isinstance(result, list)
    assert len(result) == 10


@patch('requests.get')
def test_get_Country_Add_Data_valid(mock_get):
    mock_get.return_value.json.return_value = {'data': 'mocked_data'}
    result = country_service.get_Country_Add_Data('Test Country')
    assert 'data' in result


@patch('requests.get')
def test_get_Country_Add_Data_not_found(mock_get):
    mock_get.return_value.json.return_value = {}
    result = country_service.get_Country_Add_Data('Invalid Country')
    assert not result


def test_get_country_list():
    db = get_test_db()
    result = country_service.get_country_list(db)
    assert result
