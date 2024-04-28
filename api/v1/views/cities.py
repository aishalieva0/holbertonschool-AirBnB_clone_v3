#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_all(state_id):
    """Retrieves the list of all City objects"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)

    cities = []
    for city in states.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/cities", methods=["POST"], strict_slashes=False)
def create(state_id):
    """Creates a City object"""
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if "name" not in data:
        return (jsonify({"error": "Missing name"}), 400)

    data["state_id"] = state_id
    new_city = City(**data)

    storage.new(new_city)
    storage.save()
    return (jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, val)
    storage.save()
    return jsonify(city.to_dict()), 200
