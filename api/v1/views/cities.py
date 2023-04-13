#!/usr/bin/python3
"""Index, Route /status, cities view"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_all_citiess():
    """Retrieve the list of all Amenity objects"""
    cities = storage.all(City).values()
    cities_dict = [city.to_dict() for city in cities]
    return jsonify(cities_dict)

@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """Retrieve the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieve a City object from city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object from city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    city = City(**request.json)
    city.state_id = state_id
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update City object using city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
