import mongomock
import pytest
import os
from typing import Collection

import unittest
from agilisHF.model import User
from agilisHF.import_user import ValidationError, import_data, save_user
import re

class DetailsTest(unittest.TestCase):
    db = mongomock.MongoClient().db
    users= [
        User(
            **{
                "fullname": "Test Test",
                "idcardnumber": "123456789AB",
                "emailaddress": "test@tes.com",
                "password": "Asdika1"
            }
        ),
    ]
    
    def setUp(self) -> None:
        for user in self.users:
            self.db.users.insert_one(user.to_bson())
        return super().setUp()

    def tearDown(self) -> None:
        self.db.users.drop()
        return super().tearDown()


    def test_import_data_pass_data_persist_in_db(self):
        raw = [{"fullname": "Test Test",
                "idcardnumber": "123456789AB",
                "emailaddress": "test@tes.com",
                "password": "Asdika1"}]
        import_data(raw, self.db)
        db_data = list(self.db.find({}, {'_id': False}))
        unittest.TestCase().assertCountEqual(raw, db_data)

    def test_import_data_exception_name_longer_than_100(self):
        raw = [{"fullname": "TestTestTestTestTestTest TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest",
                "idcardnumber": "123456789AB",
                "emailaddress": "test@tes.com",
                "password": "Asdika1"}]
        with pytest.raises(ValidationError):
            import_data(raw, self.db)

    def test_import_data_exception_name_no_space(self):
        raw = [{"fullname": "test",
                 "idcardnumber": "123456789AB",
                "emailaddress": "test@tes.com",
                "password": "Asdika1"}]
        with pytest.raises(ValidationError):
            import_data(raw, self.db)

    def test_import_data_exception_idcardnumber_wrong_format(self):
        raw = [{"fullname": "Test Test",
                 "idcardnumber": "12RT567899B",
                "emailaddress": "test@tes.com",
                "password": "Asdika1"}]
        with pytest.raises(ValidationError):
            import_data(raw, self.db)
        
    def test_import_data_exception_emailaddress_wrong_format(self):
        raw = [{"fullname": "Test Test",
                 "idcardnumber": "12RT567899B",
                "emailaddress": "testtescom",
                "password": "Asdika1"}]
        with pytest.raises(ValidationError):
            import_data(raw, self.db)

    def test_import_data_exception_password_wrong_format(self):
        raw = [{"fullname": "Test Test",
                 "idcardnumber": "12RT567899B",
                "emailaddress": "test@tes.com",
                "password": "asd"}]
        with pytest.raises(ValidationError):
            import_data(raw, self.db)