from fastapi import HTTPException
from models import CountryData


def get_country_data_by_name_and_year(db, country_name, yearid):
    #first100
    result = db.query(CountryData).filter(CountryData.country == country_name, CountryData.year == yearid).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


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


def delete_country_data_by_name_and_year(db, country_name, yearid):
    data_to_delete = (db.query(CountryData).
                      filter(CountryData.country == country_name, CountryData.year == yearid).first())
    if not data_to_delete:
        raise HTTPException(status_code=404, detail='Item not found')
    db.delete(data_to_delete)
    db.commit()
    return {"detail": "Deleted successfully"}


def get_all_data(db):
    result = db.query(CountryData).first()
    return result


def get_country_data_by_isocode(db, countryIsocode):
    result = db.query(CountryData).filter(CountryData.iso_code == countryIsocode).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


def get_country_data_by_isocode_and_year(db, countryIsocode, yearid):
    result = db.query(CountryData).filter(CountryData.iso_code == countryIsocode, CountryData.year == yearid).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
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
    result = db.query(CountryData.country,
                      CountryData.co2,
                      CountryData.methane,
                      CountryData.nitrous_oxide,
                      CountryData.total_ghg).filter(CountryData.country == countryName).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


def get_country_emissions_by_isocode(db, countryIsocode):
    result = db.query(CountryData.country,
                      CountryData.co2,
                      CountryData.methane,
                      CountryData.nitrous_oxide,
                      CountryData.total_ghg).filter(CountryData.iso_code == countryIsocode).all()
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


def get_energy_per_capita_by_year(db, yearid):
    result = db.query(CountryData.country,
                      CountryData.energy_per_capita).filter(CountryData.year == yearid).all()
    if not result:
        raise HTTPException(status_code=404, detail='Item not found')
    return result


# TODO: Fix the ordering
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