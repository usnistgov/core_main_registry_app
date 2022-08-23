""" discover rules for core main registry app
"""
import json
import logging

from django.contrib.staticfiles import finders

from core_main_app.commons import exceptions
from core_main_app.system import api as system_api
from core_main_app.utils.file import read_file_content
from core_main_registry_app.settings import (
    REGISTRY_XSD_FILEPATH,
    CUSTOM_REGISTRY_FILE_PATH,
    REGISTRY_XSD_FILENAME,
)
from core_main_registry_app.system import api as registry_system_api

logger = logging.getLogger("core_main_registry_app.discover")


def init_registry():
    """Init the registry. Add the registry template.

    Returns:

    """
    from core_main_registry_app.utils.refinement import watch as refinement_watch

    try:
        # Add template
        _add_template()
        # Init the refinements from the schema.
        _init_refinements()
        # Init Custom Registry
        _init_custom_registry()
        # init watcher
        refinement_watch.init()
    except Exception as exception:
        logger.error("Impossible to init the registry: %s", str(exception))


def _add_template():
    """Add the registry template.

    Returns:

    """

    xsd_filepath = REGISTRY_XSD_FILEPATH
    xsd_filename = REGISTRY_XSD_FILENAME
    if xsd_filename == "":
        raise Exception(
            "Please configure the REGISTRY_XSD_FILENAME setting in your project."
        )
    if xsd_filepath == "":
        raise Exception(
            "Please configure the REGISTRY_XSD_FILEPATH setting in your project."
        )
    try:
        system_api.get_active_global_version_manager_by_title(xsd_filename)
    except exceptions.DoesNotExist:
        default_xsd_path = finders.find(xsd_filepath)
        xsd_data = read_file_content(default_xsd_path)
        registry_system_api.insert_registry_schema(xsd_filename, xsd_data)
    except Exception as exception:
        logger.error("Impossible to add the template:  %s", str(exception))


def _init_refinements():
    """Init the refinements."""
    from core_main_registry_app.utils.refinement import refinement

    try:
        # Get global template.
        template = registry_system_api.get_current_registry_template()
        # Init.
        refinement.init_refinements(template)
    except Exception as exception:
        logger.error("Impossible to init the refinements:  %s", str(exception))


def _init_custom_registry():
    """Init the custom registry.

    Returns:
    """
    from core_main_registry_app.components.custom_resource import (
        api as custom_resource_api,
    )

    try:
        current_template_version = (
            system_api.get_active_global_version_manager_by_title(REGISTRY_XSD_FILENAME)
        )
        current_template = current_template_version.current_version
    except:
        raise Exception("Can't get the current template.")

    if custom_resource_api.get_all_by_template(current_template).count() > 0:
        logger.info("Custom resources related to current template already exist.")
    else:
        json_path = CUSTOM_REGISTRY_FILE_PATH
        if json_path == "":
            raise Exception(
                "Please configure the CUSTOM_REGISTRY_FILE_PATH setting in your project."
            )

        try:
            default_json_path = finders.find(json_path)
            with open(default_json_path, encoding="utf-8") as json_file:
                data = json.load(json_file)
                custom_resource_api.parse_and_save(data, current_template)
        except Exception as exception:
            logger.error(
                "Impossible to use the custom registry json file:  %s", str(exception)
            )
