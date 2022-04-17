#!/usr/bin/python3
"""
Handles all API actions for state objects
"""

from models import storage
from models.place import Place
from models.state import City
from models.user import User
from api.v1.views import place_view
from flask import jsonify, abort, request, make_response


@place_view.route('/cities/<city_id>/places', strict_slashes=False)
def places_get(city_id):
    """
    Get method for all places linked to a state
    """

    city = storage.get(City, city_id)
    if (city):
        new_list = []
        places = city.places
        for place in places:
            new_list.append(place.to_dict())
        return jsonify(new_list)
    abort(404)


@place_view.route('/places/<place_id>', strict_slashes=False)
def place_get(place_id):
    """
    Get a place using its id
    """

    place = storage.get(Place, place_id)
    if (place):
        return jsonify(place.to_dict())
    abort(404)


@place_view.route('/places/<place_id>', strict_slashes=False,
                  methods=['PUT'])
def state_update(place_id):
    """
    Update a state object in the database
    """

    place = storage.get(Place, place_id)
    if (place):
        data = request.get_json()
        if (request.headers.get('Content-Type') == 'application/json'):
            place_dict = place.to_dict()
            for k, v in data.items():
                if (k != 'id' and k != 'created_at' and k != 'updated_at'
                        and k != 'user_id' and k != 'city_id'):
                    place_dict[k] = v
            place.delete()
            updated_place = Place(**place_dict)
            updated_place.save()
            ret = storage.get(Place, place_id)
            return make_response(ret.to_dict(), 200)
        abort(400, "Not a JSON")
    abort(404)


@place_view.route('/places/<place_id>', strict_slashes=False,
                  methods=['DELETE'])
def place_delete(place_id):
    """
    Delete a place object
    """

    place = storage.get(Place, place_id)
    if (place):
        place.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@place_view.route('/cities/<city_id>/places', strict_slashes=False,
                  methods=['POST'])
def place_create(city_id):
    """
    Create a new place object
    """

    if (request.headers.get('Content-Type') == 'application/json'):
        city = storage.get(City, city_id)
        if (city):
            data = request.get_json()
            if not (data.get('name')):
                abort(400, "Missing name")
            if not (data.get('user_id')):
                abort(400, "Missing user_id")
            user = storage.get(User, data.get('user_id'))
            if not (user):
                abort(404)
            data['city_id'] = city_id
            new_place = Place(**data)
            new_place.save()
            from_db = storage.get(Place, new_place.id)
            return make_response(jsonify(from_db.to_dict()), 201)
        abort(404)
    abort(400, "Not a JSON")
