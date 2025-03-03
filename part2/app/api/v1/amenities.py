from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        existing_amenity = facade.get_amenity(amenity_data['name'])
        if existing_amenity:
            return {'error': 'Amenity already exist'}, 400
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        return {'id': new_amenity.id,'name': new_amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Return a list of the amenities"""
        list_of_amenities = facade.get_all_amenities()
        return [{'id': amenity.id,'name': amenity.name} for amenity in list_of_amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity_id, 'name': amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = api.payload

        try:
            amenity = facade.get_amenity(amenity_id)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        if not amenity:
            return {"error": "Amenity not found"},404
        
        amenity = facade.update_amenity(amenity_id, data)
        return {'messege': 'Amenity update successfully'}, 200