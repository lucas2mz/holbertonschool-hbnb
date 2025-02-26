from datetime import datetime
from base import Base
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
        return self.first_name

    @first_name.setter
    def first_name_set(self, condition):
        if not condition or len(condition) > 50:
            raise ValueError("First name is required and cannot exceed 50 characters")
        self.first_name = condition

    @property
    def last_name(self):
        return self.last_name
    
    @last_name.setter
    def last_name_set(self, value):
        if not value or len(value) >= 50:
            raise ValueError("Last name is required and cannot exceed 50 characters")
        self.last_name = value

    @property
    def email(self):
        return self.email
    
    @email.setter
    def email_verificator(self, value):
        try:
             validate_email(value)
             self.email = value
        except EmailNotValidError as e:
            raise EmailNotValidError("Invalid Email")