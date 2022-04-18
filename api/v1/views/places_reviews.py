#!/usr/bin/python3
"""This function will be application logic for Review"""
from flask import request, jsonify, make_response, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def find_reviews(place_id):
    """This function will find the review id from place"""
    place = storage.get(Place, place_id)
    if place:
        review_list = []
        for review in storage.all(Review).values():
            if place.id == review.place_id:
                review_list.append(review.to_dict())
            else:
                continue
        return jsonify(review_list)
    else:
        abort(404)

@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def find_review(review_id):
    """This function will find the review of given ID"""
    review_list = []
    for review in storage.all(Review).values():
        review_list.append(review.id)
        if review_id == review.id:
            return review.to_dict()
    if review_id not in review_list:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """This function will delete a review based on its ID"""
    review_list = []
    for review in storage.all(Review).values():
        review_list.append(review.id)
        if review.id == review_id:
            storage.delete(review)
            storage.save()
            return {}, 200
    if review_id not in review_list:
        abort(404)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """This function will create a review"""
    place = storage.get(Place, place_id)
    if place:
        content_header = request.headers.get('Content-Type')
        if (content_header == 'application/json'):
            json = request.get_json()
            if 'user_id' not in json:
                return make_response(jsonify({'error': 'Missing user_id'}),
                                     400)
            user = storage.get(User, json['user_id'])
            if user is None:
                abort(404)
            if 'text' not in json:
                return make_response(jsonify({'error': 'Missing text'}), 400)
            review = Review()
            review.place_id = place.id
            for key, value in json.items():
                setattr(review, key, value)
            review.save()
            return review.to_dict(), 201
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """This function will update the review by the given ID"""
    review = storage.get(Review, review_id)
    if review:
        content_header = request.headers.get('Content-Type')
        if (content_header == 'application/json'):
            json = request.get_json()
            for key, value in json.items():
                setattr(review, key, value)
            review.save()
            return review.to_dict(), 200
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        abort(404)
