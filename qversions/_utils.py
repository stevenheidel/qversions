
def validate_field(obj, name, typ):
    """
    Ensure an object field is the correct type and defined.
    """
    value = obj.__dict__.get(name)

    validate_param(name, value, typ)

def validate_param(name, value, typ):
    """
    Ensure that a method param is the correct type and defined.
    """
    if value is None:
        raise ValueError("{} must be defined".format(name))

    if not isinstance(value, typ):
        raise TypeError("{} must be a {}".format(name, typ))
