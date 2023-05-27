
from pydantic import BaseModel
from typing import Optional, List


class CargoCreate(BaseModel):
    pick_up_zip: int
    delivery_zip: int
    weight: int
    description: str


class CargoEdit(BaseModel):
    weight: int
    description: str


class Cargo(BaseModel):
    id: int
    pick_up_location_id: int
    delivery_location_id: int
    weight: int
    description: str
    nearby_trucks: Optional[List[dict]]

    class Config:
        orm_mode = True
        
