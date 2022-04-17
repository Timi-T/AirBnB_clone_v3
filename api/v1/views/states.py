#!/usr/bin/python3
"""This script will contain a route for url"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def find_states():
    """This is the function that will list all states"""
    state_list = []
    for value in storage.all(State).values():
        state_list.append(value.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def find_state(state_id):
    """This function will return a state with the given id"""
    states_id = []
    for value in storage.all(State).values():
        states_id.append(value.id)
        if (state_id == value.id):
            return value.to_dict()
    if state_id not in states_id:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """This function will delete a class based on its id"""
    states_id = []
    for value in storage.all(State).values():
        states_id.append(value.id)
        if (state_id == value.id):
            storage.delete(value)
            storage.save()
            return {}, 200
    if state_id not in states_id:
        abort(404)


@app_views.route('/states/', methods=['POST'])
def create_state():
    """This funtion will create a class"""
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.get_json()
        if 'name' in json:
            state = State()
            for key, value in json.items():
                setattr(state, key, value)
            state.save()
            return state.to_dict(), 201
        else:
            return make_response(jsonify({'error': 'Missing name'}), 400)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """This function will update the given state in the id"""
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.get_json()
        states_id = []
        for state in storage.all(State).values():
            states_id.append(state.id)
            if (state.id == state_id):
                for key, value in json.items():
                    setattr(state, key, value)
                state.save()
                return state.to_dict(), 200
        if state_id not in states_id:
            abort(404)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
