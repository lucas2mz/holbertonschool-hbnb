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
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.status_code, 200)
        
    def test_get_user_by_id(self):
        response = self.client.get(f'/api/v1/users/{user_id}') # Falta agregar user_id
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            self.assertIn("id": response.json)
            self.assertIn("first_name": response.json)
            self.assertIn("last_name": response.json)
            self.assertIn("email": response.json)

    def test_update_user(self):
        response = self.client.put(f'/api/v1/users/{user_id}', json={ #Falta agregar user_id
            "first_name": "John"
            "last_name": "Doe"
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 200)
        
        response = self.client.put(f'/api/v1/users/{user_id}', json={ #Falta agregar user_id
            "first_name": ""
            "last_name": ""
            "email": "Invalid-Email"
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.put(f'/api/v1/users/{user_id}', json={ #Falta agregar user_id
            "first_name": "John"
            "last_name": "Doe"
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__': 
    unittest.main()