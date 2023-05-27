from typing import Any, Union
from .cargo import *
from .location import *
from .truck import *


class Truck(BaseModel):
    id: int
    unique_number: str
    carrying_capacity: int
    current_location_id: int
    current_location: Optional[Union[dict, None]]


class EditTruck(BaseModel):
    new_zip: int