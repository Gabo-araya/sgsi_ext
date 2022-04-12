# base
from base.tests import BaseTestCase

# models
from parameters.models import Parameter

# enums
from parameters.definitions import ParameterDefinitionList


class ParameterTestCase(BaseTestCase):
    def test_create_all_parammeters(self):
        Parameter.create_all_parameters()
        self.assertEqual(
            len(ParameterDefinitionList.definitions), Parameter.objects.count()
        )
