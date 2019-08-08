""" System api to access data without access control neither API rules
"""
from core_main_app.components.data.models import Data


def is_local_id_already_used(local_id):
    """ Check if the local id given already exist in db

    Args:
        local_id:

    Returns:

    """
    return Data.objects(__raw__={'dict_content.Resource.@localid': str(local_id)})
