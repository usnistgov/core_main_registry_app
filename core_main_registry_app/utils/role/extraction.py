""" Role extraction API
"""


def role_extraction(dict_content):
    """Extract role from dict content.

    Args:
        dict_content

    Returns:
    """
    try:
        list_resource_role = dict_content["Resource"]["role"]
        list_role = []
        if "@xsi:type" in list_resource_role:
            list_role.append(list_resource_role["@xsi:type"])
            return list_role
        for dict_role in list_resource_role:
            list_role.append(dict_role["@xsi:type"])
        return list_role
    except KeyError:
        return None
