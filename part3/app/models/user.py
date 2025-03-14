from app import db
from datetime import datetime
from .base import Base
from email_validator import validate_email, EmailNotValidError
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import validates


bcrypt = Bcrypt()

class User(Base):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name: str, last_name: str, email: str, password: str, is_admin: bool = False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    @validates("first_name")
    def validate_first_name(self, key, first_name):
        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required and cannot exceed 50 characters")
        return first_name
    
    @validates("last_name")
    def validate_last_name(self, key, last_name):
        if not last_name or len(last_name) >= 50:
            raise ValueError("Last name is required and cannot exceed 50 characters")
        return last_name
    
    @validates("email")
    def validate_email(self, key, value):
        try:
            email_validation = validate_email(value, check_deliverability=False)
            return email_validation.normalized
        except EmailNotValidError:
            raise ValueError("Invalid email format")
    
    @validates("password")
    # def validate_password(self, key, password):
    #     hashed_password = self.hash_password(password)
    #     return hashed_password

    def validate_password(self, key, password):
        """Hashes the password before storing it."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
        