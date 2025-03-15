from datetime import datetime
from app import db
from .base import Base
from app.models.user import User
from sqlalchemy.orm import validates


class Place(Base):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), default=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, title: str, price: float, latitude: float, longitude: float, owner: User, description=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    @validates("title")
    def validate_title(self, key, title):
        if not title or len(title) > 100:
            raise ValueError("Title is required and cannot exceed 100 characters")
        return title
    
    @validates("price")
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError("Price must be a positive value")
        return price
    
    @validates("latitude")
    def validate_latitude(self, key, latitude):
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be within the range of -90.0 to 90.0")
        return latitude

    @validates("longitude")
    def validate_longitude(self, key, longitude):
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be within the range of -180.0 to 180.0")
        return longitude

    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise ValueError("Owner must be a valid User")
        self._owner = value

    def add_review(self, review):
        self.reviews.append(review)
    
    def add_amenity(self, amenity):
        self.amenities.append(amenity)
