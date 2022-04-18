#!/usr/bin/python3
"""This script will contain a application logic to user"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def find_users():
    """This is the function that will list all users"""
    user_list = []
    for user in storage.all(User).values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def find_user(user_id):
    """This function will return a user with the given id"""
    user_list = []
    for user in storage.all(User).values():
        user_list.append(user.id)
        if (user_id == user.id):
            return user.to_dict()
    if user_id not in user_list:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """This function will delete a user instance based on its id"""
    user_list = []
    for user in storage.all(User).values():
        user_list.append(user.id)
        if (user_id == user.id):
            storage.delete(user)
            storage.save()
            return {}, 200
    if user_id not in user_list:
        abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """This funtion will create a user"""
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.get_json()
        if 'email' not in json:
            return make_response(jsonify({'error': 'Missing email'}), 400)
        if 'password' not in json:
            return make_response(jsonify({'error': 'Missing password'}), 400)
        user = User(**json)
        user.save()
        return user.to_dict(), 201
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """This function will update the given user in the id"""
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.get_json()
        user_list = []
        for user in storage.all(User).values():
            user_list.append(user.id)
            if (user.id == user_id):
                for key, value in json.items():
                    setattr(user, key, value)
                user.save()
                return user.to_dict(), 200
        if user_id not in user_list:
            abort(404)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
