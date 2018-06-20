"""
Refinements creation.
"""
from core_main_registry_app.constants import UNSPECIFIED_CATEGORY
from core_main_registry_app.utils.refinement.tools import xsd_refinements


def init_refinements(template):
    """ Init the refinements for the given template. Categories used as refinement (search page...).

        Args:
            template:

        Returns:

    """
    from core_main_registry_app.components.refinement import api as refinement_api

    try:
        # Check if refinements already exist.
        if not refinement_api.check_refinements_already_exist_by_template_hash(template.hash):
            refinements_trees = xsd_refinements.loads_refinements_trees(template)
            # Create refinements.
            for root, tree in refinements_trees.iteritems():
                refinement = refinement_api.create_and_save(name=root.title,
                                                            xsd_name=root.xsd_name,
                                                            template_hash=template.hash)
                # Create categories.
                create_categories(tree, refinement)
    except Exception, e:
        raise Exception("Impossible to init the refinements. An error occurred while retrieving "
                        "the template: {0}".format(e.message))


def create_categories(tree, refinement):
    """ Create the refinement categories.

    Args:
        tree: Tree of categories.
        refinement: Refinement.

    """
    # Iterate over the categories.
    for key, leaves in tree.iteritems():
        _create_sub_categories(key, leaves, refinement)


def _create_sub_categories(key, leaves, refinement, parent=None):
    """ Create all sub categories.

    Args:
        key:
        leaves:
        refinement:
        parent:

    """
    from core_main_registry_app.components.category import api as category_api

    # No children. Only create the category.
    if len(leaves) == 0:
        category_api.create_and_save(name=key.title, path=key.path, value=key.value,
                                     parent=parent, refinement=refinement)
    elif len(leaves) > 0:
        # If we need an unspecified category.
        if UNSPECIFIED_CATEGORY:
            # Create the category.
            parent = category_api.create_and_save(name=key.title, path=key.path,
                                                  value=key.value_as_category(),
                                                  parent=parent, refinement=refinement)
            # Create the unspecified category and set the previous category as its parent.
            category_api.create_and_save(name="unspecified " + key.title, path=key.path,
                                         value=key.value, parent=parent,
                                         refinement=refinement)
        else:
            # Create the category and become a parent.
            parent = category_api.create_and_save(name=key.title, path=key.path, value=key.value,
                                                  parent=parent, refinement=refinement)
        # For each children.
        for key, value in sorted(leaves.iteritems()):
            # Create sub categories.
            _create_sub_categories(key, value, refinement, parent=parent)
