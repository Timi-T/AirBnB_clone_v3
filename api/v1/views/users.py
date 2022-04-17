#!/usr/bin/python3
"""
Handles all API actions for state objects
"""

from models import storage
from models.user import User
from api.v1.views import user_view
from flask import jsonify, abort, request, make_response


@user_view.route('/users/<user_id>', strict_slashes=False)
@user_view.route('/users', strict_slashes=False)
def user_get(user_id=None):
    """
    Get method to get all users
    if an id is present, the user associated is returned
    """

    if (user_id):
        ret_user = storage.get(User, user_id)
        if (ret_user):
            user_dict = ret_user.to_dict()
            return user_dict
        else:
            abort(404)
    all_users = storage.all(User)
    new_list = []
    for key, user in all_users.items():
        new_list.append(user.to_dict())
    return jsonify(new_list)


@user_view.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def user_update(user_id):
    """
    Update a user object in the database
    """

    user = storage.get(User, user_id)
    if (user):
        data = request.get_json()
        if (request.headers.get('Content-Type') == 'application/json'):
            user_dict = user.to_dict()
            for k, v in data.items():
                if (k != 'id' and k != 'created_at' and k != 'updated_at'
                        and k != 'email'):
                    user_dict[k] = v
            user.delete()
            updated_user = User(**user_dict)
            updated_user.save()
            ret = storage.get(User, user_id)
            return make_response(ret.to_dict(), 200)
        abort(400, "Not a JSON")
    abort(404)


@user_view.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def user_delete(user_id):
    """
    Delete an user object
    """

    user = storage.get(User, user_id)
    if (user):
        user.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@user_view.route('/users', strict_slashes=False,
                 methods=['POST'])
def user_create():
    """
    Create a new user object
    """

    data = request.get_json()
    if not (data.get('email')):
        abort(400, "Missing email")
    if not (data.get('password')):
        abort(400, "Missing password")
    if (request.headers.get('Content-Type') == 'application/json'):
        new_user = User(**data)
        new_user.save()
        from_db = storage.get(User, new_user.id)
        return make_response(jsonify(from_db.to_dict()), 201)
    abort(400)
