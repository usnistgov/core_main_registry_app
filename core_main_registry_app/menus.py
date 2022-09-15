""" Menu configuration for core_main_registry_app.
"""
from django.urls import reverse
from menu import Menu, MenuItem

# Remove 'Upload New Template' option from menu
for admin_menu_item in Menu.items["admin"]:
    if admin_menu_item.title == "TEMPLATES":
        for template_menu_item_child in admin_menu_item.children:
            if template_menu_item_child.title == "Upload New Template":
                template_menu_item_child.visible = False

config_children = (
    MenuItem(
        "Configuration",
        reverse("core-admin:core_main_registry_app_custom_registry"),
        icon="upload",
    ),
)

Menu.add_item("admin", MenuItem("CUSTOM REGISTRY", None, children=config_children))
