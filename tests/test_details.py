import mongomock
import unittest
from agilisHF.controllers import ValidationError, get_details_by_search
from agilisHF.model import Dog

""" from agilisHF.controllers import get_details_by_search
from agilisHF.model import Dog """


class DetailsTest(unittest.TestCase):
    db = mongomock.MongoClient().db
    dogs = [
        Dog(
            **{
                "name": "Test",
                "color": "white",
                "breed": "husky",
                "age": 1,
                "vaccination": [],
                "sex": True,
                "description": "Teszt",
            }
        ),
        Dog(
            **{
                "name": "Test2",
                "color": "white",
                "breed": "husky",
                "age": 5,
                "vaccination": ["covid19", "covid21"],
                "sex": True,
                "description": "Teszt",
            }
        ),
        Dog(
            **{
                "name": "Test3",
                "color": "white",
                "breed": "husky",
                "age": 5,
                "vaccination": [],
                "sex": True,
                "description": "Teszt",
            }
        ),
    ]

    def setUp(self) -> None:
        for dog in self.dogs:
            self.db.dogs.insert_one(dog.to_bson())
        return super().setUp()

    def tearDown(self) -> None:
        self.db.dogs.drop()
        return super().tearDown()

    def test_details_param_search_by_age(self):
        dogs = get_details_by_search({"age": 1}, self.db)

        assert dogs[0].name == self.dogs[0].name
        assert dogs[0].color == self.dogs[0].color
        assert dogs[0].age == self.dogs[0].age
        assert dogs[0].breed == self.dogs[0].breed

    def test_details_param_search_by_age_multiple_result(self):
        dogs = get_details_by_search({"age": 5}, self.db)

        assert len(dogs) == 2

    def test_details_param_search_by_age_empty(self):
        dogs = get_details_by_search({"age": 11}, self.db)

        assert len(dogs) == 0

    def test_details_param_search_by_age_validation_error(self):
        with self.assertRaises(ValidationError):
            get_details_by_search({"age": "0000"}, self.db)

    def test_params_are_None(self):
        with self.assertRaises(ValidationError):
            get_details_by_search(None, self.db)

    def test_multiple_params_success(self):
        dogs = get_details_by_search(
            {"age": 1, "color": "white", "breed": "husky"}, self.db
        )

        assert dogs[0].name == self.dogs[0].name
        assert dogs[0].color == self.dogs[0].color
        assert dogs[0].age == self.dogs[0].age
        assert dogs[0].breed == self.dogs[0].breed

    def test_multiple_params_should_return_empty_when_no_search_str(self):
        dogs = get_details_by_search(
            {"age": 7, "color": "white", "breed": "german"}, self.db
        )

        assert len(dogs) == 0

    def test_should_search_by_search_str_when_dog_not_found(self):
        dogs = get_details_by_search(
            {"search_str": "Test"},
            self.db,
        )

        assert len(dogs) == 3

    def test_should_search_by_search_str_when_dog_not_found(self):
        dogs = get_details_by_search(
            {"search_str": "Test"},
            self.db,
        )

        assert len(dogs) == 3

    def test_vaccination_condition_should_work(self):
        dogs1 = get_details_by_search(
            {"vaccinated": True},
            self.db,
        )
        dogs2 = get_details_by_search(
            {"vaccinated": False},
            self.db,
        )

        assert len(dogs1) == 1

        assert len(dogs2) == 2
