# app/models.py

from .extensions import mongo
from datetime import datetime

class User:
    def add_user(self, name, email):
        return mongo.db.users.insert_one({
            'name': name,
            'email': email,
            'borrowed_materials': []
        })

    def get_user_by_email(self, email):
        return mongo.db.users.find_one({'email': email})

class Material:
    def add_material(self, title, author, year, type):
        return mongo.db.materials.insert_one({
            'title': title,
            'author': author,
            'year': year,
            'type': type,
            'available': True
        })

class Borrow:
    def borrow_material(self, user_id, material_id):
        return mongo.db.borrows.insert_one({
            'user_id': user_id,
            'material_id': material_id,
            'borrow_date': datetime.utcnow(),
            'return_date': None,
            'returned': False
        })

    def return_material(self, borrow_id):
        return mongo.db.borrows.update_one(
            {'_id': borrow_id},
            {'$set': {'returned': True, 'return_date': datetime.utcnow()}}
        )
