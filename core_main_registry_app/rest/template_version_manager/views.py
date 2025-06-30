""" REST views for the registry template version manager API
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    OpenApiResponse,
)
from rest_framework.permissions import IsAuthenticated

from core_main_app.rest.template_version_manager.abstract_views import (
    AbstractStatusTemplateVersion,
)
from core_main_registry_app.components.version_manager import (
    api as version_manager_api,
)


@extend_schema(
    tags=["Template Version"],
    description="Update status to current",
)
class CurrentTemplateVersion(AbstractStatusTemplateVersion):
    """Update status to current"""

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Update status to current",
        description="Update status to current",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Template ID",
            ),
        ],
        responses={
            200: None,
            400: OpenApiResponse(description="Validation Error / Bad Request"),
            403: OpenApiResponse(description="Access Forbidden"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def status_update(self, template_object):
        """Update status to current
        Args:
            template_object: template_version
        Returns:
            TemplateVersion
        """
        return version_manager_api.set_current(
            template_object, request=self.request
        )
