""" Unit tests for rest apis
"""
from unittest.case import TestCase
from core_main_registry_app.rest import urls as rest_urls


class TestRestUrls(TestCase):
    def test_template_urls_in_urls(self):
        """test_template_urls_in_urls"""
        self.assertTrue(
            "core_main_app_rest_global_template_list"
            in str(rest_urls.urlpatterns)
        )
        self.assertTrue(
            "core_main_app_rest_user_template_list"
            in str(rest_urls.urlpatterns)
        )
