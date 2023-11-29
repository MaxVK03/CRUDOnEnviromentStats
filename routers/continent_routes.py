from fastapi import APIRouter, Depends
from sqlalchemy.sql.annotation import Annotated

from Database.database import SessionLocal
from Database.database_utils import get_db
from services import continent_service

router = APIRouter()

db_dependency = Annotated[SessionLocal, Depends(get_db)]


@router.get("/continent/temperatureChange")
async def get_temperature_change_by_continent(db=Depends(db_dependency)):
    """
    Returns the temperature change by continent

    Name: "/continent/temperatureChange"

    Acssess: "continent/temperatureChange"
        - No parameters

    :param db: Database session
    :return: Temperature change by continent
    """
    return continent_service.get_temperature_change_by_continent(db)


@router.get("/test")
async def test():
    return "test"


@router.get("/continent/temperatureChange/after/{yearid}")
async def get_temperature_change_by_continent_after_year(yearid: int, db=Depends(db_dependency)):
    """
    Returns the temperature change by continent after a given year

    Name: "/continent/temperatureChange/after/{yearid}"

    Acssess: "continent/temperatureChange/after/{yearid}"
        - yearid : int - The year after which the temperature change is calculated

    :param yearid: The year after which the temperature change is calculated
    :param db: Database session
    :return: Temperature change by continent after a given year
    """
    return continent_service.get_temperature_change_by_continent_after_year(db, yearid)
