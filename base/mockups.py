"""
This file has the Mockup class, that creates randomn instances of the
project models
"""

import os
import random

from shutil import copyfile

from django.apps import apps
from django.conf import settings
from django.core.files import File
from django.utils import timezone

from faker import Faker
from inflection import underscore

from api_client.enums import ClientCodes
from api_client.models import ClientLog
from api_client.models import DisabledClient
from base.utils import random_string
from parameters.models import Parameter
from regions.models import Commune
from regions.models import Region
from users.models import User


class Mockup:
    def __init__(self):
        language = settings.FAKER_LOCALES
        # DOCS: https://faker.readthedocs.io/en/master/index.html
        self.faker = Faker(language)

    def create_client_log(self, **kwargs):
        return ClientLog.objects.create(**kwargs)

    def create_disabled_client(self, **kwargs):
        self.set_required_choice(kwargs, "client_code", ClientCodes.choices)
        return DisabledClient.objects.create()

    def create_commune(self, **kwargs):
        self.set_required_string(kwargs, "name")
        self.set_required_foreign_key(kwargs, "region")
        return Commune.objects.create(**kwargs)

    def create_parameter(self, **kwargs):
        return Parameter.objects.create(**kwargs)

    def create_region(self, **kwargs):
        self.set_required_string(kwargs, "name")
        return Region.objects.create(**kwargs)

    def create_user(self, password=None, **kwargs):
        if kwargs.get("first_name") is None:
            kwargs["first_name"] = self.faker.first_name()

        if kwargs.get("last_name") is None:
            kwargs["last_name"] = self.faker.last_name()

        if kwargs.get("email") is None:
            kwargs["email"] = self.faker.email()

        if kwargs.get("is_active") is None:
            kwargs["is_active"] = True

        user = User.objects.create(**kwargs)

        if password is not None:
            user.set_password(password)
            user.save()

        return user

    def random_hex_int(self, *args, **kwargs):
        val = self.faker.random_int(*args, **kwargs)
        return hex(val)

    def random_float(self, minimum=-100000, maximum=100000):
        return random.uniform(minimum, maximum)  # noqa: S311

    def set_required_boolean(self, data, field, default=None, **kwargs):
        if field not in data:
            if default is None:
                data[field] = self.faker.boolean()
            else:
                data[field] = default

    def set_required_choice(self, data, field, choices, **kwargs):
        if field not in data:
            data[field] = self.faker.random_element(choices)[0]

    def set_required_date(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now().date()

    def set_required_time(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now().time()

    def set_required_datetime(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now()

    def set_required_email(self, data, field):
        if field not in data:
            data[field] = self.faker.email()

    def set_required_file(self, data, field):
        if field in data:
            # do nothing if the field is in the data
            return

        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        test_root = os.path.realpath(os.path.dirname(__file__))

        file_path = data.pop(f"{field}_file_path", None)

        if file_path is None:
            file_path = "gondola.jpg"

        if not os.path.isfile(file_path):
            file_path = f"{test_root}/test_assets/{file_path}"

        file_name = os.path.basename(file_path)
        final_path = f"{settings.MEDIA_ROOT}{file_name}"

        copyfile(file_path, final_path)

        with open(final_path, "rb") as file:
            data[field] = File(file, file_name)

    def set_required_float(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.random_float(**kwargs)

    def set_required_foreign_key(self, data, field, model=None, **kwargs):
        if model is None:
            model = field

        if field not in data and f"{field}_id" not in data:
            data[field] = getattr(self, f"create_{model}")(**kwargs)

    def set_required_int(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.faker.random_int(**kwargs)

    def set_required_ip_address(self, data, field, allow_v6=False, **kwargs):
        if field not in data:
            if allow_v6 and self.faker.boolean():
                data[field] = self.faker.ipv6()
            else:
                data[field] = self.faker.ipv4()

    def set_required_string(self, data, field, length=6, include_spaces=True):
        if field not in data:
            data[field] = random_string(
                length=length,
                include_spaces=include_spaces,
            )

    def set_required_url(self, data, field, length=6):
        if field not in data:
            data[field] = f"http://{random_string(length=length)}.com"

    def set_required_rut(self, data: dict, field: str, **kwargs):
        data.setdefault(field, self.faker.rut(**kwargs))


def add_get_or_create(cls, model):
    model_name = underscore(model.__name__)

    def get_or_create(self, **kwargs):
        try:
            return model.objects.get(**kwargs), False
        except model.DoesNotExist:
            pass

        method_name = f"create_{model_name}"
        return getattr(cls, method_name)(self, **kwargs), True

    get_or_create.__doc__ = f"Get or create for {model_name}"
    get_or_create.__name__ = f"get_or_create_{model_name}"
    setattr(cls, get_or_create.__name__, get_or_create)


def get_our_models():
    for model in apps.get_models():
        app_label = model._meta.app_label

        # test only those models that we created
        if os.path.isdir(app_label):
            yield model


for model in get_our_models():
    add_get_or_create(Mockup, model)
