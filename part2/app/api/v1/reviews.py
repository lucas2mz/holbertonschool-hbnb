from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
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
        
        review_data.pop('user_id')
        review_data.pop('place_id')

        review_data['user'] = user
        review_data['place'] = place

        new_review = facade.create_review(review_data)
        return {'id': new_review.id, 'text': new_review.text, 'rating': new_review.rating, 'user_id': user.id, 'place': place.id}, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        list_of_review = facade.get_all_reviews()
        return [{'id': review.id, 'text': review.text, 'rating': review.rating} for review in list_of_review], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Placeholder for the logic to retrieve a review by ID
        pass

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        pass

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # Placeholder for the logic to delete a review
        pass

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Placeholder for logic to return a list of reviews for a place
        pass