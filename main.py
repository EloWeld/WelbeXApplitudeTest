from fastapi import FastAPI
from app.api import *

app = FastAPI()

app.include_router(cargo.router)
app.include_router(truck.router)
app.include_router(etc.router)

