from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models
from ..db import get_db
from ..utils import calculate_distance
from geopy import Point
from sqlalchemy.exc import NoResultFound

router = APIRouter()


@router.post("/cargo/", response_model=schemas.Cargo)
def create_cargo(cargo: schemas.CargoCreate, db: Session = Depends(get_db)):
    pick_up_location = db.query(models.Location).filter(
        models.Location.zip == cargo.pick_up_zip).first()
    delivery_location = db.query(models.Location).filter(
        models.Location.zip == cargo.delivery_zip).first()

    if not pick_up_location:
        raise HTTPException(status_code=400, detail="Invalid pick up zip")
    if not delivery_location:
        raise HTTPException(status_code=400, detail="Invalid delivery zip")

    db_cargo = models.Cargo(
        pick_up_location_id=pick_up_location.id,
        delivery_location_id=delivery_location.id,
        weight=cargo.weight,
        description=cargo.description,
    )
    db.add(db_cargo)
    db.commit()
    db.refresh(db_cargo)
    return db_cargo


@router.get("/cargo/", response_model=List[schemas.Cargo])
def get_cargos(max_weight: Optional[int] = None, min_weight: Optional[int] = None, max_distance: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.Cargo)

    # Filter of cargo weight
    if min_weight is not None:
        query = query.filter(models.Cargo.weight >= min_weight)
    if max_weight is not None:
        query = query.filter(models.Cargo.weight <= max_weight)

    cargos = query.all()


    for cargo in cargos:
        try:
            trucks = db.query(models.Truck).all()
            cargo.nearby_trucks = []
            for truck in trucks:
                dist = calculate_distance(
                            Point(cargo.pick_up_location.latitude,
                                  cargo.pick_up_location.longitude),
                            Point(truck.current_location.latitude, truck.current_location.longitude))
                if dist <= 450:
                    cargo.nearby_trucks.append({
                        "truck": truck,
                        "distance": dist
                    })

        except NoResultFound:
            # Handle the case when the specified pick_up_location_id or delivery_location_id does not exist
            pass
    
    # Filter of distance 
    if max_distance is not None:
        cargos = [cargo for cargo in cargos if all(truck['distance'] <= max_distance for truck in cargo.nearby_trucks)]


    return cargos


@router.get("/cargo/{cargo_id}", response_model=schemas.Cargo)
def get_cargo(cargo_id: int, db: Session = Depends(get_db)):
    cargo = db.query(models.Cargo).get(cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")

    
    cargo.nearby_trucks = []
    trucks = db.query(models.Truck).all()
    for truck in trucks:
        dist = calculate_distance(
                Point(cargo.pick_up_location.latitude,
                      cargo.pick_up_location.longitude),
                Point(truck.current_location.latitude,
                      truck.current_location.longitude))
        if dist <= 450:
            cargo.nearby_trucks.append({
            "truck": truck,
            "distance": dist
            })
    return cargo


@router.put("/cargo/{cargo_id}", response_model=schemas.Cargo)
def update_cargo(cargo_id: int, cargo: schemas.CargoEdit, db: Session = Depends(get_db)):
    db_cargo = db.query(models.Cargo).get(cargo_id)
    if db_cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    db_cargo.weight = cargo.weight
    db_cargo.description = cargo.description
    db.commit()
    db.refresh(db_cargo)
    return db_cargo


@router.delete("/cargo/{cargo_id}", response_model=schemas.Cargo)
def delete_cargo(cargo_id: int, db: Session = Depends(get_db)):
    db_cargo = db.query(models.Cargo).get(cargo_id)
    if db_cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    
    deleted_cargo = schemas.Cargo.from_orm(db_cargo)  # Создаем новый объект для возврата
    
    db.delete(db_cargo)
    db.commit()
    
    return deleted_cargo