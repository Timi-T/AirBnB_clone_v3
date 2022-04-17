#!/usr/bin/python3
"""This function will be the application logic of amenities"""
from flask import abort, make_response, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def find_amenities():
    """This function will return all the amenities"""
    amenity_list = []
    for amenity in storage.all(Amenity).values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def find_amenity(amenity_id):
    """This will return the name of amenity from an id"""
    amenity_list = []
    for amenity in storage.all(Amenity).values():
        amenity_list.append(amenity.id)
        if amenity.id == amenity_id:
            return amenity.to_dict()
    if amenity_id not in amenity_list:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """This function will delete the amenity based on the id given"""
    amenity_list = []
    for amenity in storage.all(Amenity).values():
        amenity_list.append(amenity.id)
        if amenity_id == amenity.id:
            storage.delete(amenity)
            storage.save()
            return {}, 200
    if amenity_id not in amenity_list:
        abort(404)


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """This funtion will create a amenity"""
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.get_json()
        if 'name' in json:
            amenity = Amenity()
            for key, value in json.items():
                setattr(amenity, key, value)
            amenity.save()
            return amenity.to_dict(), 201
        else:
            return make_response(jsonify({'error': 'Missing name'}), 400)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """This funtion will update the given amenity ID"""
    content_header = request.headers.get('Content-Type')
    if content_header == 'application/json':
        amenity_list = []
        json = request.get_json()
        for amenity in storage.all(Amenity).values():
            amenity_list.append(amenity.id)
            if amenity_id == amenity.id:
                for key, value in json.items():
                    setattr(amenity, key, value)
                amenity.save()
                return amenity.to_dict(), 200
        if amenity_id not in amenity_list:
            abort(404)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
