""" Core main registry app settings
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

REGISTRY_XSD_FILENAME = getattr(settings, 'REGISTRY_XSD_FILENAME', "")
""" str: Registry xsd filename used for the initialisation.
"""
