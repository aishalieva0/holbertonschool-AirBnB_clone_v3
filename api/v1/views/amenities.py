#!/usr/bin/python3
"""amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(SAmenitytate).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def get(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create():
    """Creates a Amenity object"""
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    new_amenity = Amenity(**data)

    if "name" not in data:
        return (jsonify({"error": "Missing name"}), 400)
    else:
        storage.new(new_amenity)
        storage.save()
        return (jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def update(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, val)
    storage.save()
    return jsonify(amenity.to_dict()), 200
