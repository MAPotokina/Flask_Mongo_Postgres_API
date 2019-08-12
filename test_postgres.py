import unittest
import json
from app import create_app
from app.init_postgres import db


class PostgresTestCase(unittest.TestCase):
    """This class represents the user_Postgres test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'username': 'JohnDoe', 'firstname': 'John', 'lastname': 'Doe'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_creation(self):
        """Test API can create a user (POST request)"""
        res = self.client().post('/postgresqlUser', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('John', str(res.data))

    def test_api_can_get_all_users(self):
        """Test API can get a user (GET request)."""
        res = self.client().post('/postgresqlUser', data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/postgresqlUser')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Doe', str(res.data))

    def test_api_can_get_user_by_id(self):
        """Test API can get a single user by using it's id."""
        rv = self.client().post('/postgresqlUser', data=self.user)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/postgresqlUser?id={}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('John', str(result.data))

    def test_user_can_be_edited(self):
        """Test API can edit an existing user. (PUT request)"""
        rv = self.client().post(
            '/postgresqlUser',
            data={'username': 'JohnDoe', 'firstname': 'John', 'lastname': 'Doe'})
        self.assertEqual(rv.status_code, 201)
        rw = self.client().post(
            '/postgresqlUser',
            data={'username': 'JaneDoe', 'firstname': 'Jane', 'lastname': 'Doe'})
        self.assertEqual(rw.status_code, 201)
        rv = self.client().put(
            '/postgresqlUser?id=2',
            data={'username': 'JDoe', 'firstname': 'Jane', 'lastname': 'Doe'}
            )
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/postgresqlUser?id=2')
        self.assertIn('Jane', str(results.data))

    def test_user_deletion(self):
        """Test API can delete an existing user. (DELETE request)."""
        rv = self.client().post(
            '/postgresqlUser',
            data={'username': 'JaneDoe', 'firstname': 'Jane', 'lastname': 'Doe'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/postgresqlUser/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/postgresqlUser?id=1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()