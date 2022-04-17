#!/usr/bin/python3
"""This function will be application logic for Place"""
from flask import request, jsonify, make_response, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User

@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def find_placess(city_id):
    """This function will find the placess id from city"""
    city = storage.get(City, city_id)
    if city:
        place_list = []
        for place in storage.all(Place).values():
            if city.id == place.city_id:
                place_list.append(place.to_dict())
            else:
                continue
        return jsonify(place_list)
    else:
        abort(404)

@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def find_place(place_id):
    """This function will find the place of given ID"""
    place_list = []
    for place in storage.all(Place).values():
        place_list.append(place.id)
        if place_id == place.id:
            return place.to_dict()
    if place_id not in place_list:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """This function will delete a place based on its ID"""
    place_list = []
    for place in storage.all(Place).values():
        place_list.append(place)
        if place.id == place_id:
            storage.delete(place)
            storage.save()
            return {}, 200
    if place_id not in place_list:
        abort(404)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """This function will create a Place"""
    city = storage.get(City, city_id)
    if city:
        content_header = request.headers.get('Content-Type')
        if (content_header == 'application/json'):
            json = request.get_json()
            if 'user_id' not in json:
                return make_response(jsonify({'error': 'Missing user_id'}),
                                     400)
            user = storage.get(User, json['user_id'])
            if user is None:
                abort(404)
            if 'name' not in json:
                return make_response(jsonify({'error': 'Missing name'}), 400)
            place = Place()
            for key, value in json.items():
                setattr(place, key, value)
            place.save()
            return place.to_dict(), 201
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """This function will update the place by the given ID"""
    place = storage.get(Place, place_id)
    if place:
        content_header = request.headers.get('Content-Type')
        if (content_header == 'application/json'):
            json = request.get_json()
            for key, value in json.items():
                setattr(place, key, value)
            place.save()
            return place.to_dict(), 200
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        abort(404)
