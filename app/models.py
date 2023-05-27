from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    state = Column(String)
    zip = Column(Integer, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

class Cargo(Base):
    __tablename__ = "cargos"

    id = Column(Integer, primary_key=True, index=True)
    pick_up_location_id = Column(Integer, ForeignKey('locations.id'), index=True)
    delivery_location_id = Column(Integer, ForeignKey('locations.id'), index=True)
    weight = Column(Integer)
    description = Column(String)
    pick_up_location = relationship("Location", foreign_keys=[pick_up_location_id], lazy="joined", join_depth=1)
    delivery_location = relationship("Location", foreign_keys=[delivery_location_id], lazy="joined", join_depth=1)

class Truck(Base):
    __tablename__ = "trucks"

    id = Column(Integer, primary_key=True, index=True)
    unique_number = Column(String, unique=True, index=True)
    current_location_id = Column(Integer, ForeignKey('locations.id'), index=True)
    carrying_capacity = Column(Integer)
    current_location = relationship("Location", lazy="joined", join_depth=1)
