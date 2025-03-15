from datetime import datetime
from app import db
from .base import Base
from sqlalchemy.orm import validates


class Amenity(Base):

    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    @validates("name")
    def validate_name(self, key, name):
        if not name or len(name) > 50:
            raise ValueError("The name has to be less than 50 characters")
        return name