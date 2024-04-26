#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def get(id):
    """Retrieves a State object"""
    state = storage.get(State, id)

    if not state:
        abort(404)

    if request.method == "GET":
        return state.to_dict()
    
    if request.method == "GET":
        storage.delete(state)
        return jsonify({}), 200
            
