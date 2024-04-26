#!/usr/bin/python3
""" return the status of your API"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.review import Review
from models.place import Place
from models.user import User
from models.amenity import Amenity
from flask import jsonify


@app_views.route("/status")
def get_status():
    return {"status": "OK"}


@app_views.route("/api/v1/stats")
def get_count():
    """retrieves the number of each objects by type"""
    states = storage.count(State)
    cities = storage.count(City)
    reviews = storage.count(Review)
    places = storage.count(Place)
    users = storage.count(User)
    amenities = storage.count(Amenity)

    dict = {
        "states": states,
        "cities": cities,
        "reviews": reviews,
        "places": places,
        "users": users,
        "amenities": amenities,
    }

    return jsonify(dict)
