""" This document defines the UserManager class"""


from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            msg = "The given email must be set"
            raise ValueError(msg)
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email=None,
        first_name=None,
        last_name=None,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def create_superuser(
        self,
        email,
        password,
        first_name=None,
        last_name=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            msg = "Superuser must have is_staff=True."
            raise ValueError(msg)
        if extra_fields.get("is_superuser") is not True:
            msg = "Superuser must have is_superuser=True."
            raise ValueError(msg)

        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def get_or_none(self, **fields):
        return self.get_queryset().get_or_none(**fields)
