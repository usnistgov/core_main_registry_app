""" Unit tests for `rest.workspace.serializers` package.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch
from core_main_registry_app.rest.workspace import (
    serializers as workspace_serializers,
)


class TestWorkspaceSerializerCreate(TestCase):
    """Unit tests for `WorksapceSerializer.create` method."""

    def setUp(self):
        """setUp"""
        self.mock_serializer = workspace_serializers.WorkspaceSerializer()
        self.mock_kwargs = {"validated_data": MagicMock()}

    @patch.object(workspace_serializers, "workspace_api")
    def test_create_and_save_called(self, mock_workspace_api):
        """test_create_and_save_called"""
        self.mock_serializer.create(**self.mock_kwargs)

        mock_workspace_api.create_and_save.assert_called_with(
            title=self.mock_kwargs["validated_data"]["title"],
            owner_id=self.mock_kwargs["validated_data"]["user"].id,
            is_public=False,
        )

    @patch.object(workspace_serializers, "workspace_api")
    def test_is_public_in_validated_data_ignored(self, mock_workspace_api):
        """test_is_public_in_validated_data_ignored"""
        self.mock_kwargs["validated_data"]["is_public"] = True
        self.mock_serializer.create(**self.mock_kwargs)

        mock_workspace_api.create_and_save.assert_called_with(
            title=self.mock_kwargs["validated_data"]["title"],
            owner_id=self.mock_kwargs["validated_data"]["user"].id,
            is_public=False,
        )
