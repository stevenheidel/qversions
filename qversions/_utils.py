
def validate_field(obj, name, typ, optional=False):
    """
    Ensure an object field is the correct type and defined.
    """
    value = obj.__dict__.get(name)

    if not (value is None or isinstance(value, typ)):
        raise TypeError("{} must be a {}".format(name, typ))

    if not optional and value is None:
        raise ValueError("{} must be defined".format(name))

def validate_param(name, value, typ):
    """
    Ensure that a method param is the correct type and defined.
    """
    if value is None:
        raise ValueError("{} must be defined".format(name))

    if not isinstance(value, typ):
        raise TypeError("{} must be a {}".format(name, typ))
