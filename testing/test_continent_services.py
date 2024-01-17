from fastapi import HTTPException
import pytest
from services import continent_service
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# The TestDB had only data for 2010, 2011, and 2012
def get_test_db():
    db_url = "sqlite:///TestDB.db"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def test_get_temperature_change_by_continent_service():
    result = continent_service.get_temperature_change_by_continent(get_test_db(), 'Africa', 0)

    # Result should contain all the data for 'Africa'
    extracted_values = [{'year': data.year, 'country': data.country, 'ghg': data.share_of_temperature_change_from_ghg}
                        for data in result]
    assert len(extracted_values) == 3

    expected_values = [{'year': 2010, 'country': 'Africa', 'ghg': 9.131},
                       {'year': 2011, 'country': 'Africa', 'ghg': 9.158},
                       {'year': 2012, 'country': 'Africa', 'ghg': 9.183}]
    for e in expected_values:
        assert e in extracted_values


def test_get_temperature_change_by_continent_service_with_year():
    db = get_test_db()
    with pytest.raises(HTTPException) as result_info:
        continent_service.get_temperature_change_by_continent(db, 'Value not in DB', 2010)
    assert result_info.value.status_code == 404
