""" Custom Resource model
"""
import logging

from core_main_app.commons import exceptions as exceptions
from django.conf import settings

from core_main_registry_app.components.custom_resource.models import CustomResource
from core_main_registry_app.constants import CUSTOM_RESOURCE_TYPE

logger = logging.getLogger("core_main_registry_app.components.custom_resource.api")


def parse_and_save(data, current_template):
    """ Parse the data to create custom resources and save them.

    Args:
     data: dict
     current_template:
    Returns:
    """

    for key in data.keys():
        resource = data[key]

        custom_resource = CustomResource(template=current_template)

        if _is_type_all(resource):
            custom_resource = _create_custom_resource_type_all(custom_resource, resource)
            # TODO: make sure only one type = 'all' ?
        else:
            custom_resource = _create_custom_resource(custom_resource, resource, key)

        try:
            _check_curate(custom_resource)
            custom_resource.save()
        except Exception as e:
            raise exceptions.ModelError(str(e))


def _check_curate(custom_resource):
    """ Check if we have all information from configuration file for curate.

    Args:
        custom_resource:
    Returns:
    """
    if _is_custom_resource_type_resource(custom_resource) and 'core_curate_app' in settings.INSTALLED_APPS and \
            (custom_resource.url is None
             or custom_resource.role_choice is None
             or custom_resource.role_type is None):
        raise exceptions.ModelError("Curate app is installed. "
                                    "You need url key, role choice and role type configured in configuration file.")


def _get_value(dict, key):
    """ Get the value from the dict with the key.

    Args:
     dict:
     key:
    Returns:
    """
    try:
        return dict[key]
    except:
        logger.warning("The key {0} is missing from the JSON file.".format(key))
        return None


def _is_custom_resource_type_resource(custom_resource):
    """ Is the custom resource a resource.

    Args:
        custom_resource:
    Returns:
    """
    return custom_resource.type == CUSTOM_RESOURCE_TYPE.RESOURCE


def _is_type_all(resource):
    """ Check if type of  resource is 'all'.

    Args:
     resource:
    Returns:
    """
    return resource['type'] == CUSTOM_RESOURCE_TYPE.ALL


def _create_custom_resource_type_all(custom_resource, resource):
    """ Create a custom resource for 'all resource'.

    Args:
     custom_resource:
     resource:
    Returns:
    """
    custom_resource.type = CUSTOM_RESOURCE_TYPE.ALL
    custom_resource.title = _get_value(resource, "title")
    custom_resource.icon = _get_value(resource, "icon")
    custom_resource.icon_color = _get_value(resource, "icon_color")
    custom_resource.sort = _get_value(resource, "sort")
    return custom_resource


def _create_custom_resource(custom_resource, resource, key):
    """ Create a custom resource.

    Args:
     custom_resource:
     resource:
     key:
    Returns:
    """
    custom_resource.type = CUSTOM_RESOURCE_TYPE.RESOURCE
    custom_resource.name_in_schema = key
    custom_resource.title = _get_value(resource, "title")
    custom_resource.url = _get_value(resource, "url_key")
    custom_resource.description = _get_value(resource, "description")
    custom_resource.icon = _get_value(resource, "icon")
    custom_resource.icon_color = _get_value(resource, "icon_color")
    custom_resource.display_icon = _get_value(resource, "display_icon")
    custom_resource.role_choice = _get_value(resource, "role_choice")
    custom_resource.role_type = _get_value(resource, "role_type")
    custom_resource.sort = _get_value(resource, "sort")
    return custom_resource


def get_all_by_template(template):
    """ Return all custom resource by template.

        Parameters:
             template:

        Returns: custom registry collection
    """
    return CustomResource.get_all_by_template(template)
