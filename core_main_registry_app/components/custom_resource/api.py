""" Custom Resource api
"""

import logging

from django.conf import settings

from core_main_app.commons import exceptions as exceptions
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_registry_app.components.custom_resource.models import (
    CustomResource,
)
from core_main_registry_app.constants import CUSTOM_RESOURCE_TYPE
from core_main_registry_app.settings import REGISTRY_XSD_FILENAME

logger = logging.getLogger(
    "core_main_registry_app.components.custom_resource.api"
)


def parse_and_save(data, current_template):
    """Parse the data to create custom resources and save them.

    Args:
     data: dict
     current_template:
    Returns:
    """
    # Build list of custom resources from data
    custom_resources_list = get_resources_from_dict(data)
    # Save custom resources
    for custom_resource in custom_resources_list:
        custom_resource.template = current_template
        try:
            custom_resource.save()
        except Exception as exception:
            raise exceptions.ModelError(str(exception))


def get_resources_from_dict(resource_dict):
    """Get list of custom resources from dictionary

    Args:
        resource_dict:

    Returns:

    """
    # Initialize list
    custom_resources_list = list()
    # Create Custom Resources
    for key in resource_dict.keys():
        resource = resource_dict[key]
        custom_resource = CustomResource()
        custom_resources_list.append(
            _create_custom_resource(custom_resource, resource, key)
        )
    # Return list of custom resources
    return custom_resources_list


def _check_curate(custom_resource):
    """Check if we have all information from configuration file for curate.

    Args:
        custom_resource:
    Returns:
    """
    if (
        _is_custom_resource_type_resource(custom_resource)
        and "core_curate_app" in settings.INSTALLED_APPS
        and (
            custom_resource.role_choice is None
            or custom_resource.role_type is None
        )
    ):
        raise exceptions.ModelError(
            "Curate app is installed. "
            "You need url key, role choice and role type configured in configuration file."
        )


def _is_custom_resource_type_resource(custom_resource):
    """Is the custom resource a resource.

    Args:
        custom_resource:
    Returns:
    """
    return custom_resource.type == CUSTOM_RESOURCE_TYPE.RESOURCE.value


def _is_type_all(resource):
    """Check if type of  resource is 'all'.

    Args:
     resource:
    Returns:
    """
    try:
        return resource["type"] == CUSTOM_RESOURCE_TYPE.ALL.value
    except Exception:
        raise exceptions.ModelError("The configuration file is not valid.")


def _create_custom_resource(custom_resource, resource, key):
    """Create a custom resource.

    Args:
     custom_resource:
     resource:
     key:
    Returns:
    """
    if _is_type_all(resource):
        custom_resource.type = CUSTOM_RESOURCE_TYPE.ALL.value
    else:
        custom_resource.type = CUSTOM_RESOURCE_TYPE.RESOURCE.value
        custom_resource.role_choice = resource.get("role_choice", None)
        custom_resource.role_type = resource.get("role_type", None)
        custom_resource.description = resource.get("description", None)
        custom_resource.refinements = resource.get("refinements", None)
    custom_resource.name_in_schema = key
    custom_resource.title = resource.get("title", None)
    custom_resource.icon = resource.get("icon", None)
    custom_resource.icon_color = resource.get("icon_color", None)
    custom_resource.display_icon = resource.get("display_icon", None)
    custom_resource.sort = resource.get("sort", None)
    _check_curate(custom_resource)
    return custom_resource


def get_all_by_template(template):
    """Return all custom resource by template.

    Args:
         template:

    Returns: custom registry collection
    """
    return CustomResource.get_all_by_template(template)


def get_all_of_current_template(request):
    """Return all custom resource of the current template.

    Args:

    Returns: custom registry collection
    """
    return get_all_by_template(_get_current_template(request=request))


def get_current_custom_resource_type_all(request):
    """Return the custom resource of the current template with type 'all'.

    Args:
        request

    Returns: custom registry collection
    """
    custom_resources = CustomResource.get_custom_resource_by_template_and_type(
        _get_current_template(request=request), CUSTOM_RESOURCE_TYPE.ALL.value
    )
    if len(custom_resources) > 1:
        raise exceptions.ModelError(
            "Multiple custom resources with type 'all' were found."
        )
    if len(custom_resources) == 0:
        raise exceptions.DoesNotExist(
            "The custom resource with type 'all' does not exist."
        )
    return custom_resources[0]


def _get_current_template(request):
    """Get the current template.

    Args:
        request:

    Returns:
    """
    current_template_version = template_version_manager_api.get_active_global_version_manager_by_title(
        REGISTRY_XSD_FILENAME, request=request
    )
    current_template = template_api.get_by_id(
        current_template_version.current, request=request
    )
    return current_template


def get_by_current_template_and_slug(slug, request):
    """Get the custom resource by template and slug

    Args:
        slug:
        request:

    Returns:

    """
    return CustomResource.get_custom_resource_by_template_and_slug(
        _get_current_template(request=request), slug
    )


def get_by_role_for_current_template(role, request):
    """Get the custom resource by template and slug

    Args:
        role:
        request:

    Returns:

    """
    return CustomResource.get_by_role_for_current_template(
        _get_current_template(request=request), role
    )


def delete_custom_resources_by_template(template):
    """Delete all custom resources related to a template.

    Args:
        template:

    Returns:
    """
    CustomResource.delete_custom_resources_by_template(template)


def save_list(list_custom_resources, force_insert=False):
    """Save list of custom resource.

    Args:
        list_custom_resources:
        force_insert:

    Returns:
    """
    for custom_resource in list_custom_resources:
        custom_resource.save(force_insert=force_insert)


def replace_custom_resources_by_template(template, data):
    """Replace all custom resources by the one in data.
    Rollback if error.

    Args:
        template:
        data:

    Returns:
    """
    old_custom_resources = []
    try:
        # old custom resources
        old_custom_resources = list(get_all_by_template(template))

        # delete old custom resources
        delete_custom_resources_by_template(template)

        # create new custom resources
        parse_and_save(data, template)

    except Exception as exception:
        # rollback old custom resource
        save_list(old_custom_resources, True)
        raise exception
