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
        self.ireporter = {'name': 'Go to Borabora for vacation'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_ireporter_creation(self):
        """Test API can create a irecord (POST request)"""
        res = self.client().post('/API/V1/Ireporter/', data=self.ireporter)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_all_ireporters(self):
        """Test API can get a irecord (GET request)."""
        res = self.client().post('/API/V1/Ireporter/', data=self.ireporter)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/API/V1/Ireporter/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_ireporter_by_id(self):
      
        rv = self.client().post('/API/V1/Ireporter/', data=self.ireporter)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/API/V1/Ireporter/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Borabora', str(result.data))

    def test_ireporter_can_be_edited(self):
       
        rv = self.client().post(
            '/API/V1/Ireporter/',
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/API/V1/Ireporter/1',
            data={
                "name": "Dont just eat, but also pray and love :-)"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/API/V1/Ireporter/1')
        self.assertIn('Dont just eat', str(results.data))

    def test_bucketlist_deletion(self):
        """Test API can delete an existing irecord. (DELETE request)."""
        rv = self.client().post(
            '/API/V1/Ireporter/',
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/API/V1/Ireporter/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/API/V1/Ireporter/1')
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