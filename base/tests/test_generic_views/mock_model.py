from unittest.mock import MagicMock

from django.db import models

parent_meta = MagicMock()
parent_meta.verbose_name = "Mock Model"
parent_meta.verbose_name_plural = "mock models"
parent_meta.model_name = "mockmodel"

MockModel = MagicMock(spec=models.Model)
MockModel._meta = parent_meta
MockModel.__str__.return_value = "Object"
MockModel.__name__ = "MockModel"
MockModel.get_absolute_url = MagicMock(return_value="/mockmodel/1/")

MockQuerySet = MagicMock(spec=models.QuerySet)
MockQuerySet.model = MockModel

MockManager = MagicMock(spec=models.Manager)
MockManager._default_queryset = MockQuerySet
MockModel.configure_mock(_default_manager=MockManager)
MockModel.configure_mock(objects=MockModel._default_manager)


foreign_field_mock = MagicMock(spec=models.ForeignKey)
foreign_field_mock.related_model = MockModel
foreign_field_mock.name = "parent"

child_meta = MagicMock()
child_meta.verbose_name = "Mock Child Model"
child_meta.verbose_name_plural = "mock child models"
child_meta.get_fields.return_value = [foreign_field_mock]
child_meta.model_name = "mockchildmodel"

MockChildModel = MagicMock(spec=models.Model)
MockChildModel._meta = child_meta
MockChildModel.__str__.return_value = "Child Object"
MockChildModel.__name__ = "MockChildModel"
MockChildModel.get_absolute_url = MagicMock(return_value="/mockchildmodel/1/")
