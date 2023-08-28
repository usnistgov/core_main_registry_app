""" Fixtures files for Custom Resource
"""
import json
from os.path import join, dirname, realpath

from core_main_app.components.template.models import Template
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)
from core_main_registry_app.components.custom_resource.models import (
    CustomResource,
)
from core_main_registry_app.constants import CUSTOM_RESOURCE_TYPE


class CustomResourceFixtures(FixtureInterface):
    """Custom Resource Fixture"""

    custom_resource = None
    template = None
    custom_resource_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        self.template = CustomResourceFixtures.create_and_save_template()
        self.custom_resource = CustomResourceFixtures.create_custom_resource(
            template=self.template, slug="test"
        )
        self.custom_resource_collection = [self.custom_resource]

    @staticmethod
    def create_and_save_template():
        """create_and_save_template

        Returns:

        """
        template = Template(
            filename="Schema",
            content="<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>",
            _hash="",
        )
        template.save()
        return template

    @staticmethod
    def create_custom_resource(
        template=None,
        name_in_schema="",
        title="title",
        description="",
        slug="",
        type=CUSTOM_RESOURCE_TYPE.RESOURCE.value,
        icon="fa-database",
        icon_color="",
        display_icon=False,
        role_choice="",
        role_type="",
        sort=0,
    ):
        """create_custom_resource

        Args:
            template
            name_in_schema
            title
            description=
            slug
            type
            icon=
            icon_color
            display_icon
            role_choice
            role_type=
            sort
        Returns:

        """
        if template is None:
            template = CustomResourceFixtures.create_and_save_template()

        custom_resource = CustomResource(
            template=template,
            name_in_schema=name_in_schema,
            title=title,
            description=description,
            slug=slug,
            type=type,
            icon=icon,
            icon_color=icon_color,
            display_icon=display_icon,
            role_choice=role_choice,
            role_type=role_type,
            sort=sort,
        )
        custom_resource.save()
        return custom_resource

    @staticmethod
    def get_dict_custom_resource_minus_sort():
        """get_dict_custom_resource_minus_sort

        Returns:

        """
        mock_json_path = join(dirname(realpath(__file__)), "json")
        json_path = join(mock_json_path, "custom_resource_minus_sort.json")
        with open(json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    @staticmethod
    def get_dict_custom_resource_no_sort():
        """get_dict_custom_resource_no_sort

        Returns:

        """
        mock_json_path = join(dirname(realpath(__file__)), "json")
        json_path = join(mock_json_path, "custom_resource_no_sort.json")
        with open(json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    @staticmethod
    def get_dict_custom_resource_no_title():
        """get_dict_custom_resource_no_title

        Returns:

        """
        mock_json_path = join(dirname(realpath(__file__)), "json")
        json_path = join(mock_json_path, "custom_resource_no_title.json")
        with open(json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    @staticmethod
    def get_dict_custom_resource_no_type():
        """get_dict_custom_resource_no_type

        Returns:

        """
        mock_json_path = join(dirname(realpath(__file__)), "json")
        json_path = join(mock_json_path, "custom_resource_no_type.json")
        with open(json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    @staticmethod
    def get_dict_all_custom_resource():
        """get_dict_all_custom_resource

        Returns:

        """
        mock_json_path = join(dirname(realpath(__file__)), "json")
        json_path = join(mock_json_path, "all_custom_resource.json")
        with open(json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    @staticmethod
    def get_dict_custom_resource_all_resource():
        """get_dict_custom_resource_all_resource

        Returns:

        """
        mock_json_path = join(dirname(realpath(__file__)), "json")
        json_path = join(mock_json_path, "all_resource.json")
        with open(json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    @staticmethod
    def get_dict_custom_resource():
        """get_dict_custom_resource

        Returns:

        """
        mock_json_path = join(dirname(realpath(__file__)), "json")
        json_path = join(mock_json_path, "custom_resource.json")
        with open(json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
