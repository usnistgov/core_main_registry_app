"""
Refinements creation.
"""
from core_main_registry_app.constants import UNSPECIFIED_LABEL
from core_main_registry_app.utils.refinement.tools import xsd_refinements


def init_refinements(template):
    """Init the refinements for the given template. Categories used as refinement (search page...).

    Args:
        template:

    Returns:

    """
    from core_main_registry_app.components.refinement import api as refinement_api

    try:
        # Check if refinements already exist.
        if not refinement_api.check_refinements_already_exist_by_template_hash(
            template.hash
        ):
            refinements_trees = xsd_refinements.loads_refinements_trees(template)
            # Create refinements.
            for root, tree in list(refinements_trees.items()):
                refinement = refinement_api.create_and_save(
                    name=root.title, xsd_name=root.xsd_name, template_hash=template.hash
                )
                # Create categories.
                create_categories(tree, refinement)
    except Exception as exception:
        raise Exception(
            f"Impossible to init the refinements. An error occurred while retrieving "
            f"the template: {str(exception)}"
        )


def create_categories(tree, refinement):
    """Create the refinement categories.

    Args:
        tree: Tree of categories.
        refinement: Refinement.

    """
    # Iterate over the categories.
    for key, leaves in list(tree.items()):
        _create_sub_categories(key, leaves, refinement)


def _create_sub_categories(key, leaves, refinement, parent=None):
    """Create all sub categories.

    Args:
        key:
        leaves:
        refinement:
        parent:

    """
    from core_main_registry_app.components.category import api as category_api

    # No children. Only create the category.
    if len(leaves) == 0:
        category_api.create_and_save(
            name=key.title,
            path=key.path,
            value=key.value,
            parent=parent,
            refinement=refinement,
        )
    elif len(leaves) > 0:

        value = key.value if UNSPECIFIED_LABEL in key.title else key.value_as_category()

        # Create the category and become a parent.
        parent = category_api.create_and_save(
            name=key.title,
            path=key.path,
            value=value,
            parent=parent,
            refinement=refinement,
        )
        # For each children.
        for key, value in sorted(leaves.items()):
            # Create sub categories.
            _create_sub_categories(key, value, refinement, parent=parent)
