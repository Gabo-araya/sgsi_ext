"""
Settings overrides for unit testing.
"""

from .settings import *  # noqa:F401,F403

# Use a simpler password hash algorithm to speed up test execution when password hashing
# is intensively used, directly or indirectly.
# (See https://docs.djangoproject.com/en/4.0/topics/testing/overview/#password-hashing)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
]

# Code should not behave differently when running tests.
# Access this setting only if strictly required.
TEST = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'tmp/cache'
    }
}
