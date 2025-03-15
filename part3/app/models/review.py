from datetime import datetime
from app import db
from .base import Base
from .user import User
from .place import Place
from sqlalchemy.orm import validates


class Review(Base):

    __tablename__ = 'reviews'

    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, text: str, rating: int, place: Place, user: User):
        Base.__init__(self)
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
    
    @validates("text")
    def validate_text(self, key, text):
        if not text:
            raise ValueError("Content of the review is required")
        return text

    @validates("rating")
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Reating must be between 1-5")
        return rating

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