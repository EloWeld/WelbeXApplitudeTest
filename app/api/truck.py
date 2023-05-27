from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..db import get_db

router = APIRouter()

@router.put("/truck/{truck_id}")
def update_truck(truck_id: int, truck: schemas.EditTruck, db: Session = Depends(get_db)):
    db_truck = db.query(models.Truck).get(truck_id)
    if db_truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")
    
    location = db.query(models.Location).filter(models.Location.id == truck.new_zip).first()
    if location is None:
        raise HTTPException(status_code=400, detail="Invalid zip code")
    
    db_truck.current_location_id = location.id
    db.commit()
    db.refresh(db_truck)
    
    return db_truck
