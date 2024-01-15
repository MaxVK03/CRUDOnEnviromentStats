from typing import Optional

from pydantic import BaseModel, Field

from dataManagement.database import Base
from sqlalchemy import Column, Integer, String, Float


# specify the data that will be contained inside the country data class
# Makes use of sqlalchemy for the overall structure of the program.
class CountryData(Base):
    __tablename__ = "CountryData"
    id = Column(Integer, primary_key=True)
    country = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    iso_code = Column(String, nullable=True)
    population = Column(Integer, nullable=True)
    gdp = Column(Float, nullable=True)
    co2 = Column(Float, nullable=True)
    energy_per_capita = Column(Float, nullable=True)
    energy_per_gdp = Column(Float, nullable=True)
    methane = Column(Float, nullable=True)
    nitrous_oxide = Column(Float, nullable=True)
    share_of_temperature_change_from_ghg = Column(Float, nullable=True)
    temperature_change_from_ch4 = Column(Float, nullable=True)
    temperature_change_from_co2 = Column(Float, nullable=True)
    temperature_change_from_ghg = Column(Float, nullable=True)
    temperature_change_from_n2o = Column(Float, nullable=True)
    total_ghg = Column(Float, nullable=True)


# A country data request. Used for checking when inserting into the DB.
# TODO: add more checking
class CountryDataRequest(BaseModel):
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, min=0, max=9999)
    iso_code: Optional[str] = Field(None, min_length=1, max_length=10)
    population: Optional[int] = None
    gdp: Optional[float] = None
    co2: Optional[float] = None
    energy_per_capita: Optional[float] = None
    energy_per_gdp: Optional[float] = None
    methane: Optional[float] = None
    nitrous_oxide: Optional[float] = None
    share_of_temperature_change_from_ghg: Optional[float] = None
    temperature_change_from_ch4: Optional[float] = None
    temperature_change_from_co2: Optional[float] = None
    temperature_change_from_ghg: Optional[float] = None
    temperature_change_from_n2o: Optional[float] = None
    total_ghg: Optional[float] = None