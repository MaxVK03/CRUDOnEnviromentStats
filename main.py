from typing import Annotated
from fastapi import FastAPI, Depends
from database import SessionLocal, engine
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



