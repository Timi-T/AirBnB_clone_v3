#!/usr/bin/python3
"""
index route
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.review import Review


@app_views.route('/status')
def status():
    """display status"""
    return jsonify({'status': "OK"})


@app_views.route('/stats')
def stats():
    """get the count of each object in the storage"""

    new_dict = {}
    new_dict['amenities'] = storage.count(Amenity)
    new_dict['cities'] = storage.count(City)
    new_dict['places'] = storage.count(Place)
    new_dict['reviews'] = storage.count(Review)
    new_dict['states'] = storage.count(State)
    new_dict['users'] = storage.count(User)
    return jsonify(new_dict)
