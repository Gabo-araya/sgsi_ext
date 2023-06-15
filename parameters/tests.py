from django.core import validators

# base
from base.tests import BaseTestCase
from base.utils import random_string

# enums
from parameters.definitions import ParameterDefinitionList
from parameters.models import Parameter
from parameters.utils.parsers import parse_int_value
from parameters.utils.parsers import parse_str_value


class ParameterTestCase(BaseTestCase):
    def test_create_all_parammeters(self):
        Parameter.create_all_parameters()
        self.assertEqual(
            len(ParameterDefinitionList.definitions),
            Parameter.objects.count(),
        )

    def test_parse_str_value(self):
        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_str_value(value))
        for _ in range(3):
            value = random_string()
            self.assertEqual(parse_str_value(value), value)

    def test_parse_int_value(self):
        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_int_value(value))
        space = " "
        self.assertIsNone(parse_int_value(space))
        int_with_space = "1 "
        self.assertEqual(parse_int_value(int_with_space), 1)
        int_with_space = " 1"
        self.assertEqual(parse_int_value(int_with_space), 1)
        int_with_space = " 1 "
        self.assertEqual(parse_int_value(int_with_space), 1)
        # TODO: test for strings, could not figure out what 'sanitize_separators' does
