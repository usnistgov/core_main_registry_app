""" System api to access data without access control neither API rules
"""
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.components.version_manager.utils import get_latest_version_name
from core_main_app.utils.xml import is_schema_valid, get_hash
from core_main_app.system import api as main_system_api
from core_main_registry_app.settings import REGISTRY_XSD_FILENAME
from core_main_app.commons import exceptions as exceptions


def is_local_id_already_used(local_id):
    """Check if the local id given already exist in db

    Args:
        local_id:

    Returns:

    """
    return Data.objects(__raw__={"dict_content.Resource.@localid": str(local_id)})


def insert_registry_schema(xsd_filename, xsd_content):

    # Check if schema is valid
    is_schema_valid(xsd_content)
    template = Template(
        filename=xsd_filename, hash=get_hash(xsd_content), content=xsd_content
    ).save()
    template_version_manager = TemplateVersionManager(title=xsd_filename)
    # save the template in database
    try:
        from core_main_app.components.version_manager import api as version_manager_api

        # insert the initial template in the version manager
        template_version_manager.insert(template)
        template_version_manager.set_current_version(template)
        # insert the version manager in database
        template_version_manager.save_version_manager()
        # get template display name
        display_name = get_latest_version_name(template_version_manager)
        # update saved template
        template.display_name = display_name
        template.save()
        # return version manager
        return template_version_manager
    except Exception as e:
        template.delete()
        raise e


def get_current_registry_template():
    """Get the current template used for the registry.

    Args:

    Returns:

    """
    try:
        template_version = main_system_api.get_active_global_version_manager_by_title(
            REGISTRY_XSD_FILENAME
        )
        return main_system_api.get_template_by_id(template_version.current)
    except Exception as e:
        raise exceptions.ModelError(str(e))
