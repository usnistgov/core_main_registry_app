""" Unit tests for menus
"""
from unittest import TestCase
from unittest.mock import MagicMock

from core_main_registry_app.utils.menu.menu_utils import (
    show_template_upload_menu,
)


class TestMenus(TestCase):
    """Tests menus"""

    def setUp(self) -> None:
        """

        Returns:

        """
        self.mock_menu_item_child = MagicMock(
            title="Upload New Template", visible=True
        )
        self.mock_menu_item = MagicMock(
            title="TEMPLATES", children=[self.mock_menu_item_child]
        )
        self.mock_menu = MagicMock(items={"admin": [self.mock_menu_item]})

    def test_template_upload_in_menus(self):
        """test_template_upload_in_menus"""

        show_template_upload_menu(self.mock_menu, allow_multiple_schemas=True)
        self.assertTrue(self.mock_menu_item_child.visible)

    def test_template_upload_not_in_menus(self):
        """test_template_upload_not_in_menus"""

        show_template_upload_menu(self.mock_menu, allow_multiple_schemas=False)
        self.assertFalse(self.mock_menu_item_child.visible)
