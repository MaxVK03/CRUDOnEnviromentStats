from fastapi import APIRouter, Depends, Query
from Database.database_utils import get_db
from services import country_service
from models import CountryDataRequest

router = APIRouter()

db_dependency = Depends(get_db)


@router.get("/allData")
async def get_all_data(db=db_dependency):
    return country_service.get_all_data(db)


@router.get("/country/C_Name/{countryName}/year/{yearid}")
async def get_country_by_name_and_year(countryName: str, yearid: int, db=db_dependency):
    return country_service.get_country_data_by_name_and_year(db, countryName, yearid)


@router.post("/country")
async def create_country(countrydt: CountryDataRequest, db=db_dependency):
    return country_service.create_country_data(db, countrydt)


@router.put("/country/{countryName}")
async def update_country_by_name(countryName: str, countrydt: CountryDataRequest, db=db_dependency):
    return country_service.update_country_data_by_name(db, countryName, countrydt)


@router.delete("/country/{countryName}/{yearid}")
async def delete_country_by_name_and_year(countryName: str, yearid: int, db=db_dependency):
    return country_service.delete_country_data_by_name_and_year(db, countryName, yearid)


@router.get("/country/c_isocode/{countryIsocode}")
async def get_country_by_isocode(countryIsocode: str, db=db_dependency):
    return country_service.get_country_data_by_isocode(db, countryIsocode)


@router.get("/country/c_isocode/{countryIsocode}/year/{yearid}")
async def get_country_by_isocode_and_year(countryIsocode: str, yearid: int, db=db_dependency):
    return country_service.get_country_data_by_isocode_and_year(db, countryIsocode, yearid)


@router.put("/country/c_isocode/{countryIsocode}")
async def update_country_by_isocode(countryIsocode: str, countrydt: CountryDataRequest, db=db_dependency):
    return country_service.update_country_data_by_isocode(db, countryIsocode, countrydt)


@router.delete("/country/c_isocode/{countryIsocode}/{yearid}")
async def delete_country_by_isocode_and_year(countryIsocode: str, yearid: int, db=db_dependency):
    return country_service.delete_country_data_by_isocode_and_year(db, countryIsocode, yearid)


@router.get("/country/c_name/{countryName}/emissions")
async def get_country_emissions_by_name(countryName: str, db=db_dependency):
    return country_service.get_country_emissions_by_name(db, countryName)


@router.get("/country/c_name/{countryName}/emissions/after/{yearid}")
async def get_country_emissions_by_name_after_year(countryName: str, yearid: int, db=db_dependency):
    return country_service.get_country_emissions_by_name_after_year(db, countryName, yearid)


@router.get("/country/c_isocode/{countryIsocode}/emissions")
async def get_country_emissions_by_isocode(countryIsocode: str, db=db_dependency):
    return country_service.get_country_emissions_by_isocode(db, countryIsocode)


@router.get("/country/c_isocode/{countryIsocode}/emissions/after/{yearid}")
async def get_country_emissions_by_isocode_after_year(countryIsocode: str, yearid: int, db=db_dependency):
    return country_service.get_country_emissions_by_isocode_after_year(db, countryIsocode, yearid)


# to retrieve the energy per capita and per GDP data for all countries in a
# given year, if available, sorted per population size and returned in batches
# of M = {10, 20, 50, 100};

@router.get("/country/energyPerCapita/{yearid}")
async def get_energy_per_capita_by_year(yearid: int, db=db_dependency):
    return country_service.get_energy_per_capita_by_year(db, yearid)


@router.get("/countries/climateContribution/{year}")
async def get_climate_contribution_by_year(year: int, n: int, order: str = Query('asc', regex='^(asc|desc)$'), db=Depends(get_db)):
    return await country_service.get_climate_contribution_by_year(db, year, n, order)


# TODO: double check this as I dont back my regex
@router.get("/countries/climateContribution/previousYears")
async def get_climate_contribution_previous_years(m: int, n: int, order: str = Query('asc', regex='^(asc|desc)$'), db=Depends(get_db)):
    return await country_service.get_climate_contribution_previous_years(db, m, n, order)
