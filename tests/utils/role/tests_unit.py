""" Unit tests for role extraction
"""
from unittest import TestCase

from core_main_registry_app.utils.role.extraction import role_extraction


class TestRoleExtraction(TestCase):
    """Tests for role extraction method."""

    def test_role_extraction_returns_role(self):
        """test_role_extraction_returns_role"""
        role = "role"
        result = role_extraction({"Resource": {"role": {"@xsi:type": role}}})
        self.assertEqual(result, [role])

    def test_role_extraction_returns_none_if_key_not_found(self):
        """test_role_extraction_returns_none_if_key_not_found"""
        role = "role"
        result = role_extraction(
            {"Resource": {"not_role": {"@xsi:type": role}}}
        )
        self.assertEqual(result, None)
