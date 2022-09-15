""" Integration Test for Custom Resource API
"""
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from mock import patch

from core_main_app.commons import exceptions as exceptions
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from core_main_registry_app.components.custom_resource import api as custom_resource_api
from core_main_registry_app.components.custom_resource.models import CustomResource
from core_main_registry_app.constants import CUSTOM_RESOURCE_TYPE
from tests.components.custom_resource.fixtures.fixtures import CustomResourceFixtures

fixtureCustomResource = CustomResourceFixtures()


class TestCreateAndSaveCustomResource(MongoIntegrationBaseTestCase):
    """
    Test Create And Save Custom Resource
    """

    fixture = fixtureCustomResource

    def test_create_all_custom_resource_return_collection_of_custom_resource(self):
        """test_create_all_custom_resource_return_collection_of_custom_resource

        Returns:
        """

        # Act
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(
            self.fixture.get_dict_all_custom_resource(), template
        )
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertTrue(all(isinstance(item, CustomResource) for item in result))

    def test_create_custom_resource_return_slug_is_not_none(self):
        """test_create_custom_resource_return_slug_is_not_none

        Returns:
        """

        # Act
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(
            self.fixture.get_dict_custom_resource(), template
        )
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertIsNotNone(result[0].slug)

    def test_create_custom_resource_type_all_return_refinements_is_empty(self):
        """test_create_custom_resource_type_all_return_refinements_is_empty

        Returns:
        """
        # Act
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(
            self.fixture.get_dict_custom_resource_all_resource(), template
        )
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertEqual(len(result[0].refinements), 0)

    def test_create_custom_resource_return_refinements_is_not_none(self):
        """test_create_custom_resource_return_refinements_is_not_none

        Returns:
        """
        # Act
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(
            self.fixture.get_dict_custom_resource(), template
        )
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertIsNotNone(result[0].refinements)

    def test_create_custom_resource_return_refinements_length(self):
        """test_create_custom_resource_return_refinements_length

        Returns:
        """
        # Act
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(
            self.fixture.get_dict_custom_resource(), template
        )
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertEqual(len(result[0].refinements), 1)

    def test_create_custom_resource_return_refinements_value(self):
        """test_create_custom_resource_return_refinements_value

        Returns:
        """
        # Act
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(
            self.fixture.get_dict_custom_resource(), template
        )
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertEqual(result[0].refinements[0], "unspecified Organization")

    def test_create_custom_resource_return_slug(self):
        """test_create_custom_resource_return_slug

        Returns:
        """
        # Act
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(
            self.fixture.get_dict_custom_resource(), template
        )
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertEqual(result[0].slug, slugify(result[0].title))

    def test_create_custom_resource_return_type(self):
        """test_create_custom_resource_return_type

        Returns:
        """
        # Act
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(
            self.fixture.get_dict_custom_resource(), template
        )
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertEqual(result[0].type, CUSTOM_RESOURCE_TYPE.RESOURCE.value)

    def test_create_all_resource_custom_resource_return_type_is_not_none(self):
        """test_create_all_resource_custom_resource_return_type_is_not_none

        Returns:
        """
        # Act
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(
            self.fixture.get_dict_all_custom_resource(), template
        )
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertIsNotNone(all(item.type for item in result))

    def test_create_custom_resource_minus_sort_return_except(self):
        """test_create_custom_resource_minus_sort_return_except

        Returns:
        """
        # Act
        template = self.fixture.create_and_save_template()
        # Assert
        with self.assertRaises(exceptions.ModelError):
            custom_resource_api.parse_and_save(
                self.fixture.get_dict_custom_resource_minus_sort(), template
            )

    def test_create_custom_resource_no_title_return_except(self):
        """test_create_custom_resource_no_title_return_except

        Returns:
        """
        # Act
        template = self.fixture.create_and_save_template()
        # Assert
        with self.assertRaises(exceptions.ModelError):
            custom_resource_api.parse_and_save(
                self.fixture.get_dict_custom_resource_no_title(), template
            )

    def test_create_custom_resource_no_sort_return_except(self):
        """test_create_custom_resource_no_sort_return_except

        Returns:
        """
        # Act
        template = self.fixture.create_and_save_template()
        # Assert
        with self.assertRaises(exceptions.ModelError):
            custom_resource_api.parse_and_save(
                self.fixture.get_dict_custom_resource_no_sort(), template
            )

    def test_create_custom_resource_wrong_type_return_except(self):
        """test_create_custom_resource_wrong_type_return_except

        Returns:
        """
        # Act
        template = self.fixture.create_and_save_template()
        # Assert
        with self.assertRaises(ValidationError):
            custom_resource = CustomResource(
                template=template, title="title", type="wrong", icon="icon", sort=0
            )
            custom_resource.save()


class TestGetAllByTemplate(MongoIntegrationBaseTestCase):
    """
    Test Get All By Template
    """

    fixture = fixtureCustomResource

    def test_get_all_by_template_return_all(self):
        """test_get_all_by_template_return_all

        Returns:
        """

        # Act
        length = len(self.fixture.get_dict_all_custom_resource())
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(
            self.fixture.get_dict_all_custom_resource(), template
        )
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertEqual(length, len(result))


class TestGetByRoleForCurrentTemplate(MongoIntegrationBaseTestCase):
    """
    Test Get By Role For Current Template
    """

    fixture = fixtureCustomResource

    @patch(
        "core_main_registry_app.components.custom_resource.api._get_current_template"
    )
    def test_get_by_role_for_current_template_returns_custom_resource(
        self, _get_current_template
    ):
        """test_get_by_role_for_current_template_returns_custom_resource

        Returns:
        """

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        _get_current_template.return_value = self.fixture.template
        # Act
        custom_resource = custom_resource_api.get_by_role_for_current_template(
            self.fixture.custom_resource.role_choice, request=mock_request
        )
        # Assert
        self.assertTrue(isinstance(custom_resource, CustomResource))


class TestGetByCurrentTemplateAndSlug(MongoIntegrationBaseTestCase):
    """
    Test Get By Current Template And Slug
    """

    fixture = fixtureCustomResource

    @patch(
        "core_main_registry_app.components.custom_resource.api._get_current_template"
    )
    def test_get_by_current_template_and_slug_returns_custom_resource(
        self, _get_current_template
    ):
        """test_get_by_current_template_and_slug_returns_custom_resource

        Returns:
        """

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        _get_current_template.return_value = self.fixture.template
        # Act
        custom_resource = custom_resource_api.get_by_current_template_and_slug(
            self.fixture.custom_resource.slug, request=mock_request
        )
        # Assert
        self.assertTrue(isinstance(custom_resource, CustomResource))

    @patch(
        "core_main_registry_app.components.custom_resource.api._get_current_template"
    )
    def test_get_by_current_template_and__incorrect_slug_raises_error(
        self, _get_current_template
    ):
        """test_get_by_current_template_and__incorrect_slug_raises_error

        Returns:
        """

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        _get_current_template.return_value = self.fixture.template
        # Act
        with self.assertRaises(exceptions.DoesNotExist):
            custom_resource_api.get_by_current_template_and_slug(
                "incorrect slug", mock_request
            )


class TestDeleteCustomResourcesByTemplate(MongoIntegrationBaseTestCase):
    """
    Test Delete Custom Resources By Template
    """

    fixture = fixtureCustomResource

    def test_delete_custom_resources_by_template_return_0(self):
        """test_delete_custom_resources_by_template_return_0

        Returns:
        """

        # Act
        self.fixture.insert_data()
        custom_resource_api.delete_custom_resources_by_template(self.fixture.template)
        result = custom_resource_api.get_all_by_template(self.fixture.template)
        # Assert
        self.assertEqual(0, len(result))


class TestSaveList(MongoIntegrationBaseTestCase):
    """
    Test Save List
    """

    fixture = fixtureCustomResource

    def test_save_list(self):
        """test_save_list

        Returns:
        """

        # Act
        template = self.fixture.create_and_save_template()
        custom_resource1 = CustomResource(
            template=template, title="title1", type="resource", icon="icon", sort=0
        )
        custom_resource2 = CustomResource(
            template=template, title="title2", type="resource", icon="icon", sort=1
        )
        list_custom = [custom_resource1, custom_resource2]
        custom_resource_api.save_list(list_custom)
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertEqual(len(list_custom), len(result))


class TestReplaceCustomResourceByTemplate(MongoIntegrationBaseTestCase):
    """
    Test Replace Custom Resource By Template
    """

    fixture = fixtureCustomResource

    def test_replace_custom_resources_by_template_return_ok(self):
        """test_replace_custom_resources_by_template_return_ok"""

        # Check
        template = self.fixture.create_and_save_template()
        result = custom_resource_api.get_all_by_template(template)
        self.assertEqual(0, len(result))
        # Act
        custom_resource_api.replace_custom_resources_by_template(
            template, self.fixture.get_dict_all_custom_resource()
        )
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertEqual(10, len(result))

    def test_replace_custom_resources_by_template_check_old(self):
        """test_replace_custom_resources_by_template_check_old

        Returns:
        """

        # Check
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(
            self.fixture.get_dict_custom_resource_all_resource(), template
        )
        result = custom_resource_api.get_all_by_template(template)
        old_cr = list(result)[0]
        self.assertEqual(1, len(result))
        # Act
        custom_resource_api.replace_custom_resources_by_template(
            template, self.fixture.get_dict_all_custom_resource()
        )
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertFalse(old_cr in result)

    def test_replace_custom_resources_by_template_return_raise(self):
        """test_replace_custom_resources_by_template_return_raise

        Returns:
        """

        # Act
        template = self.fixture.create_and_save_template()
        # Assert
        with self.assertRaises(exceptions.ModelError):
            custom_resource_api.replace_custom_resources_by_template(
                template, self.fixture.get_dict_custom_resource_no_title()
            )
