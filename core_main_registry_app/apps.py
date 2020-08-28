""" Apps file for setting core main registry app package when app is ready
"""
import sys

from django.apps import AppConfig

from core_main_registry_app import discover


class InitApp(AppConfig):
    """Core main registry app application settings"""

    name = "core_main_registry_app"

    def ready(self):
        """Run when the app is ready.

        Returns:

        """
        if "migrate" not in sys.argv:
            # Init registry
            discover.init_registry()
