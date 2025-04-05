from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('places', description='Place operations')

# Define the models for related entities
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner')
}, strict=True)

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""

        current_user = get_jwt_identity()

        place_data = api.payload

        if place_data['owner_id'] != current_user:
            return {'error': 'Unauthorized action'}, 403

        existing_place = facade.get_place(place_data['title'])

        if existing_place:
            return {'error': 'Place already exist'}, 400
        
        owner = facade.get_user(place_data['owner_id'])

        if not owner:
            return {"error": "Invalid input data"}, 400
        
        place_data.pop('owner_id')

        place_data['owner'] = owner
        try:
            place_n = facade.create_place(place_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        return {'id': place_n.id, 'title': place_n.title, 'description': place_n.description, 'price': place_n.price, 'latitude': place_n.latitude, 'longitude': place_n.longitude, 'owner_id': place_n.owner.id}, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        list_of_places = facade.get_all_places()
        return [{'id': place.id, 'title': place.title, 'latitude': place.latitude, 'longitude': place.longitude} for place in list_of_places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        owner = facade.get_user(place.owner.id)
        
        if not owner:
            return {'error': 'Owner not found'}, 404

        amenities = facade.amenity_repo.get_all()

        reviews = facade.review_repo.get_all()

        response = {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            },
            'reviews': [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            } for review in reviews if review.place.id == place.id],
            'amenities': [{
                'id': amenity.id,
                'name': amenity.name
            } for amenity in amenities if amenity.places == place.id]
        }

        return response, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""

        current_user = get_jwt()
        data = api.payload

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner.id != user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.update_place(place_id, data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        return {"message": "Place updated successfully"}, 200

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Review not found"}, 404

      ##  user_id = place.owner.id

        ##if user_id != current_user:
          ##  return {"error": "Unauthorized action"}, 403
        place = facade.delete_place(place_id)
        
        return {"message": "Place deleted successfully"}, 200