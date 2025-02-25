from datetime import datetime
from base import Base

class Amenity(Base):

    def __init__(self, name):
        if not name or len(name) > 50:
            raise ValueError("The name has to be less than 50 characters")
        
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = self.created_at
