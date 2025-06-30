""" REST views for the registry Data API
"""

from django.utils.decorators import method_decorator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_main_app.components.data import api as data_api
from core_main_app.rest.data.serializers import DataSerializer
from core_main_app.rest.data.views import DataDetail
from core_main_app.utils.decorators import api_staff_member_required
from core_main_registry_app.components.data import api as registry_data_api


@extend_schema(
    tags=["Data"],
    description="Publish a data",
)
@api_view(["PATCH"])
def publish_data(request, pk):
    """Publish a data

    Args:

        request: HTTP request
        pk: ObjectId

    Returns:

        - code: 200
          content: Publication succeed
        - code: 403
          content: Authentication error
        - code: 404
          content: Object was not found
        - code: 500
          content: Internal server error
    """
    try:
        # Get data
        data_object = data_api.get_by_id(pk, request.user)

        # Publish
        registry_data_api.publish(data_object, request.user)

        # Return response
        return Response(status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = {"message": "Data not found."}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except AccessControlError as ace:
        content = {"message": str(ace)}
        return Response(content, status=status.HTTP_403_FORBIDDEN)
    except Exception as api_exception:
        content = {"message": str(api_exception)}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=["Data"],
    description="Retrieve or update a data",
)
class DataDetailRegistry(DataDetail):
    """Retrieve or update a data"""

    @extend_schema(
        summary="Delete a data",
        description="Delete a Data",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Data ID",
            ),
        ],
        responses={
            204: None,
            403: OpenApiResponse(description="Access Forbidden"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    def delete(self, request, pk):
        """Delete a Data
        Args:
            request: HTTP request
            pk: ObjectId
        Returns:
            - code: 204
              content: Deletion succeed
            - code: 403
              content: Access forbidden
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        # Only superusers allowed to delete data
        if not request.user.is_superuser:
            content = {
                "message": "You must have superuser right to delete data."
            }
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        return super(DataDetailRegistry, self).delete(request, pk)

    @extend_schema(
        summary="Update a Data",
        description="Update a Data",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Id of the data",
            ),
        ],
        request=DataSerializer,
        responses={
            200: OpenApiResponse(
                response=DataSerializer,
                description="Data updated successfully",
            ),
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Data not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    def patch(self, request, pk):
        """Data cannot be updated
        Args:
            request: HTTP request
            pk: ObjectId
        Returns:
            - code: 403
              content: Access forbidden
        """
        # Only superusers allowed to update data
        if not request.user.is_superuser:
            content = {
                "message": "You must have superuser right to update data."
            }
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        return super(DataDetailRegistry, self).patch(request, pk)
