

import os
from typing import Collection
from pymongo import MongoClient
import pytest
import unittest

from agilisHF.import_dogs import ValidationError, import_data

client = MongoClient(os.getenv("MONGO_URI"))
db: Collection = client.hf.test

@pytest.fixture(autouse=True)
def run_before_every_tests():
    db.drop()
    yield

def test_import_data_pass_with_valid_data():
    raw = [{'name': 'test', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'finally!!', 'vaccination': ['v1!!', 'vocid', 'cutness'], 'age': 10, 'sex': False}]
    result = import_data(raw, db)
    assert True == result

def test_import_data_pass_data_persist_in_db():
    raw = [{'name': 'test', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'finally!!', 'vaccination': ['v1!!', 'vocid', 'cutness'], 'age': 10, 'sex': False}]
    import_data(raw, db)
    db_data = list(db.find({}, {'_id': False}))
    unittest.TestCase().assertCountEqual(raw, db_data)

def test_import_data_exception_name_contains_cat():
    raw = [{'name': 'catzesz', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'finally!!', 'vaccination': ['v1!!', 'vocid', 'cutness'], 'age': 10, 'sex': False}]
    with pytest.raises(ValidationError):
        import_data(raw, db)

def test_import_data_exception_boy_name_not_start_with_m():
    raw = [{'name': 'test', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'finally!!', 'vaccination': ['v1!!', 'vocid', 'cutness'], 'age': 10, 'sex': True}]
    with pytest.raises(ValidationError):
        import_data(raw, db)

def test_import_data_pass_boy_name_start_with_m():
    raw = [{'name': 'Mtest', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'finally!!', 'vaccination': ['v1!!', 'vocid', 'cutness'], 'age': 10, 'sex': True}]
    result = import_data(raw, db)
    assert True == result

def test_import_data_exception_older_than_5_no_cuteness():
    raw = [{'name': 'Mtest', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'finally!!', 'vaccination': ['v1!!', 'vocid'], 'age': 10, 'sex': True}]
    with pytest.raises(ValidationError):
        import_data(raw, db)

def test_import_data_pass_older_than_5_cuteness():
    raw = [{'name': 'test', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'finally!!', 'vaccination': ['v1!!', 'vocid', 'cutness'], 'age': 10, 'sex': False}]
    result = import_data(raw, db)
    assert True == result

def test_import_data_exception_mixed_breed_name_not_contain_snow():
    raw = [{'name': 'Mtest', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'mixed', 'vaccination': ['v1!!', 'vocid'], 'age': 1, 'sex': True}]
    with pytest.raises(ValidationError):
        import_data(raw, db)

def test_import_data_pass_mixed_breed_name_contain_snow():
    raw = [{'name': 'Mtest Snow', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'mixed', 'vaccination': ['v1!!', 'vocid'], 'age': 1, 'sex': True}]
    result = import_data(raw, db)
    assert True == result

def test_import_data_exception_description_sorter_than_50():
    raw = [{'name': 'Mtest', 'color': 'brown', 'description': 'description!! brown', 'breed': 'mixed', 'vaccination': ['v1!!', 'vocid'], 'age': 1, 'sex': True}]
    with pytest.raises(ValidationError):
        import_data(raw, db)

def test_import_data_exception_description_onger_than_100():
    raw = [{'name': 'Mtest', 'color': 'brown', 'description': 'description!! brown ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd', 'breed': 'mixed', 'vaccination': ['v1!!', 'vocid'], 'age': 1, 'sex': True}]
    with pytest.raises(ValidationError):
        import_data(raw, db)

def test_import_data_pass_description_between_50_100():
    raw = [{'name': 'Mtest Snow', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'mixed', 'vaccination': ['v1!!', 'vocid'], 'age': 1, 'sex': True}]
    result = import_data(raw, db)
    assert True == result

def test_import_data_exception_color_not_in_description():
    raw = [{'name': 'Mtest', 'color': 'brown', 'description': 'description!! browan textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'mixed', 'vaccination': ['v1!!', 'vocid'], 'age': 1, 'sex': True}]
    with pytest.raises(ValidationError):
        import_data(raw, db)

def test_import_data_pass_color_in_description():
    raw = [{'name': 'Mtest Snow', 'color': 'brown', 'description': 'description!! brown textetxtetxtettetttedtetdtedtedtetdetdettetetedtetd', 'breed': 'mixed', 'vaccination': ['v1!!', 'vocid'], 'age': 1, 'sex': True}]
    result = import_data(raw, db)
    assert True == result