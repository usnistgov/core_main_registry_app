""" Menu utils
"""


def show_template_upload_menu(menu, allow_multiple_schemas=False):
    """Show template upload menu

    Args:
        menu:
        allow_multiple_schemas:

    Returns:

    """
    if not allow_multiple_schemas:
        for admin_menu_item in menu.items["admin"]:
            if admin_menu_item.title == "TEMPLATES":
                for template_menu_item_child in admin_menu_item.children:
                    if template_menu_item_child.title == "Upload New Template":
                        template_menu_item_child.visible = False
