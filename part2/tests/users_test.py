import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_list_of_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        
    def test_get_user_by_id(self):
        response = self.client.post('api/v1/users', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })

        # Obtenemos user ID
        user = response.json
        self.assertIn('id', user)
        user_id = user['id']

        response2 = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response2.status_code, 200)

        response2_user = response2.json
        self.assertEqual(response2_user['id'], user_id)
        self.assertEqual(response2_user['email'], "jane.doe@example.com")
        self.assertEqual(response2_user['first_name'], "Jane")
        self.assertEqual(response2_user['last_name'], "Doe")

    def test_get_user_by_id_not_found(self):
        response = self.client.get(f'/api/v1/users/8989789345')
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):

        re = self.client.post('api/v1/users', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })

        user = re.json
        self.assertIn('id', user)
        user_id = user['id']

        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 200)
        
        respuesta = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "",
            "last_name": "",
            "email": "Invalid-Email"
        })
        self.assertEqual(respuesta.status_code, 400)

        response = self.client.put(f'/api/v1/users/96796', json={ 
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__': 
    unittest.main()