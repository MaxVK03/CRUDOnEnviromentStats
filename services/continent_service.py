from fastapi import HTTPException
from models import CountryData


def get_temperature_change_by_continent(db):
    result = db.query(CountryData).filter(CountryData.continent.in_(
        ["Africa", "Asia", "North America", "South America", "Oceania", "Europe", "Antarctica"])
    ).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


def get_temperature_change_by_continent_after_year(db, yearid):
    result = db.query(CountryData).filter(
        CountryData.year > yearid,
        CountryData.continent.in_(
            ["Africa", "Asia", "North America", "South America", "Oceania", "Europe", "Antarctica"])
    ).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result

