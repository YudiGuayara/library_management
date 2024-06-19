# app/controllers.py

from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
from .extensions import mongo

bp = Blueprint('library', __name__)

@bp.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    try:
        # Intentar una operación simple en la base de datos
        mongo.db.command('ping')
        return jsonify({'message': 'Successfully connected to the database'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/materials', methods=['POST'])
def add_material():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    material = {
        'title': data['title'],
        'author': data['author'],
        'year': data['year'],
        'type': data['type'],
        'available': True
    }
    result = mongo.db.materials.insert_one(material)
    return jsonify({'message': 'Material added', 'material_id': str(result.inserted_id)}), 201

@bp.route('/materials/<material_id>', methods=['GET'])
def get_material(material_id):
    if not ObjectId.is_valid(material_id):
        return jsonify({'error': 'Invalid material ID'}), 400
    material = mongo.db.materials.find_one({'_id': ObjectId(material_id)})
    if material:
        material['_id'] = str(material['_id'])
        return jsonify(material), 200
    else:
        return jsonify({'error': 'Material not found'}), 404

@bp.route('/materials', methods=['GET'])
def get_all_materials():
    materials = list(mongo.db.materials.find())
    for material in materials:
        material['_id'] = str(material['_id'])
    return jsonify(materials), 200

@bp.route('/borrow', methods=['POST'])
def borrow_material():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    try:
        borrow = {
            'user_id': ObjectId(data['user_id']),
            'material_id': ObjectId(data['material_id']),
            'borrow_date': datetime.utcnow(),
            'return_date': None,
            'returned': False
        }
        result = mongo.db.borrows.insert_one(borrow)
        return jsonify({'message': 'Material borrowed', 'borrow_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/return', methods=['POST'])
def return_material():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    try:
        borrow_id = ObjectId(data['borrow_id'])
        borrow = mongo.db.borrows.find_one({'_id': borrow_id})
        if not borrow:
            return jsonify({'error': 'Borrow not found'}), 404

        if borrow['returned']:
            return jsonify({'error': 'Material already returned'}), 400

        update_result = mongo.db.borrows.update_one(
            {'_id': borrow_id},
            {'$set': {'returned': True, 'return_date': datetime.utcnow()}}
        )

        if update_result.modified_count == 1:
            return jsonify({'message': 'Material returned'}), 200
        else:
            return jsonify({'error': 'Failed to return material'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400
