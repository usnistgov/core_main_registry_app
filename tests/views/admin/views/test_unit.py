""" Unit tests for `core_main_registry_app.views.admin.views` package
"""
from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase

from core_main_registry_app.views.admin import views as admin_views


class TestUploadCustomResourceSaveCustomResources(SimpleTestCase):
    """Unit tests for `UploadCustomResource._save_custom_resources` method."""

    def setUp(self):
        self.view = admin_views.UploadCustomResource()
        self.mock_kwargs = {"request": MagicMock(), "template_id": MagicMock()}

    @patch.object(admin_views, "admin_render")
    @patch.object(admin_views, "template_api")
    def test_template_get_by_id_called(
        self, mock_template_api, mock_admin_render
    ):
        """test_template_get_by_id_called"""
        self.view._save_custom_resources(**self.mock_kwargs)

        mock_template_api.get_by_id.assert_called_with(
            self.mock_kwargs["template_id"],
            request=self.mock_kwargs["request"],
        )

    @patch.object(admin_views, "admin_render")
    @patch.object(admin_views, "template_api")
    def test_template_get_by_id_fails_puts_errors_in_context(
        self, mock_template_api, mock_admin_render
    ):
        """test_template_get_by_id_fails_puts_errors_in_context"""
        mock_template_api.get_by_id.side_effect = Exception(
            "mock_template_get_by_id_exception"
        )
        self.view._save_custom_resources(**self.mock_kwargs)

        self.assertIn(
            "errors",
            mock_admin_render.call_args_list[-1].kwargs["context"],
        )

    @patch.object(admin_views, "admin_render")
    @patch.object(admin_views, "load_json_string")
    @patch.object(admin_views, "template_api")
    def test_load_json_string_called(
        self, mock_template_api, mock_load_json_string, mock_admin_render
    ):
        """test_load_json_string_called"""
        mock_template_api.get_by_id.return_value = MagicMock()
        self.view._save_custom_resources(**self.mock_kwargs)

        mock_load_json_string.assert_called_with(
            self.mock_kwargs["request"]
            .FILES["json_file"]
            .read()
            .decode("utf-8")
        )

    @patch.object(admin_views, "admin_render")
    @patch.object(admin_views, "load_json_string")
    @patch.object(admin_views, "template_api")
    def test_load_json_string_fails_puts_errors_in_context(
        self, mock_template_api, mock_load_json_string, mock_admin_render
    ):
        """test_load_json_string_fails_puts_errors_in_context"""
        mock_template_api.get_by_id.return_value = MagicMock()
        mock_load_json_string.side_effect = Exception(
            "mock_load_json_string_exception"
        )
        self.view._save_custom_resources(**self.mock_kwargs)

        self.assertIn(
            "errors",
            mock_admin_render.call_args_list[-1].kwargs["context"],
        )

    @patch.object(admin_views, "admin_render")
    @patch.object(admin_views, "custom_resource_api")
    @patch.object(admin_views, "load_json_string")
    @patch.object(admin_views, "template_api")
    def test_replace_custom_resources_by_template_called(
        self,
        mock_template_api,
        mock_load_json_string,
        mock_custom_resource_api,
        mock_admin_render,
    ):
        """test_replace_custom_resources_by_template_called"""
        mock_template = MagicMock()
        mock_template_api.get_by_id.return_value = mock_template
        mock_data = MagicMock()
        mock_load_json_string.return_value = mock_data
        self.view._save_custom_resources(**self.mock_kwargs)

        mock_custom_resource_api.replace_custom_resources_by_template.assert_called_with(
            mock_template, mock_data
        )

    @patch.object(admin_views, "admin_render")
    @patch.object(admin_views, "custom_resource_api")
    @patch.object(admin_views, "load_json_string")
    @patch.object(admin_views, "template_api")
    def test_replace_custom_resources_by_template_puts_errors_in_context(
        self,
        mock_template_api,
        mock_load_json_string,
        mock_custom_resource_api,
        mock_admin_render,
    ):
        """test_replace_custom_resources_by_template_puts_errors_in_context"""
        mock_template_api.get_by_id.return_value = MagicMock()
        mock_load_json_string.return_value = MagicMock()
        mock_custom_resource_api.side_effect = Exception(
            "mock_custom_resource_api_exception"
        )
        self.view._save_custom_resources(**self.mock_kwargs)

        self.assertIn(
            "errors",
            mock_admin_render.call_args_list[-1].kwargs["context"],
        )

    @patch.object(admin_views, "HttpResponseRedirect")
    @patch.object(admin_views, "reverse")
    @patch.object(admin_views, "custom_resource_api")
    @patch.object(admin_views, "load_json_string")
    @patch.object(admin_views, "template_api")
    def test_success_returns_http_response_redirect(
        self,
        mock_template_api,
        mock_load_json_string,
        mock_custom_resource_api,
        mock_reverse,
        mock_http_response_redirect,
    ):
        """test_success_returns_http_response_redirect"""
        mock_template_api.get_by_id.return_value = MagicMock()
        mock_load_json_string.return_value = MagicMock()
        mock_custom_resource_api.return_value = None
        mock_http_response_redirect_value = MagicMock()
        mock_http_response_redirect.return_value = (
            mock_http_response_redirect_value
        )

        self.assertEqual(
            self.view._save_custom_resources(**self.mock_kwargs),
            mock_http_response_redirect_value,
        )
