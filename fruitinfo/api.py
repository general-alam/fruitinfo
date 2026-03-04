import requests
from urllib.parse import quote

BASE_URL = "https://www.fruityvice.com/api/fruit"


class FruitNotFoundError(Exception):
    """error raised when a fruit can't be found in the database"""
    pass


class Fruit:

    def __init__(self, name, id, family, sugar, carbs):
        self.name = name
        self.id = id
        self.family = family
        self.sugar = sugar
        self.carbs = carbs

    def __repr__(self):
        return f"Fruit({self.name})"

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "family": self.family,
            "nutrition": {
                "sugar": self.sugar,
                "carbohydrates": self.carbs
            }
        }


def get_fruit(name, session=None):
    """
    get_fruit: takes in a string (the fruit name) as a parameter, looks up the fruit by name and returns a Fruit object.
    
    Possible Errors:
    - FruitNotFoundError (if it doesn't exist)
    - Exception (if there's a connection issue)
    
    Logical Quirk:
    - FruityVice allows fruits to be searched by /api/fruit/{name} or /api/fruit/{ID}. 
    - If the input name has multiple words eg. "Horned Melon", it can't be searched by name due to the space in the URL. Notably, it can be searched by id.
    - To get around this limitation, the code below will instead _search_all fruits when the input is multiple words.
    - Better suggestions to this workaround are welcome!
    """
    
    if session is None:
        session = requests.Session()

    name = name.strip()

    if " " in name:
        return _search_all(name, session)

    try:
        response = session.get(BASE_URL + "/" + quote(name), timeout=5)
    except requests.exceptions.ConnectionError:
        raise Exception("Unable to connect to the API.")
    except requests.exceptions.Timeout:
        raise Exception("Request timed out.")

    if response.status_code == 404:
        raise FruitNotFoundError(f"'{name}' was not found.")

    if not response.ok:
        raise Exception(f"Error: HTTP {response.status_code}")

    data = response.json()

    if isinstance(data, list):
        data = data[0]

    return _parse_fruit(data)


def _search_all(name, session):
    """
    _search_all: This function is used in the case of multi-word names, searching through the entire fruit database.
    """
    try:
        response = session.get(BASE_URL + "/all", timeout=5)
    except requests.exceptions.ConnectionError:
        raise Exception("Unable to connect to the API")
    except requests.exceptions.Timeout:
        raise Exception("Request timed out.")

    if not response.ok:
        raise Exception(f"Error: HTTP {response.status_code}")

    for item in response.json():
        if item["name"].lower() == name.lower():
            return _parse_fruit(item)

    raise FruitNotFoundError(f"'{name}' was not found.")


def _parse_fruit(data):
    return Fruit(
        name=data["name"],
        id=data["id"],
        family=data["family"],
        sugar=data["nutritions"]["sugar"],
        carbs=data["nutritions"]["carbohydrates"]
    )
