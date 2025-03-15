from datetime import datetime
from app import db
from .base import Base
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Table, Column, ForeignKey, Integer

place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', ForeignKey('amenities.id'), primary_key=True)
)


class Amenity(Base):

    __tablename__ = 'amenities'

    id = Column(Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    places = relationship('Place', secondary=place_amenity, back_populates='amenities')

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    @validates("name")
    def validate_name(self, key, name):
        if not name or len(name) > 50:
            raise ValueError("The name has to be less than 50 characters")
        return name