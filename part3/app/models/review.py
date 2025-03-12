from datetime import datetime
from .base import Base
from .user import User
from .place import Place

class Review(Base):

    def __init__(self, text: str, rating: int, place: Place, user: User):
        Base.__init__(self)
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        if not value:
            raise ValueError("Content of the review is required")
        self._text = value
    
    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, value):
        if not (1 <= value <= 5):
            raise ValueError("Reating must be between 1-5")
        self._rating = value

    @property
    def place(self):
        return self._place
    
    @place.setter
    def place(self, value):
        if not isinstance(value, Place):
            raise ValueError("The Place doesn't exist")
        self._place = value

    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise ValueError("The User doesn't exist")
        self._user = value