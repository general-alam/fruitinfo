import pytest

from fruitinfo.api import get_fruit, FruitNotFoundError

"""
All the code in this testing file is dependent on information in the FruityVice database (last checked: 04 MARCH 2026).
You can view more information here: https://www.fruityvice.com/
All the fruits are listed here: https://www.fruityvice.com/api/fruit/all
"""

def test_real_banana():
    fruit = get_fruit("Banana")
    assert fruit.name == "Banana"


def test_nonexistent_fruit_not_found():
    with pytest.raises(FruitNotFoundError):
        get_fruit("wineberry")


def test_misspelled_fruit_not_found():
    with pytest.raises(FruitNotFoundError):
        get_fruit("bannanna")


def test_fruit_with_multiple_words():
    fruit = get_fruit("Japanese Persimmon")
    assert fruit.name == "Japanese Persimmon"


def test_json_output_structure():
    """
    This test tests that 
    - the fruit information is accurate
    - the json is valid
    - the structure of the json is correct.
    """
    import json
    fruit = get_fruit("Horned Melon")
    data = json.loads(json.dumps(fruit.to_dict()))
    assert data["name"] == "Horned Melon"
    assert data["id"] == 95
    assert data["family"] == "Cucurbitaceae"
    assert "nutrition" in data
    assert data["nutrition"]["sugar"] == 0.5
    assert data["nutrition"]["carbohydrates"] == 7.56
    assert "sugar" not in data
    assert "carbohydrates" not in data
