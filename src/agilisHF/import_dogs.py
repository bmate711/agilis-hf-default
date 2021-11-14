from .model import Dog

class ValidationKeyError(KeyError):
    pass

class ValidationError(Exception):
    pass

def import_data(raw, db):
    valid_raw = validate_data_list(raw)
    dogs = create_dogs(valid_raw)
    save_dogs(dogs, db)
    return True
   

def create_dogs(valid_raw_list):
    return map(lambda raw_dog: Dog(**raw_dog), valid_raw_list)

def save_dogs(dogs, db):
    dogs_bson = map(lambda dog: dog.to_bson(), dogs)
    return db.insert_many(dogs_bson)


# A kutya neve nem tartalmazhatja a 'cat' szót
# Ha a kutya fiú 'M' kell kezdődni a neve
# Ha a kutya 5 évnél idősebb, rendelkezni kell 'cuteness' oltással
# Ha a kutya keverék, akkor szerepelnie kell a nevében 'Snow' szónak
# A leírás 50-100 karakte hosszú lehet
# A kutya színének szerepelnie kell a leírásban

def validate_data_list(raw_list):
    return map(lambda raw: validate_data(raw), raw_list)

def validate_data(raw):
    validate_keys(raw)
    validate_name(raw)
    validate_breed(raw)  
    validate_age(raw)
    validate_color(raw)  
    validate_sex(raw)  
    validate_vaccination(raw)
    validate_description(raw)    
    return raw

def validate_keys(raw):
    valid_search_keys = ["name", "breed", "age", "color", "sex", "vaccination", "description"]
    for key, value in raw.items():
        if key not in valid_search_keys:
            raise ValidationKeyError("Invalid key in search conditons")
    if (len(valid_search_keys) != len(raw.items())):
        raise ValidationKeyError("Invalid key in search conditons")

def validate_name(raw):
    name = raw["name"]
    sex = raw["sex"]
    breed = raw["breed"]
    if type(name) is not str:
        raise ValidationError("Name value must be a valid string")
    if "cat" in name:
        raise ValidationError("Name contain 'cat'")
    if sex:
        if(name[0] != 'M' ):
            raise ValidationError("Name not start with 'M'")
    if breed == "mixed":
        if "Snow" not in name:
             raise ValidationError("Name should contain 'Snow'")

def validate_breed(raw):
    breed = raw["breed"]
    if type(breed) is not str:
        raise ValidationError("Breed value must be a valid string")

def validate_age(raw):
    age = raw["age"]
    if type(age) is not int:
        raise ValidationError("Age value must be a valid integer")

def validate_color(raw):
    colors = ["mixed", "black", "white", "brown"]
    color = raw["color"]
    if type(color) is not str:
        raise ValidationError("Color value must be a valid string")
    if color not in colors:
        raise ValidationError("Color value must be a valid color")

def validate_sex(raw):
    sex = raw["sex"]
    if type(sex) is not bool:
        raise ValidationError("Sex value must be a bool value")

def validate_vaccination(raw):
    vaccination = raw["vaccination"]
    age = raw["age"]
    if type(vaccination) is not list:
        raise ValidationError("Vaccination value must be a valid list")
    for v in vaccination:
        if type(v) is not str:
            raise ValidationError("Vaccination item must be a valid string")  
    if age > 5:
        if 'cutness' not in vaccination:
             raise ValidationError("Dog must be vaccinated with 'cutness'")

def validate_description(raw):
    description = raw["description"]
    color = raw["color"]
    if type(description) is not str:
        raise ValidationError("Vaccination item must be a valid string")  
    if len(description) < 50 or len(description) > 100:
        raise ValidationError("Description length should be between 50 end 100") 
    if color not in description:
        raise ValidationError("Color should be in the description")

    

    




