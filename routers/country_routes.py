from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
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
    **Returns** country data based on various criteria.

    Country can be queried by name or ISO-code (will take name over ISO code if both are provided)
    A time-frame for the data can be specified.
    Data format defaults to JSON, can be in CSV.

    **Name**: "/country/data"

    **Access**: GET /country/data

    **Query parameters**:
    - **countryName**: Optional[str] - The name of the country.
    - **countryIsocode**: Optional[str] - The iso code of the country.
    - **yearid**: Optional[int] - The year of the data.
    - **timeframe**: Optional[string] - The time frame (defaults to "after")
    - **inCSV**: Optional[boolean] - Default False - Return in CSV if True else in JSON.

    **Errors**:
    - HTTP Error: 400
        - Missing country name or ISO code.
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
        raise HTTPException(status_code=400, detail="Missing country name or ISO code")
    if inCSV:
        return StreamingResponse(iter([converter.csvSender(result)]), media_type="text/csv")
    else:
        return country_service.handle_not_found(result, "get")


@router.post("/country")
async def create_country(countrydt: CountryDataRequest, db=db_dependency):
    """
        **Name**: "/country"

        **Returns** A newly created country.
        Creates a new entry in the database with a country.
        The data of the country is specified by the user.

        **Return Representation** Defaults to JSON.

        **Access**: POST /country

        **Query parameters**:
        - country[str] - The name of the country
        - year[int] - The year of the data
        - iso_code[str] - ISO Code of the country
        - population[int] - Population of the country
        - gdp[float] - GDP of the country
        - co2[float] - CO2 emissions of the country
        - energy_per_capita[float] - energy per capita of the country
        - energy_per_gdp[float] - energy per GDP of the country
        - methane[float] - Methane emissions by the country
        - nitrous_oxide[float] - Nitrous oxide emissions of the country
        - share_of_temperature_change_from_ghg[float] - Share of temperature change from green house gasses of the country
        - temperature_change_from_ch4[float] - Temperature change from methane emissions of the country
        - temperature_change_from_co2[float] - Temperature change of carbon dioxide emissions of the country.
        - temperature_change_from_ghg[float] - Temperature change from green house gases of the country
        - temperature_change_from_n2o[float] - Temperature change by nitrious oxide emissions of the country.
        - total_ghg[float] - Total green house gas emissions by the country
    """
    #TODO: Add validation for creating a country and add the appropriate error here.
    return country_service.create_country_data(db, countrydt)


@router.put("/country/{countryIsocode}/{yearid}")
async def update_country(
    yearid: int,
    countryIsocode: str,
    countrydt: CountryDataRequest,
    db=db_dependency,
    countryName: str = None,
):
    """
        **Name**: "/country"

        **Returns** Updates a country from the database specified by the user.
        User specifies which country they want to update either through country name or country ISO code.

        **Return Representation** Defaults to JSON.

        **Access**: PUT /country

        **Query parameters**:
        - country[str] - The name of the country
        - year[int] - The year of the data
        - iso_code[str] - ISO Code of the country
        - population[int] - Population of the country
        - gdp[float] - GDP of the country
        - co2[float] - CO2 emissions of the country
        - energy_per_capita[float] - energy per capita of the country
        - energy_per_gdp[float] - energy per GDP of the country
        - methane[float] - Methane emissions by the country
        - nitrous_oxide[float] - Nitrous oxide emissions of the country
        - share_of_temperature_change_from_ghg[float] - Share of temperature change from green house gasses of the country
        - temperature_change_from_ch4[float] - Temperature change from methane emissions of the country
        - temperature_change_from_co2[float] - Temperature change of carbon dioxide emissions of the country.
        - temperature_change_from_ghg[float] - Temperature change from green house gases of the country
        - temperature_change_from_n2o[float] - Temperature change by nitrious oxide emissions of the country.
        - total_ghg[float] - Total green house gas emissions by the country

        **Errors**:
        - **HTTP Error 400: Bad Request:
          - User did not input either the country name or the ISO code.
          - User did not input the relevant year
        """
    if countryName:
        if yearid:
            return country_service.update_country(db, countryName, countryIsocode, yearid, countrydt)
        else:
            raise HTTPException(status_code=400, detail="Must input the year that needs to be updated")
    elif countryIsocode:
        if yearid:
            return country_service.update_country(
                db, countryName, countryIsocode, yearid, countrydt)
        else:
            raise HTTPException(status_code=400, detail="Must input the year that needs to be updated")
    else:
        raise  HTTPException(status_code=400, detail="Must input either country name or ISO code")


@router.delete("/country")
async def delete_country(
    countryName: str = None,
    countryIsocode: str = None,
    yearid: int = None,
    db=db_dependency,
):
    """
        **Name**: "/country"

        **Returns** Deletes a country from the database specified by the user.

        **Return Representation** Defaults to JSON, can also return CSV.

        **Access**: DELETE /country

        **Query parameters**:
        - **Country Name**: [str] - The name of the country to find the data for.
        - **Country ISO Code**[str] - The ISO code of the country to find the data for.
        - **year**: Optional[int] - The year of the data (no year, defaults to all data).
        - **Time frame**: Optional[str] - Before or after the given year, (defaults to equal to that year)

        **Errors**:
        - **HTTP Error 400: Bad Request:
          - User gave an invalid combination of input parameters.
    """
    if countryName:
        if yearid:
            return country_service.delete_country_data_by_name_and_year(db, countryName, yearid)
        else:
            raise HTTPException(status_code=400, detail="Must enter a year")
    elif countryIsocode:
        if yearid:
            return country_service.delete_country_data_by_isocode_and_year(
                db, countryIsocode, yearid
            )
        else:
            raise HTTPException(status_code=400, detail="Must enter a year")
    else:
        raise HTTPException(status_code=400, detail="Invalid combination of parameters")


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
        **Name**: "/country/emissions"

        **Returns** The emissions per country in the years specified.
        Choose the country by name or ISO code.
        Can be filtered for a certain year and later.

        **Return Representation** Defaults to JSON, can also return CSV.

        **Access**: GET /country/emissions

        **Query parameters**:
        - **Country Name**: [str] - The name of the country to find the data for.
        - **Country ISO Code**:[str] - The ISO code of the country to find the data for.
        - **year**: Optional[int] - The year of the data (defaults to all data).
        - **inCSV**: Optional[boolean] - Default False - Return in CSV if True else in JSON.

        **Errors**:
        - **HTTP Error 404: Not Found:
          - User did not input either a country name or a country ISO code.
    """
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
        raise HTTPException(status_code=404, detail="Input a country name or country ISO code")

    # Convert to CSV if requested:
    if inCSV:
        return StreamingResponse(iter([converter.csvSender(result)]), media_type="text/csv")
    else:
        return country_service.handle_not_found(result, "get")


# energy per capita and gdp
@router.get("/country/energy/")
def energy(
    numCountries: int = None,
    yearid: int = None,
    page: int = None,
    inCSV: bool = False,
    db=db_dependency,
):
    """
        **Name**: "/country/energy"

        **Returns** The emissions per country ni the specific years specified.
        Choose the country by name or ISO code.
        Can be filtered for a certain year and later.

        **Return Representation** Defaults to JSON, can also return CSV.

        **Access**: GET /country/emissions

        **Query parameters**:
        - **numCountries**: [int] - Number of countries to be displayed
        - **year**: [int] - The year of the data (defaults to all data).
        - **page** Optional[int] - which page of the batch we want {10,20,50,100}
        - **inCSV**: Optional[boolean] - Default False - Return in CSV if True else in JSON.

        **Errors**:
        - **HTTP Error 400: Bad Request:
          - User did not input the number of countries and the year for the search
    """
    if numCountries and yearid:
        result = country_service.getEnergy(
            db=db, page=page, noCountries=numCountries, year=yearid
        )
    else:
        raise HTTPException(status_code=400, detail="Must enter number of countries and relevant year")

    if inCSV:
        return StreamingResponse(iter([converter.csvSender(result)]), media_type="text/csv")
    else:
        return result


@router.get("/country/climCont/")
def climCont(
    noCountries: int = None,
    yearid: int = None,
    pastYears: int = None,
    db=db_dependency,
    sort: str = "top",
    inCSV: bool = False,
):
    """
        **Name**: "/country/climCont"

        **Returns** The top or Bottom N countries based on their contribution to climate change.

        **Return Representation** Defaults to JSON, can also return CSV.

        **Access**: GET /country/climCont

        **Query parameters**:
        - **noCountries**: [str] - The number of countries to return.
        - **year**: [int] - The year of the data (defaults to all data).
        - **pastYears**: Optional[int] - amount of past years for data to include.
        - **inCSV**: Optional[boolean] - Default False - Return in CSV if True else in JSON.
        - **sort**: Optional[str] - Default top - specifies if we return top or bottom countries for criteria.

        **Errors**:
        - **HTTP Error 400: Bad Request:
          - Number of countries was not input
          - The specific year or amount of past year was not input
    """
    if noCountries:
        if yearid:
            result = country_service.getClimContYear(
                db=db, noCountries=noCountries, year=yearid, sort=sort
            )
        elif pastYears:
            result = country_service.getClimContPast(
                db=db, noCountries=noCountries, pastYears=pastYears, sort=sort
            )
        else:
            raise HTTPException(status_code=400, detail="Must input either year or amount of past years for search")
    else:
        raise HTTPException(status_code=400, detail="Missing the number of countries")
    if inCSV:
        return StreamingResponse(iter([converter.csvSender(result)]), media_type="text/csv")
    else:
        return result


@router.get("/country/addData/")
def capital(
        countryName: str = None,
):
    """
    **Name**: "/country/addData"

    **Returns** Additional data on the specified country. Such as: capital, currency, official languages etc....

    **Return Representation** JSON

    **Access**: GET /country/addData

    **Query parameters**:
    - **countryName**: [str] - The name of the country to find the data for.

    **Errors**:
    - **HTTP Error 400: Bad Request:
      - User did not input a country name so request cannot be made.
    - **HTTP Error 404: Not found:
      - The usr input a country Name that is not in the database.
    """

    if countryName:
        result = country_service.get_Country_Add_Data(countryName)
        return result
    else:
        raise HTTPException(status_code=400, detail="Must input a country Name")


@router.get("/country/list")
async def get_country_list(db: db_dependency = Depends(get_db)):
    """
    **Name**: "/country/list"

    **Returns** All countries in the database

    **Return Representation** JSON

    **Access**: GET /country/list

    **Errors**:
    - **HTTP Error 404: Not found:
      - Unable to fetch the country data at this time.
    """
    countries = country_service.get_country_list(db)
    if countries:
        return [{"name": country[0], "iso": country[1]} for country in countries]
    else:
        raise HTTPException(status_code=404, detail="Could not fetch country data at this time.")
