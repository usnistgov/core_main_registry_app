""" Category API
"""

from core_main_registry_app.components.category.models import Category


def create_and_save(name, path, value, parent, refinement):
    """ Create and save a category.

    Args:
        name:
        path:
        value:
        parent:
        refinement:

    Returns:

    """

    # Save category
    return Category.create_and_save(name=name, path=path, value=value, parent=parent,
                                    refinement=refinement)


def get_all_filtered_by_refinement_id(refinement_id):
    """ Get all categories by refinement id.

    Parameters:
            refinement_id:

    Returns: data collection

    """
    return Category.get_all_filtered_by_refinement_id(refinement_id)
