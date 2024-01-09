from fastapi import APIRouter, Depends, HTTPException
from dataManagement.database_utils import get_db
from services import country_service, converter
from dataManagement.models import CountryDataRequest

router = APIRouter()
db_dependency = Depends(get_db)


@router.get("/country/data")
async def get_country_data(
    countryName: str = None,
    countryIsocode: str = None,
    yearid: int = None,
    timeFrame: str = "after",
    inCSV: bool = False,
    db=db_dependency,
):
    """
    **Returns* country data based on various criteria.
    Country can be queried by name or ISO-code (will take name over ISO code if both are provided)
    A time-frame for the data can be specified.
    Data format defaults to JSON, can be in CSV.

    **Name*: "/country/data"

    **Access*: GET /country/data

    **Query parameters**:
    - **countryName**: Optional[str] - The name of the country.
    - **countryIsocode**: Optional[str] - The iso code of the country.
    - **yearid**: Optional[int] - The year of the data.
    - **timeframe**: Optional[string] - The time frame (defaults to "after")
    - **inCSV**: Optional[boolean] - Default False - Return in CSV if True else in JSON.
    - **return**: Country data based on the provided criteria.
    """
    if countryName or countryIsocode:
        if yearid:
            result = country_service.get_country_data_with_timeFrame(
                db, countryName, countryIsocode, yearid, timeFrame
            )
        else:
            result = country_service.get_country_data_without_timeFrame(
                db, countryName, countryIsocode
            )
    else:
        raise HTTPException(status_code=400, detail="Invalid parameters")

    if inCSV:
        return converter.csvSender(result)
    else:
        return country_service.handle_not_found(result, "get")


@router.post("/country")
async def create_country(countrydt: CountryDataRequest, db=db_dependency):
    """
    Create a new country to add to the database.
    Access: POST /country
    :param countrydt: The country data to be added.
    :param db: The database session.
    :return: Result of the creation operation.
    """
    return country_service.create_country_data(db, countrydt)


@router.put("/country")
async def update_country(
    countrydt: CountryDataRequest,
    db=db_dependency,
    countryName: str = None,
    countryIsocode: str = None,
):
    """
    Update country data by name or iso code.
    Access: PUT /country
    :param countryName: Optional[str] - The name of the country.
    :param countryIsocode: Optional[str] - The iso code of the country.
    :param countrydt: A country data request object containing the data to be updated.
    :param db: The database session.
    :return: Result of the update operation.
    """
    if countryName:
        return country_service.update_country_data_by_name(db, countryName, countrydt)
    elif countryIsocode:
        return country_service.update_country_data_by_isocode(
            db, countryIsocode, countrydt
        )


@router.delete("/country")
async def delete_country(
    countryName: str = None,
    countryIsocode: str = None,
    yearid: int = None,
    timeFrame: str = "equal",
    db=db_dependency,
):
    """
    Delete a country by name, iso code, and/or year.
    Access: DELETE /country
    :param timeFrame:
    :param countryName: Optional[str] - The name of the country.
    :param countryIsocode: Optional[str] - The iso code of the country.
    :param yearid: Optional[int] - The year of the data (defaults to "equal").
    :param db: The database session.
    :return: Result of the deletion operation.
    """
    if countryName and yearid and timeFrame:
        return country_service.delete_country_data_by_name_and_year_and_timeFrame(
            db, countryName, yearid, timeFrame
        )
    elif countryIsocode and yearid and timeFrame:
        return country_service.delete_country_data_by_isocode_and_year(
            db, countryIsocode, yearid
        )
    else:
        raise HTTPException(status_code=404, detail="Invalid Parameters")


@router.get("/country/emissions")
async def get_country_emissions(
    countryName: str = None,
    countryIsocode: str = None,
    yearid: int = None,
    timeFrame: str = "after",
    inCSV: bool = False,
    db=db_dependency,
):
    """
    Retrieve country emissions data based on various criteria.
    Access: GET /country/emissions
    :param inCSV:
    :param timeFrame:
    :param countryName: Optional[str] - The name of the country.
    :param countryIsocode: Optional[str] - The iso code of the country.
    :param yearid: Optional[int] - The year of the data.
    :param db: The database session.
    :return: Emissions data based on the provided criteria.
    """
    print(f"Time: {timeFrame}")

    if countryName or countryIsocode:
        if yearid:
            result = country_service.get_country_emission_with_timeframe(
                db, countryName, countryIsocode, yearid, timeFrame
            )
        else:
            result = country_service.get_country_emissions_by_name(
                db, countryName, countryIsocode
            )
    else:
        raise HTTPException(status_code=404, detail="Invalid parameters")

    # Convert to CSV if requested:
    if inCSV:
        return converter.csvSender(result)
    else:
        return result


# energy per capita and gdp
@router.get("/country/energy/")
def energy(
    numCountries: int = None,
    yearid: int = None,
    page: int = None,
    inCSV: bool = False,
    db=db_dependency,
):
    print(numCountries, yearid, page)
    result = None
    if numCountries and yearid:
        result = country_service.getEnergy(
            db=db, page=page, noCountries=numCountries, year=yearid
        )

    if inCSV:
        return converter.csvSender(result)
    else:
        return country_service.handle_not_found(result, "GET")


@router.get("/country/climCont/")
def climCont(
    noCountries: int = None,
    yearid: int = None,
    pastYears: int = None,
    db=db_dependency,
    sort: str = "top",
    inCSV: bool = False,
):
    result = None
    if noCountries and sort:
        if yearid:
            result = country_service.getClimContYear(
                db=db, noCountries=noCountries, year=yearid, sort=sort
            )
        elif pastYears:
            result = country_service.getClimContPast(
                db=db, noCountries=noCountries, pastYears=pastYears, sort=sort
            )
    if inCSV:
        return converter.csvSender(result)
    else:
        return result
