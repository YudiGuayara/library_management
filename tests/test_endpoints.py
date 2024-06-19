# tests/test_endpoints.py

import unittest
from app import create_app
from app.extensions import mongo
from flask import json
from bson.objectid import ObjectId
from datetime import datetime

class LibraryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        mongo.db.materials.delete_many({})
        mongo.db.users.delete_many({})
        mongo.db.borrows.delete_many({})

        self.add_sample_data()

    def tearDown(self):
        mongo.db.materials.delete_many({})
        mongo.db.users.delete_many({})
        mongo.db.borrows.delete_many({})

        self.app_context.pop()

    def add_sample_data(self):
        user = mongo.db.users.insert_one({'name': 'John Doe', 'email': 'john@example.com'}).inserted_id
        material = mongo.db.materials.insert_one({
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'year': 1925,
            'type': 'Book',
            'available': True
        }).inserted_id

    def test_add_material(self):
        response = self.client.post('/api/materials', json={
            'title': '1984',
            'author': 'George Orwell',
            'year': 1949,
            'type': 'Book'
        }, headers={'Authorization': 'Basic librarian:secret'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Material added', response.get_json()['message'])

    def test_borrow_material(self):
        user = mongo.db.users.find_one({'email': 'john@example.com'})
        material = mongo.db.materials.find_one({'title': 'The Great Gatsby'})
        response = self.client.post('/api/borrow', json={
            'user_id': str(user['_id']),
            'material_id': str(material['_id'])
        }, headers={'Authorization': 'Basic librarian:secret'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Material borrowed', response.get_json()['message'])

    def test_return_material(self):
        user = mongo.db.users.find_one({'email': 'john@example.com'})
        material = mongo.db.materials.find_one({'title': 'The Great Gatsby'})
        borrow_id = mongo.db.borrows.insert_one({
            'user_id': user['_id'],
            'material_id': material['_id'],
            'borrow_date': datetime.utcnow(),
            'return_date': None,
            'returned': False
        }).inserted_id
        response = self.client.post('/api/return', json={
            'borrow_id': str(borrow_id)
        }, headers={'Authorization': 'Basic librarian:secret'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Material returned', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()
