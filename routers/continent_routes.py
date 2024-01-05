from fastapi import APIRouter, Depends
from dataManagement.database_utils import get_db
from services import continent_service, converter
# TODO: figure out the sample response and input stuff.
router = APIRouter()

db_dependency = Depends(get_db)

VALID_CONTINENTS = {
    "africa",
    "asia",
    "north america",
    "south america",
    "oceania",
    "europe",
    "antarctica",
}


@router.get("/continent/temperatureChange")
async def get_temperature_change_by_continent(
        continent: str = None,
        year: int = None,
        inCSV: str = None,
        db=db_dependency
        ):
    """
    Returns the temperature change by continent.
    Can be filtered for a certain year and later.

    Name: "/continent/temperatureChange"

    Access: GET continent/temperatureChange
    - year: Optional[int] - The year of the data.
    :param continent:
    :param year:
    :param inCSV:
    :param db: Database session
    :return: Temperature change by continent
    """
    if continent.lower() not in VALID_CONTINENTS:
        return "Not a continent!"

    result = None
    if continent and year:
        result = continent_service.get_temperature_change_continent_after_year(
                db=db,
                continent=continent,
                yearid=year,
                inCSV=inCSV)
    elif continent:
        result = continent_service.get_temperature_change_by_continent(
                db=db,
                continent=continent)
    else:
        return 'Invalid parameters.'

    if inCSV is not None:
        return converter.csvSender(result)
    else:
        return result
