from fastapi import APIRouter, Depends, HTTPException
from dataManagement.database_utils import get_db
from services import continent_service, converter

router = APIRouter()

db_dependency = Depends(get_db)

VALID_CONTINENTS = {
    "Africa",
    "Asia",
    "North America",
    "South America",
    "Oceania",
    "Europe",
    "Antarctica",
}


@router.get("/continent/temperatureChange")
async def get_temperature_change_by_continent(
    continent: str = None, year: int = None, inCSV: bool = False, db=db_dependency
):
    """
    **Returns** the temperature change by continent.
    Can be filtered for a certain year and later.
    Data format defaults to JSON, can be in CSV.

    **Name**: "/continent/temperatureChange"

    **Access**: GET continent/temperatureChange

    **Query parameters**:
    - **continent**: [str] - The continent to find the data for.
    - **year**: Optional[int] - The year of the data (defaults to all data).
    - **inCSV**: Optional[boolean] - Default False - Return in CSV if True else in JSON.
    - **return**: Continent data based on the provided criteria.
    """
    if not continent:
        raise HTTPException(status_code=400, detail="Request needs a continent!")

    if continent.title() not in VALID_CONTINENTS:
        raise HTTPException(status_code=400, detail="Not a valid continent")

    result = continent_service.get_temperature_change_by_continent(
        db=db, continent=continent.title(), yearid=year if year else 0
    )

    if inCSV:
        return converter.csvSender(result)
    else:
        return result
