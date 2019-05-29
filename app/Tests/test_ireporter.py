import unittest
import os
import json
from app import create_app, db


class IreporterTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go to Borabora for vacay'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/API/V1/views/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/API/V1/views/login', data=user_data)

    def test_ireporter_creation(self):
        """Test API can create (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create  by making a POST request
        res = self.client().post(
            '/API/V1/Ireporter/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_all_ireporters(self):
        """Test API can get  (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create by making a POST request
        res = self.client().post(
            '/API/V1/Ireporter/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(res.status_code, 201)

        # get all the ireporters that belong to the test user by making a GET request
        res = self.client().get(
            '/API/V1/Ireporter/',
            headers=dict(Authorization="Bearer " + access_token),
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_ireporter_by_id(self):
        """Test API can get a single ireporter by using it's id."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/API/V1/Ireporter/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)

        # assert that it is created 
        self.assertEqual(rv.status_code, 201)
        # get the response data in json format
        results = json.loads(rv.data.decode())

        result = self.client().get(
            '/API/V1/Ireporter/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        # assert that it is actually returned given its ID
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Borabora', str(result.data))

    def test_ireporter_can_be_edited(self):
        
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # first, we create  by making a POST request
        rv = self.client().post(
            '/API/V1/Ireporter/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        # get the json with the bucketlist
        results = json.loads(rv.data.decode())

        # then, we edit the creation by making a PUT request
        rv = self.client().put(
            '/API/V1/Ireporter/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data={
                "name": "Dont just eat, but also pray and love :-)"
            })
        self.assertEqual(rv.status_code, 200)

        # finally, we get the edit to see if it is actually edited.
        results = self.client().get(
            '/API/V1/Ireporter/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Dont just eat', str(results.data))

    def test_ireporter_deletion(self):
        """Test API can delete  (DELETE request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/API/V1/Ireporter/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        # get the bucketlist in json
        results = json.loads(rv.data.decode())

        # delete what we just created
        res = self.client().delete(
            '/API/V1/Ireporter/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(res.status_code, 200)

        # Test to see if it exists, should return a 404
        result = self.client().get(
            '/API/V1/Ireporter/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()