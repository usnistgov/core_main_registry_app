"""
Management of the refinements' Tree from a schema.
"""

import logging
from collections import OrderedDict

from core_main_app.utils.xsd_flattener.xsd_flattener_database_url import (
    XSDFlattenerDatabaseOrURL,
)
from core_parser_app.tools.parser.utils.xml import get_app_info_options
from xml_utils.commons.constants import LXML_SCHEMA_NAMESPACE
from xml_utils.xsd_tree.operations.namespaces import (
    get_namespaces,
    get_target_namespace,
)
from xml_utils.xsd_tree.xsd_tree import XSDTree
from core_main_registry_app.utils.refinement.tools import tree

logger = logging.getLogger(
    "core_main_registry_app.utils.refinement.tools.xsd_refinements"
)


def loads_refinements_trees(template):
    """Load refinements for the given template.

    Args:
        template:

    Returns:

    """
    # Get the flatten schema
    ref_xml_schema_content = _get_flatten_schema(template)
    xml_doc_tree = XSDTree.build_tree(ref_xml_schema_content)
    # Get the target namespace
    target_ns_prefix = _get_target_namespace_prefix(
        ref_xml_schema_content, xml_doc_tree
    )
    target_ns_prefix = (
        "{}:".format(target_ns_prefix) if target_ns_prefix != "" else ""
    )

    # Iterate over the simple types.
    simple_types = xml_doc_tree.findall(
        "./{0}simpleType".format(LXML_SCHEMA_NAMESPACE)
    )
    trees = OrderedDict()
    for simple_type in simple_types:
        try:
            # Get all the enumerations
            enums = simple_type.findall(
                "./{0}restriction/{0}enumeration".format(LXML_SCHEMA_NAMESPACE)
            )
            if len(enums) > 0:
                # Get the corresponding element
                element = xml_doc_tree.findall(
                    ".//{0}element[@type='{1}']".format(
                        LXML_SCHEMA_NAMESPACE,
                        target_ns_prefix + simple_type.attrib["name"],
                    )
                )
                if len(element) > 1:
                    logger.error(
                        "More than one element using the enumeration ({0})".format(
                            str(len(element))
                        )
                    )
                else:
                    element = element[0]
                    # get the label of refinements
                    element_name, element_label = _get_element_info(
                        element, xml_doc_tree, target_ns_prefix
                    )
                    query = []

                    # Build the path to access the element (dot notation)
                    while element is not None:
                        if element.tag == "{0}element".format(
                            LXML_SCHEMA_NAMESPACE
                        ):
                            query.insert(0, element.attrib["name"])
                        elif element.tag == "{0}simpleType".format(
                            LXML_SCHEMA_NAMESPACE
                        ):
                            element = _get_simple_type_or_complex_type_info(
                                xml_doc_tree, target_ns_prefix, element, query
                            )
                        elif element.tag == "{0}complexType".format(
                            LXML_SCHEMA_NAMESPACE
                        ):
                            element = _get_simple_type_or_complex_type_info(
                                xml_doc_tree, target_ns_prefix, element, query
                            )
                        elif element.tag == "{0}extension".format(
                            LXML_SCHEMA_NAMESPACE
                        ):
                            element = _get_extension_info(
                                xml_doc_tree, element, query
                            )

                        element = element.getparent()

                    dot_query = ".".join(query)
                    # Build the corresponding refinement tree
                    trees = tree.build_tree(
                        tree=trees,
                        element_name=element_name,
                        element_display_name=element_label,
                        enums=enums,
                        dot_query=dot_query,
                    )
        except Exception as exception:
            # Log the exception
            logger.warning(str(exception))

    return trees


def _get_flatten_schema(template):
    """Get the flatten schema of the given template.

    Args:
        template:

    Returns:

    """
    return XSDFlattenerDatabaseOrURL(template.content, request=None).get_flat()


def _get_target_namespace_prefix(ref_xml_schema_content, xml_doc_tree):
    """Get the target namespace prefix.

    Args:
        ref_xml_schema_content:
        xml_doc_tree:

    Returns:

    """
    namespaces = get_namespaces(ref_xml_schema_content)
    target_namespace, target_ns_prefix = get_target_namespace(
        xml_doc_tree, namespaces
    )

    return target_ns_prefix


def _get_element_info(element, xml_doc_tree, target_ns_prefix):
    """Get the element label.

    Args:
        element:
        xml_doc_tree:
        target_ns_prefix:

    Returns:
        Label: string.

    """
    # By default, use the element's app_info
    app_info = get_app_info_options(element)
    # Check if the element is embedded in a choice.
    # If yes, we use the first parent complexType to get the label.
    parent = element.getparent()
    if parent is not None and parent.tag == "{0}choice".format(
        LXML_SCHEMA_NAMESPACE
    ):
        while parent.getparent() is not None:
            parent = parent.getparent()
            if parent.tag == "{0}complexType".format(LXML_SCHEMA_NAMESPACE):
                parent = _get_simple_type_or_complex_type_info(
                    xml_doc_tree, target_ns_prefix, parent
                )
                app_info = get_app_info_options(parent)
                break

    # Get the label
    name = parent.attrib["name"] if "name" in parent.attrib else ""
    label = app_info["label"] if "label" in app_info else name
    label = label if label is not None else name

    return name, label


def _get_simple_type_or_complex_type_info(
    xml_doc_tree, target_ns_prefix, element, query=None
):
    """Get simple type / complex type information.

    Args:
        xml_doc_tree:
        target_ns_prefix:
        element:
        query:

    Returns:

    """
    try:
        to_search_element = xml_doc_tree.findall(
            ".//{0}element[@type='{1}']".format(
                LXML_SCHEMA_NAMESPACE,
                target_ns_prefix + element.attrib["name"],
            )
        )
        if len(to_search_element) == 0:
            logger.debug(
                "No element using the enumeration ({0})".format(
                    str(len(element))
                )
            )
            element = _find_extension(xml_doc_tree, target_ns_prefix, element)
        elif len(to_search_element) > 1:
            logger.error(
                "More than one element using the enumeration ({0})".format(
                    str(len(element))
                )
            )
        else:
            element = to_search_element[0]
            if query is not None:
                query.insert(0, element.attrib["name"])
    except Exception as exception:
        raise Exception(
            "Impossible to get simple type / complex type information: {0}".format(
                str(exception)
            )
        )

    return element


def _get_extension_info(xml_doc_tree, element, query=None):
    """Get extension information.

    Args:
        xml_doc_tree:
        element:
        query:

    Returns:

    """
    try:
        to_search_element = xml_doc_tree.findall(
            ".//{0}element[@type='{1}']".format(
                LXML_SCHEMA_NAMESPACE, element.attrib["base"]
            )
        )
        if len(to_search_element) == 0:
            logger.debug(
                "No element using the enumeration ({0})".format(
                    str(len(element))
                )
            )
        elif len(to_search_element) > 1:
            logger.error(
                "More than one element using the enumeration ({0})".format(
                    str(len(element))
                )
            )
        else:
            element = to_search_element[0]
            if query is not None:
                query.insert(0, element.attrib["name"])
    except Exception as exception:
        raise Exception(
            "Impossible to get the extension information: {0}".format(
                str(exception)
            )
        )

    return element


def _find_extension(xml_doc_tree, target_ns_prefix, element):
    """Find the element extension.

    Args:
        xml_doc_tree:
        target_ns_prefix:
        element:

    Returns:

    """
    try:
        to_search_element = xml_doc_tree.findall(
            ".//{0}extension[@base='{1}']".format(
                LXML_SCHEMA_NAMESPACE,
                target_ns_prefix + element.attrib["name"],
            )
        )
        if len(to_search_element) == 0:
            logger.debug(
                "The enumeration ({0}) was not found".format(str(len(element)))
            )
        elif len(to_search_element) > 1:
            logger.error(
                "More than one enumeration using the element ({0})".format(
                    str(len(element))
                )
            )
        else:
            element = to_search_element[0]
    except Exception as exception:
        raise Exception(
            "Impossible to get the extension information: {0}".format(
                str(exception)
            )
        )

    return element
