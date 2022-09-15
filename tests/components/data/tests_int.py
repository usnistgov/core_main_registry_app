""" Unit Test Data
"""
from mock import patch


from core_main_app.commons import exceptions as exceptions
from core_main_app.components.data.models import Data
import core_main_app.components.workspace.api as workspace_api
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request

import core_main_registry_app.components.data.api as data_registry_api
from core_main_registry_app.commons.constants import DataStatus
from tests.components.data.fixtures.fixtures import DataRegistryFixtures


fixture_data = DataRegistryFixtures()


class TestDataGetStatus(MongoIntegrationBaseTestCase):
    """Test Data Get Status"""

    fixture = fixture_data

    def test_data_get_status_return_status_from_xml_content(self):
        """test_data_get_status_return_status_from_xml_content"""

        # Act
        status = data_registry_api.get_status(self.fixture.data_1)
        # Assert
        self.assertTrue(status == DataStatus.ACTIVE)

    def test_data_get_status_raise_model_exception_if_status_key_does_not_exist(self):
        """test_data_get_status_raise_model_exception_if_status_key_does_not_exist"""

        # Act, Assert
        with self.assertRaises(exceptions.ModelError):
            data_registry_api.get_status(self.fixture.data_2)


class TestDataSetStatus(MongoIntegrationBaseTestCase):
    """Test Data Set Status"""

    fixture = fixture_data

    @patch.object(Data, "convert_to_file")
    def test_data_set_status_to_inactive_should_always_work(self, mock_convert_to_file):
        """test_data_set_status_to_inactive_should_always_work"""

        # Arrange
        user = create_mock_user("1", True, True)
        mock_request = create_mock_request(user=user)
        status = data_registry_api.get_status(self.fixture.data_1)
        self.assertTrue(status == DataStatus.ACTIVE)
        # Act
        data = data_registry_api.set_status(
            self.fixture.data_1, DataStatus.INACTIVE, mock_request
        )
        status = data_registry_api.get_status(data)
        # Assert
        self.assertTrue(status == DataStatus.INACTIVE)

    @patch.object(Data, "convert_to_file")
    def test_data_set_status_to_deleted_raise_exception_if_data_is_not_published(
        self, mock_convert_to_file
    ):
        """test_data_set_status_to_deleted_raise_exception_if_data_is_not_published"""

        # Arrange
        user = create_mock_user("1", True, True)
        mock_request = create_mock_request(user=user)
        status = data_registry_api.get_status(self.fixture.data_1)
        self.assertTrue(status == DataStatus.ACTIVE)
        # Act Assert
        with self.assertRaises(exceptions.ModelError):
            data_registry_api.set_status(
                self.fixture.data_1, DataStatus.DELETED, mock_request
            )


class TestDataPublish(MongoIntegrationBaseTestCase):
    """Test Data Publish"""

    fixture = fixture_data

    @patch.object(workspace_api, "get_global_workspace")
    def test_publish_data_without_workspace_publishes_data(self, get_global_workspace):
        """test_publish_data_without_workspace_publishes_data"""

        # Arrange
        user = create_mock_user("1", is_superuser=True, has_perm=True)
        get_global_workspace.return_value = self.fixture.workspace_1

        # Act
        data_registry_api.publish(self.fixture.data_1, user)

        # Assert
        self.assertEqual(
            self.fixture.data_1.workspace, get_global_workspace.return_value
        )

    @patch.object(workspace_api, "get_global_workspace")
    def test_publish_data_in_private_workspace_publishes_data(
        self, get_global_workspace
    ):
        """test_publish_data_in_private_workspace_publishes_data"""

        # Arrange
        user = create_mock_user("1", is_superuser=True, has_perm=True)
        get_global_workspace.return_value = self.fixture.workspace_1

        # Act
        data_registry_api.publish(self.fixture.data_2, user)

        # Assert
        self.assertEqual(
            self.fixture.data_2.workspace, get_global_workspace.return_value
        )

    @patch.object(workspace_api, "get_global_workspace")
    def test_publish_data_in_public_raises_error(self, get_global_workspace):
        """test_publish_data_in_public_raises_error"""

        # Arrange
        user = create_mock_user("1", is_superuser=True, has_perm=True)
        get_global_workspace.return_value = self.fixture.workspace_1
        self.fixture.data_2.workspace = self.fixture.workspace_1

        # Act Assert
        with self.assertRaises(exceptions.ApiError):
            data_registry_api.publish(self.fixture.data_2, user)
