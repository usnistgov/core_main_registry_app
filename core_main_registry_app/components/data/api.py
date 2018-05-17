""" Data's registry api
"""

from xml_utils.xsd_tree.xsd_tree import XSDTree

import core_main_app.components.data.api as data_api
from core_main_app.commons import exceptions as exceptions
from core_main_app.components.workspace import api as workspace_api
from core_main_app.utils.access_control.decorators import access_control
from core_main_registry_app.components.data.access_control import can_publish_data


@access_control(can_publish_data)
def publish(data, user):
    """ Assign data to a workspace.

    Args:
        data:
        user:

    Returns:

    """
    data.workspace = workspace_api.get_global_workspace()
    return data.save()


def set_status(data, status, user):
    """ Set the status of a data

    Args:
        data:
        status:
        user:

    Returns: Data

    """
    # build the xsd tree
    xml_tree = XSDTree.build_tree(data.xml_content)
    # get the root
    root = xml_tree.getroot()
    # and change the attribute
    root.attrib['status'] = status
    # update the xml content
    data.xml_content = XSDTree.tostring(xml_tree)
    # upsert the data
    return data_api.upsert(data, user)


def get_status(data):
    """ Get the status saved in the data's dict content

    Args:
        data:

    Returns:

    """
    try:
        return data.dict_content['Resource']['@status']
    except Exception, e:
        raise exceptions.ModelError(e.message)
