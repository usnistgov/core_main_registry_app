""" Authentication tests for Template Version Manager REST API
"""
from django.test import SimpleTestCase
from unittest.mock import patch
from rest_framework import status

from core_main_app.components.template.models import Template
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_main_registry_app.rest.template_version_manager import (
    views as template_version_manager_views,
)


class TestCurrentTemplateVersionPatchPermission(SimpleTestCase):
    """Test Current Template Version Patch Permission"""

    def setUp(self):
        """setUp"""

        self.fake_id = -1

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_patch(
            template_version_manager_views.CurrentTemplateVersion.as_view(),
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            template_version_manager_views.CurrentTemplateVersion.as_view(),
            mock_user,
            data={},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_registry_app.components.version_manager.api.set_current")
    @patch.object(Template, "get_by_id")
    def test_staff_returns_http_200(
        self,
        template_get_by_id,
        version_manager_set_current,
    ):
        """test_staff_returns_http_200"""

        version_manager_set_current.return_value = {}
        template_get_by_id.return_value = Template(user=None)

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            template_version_manager_views.CurrentTemplateVersion.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
