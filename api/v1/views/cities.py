#!/usr/bin/python3
"""This function will be application logic for Place"""
from flask import request, jsonify, make_response, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def find_cities(state_id):
    """This function will find the cities id from state"""
    state = storage.get(State, state_id)
    if state:
        city_list = []
        for city in storage.all(City).values():
            if state.id == city.state_id:
                city_list.append(city.to_dict())
            else:
                continue
        return jsonify(city_list)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET'])
def find_city(city_id):
    """This function will find the city of given ID"""
    city_list = []
    for city in storage.all(City).values():
        city_list.append(city.id)
        if city_id == city.id:
            return city.to_dict()
    if city_id not in city_list:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """This function will delete a city based on its ID"""
    city_list = []
    for city in storage.all(City).values():
        city_list.append(city.id)
        if city.id == city_id:
            storage.delete(city)
            storage.save()
            return {}, 200
    if city_id not in city_list:
        abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """This function will create a city"""
    state = storage.get(State, state_id)
    if state:
        content_header = request.headers.get('Content-Type')
        if (content_header == 'application/json'):
            json = request.get_json()
            if 'name' in json:
                city = City()
                city.state_id = state_id
                for key, value in json.items():
                    setattr(city, key, value)
                city.save()
                return city.to_dict(), 201
            else:
                return make_response(jsonify({'error': 'Missing name'}), 400)
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id):
    """This function will update the city by the given ID"""
    city = storage.get(City, city_id)
    if city:
        content_header = request.headers.get('Content-Type')
        if (content_header == 'application/json'):
            json = request.get_json()
            for key, value in json.items():
                setattr(city, key, value)
            city.save()
            return city.to_dict(), 200
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        abort(404)
