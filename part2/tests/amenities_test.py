import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_create_amenity(self):
        response = self.client.post('api/v1/amenities/', json={
            "name": "Wifi"
        })
        self.assertEqual(response.status_code, 201)
    
    def test_create_amenity_invalid_data(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_list_of_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.status_code, 200)
        
    def test_get_amenities_by_id(self):
        response = self.client.post('api/v1/amenities/', json={
            "name": "Wifi"
        })
        # Obtenemos user ID
        amenity = response.json
        self.assertIn('id', amenity)
        amenity_id = amenity['id']
        amenity_name = amenity['name']

        response2 = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response2.status_code, 200)

        response2_amenity = response2.json
        self.assertEqual(response2_amenity['id'], amenity_id)
        self.assertEqual(response2_amenity['name'], amenity_name)

    def test_get_amenities_by_id_not_found(self):
        response = self.client.get(f'/api/v1/amenities/807867906')
        self.assertEqual(response.status_code, 404)

    def test_update_amenities(self):

        re = self.client.post('api/v1/amenities', json={
            "name": "Wifi"
        })

        amenity = re.json
        self.assertIn('id', amenity)
        amenity_id = amenity['id']

        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "Pool"
        })
        self.assertEqual(response.status_code, 200)
        
        respuesta = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": ""
        })
        self.assertEqual(respuesta.status_code, 400)

        response = self.client.put(f'/api/v1/amenities/896796', json={ 
            "name": "Wifi"
        })
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__': 
    unittest.main()