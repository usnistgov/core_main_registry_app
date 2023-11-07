""" Authentication tests for Data REST API
"""
from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
from rest_framework import status

from core_main_app.components.data import api as data_api
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_main_registry_app.rest.data import views as data_rest_views


class TestDataDetailDeletePermissions(SimpleTestCase):
    """Test Data Detail Delete Permissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_delete(
            data_rest_views.DataDetailRegistry.as_view(), None, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(
        self,
    ):
        """test_authenticated_returns_http_403"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_delete(
            data_rest_views.DataDetailRegistry.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_returns_http_403(
        self,
    ):
        """test_staff_returns_http_403"""

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_delete(
            data_rest_views.DataDetailRegistry.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_returns_http_403(
        self,
    ):
        """test_superuser_returns_http_403"""

        mock_user = create_mock_user("1", is_superuser=True)

        response = RequestMock.do_request_delete(
            data_rest_views.DataDetailRegistry.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(data_api, "delete")
    @patch.object(data_api, "get_by_id")
    def test_superuser_and_staff_returns_http_204(
        self, mock_data_api_get_by_id, mock_data_api_delete
    ):
        """test_superuser_and_staff_returns_http_204"""

        mock_data_api_get_by_id.return_value = None
        mock_data_api_delete.return_value = None

        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_delete(
            data_rest_views.DataDetailRegistry.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(mock_data_api_delete.called)


class TestDataDetailPatchPermissions(SimpleTestCase):
    """Test Data Detail Patch Permissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_patch(
            data_rest_views.DataDetailRegistry.as_view(),
            None,
            data={"title": "edited"},
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(
        self,
    ):
        """test_authenticated_returns_http_403"""
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            data_rest_views.DataDetailRegistry.as_view(),
            mock_user,
            data={"title": "edited"},
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_returns_http_403(
        self,
    ):
        """test_staff_returns_http_403"""
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            data_rest_views.DataDetailRegistry.as_view(),
            mock_user,
            data={"title": "edited"},
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_returns_http_403(
        self,
    ):
        """test_superuser_returns_http_403"""
        mock_user = create_mock_user("1", is_superuser=True)

        response = RequestMock.do_request_patch(
            data_rest_views.DataDetailRegistry.as_view(),
            mock_user,
            data={"title": "edited"},
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(data_api, "get_by_id")
    @patch.object(data_api, "upsert")
    def test_superuser_and_staff_returns_http_200(
        self, mock_data_api_get_by_id, mock_data_api_upsert
    ):
        """test_superuser_and_staff_returns_http_200"""

        mock_data = MagicMock(title="title")
        mock_data_api_get_by_id.return_value = mock_data
        mock_data_api_upsert.return_value = mock_data

        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_patch(
            data_rest_views.DataDetailRegistry.as_view(),
            mock_user,
            data={"title": "edited"},
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(mock_data_api_upsert.called)
