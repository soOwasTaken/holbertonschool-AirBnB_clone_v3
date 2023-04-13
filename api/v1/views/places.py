#!/usr/bin/python3
"""Index, Route /status, places view"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def get_all_placess():
    """Retrieve the list of all State objects"""
    places = storage.all(Place).values()
    places = [place.to_dict() for place in places]
    return jsonify(places)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """Retrieve the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = []
    places = storage.all(Place).values()
    for place in places:
        if place.city_id == city_id:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object from place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object from place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request.json:
        abort(400, 'Missing name')
    place = Place(**request.json)
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update Place object using place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
