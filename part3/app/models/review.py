from datetime import datetime
from app import db
from .base import Base
from .user import User
from .place import Place
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Table, Column, Integer, ForeignKey


class Review(Base):

    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)
    place = relationship('Place', back_populates='reviews')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='reviews')

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