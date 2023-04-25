# base
from base.tests import BaseTestCase

# enums
from parameters.definitions import ParameterDefinitionList
from parameters.models import Parameter


class ParameterTestCase(BaseTestCase):
    def test_create_all_parammeters(self):
        Parameter.create_all_parameters()
        self.assertEqual(
            len(ParameterDefinitionList.definitions),
            Parameter.objects.count(),
        )
