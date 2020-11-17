""" REST views for the registry template version manager API
"""
from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import ApiError
from core_main_app.rest.template_version_manager.abstract_views import (
    AbstractStatusTemplateVersion,
)
from core_main_app.utils.decorators import api_staff_member_required
from core_main_registry_app.components.version_manager import api as version_manager_api


class CurrentTemplateVersion(AbstractStatusTemplateVersion):
    """Update status to current"""

    permission_classes = (IsAuthenticated,)

    def status_update(self, template_object):
        """Update status to current

        Args:

            template_object: template_version

        Returns:

            TemplateVersion
        """
        return version_manager_api.set_current(template_object, request=self.request)
