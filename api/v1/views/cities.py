#!/usr/bin/python3
"""This function will be application logic for city"""
from flask import request, jsonify, make_response, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def find_cities(state_id):
    """This function will find the cities id from states"""
    state = storage.get(State, state_id)
    if (state):
        new_list = []
        cities = state.cities
        for city in cities:
            new_list.append(city.to_dict())
        return jsonify(new_list)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def find_city(city_id):
    """This function will find the city of given ID"""
    city = storage.get(City, city_id)
    if (city):
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """This function will delete a city based on its ID"""
    city = storage.get(City, city_id)
    if (city):
        city.delete()
        storage.save()
        return {}, 200
    else:
        abort(404)

@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """This function will create a city"""
    content_header = request.headers.get('Content-Type')
    if (content_header == 'application/json'):
        state_list = []
        json = request.get_json()
        for state in storage.all(State).values():
            state_list.append(state.id)
            if state.id == state_id:
                city = City()
                if 'name' in json:
                    city.name = json['name']
                else:
                    return make_response(jsonify({'error': 'Missing name'}),
                                         400)
                city.state_id = state.id
                for key, value in json.items():
                    setattr(city, key, value)
                city.save()
                return city.to_dict(), 201
        if state_id not in state_list:
            abort(404)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """This function will uodate the city by the given ID"""
    city = storage.get(City, city_id)
    if (city):
        data = request.get_json()
        if (request.headers.get('Content-Type') == 'application/json'):
            city_dict = city.to_dict()
            for k, v in data.items():
                if (k != 'id' and k != 'created_at' and k != 'updated_at'):
                    city_dict[k] = v
                    city.delete()
                    updated_city = City(**city_dict)
                    updated_city.save()
                    ret = storage.get(City, city_id)
                    return ret.to_dict(), 200
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        abort(404)
