""" Fixtures files for Data
"""
from os.path import join, dirname, realpath

from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface


class DataRegistryFixtures(FixtureInterface):
    """Data fixtures"""

    data_1 = None
    data_2 = None
    template = None
    data_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """
        mock_data_path = join(dirname(realpath(__file__)), "data")
        xml_path = join(mock_data_path, "data.xml")
        xml_without_status_path = join(mock_data_path, "data_without_status.xml")

        with open(xml_path, "r") as xml_file:
            xml_content_with_status = xml_file.read()
        with open(xml_without_status_path, "r") as xml_file:
            xml_content_without_status = xml_file.read()

        self.data_1 = _create_data(self.template, xml_content_with_status)
        self.data_2 = _create_data(self.template, xml_content_without_status)
        self.data_collection = [self.data_1, self.data_2]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xsl_path = join(mock_data_path, "res-md.xsd")
        with open(mock_xsl_path, "r") as xsd_file:
            xsd = xsd_file.read()

        template = Template()
        template.content = xsd
        template.hash = ""
        template.filename = "res-md.xsd"
        self.template = template.save()


def _create_data(template, xml):
    data = Data(template=template, user_id="1", dict_content=None, title="title")
    data.xml_content = xml
    data.convert_to_dict()
    return data.save()
