from datetime import datetime
from base import Base
from user import User
from place import Place

class Review(Base, User, Place):

    def __init__(self, text, reating, place, user):
        if not text:
            raise ValueError("")
        if not (1 <= reating <= 5):
            raise ValueError("Reating must be between 1-5")
        if not isinstance(place, Place):
            raise ValueError("")
        if not isinstance(user, User):
            raise ValueError("")
        
        self.text = text
        self.reating = reating
        self.place = place
        self.user = user
        self.created_at = datetime.now()
        self.updated_at = self.created_at