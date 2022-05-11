from pydantic import BaseModel, Field, HttpUrl
from enum import Enum
from app.db import PyObjectId
from datetime import datetime
from typing import List, Union
from bson import ObjectId


class SatelliteEnum(str, Enum):
    setinel2 = 'setinel2'



class Band(BaseModel):
    name:str
    value: Union[int, float]
    url: HttpUrl

    

class TimeSerie(BaseModel):
    satellite: SatelliteEnum
    datetime: datetime
    bands: List[Band]

    


class Point(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    lat: float
    lon: float
    geometry: str
    timeseries:List[TimeSerie]
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True #required for the _id 
        json_encoders = {ObjectId: str}
    
