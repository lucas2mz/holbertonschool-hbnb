from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Returns a list of users"""
        list_of_users = facade.get_all_users()
        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in list_of_users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User is successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        """Update a User"""
        authenticated_user_id = get_jwt_identity()

        if str(authenticated_user_id) != str(user_id):
            return {"error": "Unauthorized action"}, 403
        
        data = api.payload

        if "email" in data or "pasword" in data:
            return {"error": "You cannot modify email or password"}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': "User not found"}, 404
        try:
            user_updated = facade.update_user(user_id, data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        return {'id': user_updated.id, 'first_name': user_updated.first_name, 'last_name': user_updated.last_name, 'email': user_updated.email}, 200