from fastapi import HTTPException, requests
from fastapi.openapi.models import Response
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import load_only, Session
from dataManagement.models import CountryData
import requests

CONTINENTS = {
    "Africa",
    "Asia",
    "North America",
    "South America",
    "Oceania",
    "Europe",
    "Antarctica",
}


# Gets all country data given a country name, a time frame and a year.
# The time frame part allows specification for before, after or equal to a specific year.
def query_country_data(db, model_field_name, value, yearid, timeFrame):
    model_field = getattr(CountryData, model_field_name)
    year_field = CountryData.year
    yearid = int(yearid) if yearid is not None else None

    timeFrame_conditions = {
        'before': year_field <= yearid,
        'after': year_field >= yearid,
        'equal': year_field == yearid
    }

    condition = timeFrame_conditions.get(timeFrame, year_field == yearid)

    if condition is not None:
        return db.query(CountryData).filter(condition, model_field == value).all()
    else:
        return db.query(CountryData).filter(model_field == value).all()


# TODO: See if possible to make more powerful.
# A Helper function for when a result cannot be found. Returns the appropriate HTTP response code
# Indicating the searched for item has not been found.
def handle_not_found(result, opType):
    if opType == "get" or opType == "delete":
        if result == [] or result is None:
            raise HTTPException(status_code=404, detail='Item not found')
        return result
    elif opType == "create":
        if result is None:
            raise HTTPException(status_code=400, detail='Failed to create item')
        return result
    else:
        return result


# A function for getting country data with the time frame. Makes use of the query country data function as it is a
# repeated function throughout the code
# The time frame part allows specification for before, after or equal to a specific year.
# Allows for Country name or ISO code depending on how the function is called.
def get_country_data_with_timeFrame(db, countryName, iso, yearid, timeFrame):
    field = 'country' if countryName else 'iso_code'
    value = countryName or iso
    return query_country_data(db, field, value, yearid, timeFrame)


# Function for getting country data without the time frame. Works the same as the function above.
# Allows for Country name or ISO code depending on how the function is called.
def get_country_data_without_timeFrame(db, countryName, iso):
    field = 'country' if countryName else 'iso_code'
    value = countryName or iso
    result = db.query(CountryData).filter(CountryData.__dict__[field] == value).all()
    return handle_not_found(result, "get")


# Gets the country emission fields when provided a time frame.
# Allows for Country name or ISO code depending on how the function is called.
# The time frame part allows specification for before, after or equal to a specific year.
def get_country_emission_with_timeframe(db, countryName, iso, yearid, timeFrame):
    field = 'country' if countryName else 'iso_code'
    value = countryName or iso
    year_field = CountryData.year

    timeFrame_conditions = {
        'before': year_field <= yearid,
        'after': year_field >= yearid,
        'equal': year_field == yearid
    }

    condition = timeFrame_conditions.get(timeFrame, year_field == yearid)
    result = None
    if condition is not None:
        result = db.query(CountryData).filter(condition, CountryData.__dict__[field] == value).options(
            load_only(
                CountryData.year,
                CountryData.country,
                CountryData.co2,
                CountryData.methane,
                CountryData.nitrous_oxide,
                CountryData.total_ghg)
        ).all()
    else:
        result = db.query(CountryData).filter(condition, CountryData.__dict__[field] == value).options(
            load_only(
                CountryData.year,
                CountryData.country,
                CountryData.co2,
                CountryData.methane,
                CountryData.nitrous_oxide,
                CountryData.total_ghg)
        ).all()
    return handle_not_found(result, "get")


# Gets all emission related data for a country when provided the name of the country.
def get_country_emissions_by_name(db, countryName, iso):
    if countryName:
        result = db.query(CountryData).filter(CountryData.country == countryName).options(
            load_only(
                CountryData.year,
                CountryData.country,
                CountryData.co2,
                CountryData.methane,
                CountryData.nitrous_oxide,
                CountryData.total_ghg)
        ).all()
        return handle_not_found(result, "get")
    else:
        result = db.query(CountryData).filter(CountryData.iso_code == iso).options(
            load_only(
                CountryData.year,
                CountryData.country,
                CountryData.co2,
                CountryData.methane,
                CountryData.nitrous_oxide,
                CountryData.total_ghg)
        ).all()
        return handle_not_found(result, "get")


# TODO: Add the required message if the country is not found.
# Deletes the country data when given the country name.
# The time frame parameter allows specification for before, after or equal to a specific year.
def delete_country_data_by_name_and_year_and_timeFrame(db, countryName, yearid, timeFrame):
    result = query_country_data(db, 'country', countryName, yearid, timeFrame)
    if not result:
        return handle_not_found(result, "delete")
    db.delete(result)
    db.commit()


# Other CRUD operations
# Creates a country data item for the provided year with the provided data.
def create_country_data(db: Session, country_data_request):
    try:
        new_country_data = CountryData(**country_data_request.dict())
        db.add(new_country_data)
        db.commit()
        db.refresh(new_country_data)
        return handle_not_found(new_country_data, "create")
    except Exception as e:
        # Handle specific exceptions as needed
        raise HTTPException(status_code=500, detail=str(e))


# TODO: Once have wifi check if this must be for a specific year. Makes sense it should be.
# Retrieves a country and then uses the provided data to update the country data for that year.
# Can retrieve the data by either the country name or the countries ISO code.
def update_country(db, countryName, iso, year, updated_data):
    field = 'country' if countryName else 'iso_code'
    value = countryName or iso
    existing_data = db.query(CountryData).filter(CountryData.__dict__[field] == value, CountryData.year == year).first()

    if not existing_data:
        raise HTTPException(status_code=404, detail='Item not found')

    for key, value in updated_data.dict().items():
        setattr(existing_data, key, value)
    db.commit()
    db.refresh(existing_data)
    return existing_data


def get_all_data(db):
    result = db.query(CountryData).all()
    return result


def delete_country_data_by_isocode_and_year(db, countryIsocode, yearid):
    data_to_delete = db.query(CountryData).filter(CountryData.iso_code == countryIsocode,
                                                  CountryData.year == yearid).first()
    if not data_to_delete:
        raise HTTPException(status_code=404, detail='Item not found')
    db.delete(data_to_delete)
    db.commit()
    return {"detail": "Deleted successfully"}


def getClimContYear(db, noCountries, year, sort):
    if sort == 'bottom' and noCountries >= 1 and year >= 1:
        result = db.query(CountryData).filter(CountryData.country.notin_(CONTINENTS)).filter(
            CountryData.year == year).order_by(
            asc(CountryData.share_of_temperature_change_from_ghg)).limit(noCountries).all()
        return handle_not_found(result, "get")
    elif sort == 'top' and noCountries >= 1 and year >= 1:
        result = db.query(CountryData).filter(CountryData.country.notin_(CONTINENTS)).filter(
            CountryData.year == year).order_by(desc(
            CountryData.share_of_temperature_change_from_ghg)).limit(noCountries).all()
        return handle_not_found(result, "get")
    else:
        return 'Invalid parameters.'


def getClimContPast(db, noCountries, pastYears, sort):
    # TODO: not hardcode the max year maybe (2022)
    target_years = [2022 - i for i in range(pastYears)]
    if sort == 'bottom' and noCountries >= 1 and pastYears >= 1:
        result = (
            db.query(CountryData)
            .filter(CountryData.country.not_in(CONTINENTS))
            .filter(CountryData.year.in_(target_years))
            .order_by(asc(CountryData.share_of_temperature_change_from_ghg))
            .limit(noCountries)
            .all()
        )
        return handle_not_found(result, "get")
    elif sort == 'top' and noCountries >= 1 and pastYears >= 1:
        result = (
            db.query(CountryData)
            .filter(CountryData.country.not_in(CONTINENTS))
            .filter(CountryData.year.in_(target_years))
            .order_by(desc(CountryData.share_of_temperature_change_from_ghg))
            .limit(noCountries)
            .all()
        )
        return handle_not_found(result, "get")
    else:
        return 'Invalid parameters.'
        # TODO: HTTP ERROR


# Gets the energy data for a provided year with paging support. If there is no provided page number then just returns
# the first page otherwise will return the requested page.
def getEnergy(db, page, noCountries, year):
    # Set a default page number if page is None
    if page is None:
        page = 1

    if noCountries is None:
        noCountries = 10

    # Calculate the offset
    offset_value = (page - 1) * noCountries

    # Query with offset and limit for pagination
    result = db.query(CountryData).options(
        load_only(
            CountryData.year,
            CountryData.country,
            CountryData.energy_per_gdp,
            CountryData.energy_per_capita,
            CountryData.population)
    ).filter(CountryData.country.not_in(CONTINENTS)).filter(CountryData.year == year).order_by(
        CountryData.population.asc()).offset(offset_value).limit(noCountries).all()

    return handle_not_found(result, "get")


def get_Country_Add_Data(country_name):
    country_name = country_name.replace(" ", "%20")
    url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
    response = requests.get(url)

    result = response.json()
    return handle_not_found(result, "get")
