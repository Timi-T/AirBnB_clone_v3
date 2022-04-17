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
    city_list = []
    for city in storage.all(City).values():
        city_list.append(city.id)
        if city.id == city_id:
            storage.delete(city)
            storage.save()
            return {}, 200
    if city_id not in city_list:
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
    content_header = request.headers.get('Content-Type')
    if (content_header == 'application/json'):
        city_list = []
        json = request.get_json()
        for city in storage.all(City).values():
            city_list.append(city.id)
            if city.id == city_id:
                for key, value in json.items():
                    setattr(city, key, value)
                city.save()
                return city.to_dict(), 200
        if city_id not in city_list:
            abort(404)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
