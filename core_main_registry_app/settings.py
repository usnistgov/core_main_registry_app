""" Core main registry app settings
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

REGISTRY_XSD_FILENAME = getattr(settings, 'REGISTRY_XSD_FILENAME', "")
""" str: Registry xsd filename used for the initialisation.
"""

CUSTOM_REGISTRY_FILE_PATH = getattr(settings, 'CUSTOM_REGISTRY_FILE_PATH', "")
""" str: Custom registry configuration file path used for the initialisation.
"""