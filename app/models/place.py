from datetime import datetime
from base import Base
from user import User

class Place(Base, User):

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

    @property
    def title(self):
        return self.title
    
    @title.setter
    def title_set(self, value):
        if not value or len(value) > 100:
            raise ValueError("Title is required and cannot exceed 100 characters")
        self.title = value
    
    @property
    def price(self):
        return self.price
    
    @price.setter
    def price_set(self, value):
        if value <= 0:
            raise ValueError("Price must be a positive value")
        self.price = value
    
    @property
    def latitude(self):
        return self.latitude
    
    @latitude.setter
    def latitude_set(self, value):
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be within the range of -90.0 to 90.0")
        self.latitude = value
        
    @property
    def longitude(self):
        return self.longitude
    
    @longitude.setter
    def longitude_set(self, value):
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be within the range of -180.0 to 180.0")
        self.longitude = value

    @property
    def owner(self):
        return self.owner
    
    @owner.setter
    def owner_set(self, value):
        if not isinstance(value, User):
            raise ValueError("Owner must be a valid User")
        self.owner = value

    def add_review(self, review):
        self.reviews.append(review)
    
    def add_amenity(self, amenity):
        self.amenities.append(amenity)
