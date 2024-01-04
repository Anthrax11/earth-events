from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Date,
    Boolean,
    ForeignKey
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped


EVENTS_TABLE = 'events'
CATEGORIES_TABLE = 'categories'
GEOMETRY_TABLE = 'geometry'
SOURCES_TABLE = 'sources'

Base = declarative_base()


class Events(Base):
    __tablename__ = EVENTS_TABLE

    id: Mapped[str] = Column(String, primary_key=True)
    title: Mapped[str] = Column(String)
    description: Mapped[str] = Column(String, nullable=True)
    link: Mapped[str] = Column(String)
    closed: Mapped[bool] = Column(Boolean)


class Categories(Base):
    __tablename__ = CATEGORIES_TABLE

    id: Mapped[str] = Column(String, ForeignKey(f"{EVENTS_TABLE}.id"))
    categories_id: Mapped[str] = Column(String, primary_key=True, unique=True)
    categories_title: Mapped[str] = Column(String)


class Geometry(Base):
    __tablename__ = GEOMETRY_TABLE

    id: Mapped[str] = Column(String, ForeignKey(f"{EVENTS_TABLE}.id"), primary_key=True)
    geometry_magnitude_value: Mapped[str] = Column(String, nullable=True)
    geometry_magnitude_unit: Mapped[str] = Column(String, nullable=True)
    geometry_date: Mapped[datetime] = Column(Date)
    geometry_type: Mapped[str] = Column(String)
    geometry_coordinates: Mapped[str] = Column(String)


class Sources(Base):
    __tablename__ = SOURCES_TABLE

    id: Mapped[str] = Column(String, ForeignKey(f"{EVENTS_TABLE}.id"), primary_key=True)
    sources_id: Mapped[str] = Column(String)
    sources_url: Mapped[str] = Column(String)