from fastapi import APIRouter, Depends
from sqlalchemy.sql.annotation import Annotated

from Database.database import SessionLocal
from Database.database_utils import get_db
from services import continent_service

router = APIRouter()

db_dependency = Annotated[SessionLocal, Depends(get_db)]


@router.get("/continent/temperatureChange")
async def get_temperature_change_by_continent(db=Depends(db_dependency)):
    return continent_service.get_temperature_change_by_continent(db)


@router.get("/test")
async def test():
    return "test"


@router.get("/continent/temperatureChange/after/{yearid}")
async def get_temperature_change_by_continent_after_year(yearid: int, db=Depends(db_dependency)):
    return continent_service.get_temperature_change_by_continent_after_year(db, yearid)


