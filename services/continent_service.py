from fastapi import HTTPException
from sqlalchemy.orm import load_only
from dataManagement.models import CountryData
# TODO: Read through the DB and Delete irrelevant columns.
# TODO: Double check all the error codes.


def get_temperature_change_by_continent(db, continent):
    result = db.query(CountryData).filter(
            CountryData.country == continent
    ).options(
        load_only(CountryData.country,
                  CountryData.year,
                  CountryData.share_of_temperature_change_from_ghg,
                  CountryData.temperature_change_from_ch4,
                  CountryData.temperature_change_from_co2,
                  CountryData.temperature_change_from_n2o,
                  CountryData.temperature_change_from_ghg
                  )).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


# TODO: rewrite the function to combine this and one above using style from the country services.
def get_temperature_change_continent_after_year(
        db, continent, yearid, inCSV):
    result = db.query(CountryData).filter(
        CountryData.year >= yearid,
        CountryData.country == continent
    ).options(
        load_only(CountryData.country,
                  CountryData.year,
                  CountryData.share_of_temperature_change_from_ghg,
                  CountryData.temperature_change_from_ch4,
                  CountryData.temperature_change_from_co2,
                  CountryData.temperature_change_from_n2o,
                  CountryData.temperature_change_from_ghg
                  )).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result
