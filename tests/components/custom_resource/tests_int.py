""" Integration Test for Custom Resource API
"""
from django.utils.text import slugify
from mock import patch
from mongoengine.errors import ValidationError

from core_main_app.commons import exceptions as exceptions
from core_main_app.utils.integration_tests.integration_base_test_case import MongoIntegrationBaseTestCase
from core_main_registry_app.components.custom_resource import api as custom_resource_api
from core_main_registry_app.components.custom_resource.models import CustomResource
from core_main_registry_app.constants import CUSTOM_RESOURCE_TYPE
from tests.components.custom_resource.fixtures.fixtures import CustomResourceFixtures

fixtureCustomResource = CustomResourceFixtures()


class TestCreateAndSaveCustomResource(MongoIntegrationBaseTestCase):

    fixture = fixtureCustomResource

    def test_create_all_custom_resource_return_collection_of_custom_resource(self):
        # Act
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(self.fixture.get_dict_all_custom_resource(), template)
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertTrue(all(isinstance(item, CustomResource) for item in result))

    def test_create_custom_resource_return_slug_is_not_none(self):
        # Act
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(self.fixture.get_dict_custom_resource(), template)
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertIsNotNone(result[0].slug)

    def test_create_custom_resource_return_slug(self):
        # Act
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(self.fixture.get_dict_custom_resource(), template)
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertEquals(result[0].slug, slugify(result[0].title))

    def test_create_custom_resource_return_type(self):
        # Act
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(self.fixture.get_dict_custom_resource(), template)
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertEquals(result[0].type, CUSTOM_RESOURCE_TYPE.RESOURCE)

    def test_create_all_resource_custom_resource_return_type_is_not_none(self):
        # Act
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(self.fixture.get_dict_all_custom_resource(), template)
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertIsNotNone(all(item.type for item in result))

    def test_create_custom_resource_minus_sort_return_except(self):
        # Act
        template = self.fixture.create_and_save_template()
        # Assert
        with self.assertRaises(exceptions.ModelError):
            custom_resource_api.parse_and_save(self.fixture.get_dict_custom_resource_minus_sort(), template)

    def test_create_custom_resource_no_title_return_except(self):
        # Act
        template = self.fixture.create_and_save_template()
        # Assert
        with self.assertRaises(exceptions.ModelError):
            custom_resource_api.parse_and_save(self.fixture.get_dict_custom_resource_no_title(), template)

    def test_create_custom_resource_no_sort_return_except(self):
        # Act
        template = self.fixture.create_and_save_template()
        # Assert
        with self.assertRaises(exceptions.ModelError):
            custom_resource_api.parse_and_save(self.fixture.get_dict_custom_resource_no_sort(), template)

    def test_create_custom_resource_wrong_type_return_except(self):
        # Act
        template = self.fixture.create_and_save_template()
        # Assert
        with self.assertRaises(ValidationError):
            custom_resource = CustomResource(template=template, title="title", type="wrong", icon="icon", sort=0)
            custom_resource.save()


class TestGetAllByTemplate(MongoIntegrationBaseTestCase):

    fixture = fixtureCustomResource

    def test_get_all_by_template_return_all(self):
        # Act
        length = len(self.fixture.get_dict_all_custom_resource())
        template = self.fixture.create_and_save_template()
        custom_resource_api.parse_and_save(self.fixture.get_dict_all_custom_resource(), template)
        result = custom_resource_api.get_all_by_template(template)
        # Assert
        self.assertEquals(length, len(result))


class TestGetByCurrentTemplateAndSlug(MongoIntegrationBaseTestCase):

    fixture = fixtureCustomResource

    @patch('core_main_registry_app.components.custom_resource.api._get_current_template')
    def test_get_by_current_template_and_slug_returns_custom_resource(self, _get_current_template):
        # Arrange
        _get_current_template.return_value = self.fixture.template
        # Act
        custom_resource = custom_resource_api.get_by_current_template_and_slug(self.fixture.custom_resource.slug)
        # Assert
        self.assertTrue(isinstance(custom_resource, CustomResource))

    @patch('core_main_registry_app.components.custom_resource.api._get_current_template')
    def test_get_by_current_template_and__incorrect_slug_raises_error(self, _get_current_template):
        # Arrange
        _get_current_template.return_value = self.fixture.template
        # Act
        with self.assertRaises(exceptions.DoesNotExist):
            custom_resource_api.get_by_current_template_and_slug("incorrect slug")
