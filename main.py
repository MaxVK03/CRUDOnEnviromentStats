from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from database import SessionLocal
from database import engine
from models import CountryData
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[SessionLocal, Depends(get_db)]


async def country_emissions(countryname: str, db: db_dependency):
    emissions_data = db.query(
        CountryData.country,
        CountryData.co2,
        CountryData.methane,
        CountryData.nitrous_oxide,
        CountryData.total_ghg
    ).filter(CountryData.country == countryname).all()
    if emissions_data is None or len(emissions_data) == 0:
        raise HTTPException(status_code=400, detail='Item not found')
    return emissions_data


class CountryDataRequest(BaseModel):
    country: str = Field(min_length=1, max_length=100)
    year: int = Field(min=0, max=9999)
    iso_code: str
    population: int
    gdp: float
    co2: float
    energy_per_capita: float
    energy_per_gdp: float
    methane: float
    nitrous_oxide: float
    temperature_change_from_ch4: float
    temperature_change_from_co2: float
    temperature_change_from_ghg: float
    temperature_change_from_n2o: float
    total_ghg: float


@app.get("/allData")
async def allData(db: db_dependency):
    return db.query(CountryData).all()


# Req1 no 1
def get_country_data(db: db_dependency,
                     country_name=None,
                     country_iso=None,
                     yearid=None,
                     after_year=None,
                     before_year=None,
                     emissions=None):
    query = db.query(CountryData)
    if country_name:
        query = query.filter(CountryData.country == country_name)
    if country_iso:
        query = query.filter(CountryData.iso_code == country_iso)
    if yearid:
        query = query.filter(CountryData.year == yearid)
    if after_year:
        query = query.filter(CountryData.year > after_year)
    if before_year:
        query = query.filter(CountryData.year < before_year)
    return query.all()  # or .all() depending on the use case


def handle_not_found(item):
    if item is None:
        raise HTTPException(status_code=400, detail='Item not found')
    return item


# Helper function for updating country data
def update_country_data(country_model, country_data):
    for key, value in country_data.dict().items():
        setattr(country_model, key, value)


# Retrieve
@app.get("/country/C_Name/{countryName}/year/{yearid}")
async def country(countryname: str, yearid: int, db: db_dependency):
    todo_model = get_country_data(db, country_name=countryname, yearid=yearid)
    return handle_not_found(todo_model)


# Create
@app.post("/country")
async def create_country(countrydt: CountryDataRequest, db: db_dependency):
    todo_model = CountryData(**countrydt.model_dump())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


# Update by country name
@app.put("/country/{countryName}/{yearid}")
async def update_country_by_name(countryname: str,
                                 yearid: int,
                                 countrydt: CountryDataRequest,
                                 db: db_dependency):
    todo_model = get_country_data(db, country_name=countryname, yearid=yearid)
    handle_not_found(todo_model)
    update_country_data(todo_model, countrydt)
    db.commit()
    db.refresh(todo_model)
    return todo_model


# Delete
@app.delete("/country/{countryName}/{yearid}")
async def delete_country_by_name(countryname: str, yearid: int, db: db_dependency):
    todo_model = get_country_data(db, country_name=countryname, yearid=yearid)
    handle_not_found(todo_model)
    db.delete(todo_model)
    db.commit()
    return {"detail": "Deleted successfully"}


# Retrieve by ISO code
@app.get("/country/C_ISO/{countryISO}/year/{yearid}")
async def country_by_iso(countryiso: str, yearid: int, db: db_dependency):
    todo_model = get_country_data(db, country_iso=countryiso, yearid=yearid)
    return handle_not_found(todo_model)


# Update by ISO code
@app.put("/country/{countryISO}/{yearid}")
async def update_country_by_iso(countryiso: str,
                                yearid: int,
                                countrydt: CountryDataRequest,
                                db: db_dependency):
    todo_model = get_country_data(db, country_iso=countryiso, yearid=yearid)
    handle_not_found(todo_model)
    update_country_data(todo_model, countrydt)
    db.commit()
    db.refresh(todo_model)
    return todo_model


# Delete by ISO code
@app.delete("/country/{countryISO}/{yearid}")
async def delete_country_by_iso(countryiso: str, yearid: int, db: db_dependency):
    todo_model = get_country_data(db, country_iso=countryiso, yearid=yearid)
    handle_not_found(todo_model)
    db.delete(todo_model)
    db.commit()
    return {"detail": "Deleted successfully"}


# Req1 no 2
# retrieve only emissions related data (at minimum everything
# under the co2, methane, nitrous oxide, and total ghg columns) for a given country
@app.get("/country/C_Name/{countryName}/emissions")
async def country(countryname: str, db: db_dependency):
    todo_model = db.query(CountryData.country,
                          CountryData.co2,
                          CountryData.methane,
                          CountryData.nitrous_oxide,
                          CountryData.total_ghg).filter(CountryData.country == countryname).all()
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


# retrieve only emissions related data from a required year onwards (at minimum everything)
@app.get("/country/C_Name/{countryName}/emissions/afterYear/{yearid}")
async def country(countryname: str, yearid: int, db: db_dependency):
    todo_model = (db.query(CountryData.country,
                           CountryData.co2,
                           CountryData.methane,
                           CountryData.nitrous_oxide,
                           CountryData.total_ghg)
                  .filter(CountryData.country == countryname)
                  .filter(CountryData.year > yearid).all())
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


# retrieve only emissions related data by ISO
@app.get("/country/C_ISO/{countryName}/emissions")
async def country(countryiso: str, db: db_dependency):
    todo_model = db.filter(CountryData.country == countryiso).all()
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


# retrieve only emissions related data from a required year onwards by iso
@app.get("/country/C_ISO/{countryName}/emissions/afterYear/{yearid}")
async def country(countryiso: str, yearid: int, db: db_dependency):
    todo_model = (db.query(CountryData.country,
                           CountryData.co2,
                           CountryData.methane,
                           CountryData.nitrous_oxide,
                           CountryData.total_ghg)
                  .filter(CountryData.country == countryiso)
                  .filter(CountryData.year > yearid).all())
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


# Req1 no 3

