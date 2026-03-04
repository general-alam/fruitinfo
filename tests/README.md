# Tests

There are two types of test files:
- `test_generic.py` - unit tests (testing specific test data using a new test fruit class)
- `test_with_api.py` - tests that use the FruityVice data (requires internet to make API calls)

## How to run
If you're interested in testing both of these, simply run the command:
```bash
pytest
```

If you'd like to run only the unit tests:
```bash
pytest tests/test_generic.py
```
Similarly, if you'd like to run only the tests involving the FruityVice API:
```bash
pytest tests/test_with_api.py
```
NOTE: the tests in `test_with_api.py` are dependent on the information in the FruityVice database (last accurate to 4th of March, 2026). If these tests fail, please see the [FruityVice database](https://www.fruityvice.com/api/fruit/all) for any changes!
