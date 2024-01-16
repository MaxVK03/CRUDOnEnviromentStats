from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
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
    **Name**: "/continent/temperatureChange"

    **Returns** the temperature change by continent.
    Get the continent's by continent name.
    Can be filtered for a certain year and later.

    **Return Representation:** Defaults to JSON, can also be in CSV.

    **Access**: GET continent/temperatureChange

    **Query parameters**:
    - **continent**: [str] - The continent to find the data for.
    - **year**: Optional[int] - The year of the data (defaults to all data).
    - **inCSV**: Optional[boolean] - Default False - Return in CSV if True else in JSON.
    - **return**: Continent data based on the provided criteria.

    **Errors:**
    - **HTTP Error 400: Bad Request:
      - The user did not input a continent
      - The user did not input a valid continent
    """
    if not continent:
        raise HTTPException(status_code=400, detail="Request needs a continent!")

    if continent.title() not in VALID_CONTINENTS:
        raise HTTPException(status_code=400, detail="Not a valid continent")

    result = continent_service.get_temperature_change_by_continent(
        db=db, continent=continent.title(), yearid=year if year else -1
    )

    if inCSV:
        return StreamingResponse(iter([converter.csvSender(result)]), media_type="text/csv")
    else:
        return result


@router.get("/continent/popChange")
async def get_population_increase(
        continent: str = None, startYear: int = None, endYear: int = None, db=db_dependency
):
    """
    **Name**: "/continent/popChange"

    **Returns** The population change from the start year to the end year.

    **Return Representation:** JS text

    **Access**: GET continent/popChange

    **Query parameters**:
    - **continent**: [str] - The continent to find the data for.
    - **startYear**: [int] - The start year of the search
    - **endYear**: [int] - The end year of the search

    **Errors:**
    - **HTTP Error 400: Bad Request:
      - The user did not input a continent
      - The user input an invalid continent
      - The user did not input a start and end year
    - **HTTP error 404: Not Found:
      - No data found for the given years
    """
    if continent.title() not in VALID_CONTINENTS:
        raise HTTPException(status_code=400, detail="Now a valid continent")

    if not continent:
        raise HTTPException(status_code=400, detail="Request needs a continent")
    else:
        if not startYear or not endYear:
            raise HTTPException(status_code=400, detail="Start and end year are required")
        else:
            populationIncrease = continent_service.get_population_change_continent(db=db,  continent=continent.title(),
                startYear=startYear, endYear=endYear)
            return populationIncrease