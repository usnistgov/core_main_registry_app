""" Unit Test for Category API
"""

from django.test import TestCase

from core_main_app.commons import exceptions as exceptions
from core_main_registry_app.components.category import (
    api as category_api,
)
from core_main_registry_app.components.category.models import (
    Category,
)
from core_main_registry_app.components.refinement.models import (
    Refinement,
)


class TestCreateAndSaveCategory(TestCase):
    """
    Test Create And Save Category
    """

    def test_create_and_save_category_creates_category(self):
        """test_create_and_save_category_creates_category"""

        # Arrange
        refinement = Refinement.create_and_save("Refinement", "", "")
        # Act
        result = category_api.create_and_save(
            "Category", "/Path", "", None, refinement
        )
        # Assert
        self.assertIsInstance(result, Category)
        self.assertEqual(result.name, "Category")


class TestCategoryGetAllFilteredByRefinementId(TestCase):
    """
    Test Category Get All Filtered By Refinement Id
    """

    def test_category_get_all_filtered_by_refinement_id_returns_empty_list(
        self,
    ):
        """test_category_get_all_filtered_by_refinement_id_returns_empty_list"""
        # Act
        result = category_api.get_all_filtered_by_refinement_id(1)
        # Assert
        self.assertEqual(len(result), 0)

    def test_category_get_all_filtered_by_refinement_id_returns_list(self):
        """test_category_get_all_filtered_by_refinement_id_returns_list"""
        # Arrange
        category = create_category()
        # Act
        result = category_api.get_all_filtered_by_refinement_id(1)
        # Assert
        self.assertEqual(len(result), 1)
        self.assertTrue(category in result)


class TestCategoryGetById(TestCase):
    """
    Test Category Get By Id
    """

    def test_category_get_by_id_raises_does_not_exist_exception(self):
        """test_category_get_by_id_raises_does_not_exist_exception"""
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            category_api.get_by_id(-1)

    def test_category_get_all_filtered_by_refinement_id_returns_list(self):
        """test_get_all_filtered_by_refinement_id_returns_list"""
        # Arrange
        category = create_category()
        # Act
        result = category_api.get_by_id(category.id)
        # Assert
        self.assertIsInstance(result, Category)


class TestCategoryGetAll(TestCase):
    """
    Test Category Get All
    """

    def test_category_get_all_returns_empty_list(self):
        """test_category_get_all_returns_empty_list"""
        # Act
        result = category_api.get_all()
        # Assert
        self.assertEqual(len(result), 0)

    def test_category_get_all_returns_list(self):
        """test_category_get_all_returns_list"""
        # Arrange
        category = create_category()
        # Act
        result = category_api.get_all()
        # Assert
        self.assertEqual(len(result), 1)
        self.assertTrue(category in result)


class TestCategoryGetAllCategoriesIdsFromNameAndRefinementId(TestCase):
    """
    Test Category Get All Categories Ids From Name And Refinement Id
    """

    def test_category_get_all_categories_ids_from_name_and_refinement_id_raises_does_not_exist_exception(
        self,
    ):
        """test_category_get_all_categories_ids_from_name_and_refinement_id_raises_does_not_exist_exception"""
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            category_api.get_all_categories_ids_from_name_and_refinement_id(
                "Category", 1
            )

    def test_category_get_all_categories_ids_from_name_and_refinement_id_returns_list(
        self,
    ):
        """test_category_get_all_categories_ids_from_name_and_refinement_id_returns_list"""
        # Arrange
        create_category()
        # Act
        result = (
            category_api.get_all_categories_ids_from_name_and_refinement_id(
                "Category", 1
            )
        )
        # Assert
        self.assertEqual(len(result), 1)


class TestCategoryGetAllCategoriesIdsByParentSlugAndRefinementId(TestCase):
    """
    Test Category Get All Categories Ids By Parent Slug And RefinementId
    """

    def test_get_all_categories_ids_by_parent_slug_and_refinement_id_raises_does_not_exist_exception(
        self,
    ):
        """test_get_all_categories_ids_by_parent_slug_and_refinement_id_raises_does_not_exist_exception"""
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            category_api.get_all_categories_ids_by_parent_slug_and_refinement_id(
                "parent", 1
            )

    def test_get_all_categories_ids_by_parent_slug_and_refinement_id_returns_list(
        self,
    ):
        """test_get_all_categories_ids_by_parent_slug_and_refinement_id_returns_list"""
        # Arrange
        create_category()
        # Act
        result = category_api.get_all_categories_ids_by_parent_slug_and_refinement_id(
            "", 1
        )
        # Assert
        self.assertEqual(len(result), 1)


def create_category():
    """create_refinement

    Return:
    """
    refinement = Refinement.create_and_save("Refinement", "", "")
    return category_api.create_and_save(
        "Category", "/Path", "", None, refinement
    )
