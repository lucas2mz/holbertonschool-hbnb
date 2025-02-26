from datetime import datetime
from base import Base
from user import User
from place import Place

class Review(Base, User, Place):

    def __init__(self, text: str, reating: int, place: Place, user: User):
        Base.__init__(self)
        self.text = text
        self.reating = reating
        self.place = place
        self.user = user

    @property
    def text(self):
        return self.text
    
    @text.setter
    def text_set(self, value):
        if not value:
            raise ValueError("Content of the review is required")
        self.text = value
    
    @property
    def reating(self):
        return self.reating
    
    @reating.setter
    def reating_set(self, value):
        if not (1 <= value <= 5):
            raise ValueError("Reating must be between 1-5")
        self.reating = value

    @property
    def place(self):
        return self.place
    
    @place.setter
    def place_set(self, value):
        if not isinstance(value, Place):
            raise ValueError("The Place doesn't exist")
        self.place = value

    @property
    def user(self):
        return self.user
    
    @user.setter
    def user_set(self, value):
        if not isinstance(value, User):
            raise ValueError("The User doesn't exist")
        self.user = value