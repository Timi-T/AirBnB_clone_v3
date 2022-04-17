#!/usr/bin/python3
"""
Handles all API actions for state objects
"""

from models import storage
from models.state import State
from api.v1.views import state_view
from flask import jsonify, abort, request, make_response


@state_view.route('/states/<state_id>', strict_slashes=False)
@state_view.route('/states', strict_slashes=False)
def state_get(state_id=None):
    """
    Get method for all states
    if an id is present, the state associated is returned
    """

    if (state_id):
        ret_state = storage.get(State, state_id)
        if (ret_state):
            state_dict = ret_state.to_dict()
            return state_dict
        else:
            abort(404)
    all_states = storage.all(State)
    new_list = []
    for key, state in all_states.items():
        new_list.append(state.to_dict())
    return jsonify(new_list)


@state_view.route('/states/<state_id>', strict_slashes=False,
                  methods=['PUT'])
def state_update(state_id):
    """
    Update a state object in the database
    """

    state = storage.get(State, state_id)
    if (state):
        data = request.get_json()
        if (request.headers.get('Content-Type') == 'application/json'):
            state_dict = state.to_dict()
            for k, v in data.items():
                if (k != 'id' and k != 'created_at' and k != 'updated_at'):
                    state_dict[k] = v
            state.delete()
            updated_state = State(**state_dict)
            updated_state.save()
            ret = storage.get(State, state_id)
            return make_response(ret.to_dict(), 200)
        abort(400, "Not a JSON")
    abort(404)


@state_view.route('/states/<state_id>', strict_slashes=False,
                  methods=['DELETE'])
def state_delete(state_id):
    """
    Delete a state object
    """

    state = storage.get(State, state_id)
    if (state):
        state.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@state_view.route('/states', strict_slashes=False,
                  methods=['POST'])
def state_create():
    """
    Create a new state object
    """

    data = request.get_json()
    if not (data.get('name')):
        abort(400, "Missing name")
    if (request.headers.get('Content-Type') == 'application/json'):
        new_state = State(**data)
        new_state.save()
        from_db = storage.get(State, new_state.id)
        return make_response(jsonify(from_db.to_dict()), 201)
    abort(400)
