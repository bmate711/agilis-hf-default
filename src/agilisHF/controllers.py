from os import name
from bson.objectid import ObjectId
from flask.json import jsonify
from flask_pymongo.wrappers import Database

from agilisHF.model import Dog

# Search conditions
# { "name": string
#   "age": number,
#   "vaccinated": boolean
#   "color": string
#   "sex": boolean
#   "search_str": string,
#   "breed": string
# }


class SearchKeyError(KeyError):
    pass


class ValidationError(Exception):
    pass


def get_details_by_search(search_conditions: dict, pymongo_db: Database):
    dogs = pymongo_db.dogs
    validate_search_conditons(search_conditions)
    search_values = {}
    for key, value in search_conditions.items():
        if key == "vaccinated":
            search_values["vaccination"] = (
                {"$exists": True, "$ne": []}
                if value == True
                else {"$exists": True, "$eq": []}
            )
        elif value is not None:
            search_values[key] = value

    # search by attributes
    dogs = dogs.find(search_values)
    result_dogs = []
    if dogs is None:
        if "search_str" not in search_conditions.keys():
            return {}
        search_dogs = dogs.find()
        # search by search string
        for dog in search_dogs:
            if (
                (dog["description"].find(search_conditions["search_str"]) > -1)
                or (dog["name"].find(search_conditions["search_str"]) > -1)
                or (dog["breed"].find(search_conditions["search_str"]) > -1)
            ):
                result_dogs.append(Dog(**dog).to_json())
        return jsonify(dogs=result_dogs)
    for dog in dogs:
        result_dogs.append(Dog(**dog).to_json())
    return jsonify(dogs=result_dogs)


def get_details_by_id(id: str, pymongo_db: Database):
    dogs = pymongo_db.dogs
    dog = dogs.find_one({"_id": ObjectId(id)})
    if dog is not None:
        return Dog(**dog).to_json()
    return {}


valid_search_keys = ["name", "breed", "age", "color", "sex", "vaccinated", "search_str"]


def validate_search_conditons(search_conditions: dict):
    for key in search_conditions.keys():
        if key not in valid_search_keys:
            raise SearchKeyError("Invalid key in search conditons")
    if "name" in search_conditions:
        if type(search_conditions["name"]) is not str:
            raise ValidationError("Name value must be a valid string")
    if "breed" in search_conditions:
        if type(search_conditions["breed"]) is not str:
            raise ValidationError("Breed value must be a valid string")
    if "color" in search_conditions:
        if type(search_conditions["color"]) is not str:
            raise ValidationError("Color value must be a valid string")
    if "age" in search_conditions:
        if type(search_conditions["age"]) is not int:
            raise ValidationError("Age value must be an integer")
    if "sex" in search_conditions:
        if type(search_conditions["sex"]) is not bool:
            raise ValidationError("Sex value must be a bool value")
    return
