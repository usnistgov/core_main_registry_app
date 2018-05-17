""" REST views for the registry Data API
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core_main_app.commons import exceptions
from core_main_app.components.data import api as data_api
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_registry_app.components.data import api as registry_data_api


@api_view(['PATCH'])
def publish_data(request, pk):
    """ Publish a data.

    Args:
        request:
        pk:

    Returns:

    """
    try:
        # Get data
        data_object = data_api.get_by_id(pk, request.user)

        # Publish
        registry_data_api.publish(data_object, request.user)

        # Return response
        return Response(status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = {'message': 'Data not found.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except AccessControlError as ace:
        content = {'message': ace.message}
        return Response(content, status=status.HTTP_403_FORBIDDEN)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
