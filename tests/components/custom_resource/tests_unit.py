""" Unit Test for Custom Resource API
"""
from unittest import mock

from core_main_app.commons import exceptions as exceptions
from django.conf import settings
from django.test import TestCase

from core_main_registry_app.components.custom_resource import api as custom_resource_api
from core_main_registry_app.components.custom_resource.models import CustomResource
from core_main_registry_app.constants import CUSTOM_RESOURCE_TYPE
from tests.components.custom_resource.fixtures.fixtures import CustomResourceFixtures

fixtureCustomResource = CustomResourceFixtures()


class TestCreateAllResourceCustomResource(TestCase):

    fixture = fixtureCustomResource

    def test_create_all_resource_custom_resource_return_type_all(self):
        # Act
        key = 'all_resource'
        custom_resource = custom_resource_api._create_custom_resource_type_all(
            self.fixture.create_custom_resource(), self.fixture.get_dict_custom_resource_all_resource()[key], key)
        # Assert
        self.assertEquals(custom_resource.type, CUSTOM_RESOURCE_TYPE.ALL)

    def test_create_all_resource_custom_resource_return_icon(self):
        # Act
        key = 'all_resource'
        custom_resource = custom_resource_api._create_custom_resource_type_all(
            self.fixture.create_custom_resource(), self.fixture.get_dict_custom_resource_all_resource()[key], key)
        # Assert
        self.assertEquals(custom_resource.icon, "fa-globe")

    def test_create_all_resource_custom_resource_return_icon_color(self):
        # Act
        key = 'all_resource'
        custom_resource = custom_resource_api._create_custom_resource_type_all(
            self.fixture.create_custom_resource(), self.fixture.get_dict_custom_resource_all_resource()[key], key)
        # Assert
        self.assertEquals(custom_resource.icon_color, "#557EB9")

    def test_create_all_resource_custom_resource_return_sort(self):
        # Act
        key = 'all_resource'
        custom_resource = custom_resource_api._create_custom_resource_type_all(
            self.fixture.create_custom_resource(), self.fixture.get_dict_custom_resource_all_resource()[key], key)
        # Assert
        self.assertEquals(custom_resource.sort, 0)


class TestCreateCustomResource(TestCase):

    fixture = fixtureCustomResource

    def test_create_custom_resource_return_type_resource(self):
        # Act
        key = 'Organization'
        custom_resource = custom_resource_api._create_custom_resource(
            self.fixture.create_custom_resource(), self.fixture.get_dict_custom_resource()[key], key)
        # Assert
        self.assertEquals(custom_resource.type, CUSTOM_RESOURCE_TYPE.RESOURCE)

    def test_create_custom_resource_return_name_in_schema(self):
        # Act
        key = 'Organization'
        custom_resource = custom_resource_api._create_custom_resource(
            self.fixture.create_custom_resource(), self.fixture.get_dict_custom_resource()[key], key)
        # Assert
        self.assertEquals(custom_resource.name_in_schema, key)

    def test_create_custom_resource_return_title(self):
        # Act
        key = 'Organization'
        custom_resource = custom_resource_api._create_custom_resource(
            self.fixture.create_custom_resource(), self.fixture.get_dict_custom_resource()[key], key)
        # Assert
        self.assertEquals(custom_resource.title, "Organization")


    def test_create_custom_resource_return_description(self):
        # Act
        key = 'Organization'
        custom_resource = custom_resource_api._create_custom_resource(
            self.fixture.create_custom_resource(), self.fixture.get_dict_custom_resource()[key], key)
        # Assert
        self.assertEquals(custom_resource.description, "a group of people that come together to contribute to or participate in a federated data operation. Organizations can be hierarchical: an organization can contain or sponsor other organizations. Organizations can also aggregate or participate with other organizations in broader collaborations.")

    def test_create_custom_resource_return_icon(self):
        # Act
        key = 'Organization'
        custom_resource = custom_resource_api._create_custom_resource(
            self.fixture.create_custom_resource(), self.fixture.get_dict_custom_resource()[key], key)
        # Assert
        self.assertEquals(custom_resource.icon, "fa-university")

    def test_create_custom_resource_return_icon_color(self):
        # Act
        key = 'Organization'
        custom_resource = custom_resource_api._create_custom_resource(
            self.fixture.create_custom_resource(), self.fixture.get_dict_custom_resource()[key], key)
        # Assert
        self.assertEquals(custom_resource.icon_color, "#2CAAE2")

    def test_create_custom_resource_return_display_icon(self):
        # Act
        key = 'Organization'
        custom_resource = custom_resource_api._create_custom_resource(
            self.fixture.create_custom_resource(), self.fixture.get_dict_custom_resource()[key], key)
        # Assert
        self.assertTrue(custom_resource.display_icon)

    def test_create_custom_resource_return_role_choice(self):
        # Act
        key = 'Organization'
        custom_resource = custom_resource_api._create_custom_resource(
            self.fixture.create_custom_resource(), self.fixture.get_dict_custom_resource()[key], key)
        # Assert
        self.assertEquals(custom_resource.role_choice, "Organization")

    def test_create_custom_resource_return_role_type(self):
        # Act
        key = 'Organization'
        custom_resource = custom_resource_api._create_custom_resource(
            self.fixture.create_custom_resource(), self.fixture.get_dict_custom_resource()[key], key)
        # Assert
        self.assertEquals(custom_resource.role_type, "Organization")

    def test_create_custom_resource_return_sort(self):
        # Act
        key = 'Organization'
        custom_resource = custom_resource_api._create_custom_resource(
            self.fixture.create_custom_resource(), self.fixture.get_dict_custom_resource()[key], key)
        # Assert
        self.assertEquals(custom_resource.sort, 1)


class TestIsCustomResourceTypeResource(TestCase):

    fixture = fixtureCustomResource

    def test_is_all_resource_return_type_resource(self):
        # Act
        custom_resource = CustomResource(type=CUSTOM_RESOURCE_TYPE.RESOURCE)
        # Assert
        self.assertTrue(custom_resource_api._is_custom_resource_type_resource(custom_resource))

    def test_is_all_resource_return_type_all(self):
        # Act
        custom_resource = CustomResource(type=CUSTOM_RESOURCE_TYPE.ALL)
        # Assert
        self.assertFalse(custom_resource_api._is_custom_resource_type_resource(custom_resource))


class TestIsTypeAll(TestCase):

    fixture = fixtureCustomResource

    def test_is_all_resource_return_is_resource_custom_resource(self):
        # Act
        key = 'Organization'
        resource = self.fixture.get_dict_custom_resource()[key]
        # Assert
        self.assertFalse(custom_resource_api._is_type_all(resource))

    def test_is_all_resource_return_is_resource_all_resource(self):
        # Act
        key = 'all_resource'
        resource = self.fixture.get_dict_custom_resource_all_resource()[key]
        # Assert
        self.assertTrue(custom_resource_api._is_type_all(resource))


class TestCheckCurate(TestCase):

    fixture = fixtureCustomResource

    def test_check_curate_core_curate_app_not_installed_return_none(self):
        # Act
        custom_resource = CustomResource()
        # Assert
        self.assertIsNone(custom_resource_api._check_curate(custom_resource))

    def test_check_curate_is_not_resource_return_none(self):
        # Act
        custom_resource = CustomResource()
        # Assert
        with mock.patch.object(settings, 'INSTALLED_APPS', ['core_curate_app']):
            self.assertIsNone(custom_resource_api._check_curate(custom_resource))

    def test_check_curate_is_resource_return_except(self):
        # Act
        custom_resource = CustomResource(type=CUSTOM_RESOURCE_TYPE.RESOURCE)
        # Assert
        with mock.patch.object(settings, 'INSTALLED_APPS', ['core_curate_app']):
            with self.assertRaises(exceptions.ModelError):
                custom_resource_api._check_curate(custom_resource)

    def test_check_curate_is_resource_with_role_type_return_except(self):
        # Act
        custom_resource = CustomResource(type=CUSTOM_RESOURCE_TYPE.RESOURCE, role_type="role_type")
        # Assert
        with mock.patch.object(settings, 'INSTALLED_APPS', ['core_curate_app']):
            with self.assertRaises(exceptions.ModelError):
                custom_resource_api._check_curate(custom_resource)

    def test_check_curate_is_resource_with_role_choice_return_except(self):
        # Act
        custom_resource = CustomResource(type=CUSTOM_RESOURCE_TYPE.RESOURCE, role_choice="role_choice")
        # Assert
        with mock.patch.object(settings, 'INSTALLED_APPS', ['core_curate_app']):
            with self.assertRaises(exceptions.ModelError):
                custom_resource_api._check_curate(custom_resource)

    def test_check_curate_is_resource_with_all_return_none(self):
        # Act
        custom_resource = CustomResource(type=CUSTOM_RESOURCE_TYPE.RESOURCE, role_type="role_type", role_choice="role_choice")
        # Assert
        with mock.patch.object(settings, 'INSTALLED_APPS', ['core_curate_app']):
            self.assertIsNone(custom_resource_api._check_curate(custom_resource))
