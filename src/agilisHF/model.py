from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional

from .objectid import PydanticObjectId


class Dog(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    name: str
    color: str
    breed: str
    description: str
    vaccination: List[str]
    age: int
    sex: bool

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data




class User(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    fullname: str
    idcardnumber: str
    emailaddress: str
    password: str


    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data