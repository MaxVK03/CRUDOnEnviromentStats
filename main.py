from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from starlette import status

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


@app.get("/country/C_Name/{countryName}/afterYear/{yearid}")
async def country(countryname: str, yearid: int, db: db_dependency):
    todo_model = (db.query(CountryData).filter(CountryData.country == countryname)
                  .filter(CountryData.year > yearid).all())
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


@app.get("/country/C_Name/{countryName}/beforeYear/{yearid}")
async def country(countryname: str, yearid: int, db: db_dependency):
    todo_model = (db.query(CountryData).filter(CountryData.country == countryname)
                  .filter(CountryData.year < yearid).all())
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


@app.get("/country/C_Name/{countryName}/year/{yearid}")
async def country(countryname: str, yearid: int, db: db_dependency):
    todo_model = (db.query(CountryData).filter(CountryData.country == countryname)
                  .filter(CountryData.year == yearid).all())
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


@app.get("/country/C_Name/{countryName}")
async def country(countryname: str, db: db_dependency):
    todo_model = db.query(CountryData).filter(CountryData.country == countryname).all()
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


@app.get("/country/C_ISO/{countryISO}/afterYear/{yearid}")
async def country(countryiso: str, yearid: int, db: db_dependency):
    todo_model = (db.query(CountryData).filter(CountryData.iso_code == countryiso)
                  .filter(CountryData.year > yearid).all())
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model




@app.get("/country/C_ISO/{countryISO}/beforeYear/{yearid}")
async def country(countryiso: str, yearid: int, db: db_dependency):
    todo_model = (db.query(CountryData).filter(CountryData.iso_code == countryiso)
                  .filter(CountryData.year < yearid).all())
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


@app.get("/country/C_ISO/{countryISO}/year/{yearid}")
async def country(countryiso: str, yearid: int, db: db_dependency):
    todo_model = db.query(CountryData).filter(CountryData.iso_code == countryiso).filter(
        CountryData.year == yearid).all()
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


@app.get("/country/C_ISO/{countryISO}")
async def country(countryiso: str, db: db_dependency):
    todo_model = db.query(CountryData).filter(CountryData.iso_code == countryiso).all()
    if todo_model is None or len(todo_model) == 0:
        return HTTPException(status_code=400, detail='Item not found')
    return todo_model


@app.post("/country")
async def create_country(countrydt: CountryDataRequest, db: db_dependency):
    todo_model = CountryData(**countrydt.model_dump())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@app.put("/country/{countryName}/{yearid}")
async def update_country(countryname: str, yearid: int, countrydt: CountryDataRequest, db: db_dependency):
    todo_model = (db.query(CountryData).filter(CountryData.country == countryname)
                  .filter(CountryData.year == yearid).first())
    if todo_model is None:
        return HTTPException(status_code=400, detail='Item not found')
    todo_model.country = countrydt.country
    todo_model.year = countrydt.year
    todo_model.iso_code = countrydt.iso_code
    todo_model.population = countrydt.population
    todo_model.gdp = countrydt.gdp
    todo_model.co2 = countrydt.co2
    todo_model.energy_per_capita = countrydt.energy_per_capita
    todo_model.energy_per_gdp = countrydt.energy_per_gdp
    todo_model.methane = countrydt.methane
    todo_model.nitrous_oxide = countrydt.nitrous_oxide
    todo_model.temperature_change_from_ch4 = countrydt.temperature_change_from_ch4
    todo_model.temperature_change_from_co2 = countrydt.temperature_change_from_co2
    todo_model.temperature_change_from_ghg = countrydt.temperature_change_from_ghg
    todo_model.temperature_change_from_n2o = countrydt.temperature_change_from_n2o
    todo_model.total_ghg = countrydt.total_ghg
    db.commit()
    db.refresh(todo_model)
    return todo_model


@app.delete("/country/{countryName}/{yearid}")
async def delete_country(countryname: str, yearid: int, db: db_dependency):
    todo_model = (db.query(CountryData).filter(CountryData.country == countryname)
                  .filter(CountryData.year == yearid).first())
    if todo_model is None:
        return HTTPException(status_code=400, detail='Item not found')
    db.delete(todo_model)
    db.commit()
    return todo_model

