from fastapi import HTTPException
from sqlalchemy.orm import load_only
# TODO: Read through the DB and Delete irrelevant columns.
# TODO: Double check all the error codes.
from dataManagement.models import CountryData


# TODO: double check this is returning the right parameters.
# Gets the temp changes for all of the continents.
def get_temperature_change_by_continent(db):
    result = db.query(CountryData).filter(CountryData.country.in_(
        ["Africa", "Asia", "North America", "South America", "Oceania", "Europe", "Antarctica"])
    ).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


# TODO: rewrite the function to combine this and one above using style from the country services.
# TODO Add the ShareOfTemperature...
def get_temperature_change_by_continent_or_after_year(db, yearid):
    result = db.query(CountryData).filter(
        CountryData.year > yearid,
        CountryData.country.in_(
            ["Africa", "Asia", "North America", "South America", "Oceania", "Europe", "Antarctica"])
    ).options(
        load_only(CountryData.country,
                  CountryData.year,
                  CountryData.temperature_change_from_ch4,
                  CountryData.temperature_change_from_co2,
                  CountryData.temperature_change_from_n2o,
                  CountryData.temperature_change_from_ghg
                  )).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result
