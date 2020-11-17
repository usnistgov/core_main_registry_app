""" Data's registry api
"""
import datetime
import random
import string

import pytz

import core_main_app.components.data.api as data_api
from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions as exceptions
from core_main_app.components.workspace import api as workspace_api
from core_main_app.utils.labels import get_data_label
from core_main_registry_app.commons.constants import DataStatus
from core_main_registry_app.components.data.access_control import can_publish_data
from core_main_registry_app.system.api import is_local_id_already_used
from core_main_registry_app.utils.role.extraction import role_extraction
from xml_utils.xsd_tree.xsd_tree import XSDTree


def get_role(data):
    """Get the list of role saved in the data's dict content

    Args:
        data:

    Returns:

    """
    return role_extraction(data.dict_content)


@access_control(can_publish_data)
def publish(data, user):
    """Assign data to a workspace.

    Args:
        data:
        user:

    Returns:

    """
    data.workspace = workspace_api.get_global_workspace()
    data.last_modification_date = datetime.datetime.now(pytz.utc)
    return data.save()


def set_status(data, status, request):
    """Set the status of a data

    Args:
        data:
        status:
        request:

    Returns: Data

    """
    if status == DataStatus.DELETED and (
        data.workspace is None or data.workspace.is_public is False
    ):
        raise exceptions.ModelError(
            "the "
            + get_data_label()
            + " should be published if the targeted status is 'Deleted'"
        )

    # build the xsd tree
    xml_tree = XSDTree.build_tree(data.xml_content)
    # get the root
    root = xml_tree.getroot()
    # and change the attribute
    root.attrib["status"] = status
    # update the xml content
    data.xml_content = XSDTree.tostring(xml_tree)
    # upsert the data
    return data_api.upsert(data, request=request)


def get_status(data):
    """Get the status saved in the data's dict content

    Args:
        data:

    Returns:

    """
    try:
        return data.dict_content["Resource"]["@status"]
    except Exception as e:
        raise exceptions.ModelError(str(e))


def generate_unique_local_id(length_id):
    """Generate an unique ID with the given length

    Args:
        length_id:

    Returns:

    """
    # we generate an local id
    local_id = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(length_id)
    )
    # we make sure this local id does not exist in db
    while is_local_id_already_used(local_id):
        # otherwise we generate one until then
        local_id = "".join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(length_id)
        )
    return local_id
