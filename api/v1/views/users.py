#!/usr/bin/python3
"""user objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a User object"""
    try:
        data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    if "name" not in data:
        return jsonify({'error': 'Missing name'}), 400

    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, val)
    storage.save()
    return jsonify(user.to_dict()), 200
