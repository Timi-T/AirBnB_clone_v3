#!/usr/bin/python3
"""This script will contain the blue print registration"""
from flask import Flask, make_response, jsonify
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """This function will close a session and reload"""
    storage.close()


@app.errorhandler(404)
def error(error):
    """This function will give a jsonfile when there is an error"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST'), port=os.getenv('HBNB_API_PORT'),
            threaded=True)
