""" Category API
"""

from core_main_registry_app.components.category.models import Category


def create_and_save(name, path, value, parent, refinement):
    """Create and save a category.

    Args:
        name:
        path:
        value:
        parent:
        refinement:

    Returns:

    """

    # Save category
    return Category.create_and_save(
        name=name, path=path, value=value, parent=parent, refinement=refinement
    )


def get_all_filtered_by_refinement_id(refinement_id):
    """Get all categories by refinement id.

    Parameters:
            refinement_id:

    Returns: data collection

    """
    return Category.get_all_filtered_by_refinement_id(refinement_id)


def get_by_id(category_id):
    """Get category by its id.

    Parameters:
        category_id:

    Returns:
        Category object

    """
    return Category.get_by_id(category_id)


def get_all_categories_ids_by_parent_slug_and_refinement_id(
    parent_slug, refinement_id
):
    """Get a list of all category ids by parent_slug and refinement id.

    Args:
        parent_slug:
        refinement_id:

    Returns:

    """
    # Get categories
    categories = Category.get_all_categories_by_parent_slug_and_refinement_id(
        parent_slug, refinement_id
    )
    # Return a list of category ids
    return list(categories.values_list("id", flat=True))


def get_all():
    """Get all categories

    Returns:

    """
    return Category.get_all()


def get_all_categories_ids_from_name_and_refinement_id(name, refinement_id):
    """Get a list of all category ids by name and refinement id.

    Args:
        name:
        refinement_id:

    Returns:

    """
    return list(
        Category.get_all_categories_ids_from_name_and_refinement_id(
            name, refinement_id
        ).values_list("id", flat=True)
    )
