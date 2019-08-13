""" discover rules for core main registry app
"""
import json
import logging
from os.path import join

from django.contrib.staticfiles import finders

from core_main_app.commons import exceptions
from core_main_app.components.template import api as template_api
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.components.template_version_manager.models import TemplateVersionManager
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.utils.file import read_file_content
from core_main_registry_app.components.custom_resource import api as custom_resource_api
from core_main_registry_app.components.template import api as template_registry_api
from core_main_registry_app.settings import REGISTRY_XSD_FILEPATH, CUSTOM_REGISTRY_FILE_PATH, REGISTRY_XSD_FILENAME
from core_main_registry_app.utils.refinement import refinement
from core_main_registry_app.utils.refinement import watch as refinement_watch

logger = logging.getLogger("core_main_registry_app.discover")


def init_registry():
    """ Init the registry. Add the registry template.

    Returns:

    """
    try:
        # Add template
        _add_template()
        # Init the refinements from the schema.
        _init_refinements()
        # Init Custom Registry
        _init_custom_registry()
        # init watcher
        refinement_watch.init()
    except Exception as e:
        logger.error("Impossible to init the registry: {0}".format(str(e)))


def _add_template():
    """ Add the registry template.

    Returns:

    """
    xsd_filepath = REGISTRY_XSD_FILEPATH
    xsd_filename = REGISTRY_XSD_FILENAME
    if xsd_filename == '':
        raise Exception('Please configure the REGISTRY_XSD_FILENAME setting in your project.')
    if xsd_filepath == '':
        raise Exception('Please configure the REGISTRY_XSD_FILEPATH setting in your project.')
    try:
        version_manager_api.get_active_global_version_manager_by_title(xsd_filename)
    except exceptions.DoesNotExist:
        default_xsd_path = finders.find(xsd_filepath)
        xsd_data = read_file_content(default_xsd_path)
        template = Template(filename=xsd_filename, content=xsd_data)
        template_version_manager = TemplateVersionManager(title=xsd_filename)
        template_version_manager_api.insert(template_version_manager, template)
    except Exception as e:
        logger.error("Impossible to add the template: {0}".format(str(e)))


def _init_refinements():
    """ Init the refinements.
    """
    try:
        # Get global template.
        template = template_registry_api.get_current_registry_template()
        # Init.
        refinement.init_refinements(template)
    except Exception as e:
        logger.error("Impossible to init the refinements: {0}".format(str(e)))


def _init_custom_registry():
    """ Init the custom registry.

    Returns:
    """

    try:
        current_template_version = version_manager_api.get_active_global_version_manager_by_title(REGISTRY_XSD_FILENAME)
        current_template = template_api.get(version_manager_api.get_current(current_template_version))
    except:
        raise Exception("Can't get the current template.")

    if len(custom_resource_api.get_all_by_template(current_template)) > 0:
        logger.info("Custom resources related to current template already exist.")
    else:
        json_path = CUSTOM_REGISTRY_FILE_PATH
        if json_path == '':
            raise Exception('Please configure the CUSTOM_REGISTRY_FILE_PATH setting in your project.')

        try:
            default_json_path = finders.find(json_path)
            with open(default_json_path) as json_file:
                data = json.load(json_file)
                custom_resource_api.parse_and_save(data, current_template)
        except Exception as e:
            logger.error("Impossible to use the custom registry json file: {0}".format(str(e)))
