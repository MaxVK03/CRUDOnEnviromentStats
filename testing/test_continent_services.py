import pytest
from fastapi import HTTPException
from services import continent_service
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataManagement import models

# The TestDB has only data for 2010, 2011, and 2012
def get_test_db():
    db_url = "sqlite:///TestDB.db"
    engine = create_engine(db_url)
    models.Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def test_get_all_temperature_change_for_continent_without_year():
    result = continent_service.get_temperature_change_by_continent(get_test_db(), 'Africa', 0)
    extracted_values = [{
        'year': data.year, 
        'country': data.country, 
        'ghg_share': data.share_of_temperature_change_from_ghg, 
        'ch4': data.temperature_change_from_ch4, 
        'co2': data.temperature_change_from_co2, 
        'n2o': data.temperature_change_from_n2o, 
        'ghg': data.temperature_change_from_ghg
    } for data in result]
    expected_values = [{'year': 2010, 'country': 'Africa', 'ghg_share': 9.131, 'ch4': 0.051, 'co2': 0.063, 'n2o': 0.009, 'ghg': 0.123},
                       {'year': 2011, 'country': 'Africa', 'ghg_share': 9.158, 'ch4': 0.052, 'co2': 0.064, 'n2o': 0.009, 'ghg': 0.125},
                       {'year': 2012, 'country': 'Africa', 'ghg_share': 9.183, 'ch4': 0.053, 'co2': 0.066, 'n2o': 0.009, 'ghg': 0.128}]
    assert len(extracted_values) == 3
    for expected_value in expected_values:
        assert expected_value in extracted_values


def test_get_all_temperature_change_for_continent_with_year():
    result = continent_service.get_temperature_change_by_continent(get_test_db(), 'Africa', 2011)
    extracted_values = [{
        'year': data.year, 
        'country': data.country, 
        'ghg_share': data.share_of_temperature_change_from_ghg, 
        'ch4': data.temperature_change_from_ch4, 
        'co2': data.temperature_change_from_co2, 
        'n2o': data.temperature_change_from_n2o, 
        'ghg': data.temperature_change_from_ghg
    } for data in result]
    expected_values = [{'year': 2011, 'country': 'Africa', 'ghg_share': 9.158, 'ch4': 0.052, 'co2': 0.064, 'n2o': 0.009, 'ghg': 0.125},
                       {'year': 2012, 'country': 'Africa', 'ghg_share': 9.183, 'ch4': 0.053, 'co2': 0.066, 'n2o': 0.009, 'ghg': 0.128}]
    assert len(extracted_values) == 2
    for expected_value in expected_values:
        assert expected_value in extracted_values


def test_get_all_temperature_change_for_continent_not_in_db():
    db = get_test_db()
    with pytest.raises(HTTPException) as result_info:
       continent_service.get_temperature_change_by_continent(db, 'Invalid', 2010)
    assert result_info.value.status_code == 404


def test_get_all_temperature_change_for_continent_with_year_outside_range():
    db = get_test_db()
    with pytest.raises(HTTPException) as result_info:
       continent_service.get_temperature_change_by_continent(db, 'Africa', 2015)
    assert result_info.value.status_code == 404
