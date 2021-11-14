"""
agilisHF - A small API for managing dog recipes.
"""

from datetime import datetime
import os
from unittest import result

from pymongo.collection import Collection, ReturnDocument

import flask
from flask import Flask, request, url_for, jsonify
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError
from fastapi.encoders import jsonable_encoder

from .import_dogs import import_data
from agilisHF.controllers import (
    SearchKeyError,
    ValidationError,
    get_details_by_id,
    get_details_by_search,
)


from .model import Dog
from .objectid import PydanticObjectId

# Configure Flask & Flask-PyMongo:
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
pymongo = PyMongo(app)
print(os.getenv("MONGO_URI"))
# Get a reference to the recipes collection.
# Uses a type-hint, so that your IDE knows what's happening!
data: Collection = pymongo.db.dog


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
    return jsonify(error=str(e)), 400


@app.errorhandler(ValidationError)
def resource_not_found(e):
    return jsonify(error=str(e)), 400


@app.route("/dogs", methods=["POST"])
def new_dog():
    raw_dog = request.get_json()
    dog = Dog(**raw_dog)
    insert_result = data.insert_one(dog.to_bson())
    dog.id = PydanticObjectId(str(insert_result.inserted_id))
    print(dog)
    return dog.to_json()

@app.route("/import", methods=["POST"])
def import_dogs():
    raw_dog_list = request.get_json()
    import_data(raw_dog_list, data)
    return jsonify(True)

@app.route("/dogs/detail", methods=["POST"])
def get_dogs():
    search_params = request.get_json()
    result_jsons = []
    res = get_details_by_search(search_params, pymongo.db)
    for dog in res:
        result_jsons.append(dog.to_json())
    return jsonify(dogs=result_jsons)


@app.route("/dogs/detail/", methods=["GET"])
def get_dog_by_id():
    id = request.args.get("id")
    dogs = get_details_by_id(id, pymongo.db)
    return dogs
