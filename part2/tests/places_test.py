import unittest
from app import create_app

class TestPlacesEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_place(self): # Test Success request
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": f"{owner_id}" #Falta agregar owner_id
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
        self.assertEqual(response.status_codem, 400)
    
    def test_list_all_places(self):
        response = self.client.get('/api/v1/places')
        self.IsInstance(response.json, list)
        self.assertEqual(response.status_code, 200)
    
    def test_get_place_details(self): # Terminar (falta manejar error 404)
        response = self.client.get(f'/api/v1/places/{place_id}') # Agregar place id
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            places = response.json
            self.assertIsInstance(places, list)
            if places:
                for place in places:
                    self.assertIn("id", place)
                    self.assertIn("title", place)
                    self.assertIn("description", place)
                    self.assertIn("latitude", place)
                    self.assertIn("longitude", place)
                    self.assertIn("owner", place)
                    self.assertIn("amenities", place) # Corregir

    def test_update_place(self): # Test Success request
        response = self.client.put(f'/api/v1/places/{place_id}', json={ # Agregar place id
            "title": "Luxury Condo",
            "description": "An upscale place to stay",
            "price": 200.0
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.put(f'/api/v1/places/{place_id}', json={ # Agregar place id
            "title": "",
            "description": "",
            "price": -200.0
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.put(f'/api/v1/places/{place_id}', json={ # Agregar place id invalida
            "title": "Luxury Condo",
            "description": "An upscale place to stay",
            "price": 200.0
        })
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__': 
    unittest.main()