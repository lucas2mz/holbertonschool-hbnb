#!/usr/bin/env python3


#from app.persistence.repository import InMemoryRepository
from app.persistence.UserRepository import UserRepository
from app.persistence.PlaceRepository import PlaceRepository
from app.persistence.ReviewRepository import ReviewRepository
from app.persistence.AmenityRepository import AmenityRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review



class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository() #self.user_repo = InMemoryRepository()
        self.place_repo = PlaceRepository()#self.place_repo = InMemoryRepository()
        self.review_repo = ReviewRepository()#self.review_repo = InMemoryRepository()
        self.amenity_repo = AmenityRepository()#self.amenity_repo = InMemoryRepository()
   
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)
    
    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)
    
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        pass

    def get_review_by_user_and_place(self, user_id, place_id):
        all_reviews = self.get_all_reviews()
        for review in all_reviews:
            if review.user.id == user_id and review.place.id == place_id:
                return review
        return None

    def update_review(self, review_id, review_data):
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)