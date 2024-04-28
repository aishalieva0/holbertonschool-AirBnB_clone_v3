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


@app_views.route(
    "/states/<state_id>", methods=["GET", "DELETE", "PUT", "POST"], strict_slashes=False
)
def get(id):
    """Retrieves a State object"""
    state = storage.get(State, id)

    if not state:
        abort(404)

    if request.method == "GET":
        return jsonify(state.to_dict())

    if request.method == "DELETE":
        storage.delete(state)
        return jsonify({}), 200

    if request.method == "PUT":
        data = request.get_json()
        if not data:
            abort(404, description="Not a JSON")
        for key, val in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, val)
        storage.save()
        return jsonify(state.to_dict()), 200

    if request.method == "POST":
        data = request.get_json()
        if not data:
            abort(404, description="Not a JSON")
        if "name" not in data:
            abort(400, description="Missing name")
        new_state = State(**data)
        storage.new(new_state)
        storage.save()
        return jsonify(state.to_dict()), 201
