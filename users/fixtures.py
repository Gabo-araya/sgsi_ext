import pytest

from users.models import User


@pytest.fixture
def superuser_user(db):
    return User.objects.create_superuser(
        email="admin@example.com",
        password="thisismagnetbestkeptsecret",  # noqa: S106
        first_name="Alex",
        last_name="Smith",
    )


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(
        email="staff@example.com",
        password="thisismagnet2ndbestkeptsecret",  # noqa: S106
        first_name="Javier",
        last_name="Miranda",
        is_staff=True,
        is_active=True,
    )


@pytest.fixture
def staff_users(staff_user):
    new_staff_users = [
        User(
            email="staff2@example.com",
            first_name="Staff",
            last_name="Two",
            is_staff=True,
        ),
        User(
            email="staff3@example.com",
            first_name="Staff",
            last_name="Three",
            is_staff=True,
        ),
    ]
    new_staff_users[0].set_password("thisismagnet3rdbestkeptsecret")
    new_staff_users[1].set_password("thisismagnet4thbestkeptsecret")
    User.objects.bulk_create(new_staff_users)
    return [staff_user, *new_staff_users]


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        email="user@example.com",
        first_name="John",
        last_name="Doe",
        password="thisismagnet2ndbestkeptsecret",  # noqa: S106
    )


@pytest.fixture
def regular_user2(db):
    return User.objects.create_user(
        email="user@example.com",
        first_name="Jane",
        last_name="Doe",
        password="thisismagnet2ndbestkeptsecret",  # noqa: S106
    )
