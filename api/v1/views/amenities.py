#!/usr/bin/python3
"""
Handles all API actions for state objects
"""

from models import storage
from models.amenity import Amenity
from api.v1.views import amenity_view
from flask import jsonify, abort, request, make_response

@amenity_view.route('/amenities/<amenity_id>', strict_slashes=False)
@amenity_view.route('/amenities', strict_slashes=False)
def amenity_get(amenity_id=None):
    """
    Get method to get all amenities
    if an id is present, the amenity associated is returned
    """

    if (amenity_id):
        ret_amenity = storage.get(Amenity, amenity_id)
        if (ret_amenity):
            amenity_dict = ret_amenity.to_dict()
            return amenity_dict
        else:
            abort(404)
    all_amenities = storage.all(Amenity)
    new_list = []
    for key,amenity in all_amenities.items():
        new_list.append(amenity.to_dict())
    return jsonify(new_list)

@amenity_view.route('/amenities/<amenity_id>', strict_slashes=False,
                   methods=['PUT'])
def amenity_update(amenity_id):
    """
    Update a amenity object in the database
    """

    amenity = storage.get(Amenity, amenity_id)
    if (amenity):
        data = request.get_json()
        if (request.headers.get('Content-Type') == 'application/json'):
            amenity_dict = amenity.to_dict()
            for k, v in data.items():
                if (k != 'id' and k != 'created_at' and k != 'updated_at'):
                    amenity_dict[k] = v
            amenity.delete()
            updated_amenity = Amenity(**amenity_dict)
            updated_amenity.save()
            ret = storage.get(Amenity, amenity_id)
            return make_response(ret.to_dict(), 200)
        abort(400, "Not a JSON")
    abort(404)

@amenity_view.route('/amenities/<amenity_id>', strict_slashes=False,
                  methods=['DELETE'])
def amenity_delete(amenity_id):
    """
    Delete an amenity object
    """

    amenity = storage.get(Amenity, amenity_id)
    if (amenity):
        amenity.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)

@amenity_view.route('/amenities', strict_slashes=False,
                  methods=['POST'])
def amenity_create():
    """
    Create a new amenity object
    """

    data = request.get_json()
    if not (data.get('name')):
        abort(400, "Missing name")
    if (request.headers.get('Content-Type') == 'application/json'):
        new_amenity = Amenity(**data)
        new_amenity.save()
        from_db = storage.get(Amenity, new_amenity.id)
        return make_response(jsonify(from_db.to_dict()), 201)
    abort(400)

























































