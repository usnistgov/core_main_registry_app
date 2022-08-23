""" Fixtures files for Data
"""
from os.path import join, dirname, realpath

from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface
from core_main_app.components.workspace.models import Workspace


class DataRegistryFixtures(FixtureInterface):
    """Data fixtures"""

    data_1 = None
    data_2 = None
    workspace_1 = None
    workspace_2 = None
    template = None
    data_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_workspace()
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """
        mock_data_path = join(dirname(realpath(__file__)), "data")
        xml_path = join(mock_data_path, "data.xml")
        xml_without_status_path = join(mock_data_path, "data_without_status.xml")

        with open(xml_path, "r", encoding="utf-8") as xml_file:
            xml_content_with_status = xml_file.read()
        with open(xml_without_status_path, "r", encoding="utf-8") as xml_file:
            xml_content_without_status = xml_file.read()

        self.data_1 = _create_data(self.template, xml_content_with_status)
        self.data_2 = _create_data(
            self.template, xml_content_without_status, self.workspace_2
        )
        self.data_collection = [self.data_1, self.data_2]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xsl_path = join(mock_data_path, "res-md.xsd")
        with open(mock_xsl_path, "r", encoding="utf-8") as xsd_file:
            xsd = xsd_file.read()

        self.template = Template()
        self.template.content = xsd
        self.template.hash = ""
        self.template.filename = "res-md.xsd"
        self.template.save()

    def generate_workspace(self):
        """Generate the workspaces.

        Returns:

        """
        self.workspace_1 = Workspace(
            title="Workspace 1",
            owner=None,
            read_perm_id="1",
            write_perm_id="1",
            is_public=True,
        )
        self.workspace_1.save()

        self.workspace_2 = Workspace(
            title="Workspace 2",
            owner="1",
            read_perm_id="1",
            write_perm_id="1",
            is_public=False,
        )
        self.workspace_2.save()


def _create_data(template, xml, workspace=None):
    data = Data(
        template=template,
        user_id="1",
        dict_content=None,
        title="title",
        workspace=workspace,
    )
    data.xml_content = xml
    data.convert_to_dict()
    data.save()
    return data
