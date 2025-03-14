from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt


api = Namespace('admin', description='Admin operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})


@api.route('/users/')
class AdminUserCreate(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        email = user_data['email']

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201


@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @api.expect(user_model, validate=True)
    @api.response(200, 'User is successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload
        email = data['email']

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': "User not found"}, 404

        try:
            user_updated = facade.update_user(user_id, data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        return {'id': user_updated.id, 'first_name': user_updated.first_name, 'last_name': user_updated.last_name, 'email': user_updated.email}, 200

    
@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        current_user = get_jwt()
        amenity_data = api.payload

        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        existing_amenity = facade.get_amenity(amenity_data['name'])
        if existing_amenity:
            return {'error': 'Amenity already exist'}, 400
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        return {'id': new_amenity.id,'name': new_amenity.name}, 201

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt()
        data = api.payload

        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        try:
            amenity = facade.get_amenity(amenity_id)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        if not amenity:
            return {"error": "Amenity not found"},404
        
        amenity = facade.update_amenity(amenity_id, data)
        return {'messege': 'Amenity update successfully'}, 200

@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt()
        data = api.payload

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        if not place:
            return {"error": "Place not found"}, 404

        try:
            updated_place = facade.update_place(place_id, data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        return {"message": "Place updated successfully"}, 200
