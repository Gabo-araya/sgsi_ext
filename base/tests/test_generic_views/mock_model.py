from django.db import models


class MockModel(models.Model):
    class Meta:
        verbose_name = "Mock Model"
        verbose_name_plural = "mock models"

    def __str__(self) -> str:
        return "Object"

    def get_absolute_url(self):
        return "/mockmodel/1/"


class MockChildModel(models.Model):
    parent = models.ForeignKey(MockModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Mock Child Model"
        verbose_name_plural = "mock child models"

    def __str__(self) -> str:
        return "Child Object"

    def get_absolute_url(self):
        return "/mockchildmodel/1/"
