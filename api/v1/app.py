#!/usr/bin/python3
"""API"""
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found"}


@app.teardown_appcontext
def tearDown(self):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
