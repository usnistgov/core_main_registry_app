"""
Constants for core main registry app
"""
from core_main_app.utils.enum import enum

# Create an unspecified category when 2+ levels.
UNSPECIFIED_CATEGORY = True
# Path to status
PATH_STATUS = "Resource.@status"

CUSTOM_RESOURCE_TYPE = enum(RESOURCE='resource',
                            ALL='all')
