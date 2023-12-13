from http.client import HTTPException

from fastapi import APIRouter, Depends
from Database.database_utils import get_db
from services import country_service
from models import CountryDataRequest

router = APIRouter()
db_dependency = Depends(get_db)


@router.get("/country/data")
async def get_country_data(countryName: str = None, countryIsocode: str = None,
                           yearid: int = None, timeFrame: str = None, db=db_dependency):
    """
    Retrieve country data based on various criteria.
    Access: GET /country/data
    - countryName: Optional[str] - The name of the country.
    - countryIsocode: Optional[str] - The iso code of the country.
    - yearid: Optional[int] - The year of the data.
    :param timeFrame:
    :param yearid:
    :param countryIsocode:
    :param countryName:
    :param db: The database session.
    :return: Country data based on the provided criteria.

    """
    if countryName and yearid and timeFrame:
        return country_service.get_country_data_with_timeFrame(db=db, countryName=countryName, iso=None, yearid=yearid,
                                                               timeFrame=timeFrame)
    elif countryIsocode and yearid and timeFrame:
        return country_service.get_country_data_with_timeFrame(db=db, countryName=None, iso=countryIsocode,
                                                               yearid=yearid,
                                                               timeFrame=timeFrame)
    elif countryName:
        return country_service.get_country_data_without_timeFrame(db=db, countryName=countryName, iso=None, yearid=None,
                                                               timeFrame=None)
    else:
        return 'Invalid parameters.'


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
async def update_country(countrydt: CountryDataRequest, db=db_dependency, countryName: str = None,
                         countryIsocode: str = None):
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
        return country_service.update_country_data_by_isocode(db, countryIsocode, countrydt)


@router.delete("/country")
async def delete_country(countryName: str = None, countryIsocode: str = None,
                         yearid: int = None, timeFrame: str = None, db=db_dependency):
    """
    Delete a country by name, iso code, and/or year.
    Access: DELETE /country
    :param timeFrame:
    :param countryName: Optional[str] - The name of the country.
    :param countryIsocode: Optional[str] - The iso code of the country.
    :param yearid: Optional[int] - The year of the data.
    :param db: The database session.
    :return: Result of the deletion operation.
    """
    if countryName and yearid and timeFrame:
        return country_service.delete_country_data_by_name_and_year_and_timeFrame(db, countryName, yearid, timeFrame)
    elif countryIsocode and yearid and timeFrame:
        return country_service.get(db, countryIsocode, yearid, timeFrame)
    else:
        return 'Invalid parameters.'


@router.get("/country/emissions")
async def get_country_emissions(countryName: str = None, countryIsocode: str = None,
                                yearid: int = None, timeFrame: str = None, db=db_dependency):
    """
    Retrieve country emissions data based on various criteria.
    Access: GET /country/emissions
    :param timeFrame:
    :param countryName: Optional[str] - The name of the country.
    :param countryIsocode: Optional[str] - The iso code of the country.
    :param yearid: Optional[int] - The year of the data.
    :param db: The database session.
    :return: Emissions data based on the provided criteria.
    """
    if countryName and yearid and timeFrame:
        return country_service.get_country_emissions(db=db, countryName=countryName, iso=None,
                                                     yearid=yearid, timeFrame=timeFrame)
