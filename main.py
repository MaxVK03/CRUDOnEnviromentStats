from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
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


class CountryDataRequest(BaseModel):
    id: int
    country: str
    year: int
    iso_code: str
    population: int
    gdp: float
    co2: float
    co2_per_capita: float
    co2_per_gdp: float
    co2_per_unit_energy: float
    coal_co2: float
    coal_co2_per_capita: float
    consumption_co2: float
    consumption_co2_per_capita: float
    consumption_co2_per_gdp: float
    cumulative_co2: float
    cumulative_coal_co2: float
    energy_per_capita: float
    energy_per_gdp: float
    flaring_co2: float
    flaring_co2_per_capita: float
    gas_co2: float
    gas_co2_per_capita: float
    ghg_excluding_lucf_per_capita: float
    ghg_per_capita: float
    land_use_change_co2: float
    land_use_change_co2_per_capita: float
    methane: float
    methane_per_capita: float
    nitrous_oxide: float
    nitrous_oxide_per_capita: float
    primary_energy_consumption: float
    share_of_temperature_change_from_ghg: float
    total_ghg: float
    total_ghg_excluding_lucf: float
    trade_co2: float
    trade_co2_share: float


@app.get("/allData")
async def allData(db: db_dependency):
    return db.query(CountryData).all()


@app.get("/country/CName/{countryid}/afterYear/{yearid}")
async def country(countryid: str, yearid: int, db: db_dependency):
    todo_model = db.query(CountryData).filter(CountryData.country == countryid).filter(CountryData.year > yearid).all()
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


@app.get("/country/CName/{countryid}/beforeYear/{yearid}")
async def country(countryid: str, yearid: int, db: db_dependency):
    todo_model = db.query(CountryData).filter(CountryData.country == countryid).filter(CountryData.year < yearid).all()
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


@app.get("/country/CName/{countryid}/year/{yearid}")
async def country(countryid: str, yearid: int, db: db_dependency):
    todo_model = db.query(CountryData).filter(CountryData.country == countryid).filter(CountryData.year == yearid).all()
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


@app.get("/country/CName/{countryid}")
async def country(countryid: str, db: db_dependency):
    todo_model = db.query(CountryData).filter(CountryData.country == countryid).all()
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


@app.get("/country/CIso/{countryid}/afterYear/{yearid}")
async def country(countryid: str, yearid: int, db: db_dependency):
    todo_model = db.query(CountryData).filter(CountryData.iso_code == countryid).filter(CountryData.year > yearid).all()
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


@app.get("/country/CIso/{countryid}/beforeYear/{yearid}")
async def country(countryid: str, yearid: int, db: db_dependency):
    todo_model = db.query(CountryData).filter(CountryData.iso_code == countryid).filter(CountryData.year < yearid).all()
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


@app.get("/country/CIso/{countryid}/year/{yearid}")
async def country(countryid: str, yearid: int, db: db_dependency):
    todo_model = db.query(CountryData).filter(CountryData.iso_code == countryid).filter(
        CountryData.year == yearid).all()
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


@app.get("/country/CIso/{countryid}")
async def country(countryid: str, db: db_dependency):
    todo_model = db.query(CountryData).filter(CountryData.iso_code == countryid).all()
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model
