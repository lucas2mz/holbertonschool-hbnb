from datetime import datetime
from base import Base
from user import User

class Place(Base, User):

    def __init__(self, title, description=None, price, latitude, longitude, owner):
        if not title or len(title) > 100:
            raise ValueError("Title is required and cannot exceed 100 characters")
        if price <= 0:
            raise ValueError("Price must be a positive value")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be within the range of -90.0 to 90.0")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be within the range of -180.0 to 180.0")
        if not isinstance(owner, User):
            raise ValueError("Owner must be a valid User instance")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)
    
    def add_amenity(self, amenity):
        self.amenities.append(amenity)
