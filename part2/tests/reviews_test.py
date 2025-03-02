import unittest
from app import create_app

class TestReviewsEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review(self):
        user_id = self.test_create_user()
        place_id = self.test_create_place()
        response = self.client.post('/api/v1/reviews', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": f"{user_id}",
            "place_id": f"{place_id}"
        })
        self.assertEqual(response.status_code, 201)


    def test_create_review_invalid_data(self):
        response = self.client.post('/api/v1/reviews', json={
            "text": "",
            "rating": -3,
            "user_id": "",
            "place_id": ""
        })
        self.assertEqual(response.status_code, 400)
    
    def test_list_all_reviews(self):
        response = self.client.get('/api/v1/reviews')
        self.IsInstance(response.json, list)
        self.assertEqual(response.status_code, 200)

    def test_delete_review(self):
        response = self.client.delete(f'/api/v1/reviews/{review_id}') # Agregar review ID
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/api/v1/reviews/{review_id}') # Agregar review ID
        self.assertEqual(response.status_code, 404)

    def test_update_review(self):
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={ # Agregar review ID
            "text": "Amazing stay!",
            "rating": 4
        })
        self.assertEqual(response.status_code, 200)
        
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={ # Agregar review ID
            "text": "",
            "rating": -4
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.put(f'/api/v1/reviews/{review_id}', json={ # Agregar review ID
            "text": "",
            "rating": -4
        })
        self.assertEqual(response.status_code, 404)
    
    def test_get_review_details(self):
        response = self.client.get(f'/api/v1/reviews/{review_id}') # Agregar review ID
    # Terminar (errores 200 y 404)


if __name__ == '__main__': 
    unittest.main()