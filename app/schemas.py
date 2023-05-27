from pydantic import BaseModel, root_validator
from typing import Optional, List


class LocationBase(BaseModel):
    city: str
    state: str
    zip: int
    latitude: float
    longitude: float


class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True
