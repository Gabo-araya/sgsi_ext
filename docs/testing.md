# Tests

pytest is the preferred tool to write tests. This tool has been chosen due to the
built-in solution lacked some desired features such as code coverage and test report
generation. In the previous DPT versions, `django-nose` was used, but it was
discontinued by its author, and it doesn't behave well when coverage tools are being
used. Django has been configured to use pytest as the test runner even when
`./manage.py test` is called.

## Writing tests and fixtures

Pytest encourages the usage of function-based tests but classes can be used too to
organize related tests together. Therefore, function-based tests are preferred.

Function-based tests have the following structure:

```python
def test_something(test_model):
    result = test_model.do_something()
    assert result == <expected_result>
```

### Test parametrization

To ease testing with varying parameters, parametrization can be used

```python
import pytest

from users.models.user import User

@pytest.mark.parametrize(
    "user_role,expected_response",
    [
      ("BUYER", 403),
      ("SELLER", 200),
      ("ADMIN", 200),
    ]
)
def test_endpoint_role_access_control(user_role, expected_response, client):
    user = User.objects.create_user(first_name="Test", last_name="User", role=user_role)
    client.force_login(user)
    response = client.get("/api/protected-endpoint")

    assert response.status_code == expected_response
```

### Fixtures

Fixtures are the most interesting feature of pytest. It enables consistent and
repeatable results. For Django-based projects, fixtures are commonly used to provide
test models to tests. Fixtures can request additional fixtures if required.

Here's an example fixture:

```python

import pytest

from users.models.group import Group
from users.models.user import User

# Simple fixture that requires DB access
@pytest.fixture
def regular_user(db) -> User:  # request the db fixture so the database is available
    return User.objects.create_user(first_name="John", last_name="Doe")

@pytest.fixture
def regular_group(db) -> Group:
    return Group.objects.create(name="Regular users")

# Fixture that requires the `regular_user` fixture, `db` is implicitly required
# It will return a group with a user.
@pytest.fixture
def regular_group_with_users(regular_user: User, regular_group: Group) -> Group:
    regular_group.user_set.add(regular_user)
    return regular_group
```

Fixtures can be defined in both the test module or the `conftest.py` module inside your
app directory. `conftest` fixtures can be shared across all the tests of the directory
where it's placed.

To make fixtures available to all tests, you should edit the root `conftest.py` module
as follows:

```python
pytest_plugins = [
    "base.fixtures",
    "users.fixtures",
    # add path to extra fixtures here
]
```

For more information, see the pytest [section about fixtures](https://docs.pytest.org/en/7.3.x/explanation/fixtures.html#about-fixtures).

### The `test_responses` test

The hallmark of DPT. This test checks the entire urlconf in search of broken views and
as such, it requires an instance of every possible model to be present in the database.

During the porting of this test to pytest, two major changes were performed:

- Mockup class was dropped in favor of fixtures.
- The test runs on a clean database.

Even when mockup class is no longer used, test fixtures have to be somehow defined.
The recommended way is to:

1. Create a `fixtures.py` module on your app directory.
2. Add the module path to the root's `conftest.py::pytest_plugins`
3. In your fixtures module, define the required fixtures. The fixture should have the
   same name as the model but underscored.

In case you want to use custom names for a fixture, make sure to edit
`base/fixtures.py` and define in `MODEL_FIXTURE_CUSTOM_NAMES` the relationship between
the model name and the test fixture it should use, this way:

```python
MODEL_FIXTURE_CUSTOM_NAMES = {
    "users.User": "regular_user",
    "parameters.Parameter": "test_parameter",
}
```
