
from fastapi import APIRouter

from app.db import SessionLocal, init_db


router = APIRouter()


@router.on_event("startup")
def startup_event():
    with SessionLocal() as session:
        init_db(session)