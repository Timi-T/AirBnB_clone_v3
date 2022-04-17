#!/usr/bin/python3
"""
Handles all API actions for state objects
"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def cities_get(state_id):
    """
    Get method for all cities linked to a state
    """
    state = storage.get(State, state_id)
    if (state):
        new_list = []
        cities = state.cities:
        for city in cities:
            new_list.append(city.to_dict())
        return jsonify(new_list)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET'])
def city_get(city_id):
    """
    Get a city using its id
    """
    city = storage.get(City, city_id)
    if (city):
        return jsonify(city.to_dict())
    else:
        abort(404)

@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def state_update(city_id):
    """
    Update a state object in the database
    """
    city = storage.get(City, city_id)
    if (city):
        data = request.get_json()
        if (request.headers.get('Content-Type') == 'application/json'):
            city_dict = city.to_dict()
            for k, v in data.items():
                if (k != 'id' and k != 'created_at' and
                        k != 'updated_at' and k != 'state_id'):
                    city_dict[k] = v
            city.delete()
            updated_city = City(**city_dict)
            updated_city.save()
            ret = storage.get(City, city_id)
            return make_response(ret.to_dict(), 200)
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def city_delete(city_id):
    """
    Delete a city object
    """
    city = storage.get(City, city_id)
    if (city):
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)

@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def city_create(state_id):
    """
    Create a new city object
    """
    state = storage.get(State, state_id)
    if (state):
        data = request.get_json()
        if not (data.get('name')):
            return make_response(jsonify({'error': 'Missing name'}), 400)
        if (request.headers.get('Content-Type') == 'application/json'):
            data['state_id'] = state_id
            new_city = City(**data)
            new_city.save()
            from_db = storage.get(City, new_city.id)
            return make_response(jsonify(from_db.to_dict()), 201)
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        abort(404)
