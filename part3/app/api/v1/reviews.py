from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/reviews')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        review_data = api.payload
        existing_review = facade.get_review(review_data['text'])
        if existing_review:
            return {"Error": "Review already exist"}, 400

        user = facade.get_user(review_data['user_id'])
        if not user:
            return {"Error": "User not found"}, 404
        
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {"Error": "Place not found"}, 404

        if place.owner.id == user.id:
            return {"Error": "You cannot review your own place."}, 400

        review_checker = facade.get_review_by_user_and_place(user.id, place.id)
        if review_checker:
            return {"Error": "You have already reviewed this place."}, 400
        
        review_data.pop('user_id')
        review_data.pop('place_id')

        review_data['user'] = user
        review_data['place'] = place

        try:
            new_review = facade.create_review(review_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        return {'id': new_review.id, 'text': new_review.text, 'rating': new_review.rating, 'user_id': user.id, 'place': place.id}, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        list_of_review = facade.get_all_reviews()
        return [{'id': review.id, 'text': review.text, 'rating': review.rating} for review in list_of_review], 200

@api.route('/reviews/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'Error': 'Review not found'}, 404
        return {'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user.id, 'place': review.place.id}, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        data = api.payload

        current_user = get_jwt_identity()

        review = facade.review_repo.get(review_id)
        if not review:
            return {'Error': 'Review not found'}, 404

        user_id = review.user.id

        if user_id != current_user:
            return {"Error": "Unauthorized action."}, 403

        try:
            update_review = facade.update_review(review_id, data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
    
        return {"message": "Review updated successfully"}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        user_id = review.user.id

        if user_id != current_user:
            return {"error": "Unauthorized action"}, 403
        review = facade.delete_review(review_id)
        
        return {"message": "Review deleted successfully"}, 200

@api.route('/reviews/places/<place_id>')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        reviews = facade.get_all_reviews()
        if not reviews:
            return {"error": "Reviews not found"}, 404
        return [{'id': review.id, 'text': review.text, 'rating': review.rating} for review in reviews if review.place.id == place_id], 200