import unittest
from app import create_app


class TestReviewsEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.user_id, self.place_id = self.create_user_and_place()

    def create_user_and_place(self):
        usuario = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })

        owner = usuario.json
        self.assertIn('id', owner)
        owner_id = owner['id']

        place = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": f"{owner_id}"
        })

        if usuario.status_code == 201 and place.status_code == 201:
            return usuario.json["id"], place.json["id"]
        else:
            return {"Invalid data"}

    def test_create_review(self):
        self.create_user_and_place()
        review = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(review.status_code, 201)


    def test_create_review_invalid_data(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": -3,
            "user_id": "",
            "place_id": ""
        })
        self.assertEqual(response.status_code, 400)
    
    def test_list_all_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.IsInstance(response.json, list)
        self.assertEqual(response.status_code, 200)

    def test_delete_review(self):
        self.create_user_and_place()
        review = self.client.post('/api/v1/reviews/', json={
            "text": "Good place to stay!",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        review = review.json
        self.assertIn('id', review)
        review_id = review['id']

        delete_review = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(delete.status_code, 200)

        error_review = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(error_review.status_code, 404)

    def test_update_review(self):
        self.create_user_and_place()
        review = self.client.post('/api/v1/reviews/', json={
            "text": "Bad place to stay!",
            "rating": 1,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        review = review.json
        self.assertIn('id', review)
        review_id = review['id']

        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Amazing stay!",
            "rating": 4
        })
        self.assertEqual(response.status_code, 200)
        
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "",
            "rating": -4
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "",
            "rating": -4
        })
        self.assertEqual(response.status_code, 404)
    
    def test_get_review_details(self):
        self.create_user_and_place()
        review = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        review = review.json
        self.assertIn('id', review)
        review_id = review['id']

        review_details = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(review_details.status_code, 200)

        self.assertEqual(place_details['id'], review_id)
        self.assertEqual(place_details['text'], "Good place to stay!")
        self.assertEqual(place_details['rating'], 4)
        self.assertEqual(place_details['user_id'], self.user_id)
        self.assertEqual(place_details['place_id'], self.place_id)

    def test_list_of_reviews_by_place(self):
        self.create_user_and_place()
        review = self.client.post('/api/v1/reviews/', json={
            "text": "Pretty place to stay!",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        
        response = self.client.get(f'/api/v1/reviews/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

        for review in response.json:
            if review['text'] == "Pretty place to stay!" and review['rating'] == 4:
                self.assertTrue(True)
                break
            else:
                self.assertFalse(False)
        error_response = self.client.get('/api/v1/reviews/places/80h80fe8u80/reviews')
        self.assertEqual(error_response.status_code, 404)


if __name__ == '__main__': 
    unittest.main()