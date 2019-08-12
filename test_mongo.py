import unittest
import json
from app import create_app
from app.init_mongodb import mongo


class MongoTestCase(unittest.TestCase):
    """This class represents the user_Mongo test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'username': 'JohnDoe', 'firstname': 'John', 'lastname': 'Doe'}

        # binds the app to the current context

    def test_user_creation(self):
        """Test API can create a user (POST request)"""
        res = self.client().post('/mongodbUser/', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('John', str(res.data))

    def test_api_can_get_all_users(self):
        """Test API can get a user (GET request)."""
        res = self.client().post('/mongodbUser/', data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/mongodbUser')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Doe', str(res.data))

    def test_api_can_get_user_by_username(self):
        """Test API can get a single user by using it's username."""
        rv = self.client().post('/mongodbUser/', data=self.user)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/mongodbUser?username={}'.format(result_in_json['username']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('John', str(result.data))

    def test_user_can_be_edited(self):
        """Test API can edit an existing user. (PUT request)"""
        rv = self.client().post(
            '/mongodbUser/',
            data={'username': 'JohnDoe', 'firstname': 'John', 'lastname': 'Doe'})
        self.assertEqual(rv.status_code, 201)
        rw = self.client().post(
            '/mongodbUser/',
            data={'username': 'JaneDoe', 'firstname': 'Jane', 'lastname': 'Doe'})
        self.assertEqual(rw.status_code, 201)
        rv = self.client().put(
            '/mongodbUser?username=JaneDoe',
            data={'username': 'JaneDoe', 'firstname': 'KKKKK', 'lastname': 'Doe'}
            )
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/mongodbUser?username=JaneDoe')
        self.assertIn('KKKKK', str(results.data))

    def test_user_deletion(self):
        """Test API can delete an existing user. (DELETE request)."""
        rv = self.client().post(
            '/mongodbUser/',
            data={'username': 'JaneDoe', 'firstname': 'Jane', 'lastname': 'Doe'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/mongodbUser/JaneDoe')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/mongodbUser?username=JaneDoe')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop user table
            mongo.db.users.drop()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
