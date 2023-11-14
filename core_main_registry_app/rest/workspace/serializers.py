"""Serializers used throughout the workspace Rest API
"""

from rest_framework.serializers import ModelSerializer

from core_main_app.components.workspace import api as workspace_api
from core_main_app.components.workspace.models import Workspace


class WorkspaceSerializer(ModelSerializer):
    """Workspace serializer"""

    class Meta:
        """Meta"""

        model = Workspace
        fields = ["id", "title", "owner", "is_public"]
        read_only_fields = ("id", "owner", "is_public")

    def create(self, validated_data):
        """Create and return a new private `Workspace` instance, given the validated
        data.
        """
        return workspace_api.create_and_save(
            title=validated_data["title"],
            owner_id=validated_data["user"].id,
            is_public=False,
        )
