"""
Constants for core main registry app
"""
from enum import Enum

# Create an unspecified category when 2+ levels.
UNSPECIFIED_CATEGORY = True
# Path to status
PATH_STATUS = "Resource.@status"

CUSTOM_RESOURCE_TYPE = Enum(
    "CUSTOM_RESOURCE_TYPE", {"RESOURCE": "resource", "ALL": "all"}
)

CATEGORY_SUFFIX = "__category"
UNSPECIFIED_LABEL = "unspecified"
