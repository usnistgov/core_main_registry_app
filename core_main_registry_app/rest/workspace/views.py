""" REST views for the workspace API
"""
from rest_framework.permissions import IsAuthenticated

from core_main_app.rest.workspace.views import WorkspaceList
from core_main_registry_app.rest.workspace.serializers import (
    WorkspaceSerializer,
)


class WorkspaceListRegistry(WorkspaceList):
    """List all user Workspace, or create a new one"""

    permission_classes = (IsAuthenticated,)
    serializer = WorkspaceSerializer
