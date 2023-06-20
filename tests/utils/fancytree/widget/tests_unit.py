""" Unit tests for the fancytree widget
"""
from unittest import TestCase

from core_main_registry_app.utils.fancytree.widget import (
    FancyTreeWidget,
    FANCYTREE_CDN_PATH,
)
from tests.mocks import MockChoicesIterator


class TestFancyTreeWidgetRender(TestCase):
    """Tests for FancyTreeWidget render method."""

    def test_output_contains_fancytree_library(self):
        """test_output_contains_fancytree_library"""
        mock_fancytree_widget = FancyTreeWidget()
        mock_fancytree_widget.choices = MockChoicesIterator()
        results = mock_fancytree_widget.render(
            "mock_name", [1, 2, 3], {"id": "mock_refinement_id"}
        )

        self.assertIn(FANCYTREE_CDN_PATH, results)
