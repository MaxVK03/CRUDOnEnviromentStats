from fastapi import APIRouter, Depends, HTTPException
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
        continent: str = "",
        year: str = "",
        inCSV: str = "",
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
    if year and not year.isdigit():
        raise HTTPException(status_code=400, detail='Not a valid year')
    if continent.lower() not in VALID_CONTINENTS:
        raise HTTPException(status_code=400, detail='Not a valid continent')

    if continent and year:
        result = continent_service.get_temperature_change_continent_after_year(
                db=db,
                continent=continent,
                yearid=int(year),
                inCSV=inCSV)
    elif continent:
        result = continent_service.get_temperature_change_by_continent(
                db=db,
                continent=continent)
    else:
        raise HTTPException(status_code=400, detail='Bad request')

    if inCSV:
        return converter.csvSender(result)
    else:
        return continent_service.handle_not_found(result, "Get");
