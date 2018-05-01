""" discover rules for core main registry app
"""
from os.path import join

from django.contrib.staticfiles import finders

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.components.template_version_manager.models import TemplateVersionManager
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.utils.file import read_file_content
from core_main_registry_app.settings import REGISTRY_XSD_FILENAME


def init_registry():
    """ Init the registry. Add the registry template.

    Returns:

    """
    try:
        # Add template
        _add_template()
    except Exception, e:
        print('ERROR : Impossible to init the registry. ' + e.message)


def _add_template():
    """ Add the registry template.

    Returns:
        Registry Template.

    """
    xsd_filename = REGISTRY_XSD_FILENAME
    if xsd_filename == '':
        raise Exception('Please configure the REGISTRY_XSD_FILENAME setting in your project.')
    try:
        version_manager_api.get_active_global_version_manager_by_title(xsd_filename)
    except exceptions.DoesNotExist:
        default_xsd_path = finders.find(join('core_main_registry_app', 'xsd', xsd_filename))
        xsd_data = read_file_content(default_xsd_path)
        template = Template(filename=xsd_filename, content=xsd_data)
        template_version_manager = TemplateVersionManager(title=xsd_filename)
        template_version_manager_api.insert(template_version_manager, template)
    except Exception, e:
        raise Exception('Impossible to add the template : ' + e.message)
