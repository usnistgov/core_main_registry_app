"""
Tree representation of refinement.
"""

from collections import OrderedDict

from core_main_registry_app.constants import (
    UNSPECIFIED_CATEGORY,
    CATEGORY_SUFFIX,
    UNSPECIFIED_LABEL,
)


class TreeInfo(object):
    """
    Representation of refinement.
    """

    xsd_name = ""
    title = ""
    selected = False

    def __init__(self, xsd_name="", title="", path="", value=""):
        self.xsd_name = xsd_name
        self.title = title
        self.path = path
        self.value = value

    def __str__(self):
        return self.title

    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)

    def __lt__(self, other):
        return self.title < other.title

    def value_as_category(self):
        """value_as_category

        Returns

        """
        return f"{self.value}{CATEGORY_SUFFIX}"


def build_tree(tree, element_name, element_display_name, enums, dot_query):
    """Create a tree of refinements.

    Args:
        tree:
        element_name:
        element_display_name:
        enums:
        dot_query:

    Returns:

    """
    # Init tree.
    type_refinement = TreeInfo(
        xsd_name=element_name, title=element_display_name
    )
    first_node = tree.setdefault(type_refinement, OrderedDict())

    # For each enumerations, we create the tree representation.
    for enum in enums:
        parent_node = first_node
        levels = enum.attrib["value"].split(":")

        for i, level in enumerate(levels):
            # Create the tree info.
            graph = TreeInfo(
                xsd_name=level,
                title=level,
                path=dot_query,
                value=":".join(levels[: i + 1]),
            )
            g_node = parent_node.setdefault(graph, OrderedDict())
            parent_node = g_node

            # Case where it is the last element of the enum
            # check if we are in the unspecified case
            if len(levels) - 1 == i and _check_case_unspecified(
                enums, enum, i, level
            ):
                # Case unspecified: create a new node for the unspecified node
                title = (
                    f"{UNSPECIFIED_LABEL} {level}"
                    if UNSPECIFIED_CATEGORY
                    else level
                )
                graph = TreeInfo(
                    xsd_name=level,
                    title=title,
                    path=dot_query,
                    value=":".join(levels[: i + 1]),
                )
                parent_node.setdefault(graph, OrderedDict())

    return tree


def _check_case_unspecified(enums, current_enum, i, current_level):
    """Check if we can find the case of the unspecified.

    Args:
        enums: list of enums
        current_enum: current enum
        i: index of current level in current enum
        current_level: current level

    Returns:
    """
    for enum in enums:
        # We work only on enums different to the current enum
        if current_enum != enum:
            levels = enum.attrib["value"].split(":")
            # check if the current level is in the levels of the enum tested.
            # check if the current level is at the same position in the enum
            # check if the enum has more level
            if (
                current_level in levels
                and levels[i] == current_level
                and len(current_enum.attrib["value"])
                < len(enum.attrib["value"])
            ):
                return True
    return False
