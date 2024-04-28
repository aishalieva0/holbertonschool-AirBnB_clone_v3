#!/usr/bin/python3
"""Review objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def return_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def return_review_id(review_id):
    """Retrieve a Review object using its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review_id(review_id):
    """Delete a Review object using its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return (jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """Create a Review object, use POST http method"""
    try:
        body = request.get_json()
    except Exception:
        return (jsonify({"error": "Not a JSON"}), 400)

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if "user_id" not in body:
        return (jsonify({"error": "Missing user_id"}), 400)
    user_id = body.get("user_id")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if "text" not in body:
        return (jsonify({"error": "Missing text"}), 400)

    body["place_id"] = place_id
    body["user_id"] = user_id
    obj = Review(**body)
    storage.new(obj)
    storage.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review_id(review_id):
    """Update a Review object using its id"""
    try:
        body = request.get_json()
    except Exception:
        return (jsonify({"error": "Not a JSON"}), 400)

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        ignore_key = ["id", "user_id", "place_id", "created_at", "updated_at"]
        for key, value in body.items():
            if key not in ignore_key:
                setattr(review, key, value)
            else:
                pass
        storage.save()
        return (jsonify(review.to_dict()), 200)
