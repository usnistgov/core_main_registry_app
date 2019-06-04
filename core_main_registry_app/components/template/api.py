""" Template's registry api
"""

from core_main_app.commons import exceptions as exceptions
from core_main_app.components.template import api as template_api
from core_main_app.components.version_manager import api as version_manager_api
from core_main_registry_app.settings import REGISTRY_XSD_FILENAME


def get_current_registry_template():
    """ Get the current template used for the registry.

    Returns:
        Template:

    """
    try:
        template_version = version_manager_api.\
            get_active_global_version_manager_by_title(REGISTRY_XSD_FILENAME)
        return template_api.get(version_manager_api.get_current(template_version))
    except Exception as e:
        raise exceptions.ModelError(str(e))
