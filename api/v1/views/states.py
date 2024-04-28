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


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    ''' Create a State object, use POST http method '''
    body = request.get_json()
    if body is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    obj = State(**body)

    if 'name' not in body:
        return (jsonify({'error': 'Mising name'}), 400)
    else:
        storage.new(obj)
        storage.save()
        return (jsonify(obj.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, val)
    storage.save()
    return jsonify(state.to_dict()), 200
