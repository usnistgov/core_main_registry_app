""" Menu configuration for core_main_registry_app.
"""
from menu import Menu

# Remove 'Upload New Template' option from menu
for admin_menu_item in Menu.items['admin']:
    if admin_menu_item.title == 'TEMPLATES':
        for template_menu_item_child in admin_menu_item.children:
            if template_menu_item_child.title == 'Upload New Template':
                template_menu_item_child.visible = False
