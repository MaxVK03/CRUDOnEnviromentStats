from pydantic import BaseModel, Field

from dataManagement.database import Base
from sqlalchemy import Column, Integer, String, Float


# specify the data that will be contained inside the country data class
# Makes use of sqlalchemy for the overall structure of the program.
class CountryData(Base):
    __tablename__ = "CountryData"
    id = Column(Integer, primary_key=True)
    country = Column(String)
    year = Column(Integer)
    iso_code = Column(String)
    population = Column(Integer)
    gdp = Column(Float)
    co2 = Column(Float)
    energy_per_capita = Column(Float)
    energy_per_gdp = Column(Float)
    methane = Column(Float)
    nitrous_oxide = Column(Float)
    share_of_temperature_change_from_ghg = Column(Float)
    temperature_change_from_ch4 = Column(Float)
    temperature_change_from_co2 = Column(Float)
    temperature_change_from_ghg = Column(Float)
    temperature_change_from_n2o = Column(Float)
    total_ghg = Column(Float)


# A country data request. Used for checking when inserting into the DB.
# TODO: add more checking
class CountryDataRequest(BaseModel):
    country: str = Field(min_length=1, max_length=100)
    year: int = Field(min=0, max=9999)
    iso_code: str = Field(min_length=1, max_length=10)
    population: int
    gdp: float
    co2: float
    energy_per_capita: float
    energy_per_gdp: float
    methane: float
    nitrous_oxide: float
    share_of_temperature_change_from_ghg: float
    temperature_change_from_ch4: float
    temperature_change_from_co2: float
    temperature_change_from_ghg: float
    temperature_change_from_n2o: float
    total_ghg: float
