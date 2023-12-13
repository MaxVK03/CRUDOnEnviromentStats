from fastapi import HTTPException
from sqlalchemy.orm import load_only

from models import CountryData


def get_temperature_change_by_continent(db):
    result = db.query(CountryData).filter(CountryData.country.in_(
        ["Africa", "Asia", "North America", "South America", "Oceania", "Europe", "Antarctica"])
    ).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


#TODO This one can be combined with the one above, using optional path parameters.
#TODO Add the ShareOfTemperature...
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

