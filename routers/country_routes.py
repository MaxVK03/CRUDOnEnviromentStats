from fastapi import APIRouter, Depends, Query
from Database.database_utils import get_db
from services import country_service
from models import CountryDataRequest

router = APIRouter()
db_dependency = Depends(get_db)

# TODO: Add errors for not found
# TODO: Add returns for creation
# TODO: Add returns for update


@router.get("/allData")
async def get_all_data(db=db_dependency):
    """
    Get all data from the database

    name: '/allData'

    Access: GET /allData
        - No parameters

    :param db: Takes in the database session, No user input required.

    :return: Returns all data from the database.
    """
    return country_service.get_all_data(db)


@router.get("/country/C_Name/{countryName}/year/{yearid}")
async def get_country_by_name_and_year(countryName: str, yearid: int, db=db_dependency):
    """
    Retrieve country data by country name and year.

    name: '/country/C_Name/{countryName}/year/{yearid}'

    Access: GET /country/C_Name/{countryName}/year/{yearid}
        - countryName: String - The name of the country.
        - yearid: int - The year of the data.

    :param countryName: The name of the country.

    :param yearid: the year of the data.

    :param db: Takes in the database session.

    :return: Returns that country data for that year.
    """
    return country_service.get_country_data_by_name_and_year(db, countryName, yearid)


# TODO: Add returns for creation
@router.post("/country")
async def create_country(countrydt: CountryDataRequest, db=db_dependency):
    """
    Create a new country to add to the database.

    name: '/country'

    Access: POST /country
        - countrydt: CountryData The country data to be added to the database.

    :param countrydt: The country data to be added to the database.

    :param db: The database session.

    :return: Nothing
    """
    return country_service.create_country_data(db, countrydt)


@router.put("/country/{countryName}")
async def update_country_by_name(countryName: str, countrydt: CountryDataRequest, db=db_dependency):
    """
    Update a country by name.

    name: '/country/{countryName}'

    Access: PUT /country/{countryName}
        - countryName: String - The name of the country to be updated.

    :param countryName: The name of the country to be updated.

    :param countrydt: A country data request object containing the data to be updated Allows for
    validation.

    :param db: The database session.

    :return: Nothing
    """
    return country_service.update_country_data_by_name(db, countryName, countrydt)


@router.delete("/country/{countryName}/{yearid}")
async def delete_country_by_name_and_year(countryName: str, yearid: int, db=db_dependency):
    """
    Delete a country by name and year.

    name: '/country/{countryName}/{yearid}'

    Access: DELETE /country/{countryName}/{yearid}
        - countryName: String - The name of the country to be deleted.
        - yearid: int - The year of the data to be deleted.

    :param countryName: The name of the country to be deleted.
    :param yearid: The year of the data to be deleted.
    :param db: The database session.
    return: Nothing
    """
    return country_service.delete_country_data_by_name_and_year(db, countryName, yearid)


@router.get("/country/c_isocode/{countryIsocode}")
async def get_country_by_isocode(countryIsocode: str, db=db_dependency):
    """
    Retrieve country data by country iso code.

    Name: '/country/c_isocode/{countryIsocode}'

    Access: GET /country/c_isocode/{countryIsocode}
        - countryIsocode: String - The iso code of the country.

    :param countryIsocode: The iso code of the country.
    :param db: The database session.
    :return: The data matching the iso code.
    """
    return country_service.get_country_data_by_isocode(db, countryIsocode)


@router.get("/country/c_isocode/{countryIsocode}/year/{yearid}")
async def get_country_by_isocode_and_year(countryIsocode: str, yearid: int, db=db_dependency):
    """
    Retrieve country data by country iso code and year.

    Name: '/country/c_isocode/{countryIsocode}/year/{yearid}'

    Access: GET /country/c_isocode/{countryIsocode}/year/{yearid}
        - countryIsocode: String - The iso code of the country.
        - yearid: int - The year of the data.

    :param countryIsocode: The iso code of the country.
    :param yearid: The year of the data.
    :param db: The database session.
    :return: The data matching the iso code and year.
    """
    return country_service.get_country_data_by_isocode_and_year(db, countryIsocode, yearid)


@router.put("/country/c_isocode/{countryIsocode}")
async def update_country_by_isocode(countryIsocode: str, countrydt: CountryDataRequest, db=db_dependency):
    """
    Update a country by iso code.

    Name: '/country/c_isocode/{countryIsocode}'

    Access: PUT /country/c_isocode/{countryIsocode}
        - countryIsocode: String - The iso code of the country to be updated.

    :param countryIsocode: The iso code of the country to be updated.

    :param countrydt: A country data request object containing the data to be updated Allows for
    validation.

    :param db: The database session.

    :return: Nothing
    """
    return country_service.update_country_data_by_isocode(db, countryIsocode, countrydt)


@router.delete("/country/c_isocode/{countryIsocode}/{yearid}")
async def delete_country_by_isocode_and_year(countryIsocode: str, yearid: int, db=db_dependency):
    """
    Delete a country by iso code and year.

    Name: '/country/c_isocode/{countryIsocode}/{yearid}'

    Access: DELETE /country/c_isocode/{countryIsocode}/{yearid}
        - countryIsocode: String - The iso code of the country to be deleted.
        - yearid: int - The year of the data to be deleted.

    :param countryIsocode: The iso code of the country to be deleted.

    :param yearid: The year of the data to be deleted.

    :param db: The database session.

    :return: Nothing
    """
    return country_service.delete_country_data_by_isocode_and_year(db, countryIsocode, yearid)


@router.get("/country/c_name/{countryName}/emissions")
async def get_country_emissions_by_name(countryName: str, db=db_dependency):
    """
    Retrieve country emissions by country name.

    Name: '/country/c_name/{countryName}/emissions'

    Access: GET /country/c_name/{countryName}/emissions
        - countryName: String - The name of the country.

    :param countryName: The name of the country.

    :param db: The database session.

    :return: The emissions for that country.
    """
    return country_service.get_country_emissions_by_name(db, countryName)


@router.get("/country/c_name/{countryName}/emissions/after/{yearid}")
async def get_country_emissions_by_name_after_year(countryName: str, yearid: int, db=db_dependency):
    """
    Retrieve country emissions by country name and year.

    Name: '/country/c_name/{countryName}/emissions/after/{yearid}'

    Access: GET /country/c_name/{countryName}/emissions/after/{yearid}
        - countryName: String - The name of the country.
        - yearid: int - The beggining year of the data.

    :param countryName: The name of the country.

    :param yearid: The beggining year of the data.

    :param db: The database session.

    :return: Nothing
    """
    return country_service.get_country_emissions_by_name_after_year(db, countryName, yearid)


@router.get("/country/c_isocode/{countryIsocode}/emissions")
async def get_country_emissions_by_isocode(countryIsocode: str, db=db_dependency):
    """
    Retrieve country emissions by country iso code.

    Name: '/country/c_isocode/{countryIsocode}/emissions'

    Access: GET /country/c_isocode/{countryIsocode}/emissions
        - countryIsocode: String - The iso code of the country.

    :param countryIsocode: The iso code of the country.

    :param db: The database session.

    :return: Nothing
    """
    return country_service.get_country_emissions_by_isocode(db, countryIsocode)


@router.get("/country/c_isocode/{countryIsocode}/emissions/after/{yearid}")
async def get_country_emissions_by_isocode_after_year(countryIsocode: str, yearid: int, db=db_dependency):
    """
    Retrieve country emissions by country iso code and year.

    Name: '/country/c_isocode/{countryIsocode}/emissions/after/{yearid}'

    Access: GET /country/c_isocode/{countryIsocode}/emissions/after/{yearid}
        - countryIsocode: String - The iso code of the country.
        - yearid: int - The beggining year of the data.

    :param countryIsocode: The iso code of the country.

    :param yearid: The beggining year of the data.

    :param db: The database session.

    :return: The emissions for that country.
    """
    return country_service.get_country_emissions_by_isocode_after_year(db, countryIsocode, yearid)


@router.get("/country/energyPerCapitaAndGDP/{yearid}")
async def get_energy_per_capita_by_year(yearid: int, db=db_dependency):
    """
    Retrieve energy per capita by year.

    Name: '/country/energyPerCapita/{yearid}'

    Access: GET /country/energyPerCapita/{yearid}
        - yearid: int - The year of the data.

    :param yearid: The year of the data.

    :param db: The database session.

    :return: The energy per capita for that year.
    """
    return country_service.get_country_energy_by_year(db, yearid)


@router.get("/countries/climateContribution/{year}")
async def get_climate_contribution_by_year(year: int, n: int, order: str = Query('asc', regex='^(asc|desc)$'),
                                           db=db_dependency):
    """
    Retrieve climate contribution by year.

    Name: '/countries/climateContribution/{year}'

    Access: GET /countries/climateContribution/{year}
        - year: int - The year of the data.

    :param year: The year of the data.

    :param n: The number of countries to return.

    :param order: The order of the data.

    :param db: The database session.

    :return: The climate contribution for that year.
    """
    return await country_service.get_climate_contribution_by_year(db, year, n, order)


# TODO: double check this as I dont back my regex
@router.get("/countries/climateContribution/previousYears")
async def get_climate_contribution_previous_years(m: int, n: int,
                                                  order: str = Query('asc', regex='^(asc|desc)$'), db=db_dependency):
    """
    Retrieve climate contribution by year.

    Name: '/countries/climateContribution/previousYears'

    Access: GET /countries/climateContribution/previousYears
        - m: int - The year of the data.
        - n: int - The number of countries to return.
        - order: String - The order of the data.

    :param m: The year of the data.

    :param n: The number of countries to return.

    :param order: The order of the data.

    :param db: The database session.

    :return: The climate contribution for that year.
    """
    return await country_service.get_climate_contribution_previous_years(db, m, n, order)
