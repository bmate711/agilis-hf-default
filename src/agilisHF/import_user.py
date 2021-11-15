from src.agilisHF.controllers import ValidationError
from .model import User
import bcrypt
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regex2 = r'\b[A-Za-z]+" "+[A-Za-z]\b'
regex3 = r'\b[0-9]{9}+[A-Z]{2}\b'

class ValidationKeyError(KeyError):
    pass

class ValidationError(Exception):
    pass

def import_data(raw, db):
    valid_raw = validate_data_list(raw, db)
    user = create_user(valid_raw)
    save_user(user, db)
    return True

def create_user(valid_raw_list):
    return map(lambda raw_user: User(**raw_user), valid_raw_list)

def save_user(user, db):
    user_bson = map(lambda user: user.to_bson(), user)
    return db.insert_many(user_bson)

def validate_data_list(raw_list, db):
    return map(lambda raw: validate_data(raw), raw_list)

def validate_data(raw, db):
    validate_keys(raw)
    validate_fullname(raw)
    validate_idcardnumber(raw)
    validate_emailaddress(raw, db)
    validate_password(raw)
    return raw

def validate_keys(raw):
    valid_search_keys = ["fullname", "idcardnumber", "emailaddress", "password"]
    for key, value in raw.items():
        if key not in valid_search_keys:
            raise ValidationKeyError("Invalid key in search conditons")
    if (len(valid_search_keys) != len(raw.items())):
        raise ValidationKeyError("Invalid key in search conditons")

def validate_fullname(raw):
    name = raw["name"]
    if type(name) is not str:
        raise ValidationError("Name value must be a valid string")
    if (re.fullmatch(regex2, name)):
        raise ValidationError("Invalid name, must contain a first name and a last name and can't contain numbers")
    if len(name) < 2 or len(name) > 128:
        raise ValidationError("Invalid name, a name length should be between 2 and 128") 

def validate_idcardnumber(raw):
    idcardnumber = raw["idcardnumber"]
    if type(idcardnumber) is not str:
        raise ValidationError("Idcardnumber value must be a valid string")
    if (re.fullmatch(regex3, idcardnumber)):
        raise ValidationError("ID card must be 11 character, the first 9 should be number and the last 2 should be letter")

def validate_emailaddress(raw, db):
    emailaddress= raw['emailaddress']
    if type(emailaddress) is not str:
        raise ValidationError("Emailaddress value must be a valid string")
    if(re.fullmatch(regex,emailaddress)):
        raise ValidationError("Invalid email form")
    users=db.users
    existing_user=users.find_one({"emailadress":emailaddress})
    if not existing_user is None :
        raise ValidationError("Email address is already exist")

def validate_password(raw):
    password= raw['password']
    if type(password) is not str:
        raise ValidationError("Password value must be a valid string")
    if not re.search('[A-Z]', password) or not re.search('[0-9]', password):
        raise ValidationError("It must contain capital letter, and number")
    hashpass=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    raw.insert({'password':hashpass})

    