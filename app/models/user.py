from datetime import datetime
from base import Base

class User(Base):

    def __init__(self, first_name: str, last_name: str, email: str, is_admin: bool = False):
        if not first_name or len(first_name) >= 50:
            raise ValueError("First name is required and cannot exceed 50 characters")
        if not last_name or len(last_name) >= 50:
            raise ValueError("Last name is required and cannot exceed 50 characters")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.created_at = datetime.now()
        self.updated_at = self.created_at
