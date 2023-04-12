from api.v1.views import app_views
from flask import jsonify

# Create a route


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON with the status"""
    return jsonify({"status": "OK"})
