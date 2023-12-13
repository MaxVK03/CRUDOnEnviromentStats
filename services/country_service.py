from fastapi import HTTPException
from sqlalchemy import asc
from sqlalchemy.orm import load_only
from models import CountryData


def query_country_data(db, model_field_name, value, yearid, timeFrame):
    model_field = getattr(CountryData, model_field_name)
    year_field = CountryData.year

    # Ensure yearid is an integer
    yearid = int(yearid) if yearid is not None else None

    timeFrame_conditions = {
        'before': year_field < yearid,
        'after': year_field > yearid,
        'equal': year_field == yearid
    }

    condition = timeFrame_conditions.get(timeFrame, year_field == yearid)

    if condition is not None:
        return db.query(CountryData).filter(condition, model_field == value).all()
    else:
        # Handle case where timeFrame is not one of 'before', 'after', or 'equal'
        return db.query(CountryData).filter(model_field == value).all()


def handle_not_found(result):
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


# Below are all gets
def get_country_data_with_timeFrame(db, countryName, iso, yearid, timeFrame):
    field = 'country' if countryName else 'iso_code'
    value = countryName or iso
    return query_country_data(db, field, value, yearid, timeFrame)


def get_country_emissions(db, countryName, iso, yearid, timeFrame):
    result = None
    field = 'country' if countryName else 'iso_code'
    value = countryName or iso

    if timeFrame is None:
        result = db.query(CountryData).filter(CountryData.__dict__[field] == value).all()
    else:
        result = query_country_data(db, field, value, yearid, timeFrame)

    return handle_not_found(result)


# Below are all deletes
def delete_country_data_by_name_and_year_and_timeFrame(db, countryName, yearid, timeFrame):
    result = query_country_data(db, 'country', countryName, yearid, timeFrame)
    db.delete(result)
    db.commit()


# Other CRUD operations
def create_country_data(db, country_data_request):
    new_country_data = CountryData(**country_data_request.dict())
    db.add(new_country_data)
    db.commit()
    db.refresh(new_country_data)
    return new_country_data


def update_country_data_by_name(db, country_name, updated_data):
    existing_data = db.query(CountryData).filter(CountryData.country == country_name).first()
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


def update_country_data_by_isocode(db, countryIsocode, countrydt):
    existing_data = db.query(CountryData).filter(CountryData.iso_code == countryIsocode).first()
    if not existing_data:
        raise HTTPException(status_code=404, detail='Item not found')
    for key, value in countrydt.dict().items():
        setattr(existing_data, key, value)
    db.commit()
    db.refresh(existing_data)
    return existing_data


def delete_country_data_by_isocode_and_year(db, countryIsocode, yearid):
    data_to_delete = db.query(CountryData).filter(CountryData.iso_code == countryIsocode,
                                                  CountryData.year == yearid).first()
    if not data_to_delete:
        raise HTTPException(status_code=404, detail='Item not found')
    db.delete(data_to_delete)
    db.commit()
    return {"detail": "Deleted successfully"}


def get_country_emissions_by_name(db, countryName):
    result = db.query(CountryData).filter(CountryData.country == countryName).options(
        load_only(
            CountryData.year,
            CountryData.country,
            CountryData.co2,
            CountryData.methane,
            CountryData.nitrous_oxide,
            CountryData.total_ghg)
    ).all()
    return handle_not_found(result)


def get_country_emissions_by_isocode(db, countryIsocode):
    result = db.query(CountryData).filter(CountryData.iso_code == countryIsocode).options(
        load_only(
            CountryData.year,
            CountryData.country,
            CountryData.co2,
            CountryData.methane,
            CountryData.nitrous_oxide,
            CountryData.total_ghg)
    ).all()
    return handle_not_found(result)


def get_country_emissions_by_name_after_year(db, countryName, yearid):
    result = db.query(CountryData).filter(CountryData.country == countryName, CountryData.year >= yearid).options(
        load_only(
            CountryData.year,
            CountryData.country,
            CountryData.co2,
            CountryData.methane,
            CountryData.nitrous_oxide,
            CountryData.total_ghg)
    ).all()
    return handle_not_found(result)


def get_country_data_without_timeFrame(db, countryName, iso, yearid, timeFrame):
    field = 'country' if countryName else 'iso_code'
    value = countryName or iso
    result = db.query(CountryData).filter(CountryData.__dict__[field] == value).all()
    return result
