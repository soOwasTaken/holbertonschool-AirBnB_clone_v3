#!/usr/bin/python3
"""app v1 port set to 5050"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


def teardown_storage(exception):
    """Closes the storage connection"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)