import unittest
from app import create_app


class TestPlacesEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def test_create_place(self): # Test Success request
        usuario = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })

        owner = usuario.json
        self.assertIn('id', owner)
        owner_id = owner['id']

        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": f"{owner_id}"
        })
        self.assertEqual(response.status_code, 201)
    
    def test_create_place_invalid_data(self): # Test Bad Request
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "",
            "price": -256.0,
            "latitude": 190,
            "longitude": -190.4194,
            "owner_id": "" 
        })
        self.assertEqual(response.status_code, 400)
    
    def test_list_all_places(self): # Test list all places
        response = self.client.get('/api/v1/places')
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.status_code, 200)
    
    def test_get_place_details(self): # Terminar (falta manejar error 404)
        usuario = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane2.doe@example.com"
        })

        owner = usuario.json
        self.assertIn('id', owner)
        owner_id = owner['id']

        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": f"{owner_id}"
        })

        place = response.json
        self.assertIn('id', place)
        place_id = place['id']

        details = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(details.status_code, 200)

        self.assertEqual(details.json['id'], place_id)
        self.assertEqual(details.json['title'], "Cozy Apartment")
        self.assertEqual(details.json['description'], "A nice place to stay")
        self.assertEqual(details.json['latitude'], 37.7749)
        self.assertEqual(details.json['longitude'], -122.4194)
        self.assertEqual(details.json['owner'], owner)

    def test_update_place(self): # Test Success request
        usuario = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane3.doe@example.com"
        })

        owner = usuario.json
        self.assertIn('id', owner)
        owner_id = owner['id']

        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": f"{owner_id}"
        })

        place = response.json
        self.assertIn('id', place)
        place_id = place['id']

        update = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Luxury Condo",
            "description": "An upscale place to stay",
            "price": 200.0
        })
        self.assertEqual(update.status_code, 200)

        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "",
            "description": "",
            "price": -200.0
        })
        self.assertEqual(response.status_code, 400)

        response2 = self.client.put('/api/v1/places/789342', json={
            "title": "Luxury Condo",
            "description": "An upscale place to stay",
            "price": 200.0
        })
        self.assertEqual(response2.status_code, 404)


if __name__ == '__main__': 
    unittest.main()