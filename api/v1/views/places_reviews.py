#!/usr/bin/python3
"""
Handles all API actions for state objects
"""

from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import review_view
from flask import jsonify, abort, request, make_response


@review_view.route('/places/<place_id>/reviews', strict_slashes=False)
def reviews_get(place_id):
    """
    Get method for all reviews linked to a state
    """

    place = storage.get(Place, place_id)
    if (place):
        new_list = []
        reviews = place.reviews
        for review in reviews:
            new_list.append(review.to_dict())
        return jsonify(new_list)
    abort(404)


@review_view.route('/reviews/<place_id>', strict_slashes=False)
def review_get(place_id):
    """
    Get a review using its id
    """

    review = storage.get(Review, place_id)
    if (review):
        return jsonify(review.to_dict())
    abort(404)


@review_view.route('/reviews/<review_id>', strict_slashes=False,
                   methods=['PUT'])
def state_update(review_id):
    """
    Update a state object in the database
    """

    if (request.headers.get('Content-Type') == 'application/json'):
        review = storage.get(Review, review_id)
        if (review):
            data = request.get_json()
            review_dict = review.to_dict()
            for k, v in data.items():
                if (k != 'id' and k != 'created_at' and k != 'updated_at'
                        and k != 'user_id' and k != 'place_id'):
                    review_dict[k] = v
            review.delete()
            updated_review = Review(**review_dict)
            updated_review.save()
            ret = storage.get(Review, review_id)
            return make_response(ret.to_dict(), 200)
        abort(404)
    abort(400, "Not a JSON")


@review_view.route('/reviews/<place_id>', strict_slashes=False,
                   methods=['DELETE'])
def review_delete(place_id):
    """
    Delete a review object
    """

    review = storage.get(Review, place_id)
    if (review):
        review.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@review_view.route('/places/<place_id>/reviews', strict_slashes=False,
                   methods=['POST'])
def review_create(place_id):
    """
    Create a new review object
    """

    if (request.headers.get('Content-Type') == 'application/json'):
        place = storage.get(Place, place_id)
        if (place):
            data = request.get_json()
            if not (data.get('text')):
                abort(400, "Missing text")
            if not (data.get('user_id')):
                abort(400, "Missing user_id")
            user = storage.get(User, data.get('user_id'))
            if not (user):
                abort(404)
            data['place_id'] = place_id
            new_review = Review(**data)
            new_review.save()
            from_db = storage.get(Review, new_review.id)
            return make_response(jsonify(from_db.to_dict()), 201)
        abort(404)
    abort(400, "Not a JSON")
