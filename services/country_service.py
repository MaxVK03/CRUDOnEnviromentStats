from fastapi import HTTPException
from sqlalchemy import asc
from sqlalchemy.orm import load_only
from models import CountryData


def get_country_data(db, countryName, iso, yearid, timeFrame):
    result = None
    if countryName:
        if timeFrame == 'before':
            result = db.query(CountryData).filter(CountryData.country == countryName,
                                                  CountryData.year < yearid).all()
        elif timeFrame == 'after':
            result = db.query(CountryData).filter(CountryData.country == countryName,
                                                  CountryData.year > yearid).all()
        elif timeFrame == 'equal':
            result = db.query(CountryData).filter(CountryData.country == countryName,
                                                  CountryData.year == yearid).all()
        elif yearid is None and timeFrame is None:
            result = db.query(CountryData).filter(CountryData.country == countryName,
                                                  CountryData.year == yearid).all()
    elif iso:
        if timeFrame == 'before':
            result = db.query(CountryData).filter(CountryData.iso_code == iso,
                                                  CountryData.year < yearid).all()
        elif timeFrame == 'after':
            result = db.query(CountryData).filter(CountryData.iso_code == iso,
                                                  CountryData.year > yearid).all()
        elif timeFrame == 'equal':
            result = db.query(CountryData).filter(CountryData.iso_code == iso,
                                                  CountryData.year == yearid).all()
        elif yearid is None and timeFrame is None:
            result = db.query(CountryData).filter(CountryData.iso_code == iso,
                                                  CountryData.year == yearid).all()
    return result



def delete_country_data_by_name_and_year_and_timeFrame(db, countryName, yearid, timeFrame):
    if timeFrame == 'before':
        result = db.query(CountryData).filter(CountryData.country == countryName,
                                              CountryData.year < yearid).all()
    elif timeFrame == 'after':
        result = db.query(CountryData).filter(CountryData.country == countryName,
                                              CountryData.year > yearid).all()
    elif timeFrame == 'equal':
        result = db.query(CountryData).filter(CountryData.country == countryName,
                                              CountryData.year == yearid).all()


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
    result = db.query(CountryData).first()
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
    data_to_delete = (db.query(CountryData)
                      .filter(CountryData.iso_code == countryIsocode, CountryData.year == yearid).first())
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
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


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
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


def get_country_emissions_by_name_after_year(db, countryName, yearid):
    result = db.query(CountryData.country,
                      CountryData.co2,
                      CountryData.methane,
                      CountryData.nitrous_oxide,
                      CountryData.total_ghg).filter(CountryData.country == countryName,
                                                    CountryData.year >= yearid).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


# TODO Fix filtering on two things, this gives internal server error.
def get_country_emissions_by_isocode_after_year(db, countryIsocode, yearid):
    result = db.query(CountryData.country,
                      CountryData.co2,
                      CountryData.methane,
                      CountryData.nitrous_oxide,
                      CountryData.total_ghg).filter(CountryData.iso_code == countryIsocode,
                                                    CountryData.year >= yearid).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


def get_country_energy_by_year(db, yearid):
    result = db.query(CountryData).filter(CountryData.year == yearid).options(
        load_only(
            CountryData.country,
            CountryData.year,
            CountryData.population,
            CountryData.energy_per_capita,
            CountryData.energy_per_gdp
        )
    ).order_by(asc(CountryData.population)).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


# TODO: Fix the ordering
# Hi Max, Arnaud here. I just found that you can do .order_by(asc|desc( ' what you want to filter by))
# I presume this will be helpful for this part. I don't think you need to do the regex.
def get_climate_contribution_by_year(db, year, n, order):
    if order == 'asc':
        result = db.query(CountryData.country,
                          CountryData.co2,
                          CountryData.methane,
                          CountryData.nitrous_oxide,
                          CountryData.total_ghg).filter(CountryData.year == year).limit(n).all()
    elif order == 'desc':
        result = db.query(CountryData.country,
                          CountryData.co2,
                          CountryData.methane,
                          CountryData.nitrous_oxide,
                          CountryData.total_ghg).filter(CountryData.year == year).limit(n).all()
    else:
        raise HTTPException(status_code=404, detail='Item not found')
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


# TODO: Fix the ordering
def get_climate_contribution_previous_years(db, m, n, order):
    if order == 'asc':
        result = db.query(CountryData.country,
                          CountryData.co2,
                          CountryData.methane,
                          CountryData.nitrous_oxide,
                          CountryData.total_ghg).filter(CountryData.year <= m).limit(n).all()
    elif order == 'desc':
        result = db.query(CountryData.country,
                          CountryData.co2,
                          CountryData.methane,
                          CountryData.nitrous_oxide,
                          CountryData.total_ghg).filter(CountryData.year <= m).limit(n).all()
    else:
        raise HTTPException(status_code=404, detail='Item not found')
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result

