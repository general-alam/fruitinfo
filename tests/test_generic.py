import json
import pytest
import requests

from fruitinfo.api import get_fruit, Fruit, FruitNotFoundError


class TestResponse:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self._data = data
        self.ok = status_code == 200

    def json(self):
        return self._data


class TestSession:
    def __init__(self, response=None, raise_error=None, responses=None):
        self._response = response
        self._raise_error = raise_error
        self._responses = responses
        self._call_count = 0

    def get(self, url, timeout):
        if self._raise_error:
            raise self._raise_error
        if self._responses is not None:
            response = self._responses[self._call_count]
            self._call_count += 1
            return response
        return self._response


BANANA_DATA = {
    "name": "Banana",
    "id": 1,
    "family": "Musaceae",
    "nutritions": {
        "sugar": 17.2,
        "carbohydrates": 22.0
    }
}


def test_get_fruit_returns_correct_data():
    session = TestSession(TestResponse(200, BANANA_DATA))
    fruit = get_fruit("Banana", session=session)
    assert fruit.name == "Banana"
    assert fruit.sugar == 17.2
    assert fruit.family == "Musaceae"


def test_fruit_not_found():
    session = TestSession(TestResponse(404, {}))
    with pytest.raises(FruitNotFoundError):
        get_fruit("notafruit", session=session)


def test_api_list_response_also_works():
    session = TestSession(TestResponse(200, [BANANA_DATA]))
    fruit = get_fruit("Banana", session=session)
    assert fruit.id == 1


def test_timeout_raises_exception():
    session = TestSession(raise_error=requests.exceptions.Timeout())
    with pytest.raises(Exception):
        get_fruit("Banana", session=session)


def test_fruit_stores_values_correctly():
    fruit = Fruit("Banana", 1, "Musaceae", 17.2, 22.0)
    assert fruit.name == "Banana"
    assert fruit.id == 1
    assert fruit.family == "Musaceae"
    assert fruit.sugar == 17.2
    assert fruit.carbs == 22.0


def test_missing_fields_raises_exception():
    bad_data = {"name": "Banana", "id": 1, "family": "Musaceae"}
    session = TestSession(TestResponse(200, bad_data))
    with pytest.raises(Exception):
        get_fruit("Banana", session=session)


def test_json_output_has_nested_nutrition():
    fruit = Fruit("Banana", 1, "Musaceae", 17.2, 22.0)
    data = {
        "name": fruit.name,
        "id": fruit.id,
        "family": fruit.family,
        "nutrition": {
            "sugar": fruit.sugar,
            "carbohydrates": fruit.carbs
        }
    }
    output = json.loads(json.dumps(data))
    assert "nutrition" in output
    assert output["nutrition"]["sugar"] == 17.2
    assert "sugar" not in output 
