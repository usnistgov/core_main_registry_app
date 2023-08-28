""" Fixtures files for template version manager
"""
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)


class TemplateVersionManagerFixtures(FixtureInterface):
    """Template Version Manager fixtures"""

    template_1_1 = None
    template_1_2 = None
    template_1_3 = None
    template_2_1 = None
    template_vm_1 = None
    template_vm_2 = None
    template_vm_collection = None

    def insert_data(self):
        """Insert a set of Templates and Template Version Managers.

        Returns:

        """
        self.template_vm_1 = TemplateVersionManager(
            title="template 1",
            user=None,
            is_disabled=False,
        )
        self.template_vm_1.save()

        self.template_vm_2 = TemplateVersionManager(
            title="template 2",
            user="1",
            is_disabled=False,
        )
        self.template_vm_2.save()

        self.template_1_1 = Template(
            filename="template1_1.xsd",
            content="content1_1",
            _hash="hash1_1",
            version_manager=self.template_vm_1,
        )
        self.template_1_1.save()
        self.template_1_2 = Template(
            filename="template1_2.xsd",
            content="content1_2",
            _hash="hash1_2",
            version_manager=self.template_vm_1,
            is_disabled=True,
        )
        self.template_1_2.save()
        self.template_1_3 = Template(
            filename="template1_3.xsd",
            content="content1_3",
            _hash="hash1_3",
            version_manager=self.template_vm_1,
            is_current=True,
        )
        self.template_1_3.save()
        self.template_2_1 = Template(
            filename="template2_1.xsd",
            content="content2_1",
            _hash="hash2_1",
            version_manager=self.template_vm_2,
            is_current=True,
        )
        self.template_2_1.save()

        self.template_vm_collection = [self.template_vm_1, self.template_vm_2]
