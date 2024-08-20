""" Unit Test for Migrations
"""

from unittest.mock import patch

from django.db.migrations.exceptions import BadMigrationError
from django.test import TestCase

from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_registry_app import discover
from core_main_registry_app.components.custom_resource.models import (
    CustomResource,
)
from core_main_registry_app.components.refinement.models import Refinement


class TestInitData(TestCase):
    """TestInitData"""

    @patch.object(Refinement, "objects")
    @patch.object(CustomResource, "objects")
    @patch.object(TemplateVersionManager, "objects")
    @patch("core_main_registry_app.discover.main_registry_settings")
    def test_func_raises_error_if_REGISTRY_XSD_FILENAME_not_set(
        self,
        mock_settings,
        mock_tvm_objects,
        mock_cr_objects,
        mock_refinement_objects,
    ):
        """test_func_raises_error_if_REGISTRY_XSD_FILENAME_not_set"""
        mock_tvm_objects.count.return_value = 0
        mock_cr_objects.count.return_value = 0
        mock_refinement_objects.count.return_value = 0
        mock_settings.REGISTRY_XSD_FILENAME = None

        with self.assertRaises(BadMigrationError):
            discover.init_registry()

    @patch.object(Refinement, "objects")
    @patch.object(CustomResource, "objects")
    @patch.object(TemplateVersionManager, "objects")
    @patch("core_main_registry_app.discover.main_registry_settings")
    def test_func_raises_error_if_REGISTRY_XSD_FILEPATH_not_set(
        self,
        mock_settings,
        mock_tvm_objects,
        mock_cr_objects,
        mock_refinement_objects,
    ):
        """test_func_raises_error_if_REGISTRY_XSD_FILEPATH_not_set"""
        mock_tvm_objects.count.return_value = 0
        mock_cr_objects.count.return_value = 0
        mock_refinement_objects.count.return_value = 0
        mock_settings.REGISTRY_XSD_FILEPATH = None

        with self.assertRaises(BadMigrationError):
            discover.init_registry()

    @patch.object(Refinement, "objects")
    @patch.object(CustomResource, "objects")
    @patch.object(TemplateVersionManager, "objects")
    @patch("core_main_registry_app.discover.main_registry_settings")
    def test_func_raises_error_if_CUSTOM_REGISTRY_FILE_PATH_not_set(
        self,
        mock_settings,
        mock_tvm_objects,
        mock_cr_objects,
        mock_refinement_objects,
    ):
        """test_func_raises_error_if_CUSTOM_REGISTRY_FILE_PATH_not_set"""
        mock_tvm_objects.count.return_value = 0
        mock_cr_objects.count.return_value = 0
        mock_refinement_objects.count.return_value = 0
        mock_settings.CUSTOM_REGISTRY_FILE_PATH = None

        with self.assertRaises(BadMigrationError):
            discover.init_registry()

    @patch.object(Refinement, "objects")
    @patch.object(CustomResource, "objects")
    @patch.object(TemplateVersionManager, "objects")
    def test_func_raises_error_if_refinements_not_empty(
        self,
        mock_tvm_objects,
        mock_cr_objects,
        mock_refinement_objects,
    ):
        """test_func_raises_error_if_refinements_not_empty"""
        mock_tvm_objects.count.return_value = 0
        mock_cr_objects.count.return_value = 0
        mock_refinement_objects.count.return_value = 1

        self.assertIsNone(discover.init_registry())

    @patch.object(Refinement, "objects")
    @patch.object(CustomResource, "objects")
    @patch.object(TemplateVersionManager, "objects")
    def test_func_raises_error_if_custom_resources_not_empty(
        self,
        mock_tvm_objects,
        mock_cr_objects,
        mock_refinement_objects,
    ):
        """test_func_raises_error_if_custom_resources_not_empty"""
        mock_tvm_objects.count.return_value = 0
        mock_cr_objects.count.return_value = 1
        mock_refinement_objects.count.return_value = 0

        self.assertIsNone(discover.init_registry())

    @patch.object(Refinement, "objects")
    @patch.object(CustomResource, "objects")
    @patch.object(TemplateVersionManager, "objects")
    def test_func_raises_error_if_tvm_not_empty(
        self,
        mock_tvm_objects,
        mock_cr_objects,
        mock_refinement_objects,
    ):
        """test_func_raises_error_if_tvm_not_empty"""
        mock_tvm_objects.count.return_value = 1
        mock_cr_objects.count.return_value = 0
        mock_refinement_objects.count.return_value = 0

        self.assertIsNone(discover.init_registry())

    @patch.object(Refinement, "objects")
    @patch.object(CustomResource, "objects")
    @patch.object(TemplateVersionManager, "objects")
    @patch("core_main_registry_app.discover.main_registry_settings")
    def test_func_raises_error_if_loaded_does_not_exist(
        self,
        mock_settings,
        mock_tvm_objects,
        mock_cr_objects,
        mock_refinement_objects,
    ):
        """test_func_raises_error_if_loaded_does_not_exist"""
        mock_tvm_objects.count.return_value = 0
        mock_cr_objects.count.return_value = 0
        mock_refinement_objects.count.return_value = 0
        mock_settings.CUSTOM_REGISTRY_FILE_PATH = "bad"

        with self.assertRaises(BadMigrationError):
            discover.init_registry()
