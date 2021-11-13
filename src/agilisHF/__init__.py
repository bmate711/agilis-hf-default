"""
agilisHF - A small API for managing dog recipes.
"""

from datetime import datetime
import os

from pymongo.collection import Collection, ReturnDocument

import flask
from flask import Flask, request, url_for, jsonify
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError
from fastapi.encoders import jsonable_encoder

from agilisHF.controllers import SearchKeyError, get_details


from .model import Dog
from .objectid import PydanticObjectId

# Configure Flask & Flask-PyMongo:
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
pymongo = PyMongo(app)
print(os.getenv("MONGO_URI"))
# Get a reference to the recipes collection.
# Uses a type-hint, so that your IDE knows what's happening!
data: Collection = pymongo.db.dogs


@app.errorhandler(404)
def resource_not_found(e):
    """
    An error-handler to ensure that 404 errors are returned as JSON.
    """
    return jsonify(error=str(e)), 404


@app.errorhandler(DuplicateKeyError)
def resource_not_found(e):
    """
    An error-handler to ensure that MongoDB duplicate key errors are returned as JSON.
    """
    return jsonify(error=f"Duplicate key error."), 400


@app.errorhandler(SearchKeyError)
def resource_not_found(e):
    """
    An error-handler to ensure that MongoDB duplicate key errors are returned as JSON.
    """
    return jsonify(error=str(e)), 400


@app.route("/dogs", methods=["POST"])
def new_dog():
    raw_dog = request.get_json()
    dog = Dog(**raw_dog)
    insert_result = data.insert_one(dog.to_bson())
    dog.id = PydanticObjectId(str(insert_result.inserted_id))
    print(dog)
    return dog.to_json()


@app.route("/dogs/detail", methods=["POST"])
def get_dogs():
    search_params = request.get_json()
    dogs = get_details(search_params, pymongo.db)
    return dogs
