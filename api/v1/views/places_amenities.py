#!/usr/bin/python3
"""
Handles all API actions for state objects
"""

from models import storage
from models.amenity import Amenity
from models.place import Place
from api.v1.views import place_amenity_view
from flask import jsonify, abort, request, make_response

@place_amenity_view.route('/places/<place_id>/amenities', strict_slashes=False)
def place_amenities_get(place_id):
    """
    Get method for all amenities linked to a state
    """

    place = storage.get(Place, place_id)
    if (place):
        new_list = []
        amenities = place.amenities
        for amenity in amenities:
            new_list.append(amenity.to_dict())
        return jsonify(new_list)
    abort(404)

@place_amenity_view.route('/places/<place_id>/amenities/<amenity_id>',
                          strict_slashes=False)
def amenity_get(place_id, amenity_id):
    """
    Get a amenity using its id
    """

    place = storage.get(Place, place_id)
    if (place):
        new_list = []
        amenities = place.amenities
        for amenity in amenities:
            if (amenity.id == amenity_id):
                new_list.append(amenity.to_dict())
        return jsonify(new_list)
    abort(404)

@place_amenity_view.route('/places/<place_id>/amenities/<amenity_id>',
                    strict_slashes=False, methods=['DELETE'])
def amenity_delete(place_id, amenity_id):
    """
    Delete a amenity object linked to a place
    """

    if (os.getenv('HBNB_TYPE_STORAGE') != 'db'):
        place = storage.get(Place, place_id)
        if (place):
            amenities = place.amenities()
            for amen in amenities:
                if (amen.id == amenity_id):
                    amenities.pop(amen)
                    storage.save()
                    return make_response(jsonify({}), 200)
            abort(404)
        abort(404)
    place = storage.get(Place, place_id)
    if (place):
        amenity = storage.get(Amenity, amenity_id)
        if (amenity):
            amenities = place.amenities
            if (amenity in amenities):
                place.remove(amenity)
                return make_response(jsonify({}), 200)
            abort(404)
        abort(404)
    abort(404)

@place_amenity_view.route('/places/<place_id>/amenities/amenity_id', strict_slashes=False,
                  methods=['POST'])
def amenity_create(amenity_id):
    """
    Create a new amenity object
    """

    amenity = storage.get(Place, place_id)
    if (amenity):
        data = request.get_json()
        if not (data.get('name')):
            abort(400, "Missing name")
        if not (data.get('user_id')):
            abort(400, "Missing user_id")
        user = storage.get(User, data.get('user_id'))
        if not (user):
            abort(404)
        if (request.headers.get('Content-Type') == 'application/json'):
            data['amenity_id'] = place_id
            new_amenity = Amenity(**data)
            new_amenity.save()
            from_db = storage.get(Amenity, new_amenity.id)
            return make_response(jsonify(from_db.to_dict()), 201)
        abort(400)
    abort(404)
