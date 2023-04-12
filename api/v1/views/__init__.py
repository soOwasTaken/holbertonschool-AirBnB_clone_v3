from flask import Blueprint

# Create a Blueprint instance
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import the routes
from api.v1.views.index import *