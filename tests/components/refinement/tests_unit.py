""" Unit Test for Refinement API
"""

from django.test import TestCase
from core_main_app.commons.exceptions import DoesNotExist
from core_main_registry_app.components.refinement import (
    api as refinement_api,
)
from core_main_registry_app.components.refinement.models import (
    Refinement,
)


class TestRefinementCreateAndSave(TestCase):
    """
    Test Refinement Create And Save
    """

    def test_create_and_save_refinement_creates_refinement(self):
        """test_create_and_save_refinement_creates_refinement"""
        # Act
        result = refinement_api.create_and_save("Refinement", "", "")
        # Assert
        self.assertIsInstance(result, Refinement)
        self.assertEqual(result.name, "Refinement")


class TestRefinementGetAll(TestCase):
    """
    Test Refinement Get All
    """

    def test_refinement_get_all_refinement_returns_empty_list(self):
        """test_get_all_refinements_returns_empty_list"""
        # Act
        result = refinement_api.get_all()
        # Assert

        self.assertEqual(len(result), 0)

    def test_refinement_get_all_refinement_returns_list(self):
        """test_get_all_refinements_returns_empty_list"""
        # Arrange
        refinement_1 = create_refinement()
        refinement_2 = create_refinement()
        # Act
        result = refinement_api.get_all()
        # Assert

        self.assertEqual(len(result), 2)
        self.assertTrue(refinement_1 in result)
        self.assertTrue(refinement_2 in result)


class TestRefinementGetAllFilteredByTemplateHash(TestCase):
    """
    Test Refinement Get All Filtered By Template Hash
    """

    def test_refinement_get_all_filtered_by_template_hash_returns_empty_list(
        self,
    ):
        """test_refinement_get_all_filtered_by_template_hash_returns_empty_list"""
        # Arrange
        create_refinement()
        # Act
        result = refinement_api.get_all_filtered_by_template_hash("hash")
        # Assert

        self.assertEqual(len(result), 0)

    def test_refinement_get_all_filtered_by_template_hash_returns_list(self):
        """test_refinement_get_all_filtered_by_template_hash_returns_list"""
        # Arrange
        refinement_1 = create_refinement()
        refinement_2 = create_refinement()
        # Act
        result = refinement_api.get_all_filtered_by_template_hash("")
        # Assert

        self.assertEqual(len(result), 2)
        self.assertTrue(refinement_1 in result)
        self.assertTrue(refinement_2 in result)


class TestRefinementCheckRefinementsAlreadyExistByTemplateHash(TestCase):
    """
    Test Refinement Check Refinements Already Exist By Template Hash
    """

    def test_check_refinements_already_exist_by_template_hash_returns_false(
        self,
    ):
        """test_check_refinements_already_exist_by_template_hash_returns_false"""
        # Arrange
        create_refinement()
        # Act
        result = (
            refinement_api.check_refinements_already_exist_by_template_hash(
                "hash"
            )
        )
        # Assert
        self.assertFalse(result)

    def test_check_refinements_already_exist_by_template_hash_returns_true(
        self,
    ):
        """test_check_refinements_already_exist_by_template_hash_returns_true"""
        # Arrange
        create_refinement()

        # Act
        result = refinement_api.get_all_filtered_by_template_hash("")
        # Assert
        self.assertTrue(result)


class TestRefinementGetByTemplateHashAndBySlug(TestCase):
    """
    Test Refinement Get By Template Hash And By Slug
    """

    def test_refinement_get_by_template_hash_and_by_slug_raises_does_not_exist_exception(
        self,
    ):
        """test_get_by_template_hash_and_by_slug_raises_error_does_not_exist"""
        # Arrange
        create_refinement()
        # Act # Assert
        with self.assertRaises(DoesNotExist):
            refinement_api.get_by_template_hash_and_by_slug("hash", "slug")

    def test_refinement_get_by_template_hash_and_by_slug_returns_refinement(
        self,
    ):
        """test_refinement_get_by_template_hash_and_by_slug_returns_refinement"""
        # Arrange
        create_refinement()

        # Act
        result = refinement_api.get_by_template_hash_and_by_slug("", "")
        # Assert
        self.assertIsInstance(result, Refinement)


def create_refinement():
    """create_refinement

    Return:
    """
    return Refinement.create_and_save("Refinement", "", "")
