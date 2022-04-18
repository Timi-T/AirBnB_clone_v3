#!/usr/bin/python3
"""
Handles all API actions for state objects
"""

from models import storage
from models.amenity import Amenity
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
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


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
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


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def amenity_delete(place_id, amenity_id):
    """
    Delete a amenity object linked to a place
    """

    place = storage.get(Place, place_id)
    if (place):
        amenities = place.amenities
        found = 0
        i = 0
        for amen in amenities:
            if (amen.id == amenity_id):
                found = 1
                break
            i += 1
        if (found == 1):
            amenities.pop(i)
            storage.save()
            return make_response(jsonify({}), 200)
        abort(404)
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def amenity_create(place_id, amenity_id):
    """
    Create a new amenity object
    """

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if (place and amenity):
        amenities = place.amenities
        for amen in amenities:
            if (amen.id == amenity_id):
                return make_response(jsonify(amen.to_dict()), 200)
        amenities.append(amenity)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)
    abort(404)
