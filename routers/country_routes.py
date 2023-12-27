from fastapi import APIRouter, Depends
from dataManagement.database_utils import get_db
from services import country_service, converter
from dataManagement.models import CountryDataRequest

router = APIRouter()
db_dependency = Depends(get_db)


@router.get("/country/data")
async def get_country_data(countryName: str = None, countryIsocode: str = None,
                           yearid: int = None, timeFrame: str = None, inCSV: str = None, db=db_dependency):
    """
    Retrieve country data based on various criteria.
    Access: GET /country/data
    - countryName: Optional[str] - The name of the country.
    - countryIsocode: Optional[str] - The iso code of the country.
    - yearid: Optional[int] - The year of the data.
    :param inCSV:
    :param timeFrame:
    :param yearid:
    :param countryIsocode:
    :param countryName:
    :param db: The database session.
    :return: Country data based on the provided criteria.


    """

    result = None
    if countryName and yearid and timeFrame:
        result = country_service.get_country_data_with_timeFrame(db=db, countryName=countryName, iso=None,
                                                                 yearid=yearid,
                                                                 timeFrame=timeFrame)
    elif countryIsocode and yearid and timeFrame:
        result = country_service.get_country_data_with_timeFrame(db=db, countryName=None, iso=countryIsocode,
                                                                 yearid=yearid,
                                                                 timeFrame=timeFrame)
    elif countryName:
        result = country_service.get_country_data_without_timeFrame(db=db, countryName=countryName, iso=None,
                                                                    yearid=None,
                                                                    timeFrame=None)
    elif countryIsocode:
        result = country_service.get_country_data_without_timeFrame(db=db, countryName=None, iso=countryIsocode,
                                                                    yearid=None, timeFrame=None)
    else:
        return 'Invalid parameters.'

    if inCSV is not None:
        return converter.csvSender(result)
    else:
        return result


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
        return country_service.delete_country_data_by_isocode_and_year(db, countryIsocode, yearid)
    else:
        return 'Invalid parameters.'


@router.get("/country/emissions")
async def get_country_emissions(countryName: str = None, countryIsocode: str = None,
                                yearid: int = None, timeFrame: str = None, inCSV:str = None, db=db_dependency):
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

    result = None
    if countryName and yearid and timeFrame:
         result = country_service.get_country_emission_with_timeframe(db=db, countryName=countryName, iso=None,
                                                                   yearid=yearid, timeFrame=timeFrame)
    elif countryIsocode and yearid and timeFrame:
        result = country_service.get_country_emission_with_timeframe(db=db, countryName=None, iso=countryIsocode,
                                                                   yearid=yearid, timeFrame=timeFrame)
    elif countryName:
        result = country_service.get_country_emissions_by_name(db=db, countryName=countryName)

    # Convert to CSV if requested:
    if inCSV is not None:
        return converter.csvSender(result)
    else:
        return result


# energy per capita and gdp
@router.get("/country/energy/")
def energy(noCountries: int = None,
           yearid: int = None, page: int = None, inCSV:str = None, db=db_dependency):
    result = None
    if noCountries and yearid:
        result = country_service.getEnergy(db=db, page=page, noCountries=noCountries, year=yearid)

    if inCSV is not None:
        return converter.csvSender(result)
    else:
        return result


@router.get("/country/climCont/")
def climCont(noCountries: int = None,
             yearid: int = None, db=db_dependency, sort: str = None, inCSV:str = None):
    result = None
    if noCountries and yearid and sort:
        result = country_service.getClimCont(db=db, noCountries=noCountries, year=yearid, sort=sort)

    if inCSV is not None:
        return converter.csvSender(result)
    else:
        return result
