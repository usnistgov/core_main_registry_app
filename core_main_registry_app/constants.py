"""
Constants for core main registry app
"""
from core_main_app.utils.enum import enum

NMRR_XSD_FILENAME = 'res-md.xsd'
# Create an unspecified category when 2+ levels.
UNSPECIFIED_CATEGORY = True
# Path to status
PATH_STATUS = "Resource.@status"

CUSTOM_RESOURCE_TYPE = enum(RESOURCE='resource',
                            ALL='all')
