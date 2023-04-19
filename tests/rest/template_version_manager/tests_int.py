""" Integration Test for registry Template Version Manager Rest API
"""

from rest_framework import status

from core_main_app.rest.template_version_manager import views
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from tests.components.template_version_manager.fixtures.fixtures import (
    TemplateVersionManagerFixtures,
)

fixture_template = TemplateVersionManagerFixtures()


class TestCurrentTemplateVersion(IntegrationBaseTestCase):
    """Test Current Template Version"""

    fixture = fixture_template

    def test_patch_returns_http_200(self):
        """test_patch_returns_http_200"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.CurrentTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_1_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_wrong_id_returns_http_404(self):
        """test_patch_wrong_id_returns_http_404"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.CurrentTemplateVersion.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_disabled_returns_http_400(self):
        """test_patch_disabled_returns_http_400"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.CurrentTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_1_2.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_global_as_user_returns_http_403(self):
        """test_patch_global_as_user_returns_http_403"""

        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_patch(
            views.CurrentTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_1_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_other_user_returns_http_403(self):
        """test_patch_other_user_returns_http_403"""

        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_patch(
            views.CurrentTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_2_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
