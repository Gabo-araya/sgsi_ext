import uuid

from base import utils


# public methods
def file_path(instance, name):
    """
    Generic method used to give a FileField or ImageField its `upload_to`
    parameter.

    This returns the name of the model instance, concatenated with the id of the
    object and the name of the file.
    """
    base_path = "{}/{}/{}/{}"

    return base_path.format(
        instance.__class__.__name__,
        utils.today().strftime(r"%Y/%m/%d"),
        uuid.uuid4(),
        name,
    )
