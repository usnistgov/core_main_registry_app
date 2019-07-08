""" Fixtures files for Custom Resource
"""
import json
from os.path import join, dirname, realpath

from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface
from core_main_registry_app.components.custom_resource.models import CustomResource
from core_main_app.components.template.models import Template


class CustomResourceFixtures(FixtureInterface):
    """ Custom Resource Fixture
    """
    def insert_data(self):
        pass

    @staticmethod
    def create_and_save_template():
        template = Template(filename="Schema",
                            content="<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>",
                            hash="")
        template.save()
        return template

    @staticmethod
    def create_custom_resource():
        return CustomResource()

    @staticmethod
    def get_dict_custom_resource_minus_sort():
        mock_json_path = join(dirname(realpath(__file__)), "json")
        json_path = join(mock_json_path, "custom_resource_minus_sort.json")
        with open(json_path, "r") as json_file:
            return json.load(json_file)

    @staticmethod
    def get_dict_custom_resource_no_sort():
        mock_json_path = join(dirname(realpath(__file__)), "json")
        json_path = join(mock_json_path, "custom_resource_no_sort.json")
        with open(json_path, "r") as json_file:
            return json.load(json_file)

    @staticmethod
    def get_dict_custom_resource_no_title():
        mock_json_path = join(dirname(realpath(__file__)), "json")
        json_path = join(mock_json_path, "custom_resource_no_title.json")
        with open(json_path, "r") as json_file:
            return json.load(json_file)

    @staticmethod
    def get_dict_custom_resource_no_type():
        mock_json_path = join(dirname(realpath(__file__)), "json")
        json_path = join(mock_json_path, "custom_resource_no_type.json")
        with open(json_path, "r") as json_file:
            return json.load(json_file)

    @staticmethod
    def get_dict_all_custom_resource():
        mock_json_path = join(dirname(realpath(__file__)), "json")
        json_path = join(mock_json_path, "all_custom_resource.json")
        with open(json_path, "r") as json_file:
            return json.load(json_file)

    @staticmethod
    def get_dict_custom_resource_all_resource():
        mock_json_path = join(dirname(realpath(__file__)), "json")
        json_path = join(mock_json_path, "all_resource.json")
        with open(json_path, "r") as json_file:
            return json.load(json_file)

    @staticmethod
    def get_dict_custom_resource():
        mock_json_path = join(dirname(realpath(__file__)), "json")
        json_path = join(mock_json_path, "custom_resource.json")
        with open(json_path, "r") as json_file:
            return json.load(json_file)
