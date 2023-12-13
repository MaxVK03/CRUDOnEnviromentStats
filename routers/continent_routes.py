from fastapi import APIRouter, Depends
from Database.database_utils import get_db
from services import continent_service

router = APIRouter()

db_dependency = Depends(get_db)


@router.get("/continent/temperatureChange")
async def get_temperature_change_by_continent(db=db_dependency):
    """
    Returns the temperature change by continent

    Name: "/continent/temperatureChange"

    Acssess: "continent/temperatureChange"
        - No parameters

    :param db: Database session
    :return: Temperature change by continent
    """
    return continent_service.get_temperature_change_by_continent(db)


@router.get("/continent/temperatureChange/after/{yearid}")
async def get_temperature_change_by_continent_after_year(yearid: int, db=db_dependency):
    """
    Returns the temperature change by continent after a given year

    Name: "/continent/temperatureChange/after/{yearid}"

    Access: "continent/temperatureChange/after/{yearid}"
        - yearid : int - The year after which the temperature change is calculated

    :param yearid: The year after which the temperature change is calculated
    :param db: Database session
    :return: Temperature change by continent after a given year
    """
    return continent_service.get_temperature_change_by_continent_or_after_year(db, yearid)
