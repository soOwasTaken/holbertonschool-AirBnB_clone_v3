#!/usr/bin/python3
"""app v1 port set to 5050"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
import os
app = Flask(__name__)
app.register_blueprint(app_views)


def teardown_storage(exception):
    """Closes the storage connection"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """ all ips, port 5050"""
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5050))

    app.run(host=host, port=port, threaded=True)
