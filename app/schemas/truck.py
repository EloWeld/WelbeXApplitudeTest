
from pydantic import BaseModel
from typing import Optional, List

from app.schemas import Location



class TruckBase(BaseModel):
    unique_number: str
    current_location_id: int
    carrying_capacity: int


class Truck(TruckBase):
    id: int
    current_location: Location

    class Config:
        orm_mode = True



Truck.update_forward_refs()