""" Menu configuration for core_main_registry_app.
"""
from django.urls import reverse
from menu import Menu, MenuItem

from core_main_registry_app.settings import ALLOW_MULTIPLE_SCHEMAS
from core_main_registry_app.utils.menu.menu_utils import (
    show_template_upload_menu,
)

# Remove 'Upload New Template' option from menu
show_template_upload_menu(
    menu=Menu, allow_multiple_schemas=ALLOW_MULTIPLE_SCHEMAS
)

config_children = (
    MenuItem(
        "Configuration",
        reverse("core-admin:core_main_registry_app_custom_registry"),
        icon="upload",
    ),
)

Menu.add_item(
    "admin", MenuItem("CUSTOM REGISTRY", None, children=config_children)
)
