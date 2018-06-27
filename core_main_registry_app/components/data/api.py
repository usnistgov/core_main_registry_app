""" Data's registry api
"""
import random
import datetime
import string

import core_main_app.components.data.api as data_api
from core_main_app.commons import exceptions as exceptions
from core_main_app.components.data.models import Data
from core_main_app.components.workspace import api as workspace_api
from core_main_app.utils.access_control.decorators import access_control
from core_main_registry_app.commons.constants import DataStatus
from core_main_registry_app.components.data.access_control import can_publish_data
from xml_utils.xsd_tree.xsd_tree import XSDTree


def get_role(data):
    """ Get the list of role saved in the data's dict content

    Args:
        data:

    Returns:

    """
    try:
        list_resource_role = data.dict_content['Resource']['role']
        list_role = []
        if '@xsi:type' in list_resource_role:
            list_role.append(list_resource_role['@xsi:type'])
            return list_role
        for dict_role in list_resource_role:
            list_role.append(dict_role['@xsi:type'])
        return list_role
    except Exception, e:
        raise exceptions.ModelError(e.message)


@access_control(can_publish_data)
def publish(data, user):
    """ Assign data to a workspace.

    Args:
        data:
        user:

    Returns:

    """
    data.workspace = workspace_api.get_global_workspace()
    data.last_modification_date = datetime.datetime.now()
    return data.save()


def set_status(data, status, user):
    """ Set the status of a data

    Args:
        data:
        status:
        user:

    Returns: Data

    """
    if status == DataStatus.DELETED and (data.workspace is None or data.workspace.is_public is False):
        raise exceptions.ModelError("the data should be published if the targeted status is 'Deleted'")

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


def is_local_id_already_used(local_id):
    """ Check if the local id given already exist in db

    Args:
        local_id:

    Returns:

    """
    return len(Data.execute_query({'dict_content.Resource.@localid': str(local_id)})) > 0


def generate_unique_local_id(length_id):
    """ Generate an unique ID with the given length

    Args:
        length_id:

    Returns:

    """
    # we generate an local id
    local_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length_id))
    # we make sure this local id does not exist in db
    while is_local_id_already_used(local_id):
        # otherwise we generate one until then
        local_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length_id))
    return local_id
