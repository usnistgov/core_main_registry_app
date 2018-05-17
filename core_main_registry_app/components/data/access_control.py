""" Set of functions to define the rules for access control in registry
"""
from core_main_app.components.data.access_control import check_can_write_data, has_perm_publish_data


def can_publish_data(func, data, user):
    """ Can user publish data.

    Args:
        func:
        data:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(data, user)

    has_perm_publish_data(user)
    check_can_write_data(data, user)
    return func(data, user)