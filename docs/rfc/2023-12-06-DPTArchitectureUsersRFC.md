# About DPT Architecture - Users

## Context

While Django provides a simple user model that serves the basic authentication needs, sometimes more information about the users is needed and since most of our clients are located in Chile, the majority of them need to store the person's national identity number.

## Proposed solution

A reimplementation of the User model is provided, using the email account as the main identifier of account, instead of username. All the other fields are kept from parent classes as-is.

## Modeling

```plantuml
class django.contrib.auth.base_user.AbstractBaseUser {
  password: CharField
  last_login: DateTimeField
  __Properties__
  is_anonymous
  is_authenticated
  __
  save(*args, **kwargs)
  check_password(raw_password)
  set_password(raw_password)
  has_unusable_password()
  set_unusable_password()
  ...
}

class django.contrib.auth.models.PermissionsMixin {
  is_superuser: BooleanField
  groups: ManyToManyField
  user_permissions: ManyToManyField
  get_user_permissions(obj)
  get_group_permissions(obj)
  get_all_permissions(obj)
  has_perm(perm, obj)
  has_perms(perm, obj)
}

class django.contrib.auth.models.AbstractUser {
  username: CharField
  first_name: CharField
  last_name: CharField
  email: EmailField
  is_staff: BooleanField
  is_active: BooleanField
  date_joined: DateTimeField
  get_full_name()
  get_short_name()
}

class base.models.BaseModel {
  created_at: DateTimeField
  updated_at: DateTimeField
}

class users.models.User {
  email: EmailField
  first_name: CharField
  last_name: PositiveIntegerField
  is_staff: BooleanField
  is_active: BooleanField
  date_joined: DateTimeField
  send_example_email()
  send_recover_password_email(request)
  force_logout()
}

django.db.models.Model <|-- django.contrib.auth.base_user.AbstractBaseUser
django.contrib.auth.base_user.AbstractBaseUser <|-r- django.contrib.auth.models.AbstractUser
django.contrib.auth.models.PermissionsMixin <|-- django.contrib.auth.models.AbstractUser

django.contrib.auth.models.AbstractUser <|-- django.contrib.auth.models.User

base.mixins.AuditMixin <|-- base.models.BaseModel
django.db.models.Model <|-- base.models.BaseModel

django.contrib.auth.base_user.AbstractBaseUser <|-- users.models.User
django.contrib.auth.models.PermissionsMixin <|-- users.models.User
base.models.BaseModel <|-- users.models.User
```
