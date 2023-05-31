import os
import random
import time
from sqlalchemy import create_engine, func, insert, text
from sqlalchemy.orm import sessionmaker

from app.utils import generate_unique_number
from .models import Base
import csv

from app import models


# Establish the database connection
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db") # Default to "db" if not provided

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import Session

def get_db():
    # Define a generator function to manage the database session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_trucks(db: Session):
    # Function to initialize trucks in the database
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

def update_trucks(db: Session):
    # Function to update the current location of trucks
    start_time = time.time()  # Start measuring execution time

    truck_count = db.query(func.count(models.Truck.id)).scalar()
    if truck_count > 0:
        truck_ids = db.query(models.Truck.id).all()
        existing_location_ids = db.query(models.Location.id).all()
        random_location_ids = random.choices(existing_location_ids, k=truck_count)
        truck_ids_tuple = tuple(truck_id[0] for truck_id in truck_ids)

        update_query = text(
            "UPDATE trucks SET current_location_id = :loc_id "
            "WHERE id IN :truck_ids"
        )

        for loc_id, truck_id in zip(random_location_ids, truck_ids_tuple):
            db.execute(update_query, {"loc_id": loc_id[0], "truck_ids": (truck_id,)})

        db.commit()

    end_time = time.time()  # Stop measuring execution time
    execution_time = end_time - start_time
    print(f"update_trucks execution time: {execution_time} seconds")

def init_locations_from_file(filepath: str, db: Session):
    # Function to initialize locations from a CSV file
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
    # Function to initialize the database with locations and trucks
    start_time = time.time()
    init_locations_from_file('uszips.csv', db)
    end_time = time.time()
    print(f"init_locations_from_file execution time: {end_time - start_time} seconds")

    start_time = time.time()
    init_trucks(db)
    end_time = time.time()
