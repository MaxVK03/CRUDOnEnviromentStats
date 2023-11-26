from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal
from database import engine
from models import CountryData
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[SessionLocal, Depends(get_db)]


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
