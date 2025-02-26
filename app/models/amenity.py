from datetime import datetime
from base import Base

class Amenity(Base):

    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self.name
    
    @name.setter
    def name_set(self, value):
        if not value or len(value) > 50:
            raise ValueError("The name has to be less than 50 characters")
        self.name = value