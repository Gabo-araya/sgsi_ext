"""
IMPORTANT: Each time you define a new model, you need to define an entry containing
the underscored name and a fixture providing an instance.
"""

import pytest


@pytest.fixture
def default_objects(regular_user):
    """
    Return a dictionary of underscore model names to models.

    Each time a model is defined, a fixture must be defined and added to the signature.
    Also, a mapping of underscored model name to fixture value must be appended.
    """
    return {
        "user": regular_user,
    }
