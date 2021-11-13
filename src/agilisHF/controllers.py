from os import name
from flask_pymongo.wrappers import Database

from agilisHF.model import Dog

# Search conditions
# { "name": string
#   "age": number,
#   "vaccinated": boolean
#   "color": string
#   "sex": boolean
# }


def get_details(search_conditions: dict, pymongo_db: Database):
    dogs = pymongo_db.dogs
    # search by attributes
    dog: Dog = dogs.find_one(
        {
            "name": search_conditions["name"],
            "age": search_conditions["age"],
            "vaccinated": search_conditions["vaccinated"],
            "color": search_conditions["color"],
            "sex": search_conditions["sex"],
        }
    )

    if dog is None:
        search_dogs = dogs.find()
        result_dogs = []
        # search by search string
        for dog in search_dogs:
            if (dog.description.find(search_conditions["search_str"]) > -1) or (
                dog.name.find(search_conditions["search_str"]) > -1
            ):
                result_dogs.append(dog.to_json())
        return result_dogs
    return dog.to_json()
