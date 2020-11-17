""" Authentication tests for Template Version Manager REST API
"""
from django.test import SimpleTestCase
from mock.mock import patch
from rest_framework import status

from core_main_app.components.template.models import Template
from core_main_registry_app.rest.template_version_manager import (
    views as template_version_manager_views,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestCurrentTemplateVersionPatchPermission(SimpleTestCase):
    def setUp(self):
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_patch(
            template_version_manager_views.CurrentTemplateVersion.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            template_version_manager_views.CurrentTemplateVersion.as_view(),
            mock_user,
            data={},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_registry_app.components.version_manager.api.set_current")
    @patch("core_main_app.components.version_manager.api.get_from_version")
    @patch.object(Template, "get_by_id")
    def test_staff_returns_http_200(
        self,
        template_get_by_id,
        version_manager_get_from_version,
        version_manager_set_current,
    ):
        version_manager_set_current.return_value = {}
        version_manager_get_from_version.return_value = {}
        template_get_by_id.return_value = Template(user=None)

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            template_version_manager_views.CurrentTemplateVersion.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
