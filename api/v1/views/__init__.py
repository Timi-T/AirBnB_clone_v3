#!/usr/bin/python3
"""
initialize the web application
"""

from flask import Blueprint, jsonify, url_for


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
state_view = Blueprint('state_view', __name__, url_prefix='/api/v1')
city_view = Blueprint('city_view', __name__, url_prefix='/api/v1')
amenity_view = Blueprint('amenity_view', __name__, url_prefix='/api/v1')
user_view = Blueprint('user_view', __name__, url_prefix='/api/v1')
place_view = Blueprint('place_view', __name__, url_prefix='/api/v1')
review_view = Blueprint('review_view', __name__, url_prefix='/api/v1')
place_amenity_view = Blueprint('place_amenity_view', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
