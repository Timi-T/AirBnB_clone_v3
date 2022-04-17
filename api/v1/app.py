#!/usr/bin/python3
"""
create instance of flask app
"""

from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from api.v1.views import state_view
from api.v1.views import city_view
from api.v1.views import amenity_view
from api.v1.views import user_view
from api.v1.views import place_view
from api.v1.views import review_view
from api.v1.views import place_amenity_view
import os


try:
    host_address = os.getenv('HBNB_API_HOST')
except Exception:
    host_address = '0.0.0.0'

try:
    port_number = int(os.getenv('HBNB_API_PORT'))
except Exception:
    port_number = 5000

app = Flask(__name__)
app.register_blueprint(app_views)
app.register_blueprint(state_view)
app.register_blueprint(city_view)
app.register_blueprint(amenity_view)
app.register_blueprint(user_view)
app.register_blueprint(place_view)
app.register_blueprint(review_view)
app.register_blueprint(place_amenity_view)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def close_session(response_or_exc):
    """close current session"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """handle 404 (not found errors)"""
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    """handle error for unsupported data format"""
    if (error):
        return make_response(error, 400)

@app.errorhandler(400)
def bad_request(error):
    """handle error for unsupported data format"""
    return make_response("Not a JSON", 400)

if __name__ == "__main__":
    app.run(host=host_address, port=port_number, threaded=True)
