#!/usr/bin/python3
from flask import Flask
from api.v1.views import app_views
from models import storage
import os
app = Flask(__name__)
app.register_blueprint(app_views)


def teardown_storage(exception):
    """Closes the storage connection"""
    storage.close()


if __name__ == "__main__":
    # Get the host and port from environment variables, or use default values
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5050))

    app.run(host=host, port=port, threaded=True)
