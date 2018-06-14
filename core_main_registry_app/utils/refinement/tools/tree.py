"""
Tree representation of refinement.
"""

from collections import OrderedDict


class TreeInfo:
    """
    Representation of refinement.
    """

    title = ""
    selected = False

    def __init__(self, title="", path="", value=""):
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
        return "{0}_{1}".format(self.value, TreeInfo.get_category_label())

    @staticmethod
    def get_category_label():
        return "_category"


def build_tree(tree, root, enums, dot_query):
    """ Create a tree of refinements.

    Args:
        tree:
        root:
        enums:
        dot_query:

    Returns:

    """
    # For each enumerations, we create the tree representation.
    for enum in enums:
        # Init tree.
        t = tree
        t = t.setdefault(TreeInfo(title=root), OrderedDict())
        # Levels are represented by the character ':' in the schema. (Level1: Level2: ... LevelN).
        groups = enum.attrib['value'].split(':')
        split_index = 0
        # For each level.
        for part in groups:
            # Increment split index. Go to the next level.
            split_index += 1
            # Get the dot notation of the element.
            path = dot_query
            # Get the value of the element.
            value = ':'.join(groups[:split_index])
            # Get the name of the element.
            title = part
            # Create the tree info.
            g = TreeInfo(title=title, path=path, value=value)
            # Add the element to the tree as the parent.
            t = t.setdefault(g, OrderedDict())

    return tree
