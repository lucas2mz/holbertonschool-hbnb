from datetime import datetime
from .base import Base
from email_validator import validate_email, EmailNotValidError


class User(Base):

    def __init__(self, first_name: str, last_name: str, email: str, is_admin: bool = False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, condition):
        if not condition or len(condition) > 50:
            raise ValueError("First name is required and cannot exceed 50 characters")
        self._first_name = condition

    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        if not value or len(value) >= 50:
            raise ValueError("Last name is required and cannot exceed 50 characters")
        self._last_name = value

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        try:
             email_validation = validate_email(value, check_deliverability=False)
             self._email = email_validation.normalized
        except EmailNotValidError as e:
            raise ValueError("Invalid email")