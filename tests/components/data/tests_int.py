""" Unit Test Data
"""
from mock import patch

import core_main_registry_app.components.data.api as data_registry_api
from core_main_app.commons import exceptions as exceptions
from core_main_app.components.data.models import Data
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from core_main_registry_app.commons.constants import DataStatus
from tests.components.data.fixtures.fixtures import DataRegistryFixtures

fixture_data = DataRegistryFixtures()


class TestDataGetStatus(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_data_get_status_return_status_from_xml_content(self):
        # Act
        status = data_registry_api.get_status(self.fixture.data_1)
        # Assert
        self.assertTrue(status == DataStatus.ACTIVE)

    def test_data_get_status_raise_model_exception_if_status_key_does_not_exist(self):
        # Act, Assert
        with self.assertRaises(exceptions.ModelError):
            data_registry_api.get_status(self.fixture.data_2)


class TestDataSetStatus(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    @patch.object(Data, "convert_to_file")
    def test_data_set_status_to_inactive_should_always_work(self, mock_convert_to_file):
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
