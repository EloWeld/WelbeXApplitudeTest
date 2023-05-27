import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from app.api import *

app = FastAPI()

app.include_router(cargo.router)
app.include_router(truck.router)
app.include_router(etc.router)

scheduler = BackgroundScheduler()
scheduler.start()

def update_trucks_job():
    from app.db import update_trucks, SessionLocal
    update_trucks(SessionLocal())

scheduler.add_job(update_trucks_job, 'interval', minutes=5)

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()