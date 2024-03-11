""" Unit test views
"""
from unittest.mock import patch

from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, SimpleTestCase

from core_main_app.commons.exceptions import ModelError
from core_main_app.components.template.models import Template
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_registry_app.views.admin import views as admin_views


class TestCustomRegistry(SimpleTestCase):
    """Test Custom Registry"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1", is_staff=True)

    @patch(
        "core_main_registry_app.components.template.api.get_current_registry_template"
    )
    @patch("core_main_registry_app.views.admin.views.admin_render")
    @patch.object(admin_views, "messages")
    def test_get_custom_registry_returns_rendered_page(
        self,
        mock_messages,
        mock_admin_render,
        mock_get_current_registry_template,
    ):
        """test_get_custom_registry_returns_rendered_page

        Returns:

        """
        # Arrange
        request = self.factory.get("core_main_registry_app_custom_registry")
        request.user = self.user1
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        # Act
        response = admin_views.CustomRegistry.as_view()(request)

        # Assert
        self.assertTrue(response, mock_admin_render.return_value)
        self.assertTrue(mock_get_current_registry_template.called)

    @patch(
        "core_main_registry_app.components.template.api.get_current_registry_template"
    )
    @patch("core_main_registry_app.views.admin.views.admin_render")
    @patch.object(admin_views, "messages")
    def test_get_custom_registry_with_model_error_returns_rendered_page_with_message(
        self,
        mock_messages,
        mock_admin_render,
        mock_get_current_registry_template,
    ):
        """test_get_custom_registry_returns_rendered_page

        Returns:

        """
        # Arrange
        mock_get_current_registry_template.side_effect = ModelError("error")
        request = self.factory.get("core_main_registry_app_custom_registry")
        request.user = self.user1
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        # Act
        response = admin_views.CustomRegistry.as_view()(request)

        # Assert
        self.assertTrue(response, mock_admin_render.return_value)
        self.assertTrue(mock_get_current_registry_template.called)
        self.assertTrue(mock_messages.add_message.called)


class TestManageTemplates(SimpleTestCase):
    """Test Manage Templates"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1", is_staff=True)

    @patch("core_main_registry_app.views.admin.views.admin_render")
    @patch("core_main_app.components.template_version_manager.api.get_by_id")
    @patch(
        "core_main_app.components.template_version_manager.api.get_global_version_managers"
    )
    @patch(
        "core_main_registry_app.components.template.api.get_current_registry_template"
    )
    def test_get_manage_templates_returns_rendered_page(
        self,
        mock_get_current_registry_template,
        mock_get_global_version_managers,
        mock_get_by_id,
        mock_admin_render,
    ):
        """test_get_manage_templates_returns_rendered_page

        Returns:

        """
        # Arrange
        request = self.factory.get("core_main_registry_app_templates")
        request.user = self.user1

        mock_get_current_registry_template.return_value = Template(
            version_manager_id=1
        )
        mock_get_global_version_managers.return_value = []
        mock_get_by_id.return_value = None
        # Act
        response = admin_views.ManageTemplatesRegistryView.as_view()(request)

        # Assert
        self.assertTrue(response, mock_admin_render.return_value)
        self.assertTrue(mock_get_current_registry_template.called)
        self.assertTrue(mock_get_global_version_managers.called)
        self.assertTrue(mock_get_by_id.called)
