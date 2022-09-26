"""
Version Manager API
"""

from core_main_app.commons import exceptions as exceptions
from core_main_app.components.version_manager import api as version_manager_api
from core_main_registry_app.components.custom_resource import (
    api as custom_resource_api,
)


# NOTE: access control by main set current
def set_current(version, request):
    """Set the current version of the object, then saves it.

    Args:
        version:
        request:

    Returns:

    """
    if custom_resource_api.get_all_by_template(version).count() == 0:
        raise exceptions.ApiError(
            "Please link a Custom Resources file to this template before setting it to current."
        )
    version_manager_api.set_current(version, request=request)
