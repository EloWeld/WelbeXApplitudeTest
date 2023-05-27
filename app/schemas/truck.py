
from pydantic import BaseModel
from typing import Optional, List

from app.schemas import Location


class Truck(BaseModel):
    id: int
    unique_number: str
    current_location_id: int
    carrying_capacity: int
    current_location: Location

    class Config:
        orm_mode = True


class EditTruck(BaseModel):
    new_zip: int

Truck.update_forward_refs()