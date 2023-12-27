from fastapi import APIRouter, Depends
from dataManagement.database_utils import get_db
from services import continent_service
# TODO: figure out the sample response and input stuff.
router = APIRouter()

db_dependency = Depends(get_db)


@router.get("/continent/temperatureChange")
async def get_temperature_change_by_continent(db=db_dependency, continent: str = None, year: int = None,
                                              timeFrame: str = None):
    """
    Returns the temperature change by continent

    Name: "/continent/temperatureChange"

    Acssess: "continent/temperatureChange"
        - No parameters

    :param year:
    :param timeFrame:
    :param continent:
    :param db: dataManagement session
    :return: Temperature change by continent
    """
    return continent_service.get_temperature_change_by_continent(db)
