""" Core main registry app settings

Settings with the following syntax can be overwritten at the project level:
SETTING_NAME = getattr(settings, "SETTING_NAME", "Default Value")
"""
from os.path import join

from django.conf import settings

if not settings.configured:
    settings.configure()

REGISTRY_XSD_FILEPATH = getattr(
    settings,
    "REGISTRY_XSD_FILEPATH",
    join("core_main_registry_app", "xsd", "res-md.xsd"),
)
""" str: Registry xsd path used for the initialisation.
"""

REGISTRY_XSD_FILENAME = getattr(settings, "REGISTRY_XSD_FILENAME", "")
""" str: Registry xsd filename used for the initialisation.
"""

CUSTOM_REGISTRY_FILE_PATH = getattr(
    settings,
    "CUSTOM_REGISTRY_FILE_PATH",
    join("core_main_registry_app", "json", "custom_registry.json"),
)
""" str: Custom registry configuration file path used for the initialisation.
"""

ENABLE_BLOB_ENDPOINTS = getattr(settings, "ENABLE_BLOB_ENDPOINTS", False)
""" bool: Enable blob api and user views for blob management.
"""

ALLOW_MULTIPLE_SCHEMAS = getattr(settings, "ALLOW_MULTIPLE_SCHEMAS", False)
""" bool: Enable the use of multiple schemas in the registry.
"""
