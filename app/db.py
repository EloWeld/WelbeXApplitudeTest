import random
import time
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from app.utils import generate_unique_number
from .models import Base
import csv

from app import models

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Three.ru2015@localhost/cargo_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

def init_trucks(db: Session):
    # To generate maximum 20 trucks
    min_trucks_amount = 20 - db.query(models.Truck).count()

    if min_trucks_amount > 0:
        existing_locations = db.query(models.Location).all()

        for _ in range(min_trucks_amount):
            unique_number = generate_unique_number()
            current_location = random.choice(existing_locations)
            carrying_capacity = random.randint(1, 1000)

            truck = models.Truck(
                unique_number=unique_number,
                current_location_id=current_location.id,
                carrying_capacity=carrying_capacity,
            )
            db.add(truck)

        db.commit()

def init_locations_from_file(filepath: str, db: Session):
    locations = []

    if db.query(models.Location).count() > 0:
        print("Locations already added, continue")
        return
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            location = {
                'zip': row['zip'],
                'latitude': float(row['lat']),
                'longitude': float(row['lng']),
                'city': row['city'],
                'state': row['state_id'],
            }
            locations.append(location)
    
    stmt = insert(models.Location).values(locations)
    db.execute(stmt)
    db.commit()

def init_db(db: Session):
    start_time = time.time()
    init_locations_from_file('uszips.csv', db)
    end_time = time.time()
    print(f"init_locations_from_file execution time: {end_time - start_time} seconds")

    start_time = time.time()
    init_trucks(db)
    end_time = time.time()
    print(f"init_trucks execution time: {end_time - start_time} seconds")
