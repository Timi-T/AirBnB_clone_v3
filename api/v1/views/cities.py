#!/usr/bin/python3
"""
Handles all API actions for state objects
"""

from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities_get(state_id):
    """
    Get method for all cities linked to a state
    """
    state = storage.get(State, state_id)
    if (state):
        new_list = []
        cities = state.cities
        for city in cities:
            new_list.append(city.to_dict())
        return jsonify(new_list)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def city_get(city_id):
    """
    Get a city using its id"""
    city = storage.get(City, city_id)
    if (city):
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def state_update(city_id):
    """
    Update a state object in the database
    """
    city = storage.get(City, city_id)
    if (city):
        data = request.get_json()
        if (request.headers.get('Content-Type') == 'application/json'):
            for k, v in data.items():
                if (k != 'id' and k != 'created_at' and k != 'updated_at'):
                    setattr(city, k, v)
                    return city.to_dict(), 200
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_delete(city_id):
    """
    Delete a city object
    """
    city = storage.get(City, city_id)
    if (city):
        storage.delete(city)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def city_create(state_id):
    """
    Create a new city object
    """
    state = storage.get(State, state_id)
    if (state):
        data = request.get_json()
        if (request.headers.get('Content-Type') == 'application/json'):
            if 'name' not in data:
                return make_response(jsonify({'error': 'Missing name'}), 400)
            else:
                city = City()
                city.state_id = state.id
                for key, value in data.items():
                    setattr(city, key, value)
                city.save()
                return city.to_dict(), 201
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
    abort(404)
