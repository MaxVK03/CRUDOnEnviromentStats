from fastapi import HTTPException
from sqlalchemy.orm import load_only
from dataManagement.models import CountryData


# TODO: Double check all the error codes.
# TODO: use opType in handle_no_found or remove it.

# Function that is called before return the query result.
# If the query return is empty, a HTTP error is raised.
def handle_not_found(result, opType):
    if result == []:
        raise HTTPException(status_code=404, detail='No items found matching query')
    elif result is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


# Get the temperature change data for a given continent from the database.
def get_temperature_change_by_continent(db, continent, yearid):
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
    print(type(result))
    return handle_not_found(result, "get")

# Function that calculates the population change of a country based on a start and end year.
def get_population_change_continent(db, continent, startYear, endYear):
    startPop = db.query(CountryData.population).filter(
        CountryData.country == continent,
        CountryData.year == startYear).scalar()

    endPop = db.query(CountryData.population).filter(CountryData.country == continent,
        CountryData.year == endYear).scalar()

    if startPop and endPop:
        return ((endPop - startPop) / startPop) * 100
    else:
        raise HTTPException(status_code=404, detail="No data for given years found")